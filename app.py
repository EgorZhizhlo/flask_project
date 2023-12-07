from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from static.forms import RegistrationForm, LoginForm, ChangeUsername, ChangeEmail, ChangePassword, CreatePost
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:NeforMAL_1488@db/flask_db'
app.config['SECRET_KEY'] = 'a really really really really long secret key'
db = SQLAlchemy(app)
manager = LoginManager(app)
admin_key = "7dY5syEJUMWUA6zT8e9BLYCwtirEYNfdJob1kxDThmJ4Tg6hwe880mM9Yi39KrYY57XezpsCRIv5Wb6zSFBiHAcSnEcVPmj5d1LL"


# models
# ////////////////////////////////////////////////////////

class USERS(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(400), unique=True, nullable=False)
    repeat_password = db.Column(db.String(400), unique=True, nullable=False)
    admin_key = db.Column(db.String(400), unique=True)


class POSTS(db.Model, UserMixin):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    author = db.Column(db.String(120), unique=True, nullable=False)
    text = db.Column(db.String(1000), unique=True, nullable=False)


with app.app_context():
    db.create_all()


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# main blog pages
# ////////////////////////////////////////////////////////


@app.route('/')
def main():
    form = RegistrationForm()
    form1 = LoginForm()
    create_superuser()
    posts = POSTS.query.all()
    return render_template("main.html", form=form, form1=form1, admin_key=admin_key, posts=posts)


@app.route('/about/')
def about():
    form = RegistrationForm()
    form1 = LoginForm()
    return render_template("about.html", form=form, admin_key=admin_key, form1=form1)


@app.route('/science/')
def science():
    form = RegistrationForm()
    form1 = LoginForm()
    return render_template("science.html", form=form, admin_key=admin_key, form1=form1)


@app.route('/entertainment/')
def entertainment():
    form = RegistrationForm()
    form1 = LoginForm()
    return render_template("entertainment.html", form=form, admin_key=admin_key, form1=form1)


@app.route('/neanderthal/')
def neanderthal():
    form = RegistrationForm()
    form1 = LoginForm()
    return render_template("neanderthal.html", form=form, admin_key=admin_key, form1=form1)


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# registration and authorisation
# ////////////////////////////////////////////////////////

@manager.user_loader
def load_user(user_id):
    return USERS.query.get(user_id)


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
                db.session.add(USERS(username=username, email=email, password=n_password, repeat_password=n_password))
                db.session.commit()
    return redirect(url_for("main"))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username and password:
        user = USERS.query.filter_by(username=username).first()
        if user is not None:
            if check_password_hash(user.password, password):
                login_user(user)
    return redirect(url_for('main'))


@app.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# admin panel
# ////////////////////////////////////////////////////////


def create_superuser():
    supperuser = USERS.query.filter_by(username=admin_key[30:37] + 'SUPERUSER' + admin_key[20:27]).first()
    if supperuser is None:
        db.session.add(USERS(username=admin_key[30:37] + 'SUPERUSER' + admin_key[20:27], email='egor2006.zh@gmail.com',
                             password=generate_password_hash('NeforMAL_1488'),
                             repeat_password=generate_password_hash('NeforMAL_1488'), admin_key=admin_key))
        db.session.commit()
    return 0


@app.route('/admin_panel/', methods=['GET', 'POST'])
@login_required
def admin_panel():
    form = RegistrationForm()
    form1 = LoginForm()
    return render_template("admin_panel.html", form=form, form1=form1, admin_key=admin_key)


@app.route('/posts_control/', methods=['GET', 'POST'])
@login_required
def posts_control():
    form = RegistrationForm()
    form1 = LoginForm()
    form2 = CreatePost()
    posts = POSTS.query.all()
    users = USERS.query.all()
    return render_template("posts_control.html", form=form, form1=form1, form2=form2, admin_key=admin_key, posts=posts,
                           users=users)


@app.route('/users_control/', methods=['GET', 'POST'])
@login_required
def users_control():
    form = RegistrationForm()
    form1 = LoginForm()
    users = USERS.query.all()
    return render_template("users_control.html", form=form, form1=form1, admin_key=admin_key, users=users)


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# user control
# ////////////////////////////////////////////////////////


@app.route('/users_control/change_username/<int:user_id>', methods=['GET', 'POST'])
@login_required
def admin_change_username(user_id):
    form = RegistrationForm()
    form1 = LoginForm()
    form2 = ChangeUsername()
    user = USERS.query.filter_by(id=user_id).first()
    if user is not None:
        return render_template("change_username.html", form=form, form1=form1, form2=form2, admin_key=admin_key,
                               user=user)
    else:
        return redirect(url_for("users_control"))


