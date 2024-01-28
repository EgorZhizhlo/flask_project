from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from static.forms import RegistrationForm, LoginForm, ChangeUsername, ChangeEmail, ChangePassword, CreatePost
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user

import pandas as pd
import numpy as np
import seaborn as sns
import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler

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
    password = db.Column(db.String(400), unique=False, nullable=False)
    repeat_password = db.Column(db.String(400), unique=False, nullable=False)
    admin_key = db.Column(db.String(400), unique=False)


class POSTS(db.Model, UserMixin):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    author = db.Column(db.String(120), unique=False, nullable=False)
    email_author = db.Column(db.String(120), unique=False, nullable=False)
    text = db.Column(db.String(1000), unique=False, nullable=False)


class LSTM_m(db.Model, UserMixin):
    __tablename__ = 'LSTM'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, unique=False, nullable=False)
    month = db.Column(db.String(30), unique=False, nullable=False)
    passengers = db.Column(db.Float, unique=False, nullable=False)
    predictions = db.Column(db.Float, unique=False, nullable=False)
    wrong_answer = db.Column(db.Float, unique=False, nullable=False)


with app.app_context():
    db.create_all()


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# main blog pages
# ////////////////////////////////////////////////////////


@app.route('/')
def main():
    page = request.args.get('page', 1, type=int)
    form = RegistrationForm()
    form1 = LoginForm()
    create_superuser()
    posts = POSTS.query.paginate(page=page, per_page=3)
    return render_template("main.html", form=form, form1=form1, admin_key=admin_key, posts=posts)


@app.route('/about_post/<int:post_id>')
def about_post(post_id):
    form = RegistrationForm()
    form1 = LoginForm()
    post = POSTS.query.filter_by(id=post_id).first()
    return render_template("about_post.html", form=form, form1=form1, admin_key=admin_key, post=post)


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
    if new_password is not None:
        if new_repeat_password is not None:
            if new_password == new_repeat_password:
                if len(new_password) >= 8:
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
@login_required
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
@login_required
def admin_create_post():
    title = request.form.get('title')
    author = request.form.get('author')
    text = request.form.get('text')
    if len(text) >= 1:
        if len(author) > 2:
            if len(title) >= 1:
                user = USERS.query.filter_by(username=author).first()
                db.session.add(POSTS(title=title, author=author, text=text, email_author=user.email))
                db.session.commit()
    return redirect(url_for("posts_control"))


@app.route(f'/delete_post/{admin_key}/<int:post_id>', methods=['GET', 'POST'])
@login_required
def admin_delete_post(post_id):
    post = POSTS.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("posts_control"))


@app.route('/posts_control/change_title/<int:post_id>', methods=['GET', 'POST'])
@login_required
def admin_change_title(post_id):
    form = RegistrationForm()
    form1 = LoginForm()
    form2 = CreatePost()
    post = POSTS.query.filter_by(id=post_id).first()
    if post is not None:
        return render_template("change_title.html", form=form, form1=form1, form2=form2, admin_key=admin_key,
                               post=post)
    else:
        return redirect(url_for("posts_control"))


@app.route('/change_t/<int:post_id>', methods=['GET', 'POST'])
@login_required
def change_title(post_id):
    title = request.form.get('title')
    if len(title) >= 1:
        post = POSTS.query.filter_by(id=post_id).first()
        post.title = title
        db.session.commit()
    return redirect(url_for("posts_control"))


@app.route('/posts_control/change_author/<int:post_id>', methods=['GET', 'POST'])
@login_required
def admin_change_author(post_id):
    form = RegistrationForm()
    form1 = LoginForm()
    users = USERS.query.all()
    post = POSTS.query.filter_by(id=post_id).first()
    if post is not None:
        return render_template("change_author.html", form=form, form1=form1, users=users, admin_key=admin_key,
                               post=post)
    else:
        return redirect(url_for("posts_control"))


