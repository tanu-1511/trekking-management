from flask import Flask

from config import Config
from extensions import db, login_manager, bcrypt


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)
bcrypt.init_app(app)


@app.route("/")
def home():
    return "Trekking Management Application"


if __name__ == "__main__":
    app.run(debug=True)