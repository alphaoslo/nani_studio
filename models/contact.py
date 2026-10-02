from datetime import datetime, timezone
from extensions import db

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), default='')
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Unread')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
