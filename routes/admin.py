import os
from functools import wraps
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, current_app
from werkzeug.utils import secure_filename
from extensions import db
from models.user import User
from models.service import Service
from models.portfolio import Portfolio
from models.booking import Booking
from models.contact import ContactMessage

admin_bp = Blueprint('admin', __name__)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['admin_id'] = user.id
            session['admin_username'] = user.username
            flash('Logged in successfully.', 'success')
            return redirect(url_for('admin.dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('admin.login'))

@admin_bp.route('/')
@login_required
def dashboard():
    total_bookings = Booking.query.count()
    pending = Booking.query.filter_by(status='Pending').count()
    confirmed = Booking.query.filter_by(status='Confirmed').count()
    completed = Booking.query.filter_by(status='Completed').count()
    portfolio_count = Portfolio.query.count()
    unread_messages = ContactMessage.query.filter_by(status='Unread').count()
    return render_template('admin/dashboard.html',
                           total_bookings=total_bookings,
                           pending=pending,
                           confirmed=confirmed,
                           completed=completed,
                           portfolio_count=portfolio_count,
                           unread_messages=unread_messages)

# --- Services CRUD ---
@admin_bp.route('/services')
@login_required
def services():
    all_services = Service.query.order_by(Service.category, Service.name).all()
    return render_template('admin/services.html', services=all_services)

@admin_bp.route('/services/add', methods=['POST'])
@login_required
def add_service():
    name = request.form.get('name', '').strip()
    category = request.form.get('category', '').strip()
    description = request.form.get('description', '').strip()
    icon = request.form.get('icon', 'bi-camera').strip()
    if name and category and description:
        db.session.add(Service(name=name, category=category, description=description, icon=icon))
        db.session.commit()
        flash('Service added.', 'success')
    else:
        flash('All fields required.', 'danger')
    return redirect(url_for('admin.services'))

@admin_bp.route('/services/edit/<int:id>', methods=['POST'])
@login_required
def edit_service(id):
    s = Service.query.get_or_404(id)
    s.name = request.form.get('name', s.name)
    s.category = request.form.get('category', s.category)
    s.description = request.form.get('description', s.description)
    s.icon = request.form.get('icon', s.icon)
    s.active = 'active' in request.form
    db.session.commit()
    flash('Service updated.', 'success')
    return redirect(url_for('admin.services'))

@admin_bp.route('/services/delete/<int:id>', methods=['POST'])
@login_required
def delete_service(id):
    s = Service.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    flash('Service deleted.', 'info')
    return redirect(url_for('admin.services'))

# --- Portfolio CRUD ---
@admin_bp.route('/portfolio')
@login_required
def portfolio():
    items = Portfolio.query.order_by(Portfolio.created_at.desc()).all()
    return render_template('admin/portfolio.html', items=items)

@admin_bp.route('/portfolio/add', methods=['POST'])
@login_required
def add_portfolio():
    title = request.form.get('title', '').strip()
    category = request.form.get('category', '').strip()
    description = request.form.get('description', '').strip()
    video_url = request.form.get('video_url', '').strip()
    featured = 'featured' in request.form

    image_path = ''
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')

    if title and category:
        db.session.add(Portfolio(title=title, category=category, description=description,
                                 image=image_path, video_url=video_url, featured=featured))
        db.session.commit()
        flash('Portfolio item added.', 'success')
    else:
        flash('Title and category required.', 'danger')
    return redirect(url_for('admin.portfolio'))

@admin_bp.route('/portfolio/edit/<int:id>', methods=['POST'])
@login_required
def edit_portfolio(id):
    item = Portfolio.query.get_or_404(id)
    item.title = request.form.get('title', item.title)
    item.category = request.form.get('category', item.category)
    item.description = request.form.get('description', item.description)
    item.video_url = request.form.get('video_url', item.video_url)
    item.featured = 'featured' in request.form

    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            item.image = os.path.join(current_app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')

    db.session.commit()
    flash('Portfolio item updated.', 'success')
    return redirect(url_for('admin.portfolio'))

@admin_bp.route('/portfolio/delete/<int:id>', methods=['POST'])
@login_required
def delete_portfolio(id):
    item = Portfolio.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Portfolio item deleted.', 'info')
    return redirect(url_for('admin.portfolio'))

# --- Bookings ---
@admin_bp.route('/bookings')
@login_required
def bookings():
    status_filter = request.args.get('status', '')
    search = request.args.get('search', '')
    query = Booking.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    if search:
        query = query.filter(Booking.customer_name.ilike(f'%{search}%'))
    all_bookings = query.order_by(Booking.created_at.desc()).all()
    return render_template('admin/bookings.html', bookings=all_bookings, status_filter=status_filter, search=search)

@admin_bp.route('/bookings/update/<int:id>', methods=['POST'])
@login_required
def update_booking(id):
    b = Booking.query.get_or_404(id)
    b.status = request.form.get('status', b.status)
    db.session.commit()
    flash('Booking status updated.', 'success')
    return redirect(url_for('admin.bookings'))

# --- Messages ---
@admin_bp.route('/messages')
@login_required
def messages():
    all_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', messages=all_messages)

@admin_bp.route('/messages/mark/<int:id>/<status>', methods=['POST'])
@login_required
def mark_message(id, status):
    m = ContactMessage.query.get_or_404(id)
    if status in ('Read', 'Unread'):
        m.status = status
        db.session.commit()
        flash(f'Message marked as {status}.', 'success')
    return redirect(url_for('admin.messages'))

@admin_bp.route('/messages/delete/<int:id>', methods=['POST'])
@login_required
def delete_message(id):
    m = ContactMessage.query.get_or_404(id)
    db.session.delete(m)
    db.session.commit()
    flash('Message deleted.', 'info')
    return redirect(url_for('admin.messages'))
