from app import create_app
from extensions import db
from models.user import User
from models.service import Service

def seed():
    app = create_app()
    with app.app_context():
        # Create admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)

        # Seed services
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
        print('Seed data inserted successfully.')

if __name__ == '__main__':
    seed()
