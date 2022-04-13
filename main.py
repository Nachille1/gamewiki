from flask import Flask, render_template, redirect, request
from data import db_session
from data.users import User
from data.loginform import LoginForm
from data.settingsform import SettingsForm
from flask_login import LoginManager, login_user, login_required, logout_user
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def main():
    return render_template('news.html', title='GameWiki')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/user/<int:id>', methods=['GET', 'POST'])
def profile(id):
    return render_template('profile.html', title='Профиль')


@app.route('/profile_settings/<int:user_id>', methods=['GET', 'POST'])
def profile_settings(user_id):
    form = SettingsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            user.age = form.age.data
            user.address = form.address.data
            user.about = form.about.data
            db_sess.commit()
            return redirect("/")
        return render_template('profile_settings.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('profile_settings.html', title='Настройки профиля', form=form)


@app.route('/dota2')
def dota_news():
    return render_template('dota2.html', title='Dota 2')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    db_session.global_init("db/GameWiki.db")
    app.run()
