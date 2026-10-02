from flask import Flask
from config import Config
from extensions import db

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # Ensure instance folder exists
    import os
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    db.init_app(app)

    # Register blueprints
    from routes.main import main_bp
    from routes.services import services_bp
    from routes.portfolio import portfolio_bp
    from routes.booking import booking_bp
    from routes.contact import contact_bp
    from routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Error handlers
    from flask import render_template

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)

app = create_app()
