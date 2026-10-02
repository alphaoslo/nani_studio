from flask import Blueprint, render_template, request, flash, redirect, url_for
from extensions import db
from models.contact import ContactMessage

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/contact', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        errors = []
        if not name:
            errors.append('Name is required.')
        if not phone:
            errors.append('Phone is required.')
        if not email or '@' not in email:
            errors.append('Valid email is required.')
        if not message:
            errors.append('Message is required.')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('customer/contact.html')

        msg = ContactMessage(
            name=name,
            phone=phone,
            email=email,
            subject=subject,
            message=message,
        )
        db.session.add(msg)
        db.session.commit()
        flash('Message sent successfully! We will get back to you soon.', 'success')
        return redirect(url_for('contact.index'))

    return render_template('customer/contact.html')
