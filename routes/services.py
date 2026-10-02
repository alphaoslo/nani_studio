from flask import Blueprint, render_template
from models.service import Service

services_bp = Blueprint('services', __name__)

@services_bp.route('/services')
def index():
    services = Service.query.filter_by(active=True).all()
    categories = {}
    for s in services:
        categories.setdefault(s.category, []).append(s)
    return render_template('customer/services.html', categories=categories)
