from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from static.forms import RegistrationForm, LoginForm
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:NeforMAL_1488@localhost/flask_db'
app.config['SECRET_KEY'] = 'a really really really really long secret key'
db = SQLAlchemy(app)
manager = LoginManager(app)


class Registration(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(400), unique=True, nullable=False)
    repeat_password = db.Column(db.String(400), unique=True, nullable=False)


with app.app_context():
    db.create_all()


@manager.user_loader
def load_user(user_id):
    return Registration.query.get(user_id)


@app.route('/')
def main():
    form = RegistrationForm()
    form1 = LoginForm()

    return render_template("main.html", form=form, form1=form1)


@app.route('/about/')
def about():
    return render_template("about.html")


@app.route('/science/')
def science():
    return render_template("science.html")


@app.route('/entertainment/')
def entertainment():
    return render_template("entertainment.html")


@app.route('/neanderthal/')
def neanderthal():
    return render_template("neanderthal.html")


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    repeat_password = request.form.get('repeat_password')
    if len(username) > 2:
        if len(email) > 2 and '@' in email:
            if password == repeat_password:
                n_password = generate_password_hash(password)
                db.session.add(Registration(username=username, email=email, password=n_password, repeat_password=n_password))
                db.session.commit()
    return redirect(url_for("main"))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username and password:
        user = Registration.query.filter_by(username=username).first()
        if user is not None:
            if check_password_hash(user.password, password):
                login_user(user)
    return redirect(url_for('main'))


@app.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run()
