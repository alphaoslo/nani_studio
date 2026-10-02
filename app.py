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
        _seed_defaults()

    return app


def _seed_defaults():
    """Auto-create default admin user and services if database is empty."""
    from models.user import User
    from models.service import Service

    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)

    if Service.query.count() == 0:
        services = [
            Service(name='Weddings', category='Photography', description='Professional wedding photography capturing every precious moment.', icon='bi-heart'),
            Service(name='Events', category='Photography', description='Event photography for all occasions — birthdays, corporate, and more.', icon='bi-calendar-event'),
            Service(name='Portraits', category='Photography', description='Studio and outdoor portrait sessions with professional lighting.', icon='bi-person'),
            Service(name='Pre-Wedding Shoots', category='Photography', description='Beautiful pre-wedding photoshoots at scenic locations.', icon='bi-camera'),
            Service(name='Cinematic Videos', category='Videography', description='High-quality cinematic video production for your special moments.', icon='bi-film'),
            Service(name='Wedding Films', category='Videography', description='Full wedding film coverage with cinematic storytelling.', icon='bi-camera-video'),
            Service(name='Event Videos', category='Videography', description='Professional video coverage for all types of events.', icon='bi-camera-video-fill'),
            Service(name='Video Editing', category='Videography', description='Professional video editing with color grading and transitions.', icon='bi-scissors'),
            Service(name='Aerial Photography', category='Drone Shoot', description='Stunning aerial photography using professional drones.', icon='bi-airplane'),
            Service(name='Aerial Videography', category='Drone Shoot', description='Cinematic drone videography for events and properties.', icon='bi-wind'),
            Service(name='Property Coverage', category='Drone Shoot', description='Aerial coverage of properties and real estate.', icon='bi-building'),
            Service(name='Event Coverage', category='Drone Shoot', description='Drone coverage for large events and gatherings.', icon='bi-geo-alt'),
            Service(name='Photo Retouching', category='Photo & Video Editing', description='Professional photo retouching and enhancement.', icon='bi-magic'),
            Service(name='Color Grading', category='Photo & Video Editing', description='Professional color grading for photos and videos.', icon='bi-palette'),
            Service(name='Cinematic Editing', category='Photo & Video Editing', description='Cinematic video editing with professional transitions.', icon='bi-play-circle'),
            Service(name='Album Design', category='Photo & Video Editing', description='Custom photo album design and layout.', icon='bi-book'),
        ]
        db.session.add_all(services)

    db.session.commit()


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)

app = create_app()
