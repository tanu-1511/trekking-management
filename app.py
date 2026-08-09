from flask import Flask, render_template

from config import Config
from extensions import db, login_manager, bcrypt

from models.user import User

from routes.auth import auth
from routes.admin import admin
from routes.staff import staff
from routes.user import user


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)
bcrypt.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(staff)
app.register_blueprint(user)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)