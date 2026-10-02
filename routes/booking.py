from flask import Blueprint, render_template, request, flash, redirect, url_for
from extensions import db
from models.booking import Booking

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/booking', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('customer_name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        service = request.form.get('service', '').strip()
        event_date = request.form.get('event_date', '').strip()
        event_type = request.form.get('event_type', '').strip()
        location = request.form.get('location', '').strip()
        message = request.form.get('message', '').strip()
        package = request.form.get('package', '').strip()

        errors = []
        if not name:
            errors.append('Name is required.')
        if not phone:
            errors.append('Phone is required.')
        if not email or '@' not in email:
            errors.append('Valid email is required.')
        if not service:
            errors.append('Service is required.')
        if not event_date:
            errors.append('Event date is required.')
        if not event_type:
            errors.append('Event type is required.')
        if not location:
            errors.append('Location is required.')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('customer/booking.html')

        booking = Booking(
            customer_name=name,
            phone=phone,
            email=email,
            service=service,
            event_date=event_date,
            event_type=event_type,
            location=location,
            message=message,
            package=package,
        )
        db.session.add(booking)
        db.session.commit()
        flash('Booking submitted successfully! We will contact you soon.', 'success')
        return redirect(url_for('booking.index'))

    return render_template('customer/booking.html')
