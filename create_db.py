from app import app
from extensions import db, bcrypt

from models.user import User
from models.trek import Trek
from models.booking import Booking


with app.app_context():

    # Create all tables
    db.create_all()

    # Check if admin already exists
    admin = User.query.filter_by(email="admin@trek.com").first()

    if not admin:

        hashed_password = bcrypt.generate_password_hash("admin123").decode("utf-8")

        admin = User(
            name="Admin",
            email="admin@trek.com",
            phone="1234567890",
            password=hashed_password,
            role="admin",
            approved=True,
            blacklisted=False
        )

        db.session.add(admin)
        db.session.commit()
        print("Admin account created")
    else:
        print("Admin exists.")

print("Database started")