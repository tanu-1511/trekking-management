from datetime import datetime
from extensions import db


class Booking(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    trek_id = db.Column(
        db.Integer,
        db.ForeignKey("trek.id"),
        nullable=False
    )

    booking_date = db.Column(
        db.DateTime,
        default=datetime.now
    )

    status = db.Column(
        db.String(20),
        default="Booked"
    )

    trek = db.relationship(
        "Trek",
        backref="bookings"
    )