@app.route('/change_a/<int:post_id>', methods=['GET', 'POST'])
@login_required
def change_author(post_id):
    author = request.form.get('author')
    if len(author) > 2:
        post = POSTS.query.filter_by(id=post_id).first()
        post.author = author
        db.session.commit()
    return redirect(url_for("posts_control"))


@app.route('/posts_control/change_text/<int:post_id>', methods=['GET', 'POST'])
@login_required
def admin_change_text(post_id):
    form = RegistrationForm()
    form1 = LoginForm()
    post = POSTS.query.filter_by(id=post_id).first()
    if post is not None:
        return render_template("change_text.html", form=form, form1=form1, admin_key=admin_key,
                               post=post)
    else:
        return redirect(url_for("posts_control"))


@app.route('/change_te/<int:post_id>', methods=['GET', 'POST'])
@login_required
def change_text(post_id):
    text = request.form.get('text')
    if len(text) >= 1:
        post = POSTS.query.filter_by(id=post_id).first()
        post.text = text
        db.session.commit()
    return redirect(url_for("posts_control"))


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# LSTM model
# ////////////////////////////////////////////////////////

def create_inout_sequences(input_data, tw):
    inout_seq = []
    L = len(input_data)
    for i in range(L - tw):
        train_seq = input_data[i:i + tw]
        train_label = input_data[i + tw:i + tw + 1]
        inout_seq.append((train_seq, train_label))
    return inout_seq


class LSTM(nn.Module):
    def __init__(self, input_size=1, hidden_layer_size=100, output_size=1):
        super().__init__()
        self.hidden_layer_size = hidden_layer_size

        self.lstm = nn.LSTM(input_size, hidden_layer_size)

        self.linear = nn.Linear(hidden_layer_size, output_size)

        self.hidden_cell = (torch.zeros(1, 1, self.hidden_layer_size),
                            torch.zeros(1, 1, self.hidden_layer_size))

    def forward(self, input_seq):
        lstm_out, self.hidden_cell = self.lstm(input_seq.view(len(input_seq), 1, -1), self.hidden_cell)
        predictions = self.linear(lstm_out.view(len(input_seq), -1))
        return predictions[-1]


@app.route('/LSTM/activate/', methods=['GET', 'POST'])
def LSTM_n():
    flight_data = sns.load_dataset("flights")
    if LSTM_m.query.count() != 0:
        LSTM_m.query.delete()
        db.session.commit()

    data_year = flight_data['year'].values.astype(int)[-12:]
    data_month = flight_data['month'].values.astype(str)[-12:]
    data_passengers = flight_data['passengers'].values.astype(float)

    test_data_size = 12
    train_data_pass = data_passengers[:-test_data_size]
    test_data_pass = data_passengers[-test_data_size:]

    scaler = MinMaxScaler(feature_range=(-1, 1))
    train_data_normalized = scaler.fit_transform(train_data_pass.reshape(-1, 1))
    train_data_normalized = torch.FloatTensor(train_data_normalized).view(-1)

    train_window = 12
    train_inout_seq = create_inout_sequences(train_data_normalized, train_window)

    model = LSTM()
    loss_function = nn.MSELoss()

    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    epochs = 150

    for i in range(epochs):
        for seq, labels in train_inout_seq:
            optimizer.zero_grad()
            model.hidden_cell = (torch.zeros(1, 1, model.hidden_layer_size),
                                 torch.zeros(1, 1, model.hidden_layer_size))
            y_pred = model(seq)
            single_loss = loss_function(y_pred, labels)
            single_loss.backward()
            optimizer.step()
        if i % 25 == 1:
            print(f'epoch: {i:3} loss: {single_loss.item():10.8f}')
    print(f'epoch: {i:3} loss: {single_loss.item():10.10f}')

    fut_pred = 12
    test_inputs = train_data_normalized[-train_window:].tolist()
    model.eval()

    for i in range(fut_pred):
        seq = torch.FloatTensor(test_inputs[-train_window:])
        with torch.no_grad():
            model.hidden = (torch.zeros(1, 1, model.hidden_layer_size),
                            torch.zeros(1, 1, model.hidden_layer_size))
            test_inputs.append(model(seq).item())

    predictions = scaler.inverse_transform(np.array(test_inputs[fut_pred:]).reshape(-1, 1))

    for i in range(fut_pred):
        db.session.add(LSTM_m(year=data_year[i], month=data_month[i], passengers=test_data_pass[i],
                              predictions=predictions[i][0],
                              wrong_answer=test_data_pass[i] - predictions[i][0]))

    db.session.commit()

    return redirect(url_for("LSTM_site_view"))