@app.route('/change_u/<int:user_id>', methods=['GET', 'POST'])
@login_required
def change_username(user_id):
    new_username = request.form.get('username')
    if new_username is not None:
        if len(new_username) > 2:
            user = USERS.query.filter_by(id=user_id).first()
            user.username = new_username
            db.session.commit()
    return redirect(url_for('users_control'))


@app.route('/users_control/change_email/<int:user_id>', methods=['GET', 'POST'])
@login_required
def admin_change_email(user_id):
    form = RegistrationForm()
    form1 = LoginForm()
    form2 = ChangeEmail()
    user = USERS.query.filter_by(id=user_id).first()
    if user is not None:
        return render_template("change_email.html", form=form, form1=form1, form2=form2, admin_key=admin_key, user=user)
    else:
        return redirect(url_for("users_control"))


@app.route('/change_e/<int:user_id>', methods=['GET', 'POST'])
@login_required
def change_email(user_id):
    new_email = request.form.get('email')
    if new_email is not None:
        if len(new_email) > 2:
            if '@' in new_email:
                user = USERS.query.filter_by(id=user_id).first()
                user.email = new_email
                db.session.commit()
    return redirect(url_for('users_control'))


@app.route('/users_control/change_password/<int:user_id>', methods=['GET', 'POST'])
@login_required
def admin_change_password(user_id):
    form = RegistrationForm()
    form1 = LoginForm()
    form2 = ChangePassword()
    user = USERS.query.filter_by(id=user_id).first()
    if user is not None:
        return render_template("change_password.html", form=form, form1=form1, form2=form2, admin_key=admin_key,
                               user=user)
    else:
        return redirect(url_for("users_control"))


@app.route('/change_p/<int:user_id>', methods=['GET', 'POST'])
@login_required
def change_password(user_id):
    new_password = request.form.get('password')
    new_repeat_password = request.form.get('repeat_password')
    print(new_password, new_repeat_password)
    if new_password is not None:
        if new_repeat_password is not None:
            if new_password == new_repeat_password:
                if len(new_password) >= 8:
                    print(new_password, new_repeat_password)
                    user = USERS.query.filter_by(id=user_id).first()
                    user.password = generate_password_hash(new_password)
                    user.repeat_password = generate_password_hash(new_repeat_password)
                    db.session.commit()
    return redirect(url_for('users_control'))


@app.route(f'/delete_user/{admin_key}/<int:user_id>', methods=['GET', 'POST'])
@login_required
def admin_delete_user(user_id):
    user = USERS.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users_control'))


@app.route('/users_control/create_user', methods=['GET', 'POST'])
def admin_create_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    repeat_password = request.form.get('repeat_password')
    if len(username) > 2:
        if len(email) > 2 and '@' in email:
            if password == repeat_password:
                n_password = generate_password_hash(password)
                db.session.add(USERS(username=username, email=email, password=n_password, repeat_password=n_password))
                db.session.commit()
    return redirect(url_for("users_control"))


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# post control
# ////////////////////////////////////////////////////////


@app.route('/posts_control/create_post', methods=['GET', 'POST'])
def admin_create_post():
    title = request.form.get('title')
    author = request.form.get('author')
    text = request.form.get('text')
    if text is not None:
        db.session.add(POSTS(title=title, author=author, text=text))
        db.session.commit()
        return redirect(url_for("posts_control"))


@app.route(f'/delete_post/{admin_key}/<int:post_id>', methods=['GET', 'POST'])
def admin_delete_post(post_id):
    post = POSTS.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("posts_control"))


@app.route('/posts_control/change_t/<int:post_id>', methods=['GET', 'POST'])
def admin_change_title(post_id):
    form = RegistrationForm()
    form1 = LoginForm()
    form2 = ChangePassword()
    post = POSTS.query.filter_by(id=post_id).first()
    if post is not None:
        return render_template("change_password.html", form=form, form1=form1, form2=form2, admin_key=admin_key,
                               post=post)
    else:
        return redirect(url_for("users_control"))


@app.route('/posts_control/change_a/<int:post_id>', methods=['GET', 'POST'])
def admin_change_author(post_id):
    form = RegistrationForm()
    form1 = LoginForm()
    form2 = ChangePassword()
    post = POSTS.query.filter_by(id=post_id).first()
    if post is not None:
        return render_template("change_password.html", form=form, form1=form1, form2=form2, admin_key=admin_key,
                               post=post)
    else:
        return redirect(url_for("users_control"))


@app.route('/posts_control/change_text/<int:post_id>', methods=['GET', 'POST'])
def admin_change_text(post_id):
    form = RegistrationForm()
    form1 = LoginForm()
    form2 = ChangePassword()
    post = POSTS.query.filter_by(id=post_id).first()
    if post is not None:
        return render_template("change_password.html", form=form, form1=form1, form2=form2, admin_key=admin_key,
                               post=post)
    else:
        return redirect(url_for("users_control"))


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


if __name__ == '__main__':
    app.run(host="0.0.0.0")
