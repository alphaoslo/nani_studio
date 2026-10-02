from flask import Blueprint, render_template
from models.portfolio import Portfolio

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/portfolio')
def index():
    items = Portfolio.query.order_by(Portfolio.created_at.desc()).all()
    categories = list(set(item.category for item in items))
    return render_template('customer/portfolio.html', items=items, categories=categories)
