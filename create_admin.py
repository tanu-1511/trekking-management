from app import app
from extensions import db, bcrypt
from models.user import User


with app.app_context():

    admin = User.query.filter_by(role="admin").first()

    if admin:

        admin.password = bcrypt.generate_password_hash("admin123").decode("utf-8")
        admin.approved = True
        admin.blacklisted = False

        db.session.commit()

        print("Admin password reset successfully!")
        print("Email:", admin.email)
        print("Password: admin123")

    else:

        print("No admin account found.")