from extensions import db

class Trek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location =db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    start_date= db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    available_slots= db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    description =db.Column(db.Text)
    assigned_staff_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )