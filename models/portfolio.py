from datetime import datetime, timezone
from extensions import db

class Portfolio(db.Model):
    __tablename__ = 'portfolio'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, default='')
    image = db.Column(db.String(200), default='')
    video_url = db.Column(db.String(500), default='')
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