@app.route('/LSTM/', methods=['GET', 'POST'])
def LSTM_site_view():
    form = RegistrationForm()
    form1 = LoginForm()
    lstm = LSTM_m.query.all()
    c_lstm = LSTM_m.query.count()
    return render_template("LSTM.html", form=form, form1=form1, admin_key=admin_key, lstm=lstm, c_lstm=c_lstm)


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# Search
# ////////////////////////////////////////////////////////
@app.route('/search')
def search():
    search = '%{}%'.format(request.args.get('search'))
    form = RegistrationForm()
    form1 = LoginForm()
    page = request.args.get('page', 1, type=int)
    posts = POSTS.query.filter(POSTS.title.like(search) | POSTS.author.like(search) | POSTS.text.like(search)).paginate(
        page=page, per_page=3)
    return render_template("search.html", form=form, form1=form1, admin_key=admin_key, posts=posts, search=search)


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# Big search
# ////////////////////////////////////////////////////////
@app.route('/big_search', methods=['GET', 'POST'])
def big_search():
    search = '%{}%'.format(request.args.get('search'))
    dc
    chbox.sort()
    form = RegistrationForm()
    form1 = LoginForm()
    posts = ""
    if chbox == ['1']:
        posts = POSTS.query.filter(POSTS.author.like(search))
    if chbox == ['2']:
        posts = POSTS.query.filter(POSTS.email_author.like(search))
    if chbox == ['3']:
        posts = POSTS.query.filter(POSTS.title.like(search))
    if chbox == ['4']:
        posts = POSTS.query.filter(POSTS.text.like(search))
    if chbox == ['1', '2']:
        posts = POSTS.query.filter(POSTS.author.like(search) & POSTS.email_author.like(search))
    if chbox == ['2', '3']:
        posts = POSTS.query.filter(POSTS.email_author.like(search) & POSTS.title.like(search))
    if chbox == ['2', '4']:
        posts = POSTS.query.filter(POSTS.email_author.like(search) & POSTS.text.like(search))
    if chbox == ['3', '4']:
        posts = POSTS.query.filter(POSTS.title.like(search) & POSTS.text.like(search))
    if chbox == ['1', '3']:
        posts = POSTS.query.filter(POSTS.author.like(search) & POSTS.title.like(search))
    if chbox == ['1', '4']:
        posts = POSTS.query.filter(POSTS.author.like(search) & POSTS.text.like(search))
    if chbox == ['1', '2', '3']:
        posts = POSTS.query.filter(
            POSTS.author.like(search) & POSTS.email_author.like(search) & POSTS.title.like(search))
    if chbox == ['1', '2', '4']:
        posts = POSTS.query.filter(
            POSTS.author.like(search) & POSTS.email_author.like(search) & POSTS.text.like(search))
    if chbox == ['1', '3', '4']:
        posts = POSTS.query.filter(POSTS.author.like(search) & POSTS.title.like(search) & POSTS.text.like(search))
    if chbox == ['2', '3', '4']:
        posts = POSTS.query.filter(POSTS.email_author.like(search) & POSTS.title.like(search) & POSTS.text.like(search))
    if chbox == ['1', '2', '3', '4']:
        posts = POSTS.query.filter(
            POSTS.author.like(search) & POSTS.email_author.like(search) & POSTS.title.like(search) & POSTS.text.like(
                search))
    return render_template("big_search.html", form=form, form1=form1, admin_key=admin_key, posts=posts)


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

if __name__ == '__main__':
    app.run(host="0.0.0.0")
