from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin

app = Flask(__name__)
app.config['SECRET_KEY'] = "k9_secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///k9.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# MODELO USUARIO
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default="guard")   # admin, guardias, etc.


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# INICIO
@app.route("/")
@login_required
def index():
    return render_template("index.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()

        if user and user.password == request.form["password"]:
            login_user(user)
            return redirect(url_for("index"))

        flash("Credenciales incorrectas")

    return render_template("login.html")


# LOGOUT
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


# CREAR TABLAS si no existen
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
