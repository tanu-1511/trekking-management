from flask import Flask, render_template
from routes.auth import auth
from config import Config
#from extensions import db, login_manager, bcrypt
from extensions import db, bcrypt


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
#login_manager.init_app(app)
bcrypt.init_app(app)
app.register_blueprint(auth)

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)