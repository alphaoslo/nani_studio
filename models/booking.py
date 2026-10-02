from datetime import datetime, timezone
from extensions import db

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.String(20), nullable=False)
    event_type = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, default='')
    package = db.Column(db.String(500), default='')
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
