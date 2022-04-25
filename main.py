import datetime
from flask import Flask, render_template, redirect, request, url_for
from data import db_session
from data.users import User
from data.add_news import AddNews
from forms.loginform import LoginForm
from forms.settingsform import SettingsForm
from flask_login import LoginManager, login_user, login_required, logout_user
from forms.user import RegisterForm
from forms.add_newsform import AddNewsForm
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
uploads_dir = os.path.join('', 'static/img')


@app.route('/')
def main():
    db_sess = db_session.create_session()
    news_list = db_sess.query(AddNews).all()
    return render_template('news.html', title='GameWiki', news_list=news_list[::-1])


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
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    return render_template('profile.html', title='Профиль', user=user)


@app.route('/profile_settings/<int:user_id>', methods=['GET', 'POST'])
def profile_settings(user_id):
    form = SettingsForm()
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    if request.method == 'POST':
        if request.files['profile']:
            profile = request.files['profile']
            profile.save(os.path.join(uploads_dir, secure_filename(profile.filename)))
            for file in request.files.getlist('charts'):
                file.save(os.path.join(uploads_dir, secure_filename(file.name)))
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            user.age = form.age.data
            user.address = form.address.data
            user.about = form.about.data
            if request.files['profile']:
                user.profile_image = f'../static/img/{profile.filename}'
            db_sess.commit()
            return redirect("/")
        return render_template('profile_settings.html',
                               message="Неправильный логин или пароль",
                               form=form)
    form.age.data = user.age
    form.about.data = user.about
    form.email.data = user.email
    form.address.data = user.address
    return render_template('profile_settings.html', title='Настройки профиля', form=form)


@app.route('/dota2')
def dota_news():
    db_sess = db_session.create_session()
    news_list = db_sess.query(AddNews).filter(AddNews.game == 'dota').all()
    return render_template('dota2.html', title='Dota 2', news_list=news_list[::-1])


@app.route('/add_news_dota', methods=['GET', 'POST'])
def add_news_dota():
    form = AddNewsForm()
    if request.method == 'POST':
        if request.files['profile']:
            profile = request.files['profile']
            profile.save(os.path.join(uploads_dir, secure_filename(profile.filename)))
            for file in request.files.getlist('charts'):
                file.save(os.path.join(uploads_dir, secure_filename(file.name)))
            db_sess = db_session.create_session()
            add_new = AddNews()
            add_new.header = form.header.data
            add_new.description = form.description.data
            add_new.game = 'dota'
            add_new.date = datetime.datetime.now().strftime('%d %b %Y')
            add_new.image = f'../static/img/{profile.filename}'
            db_sess.add(add_new)
            db_sess.commit()
            return redirect("/dota2")
        else:
            return render_template('add_news.html', title='Добавление новости', form=form, message='Добавьте картинку!')
    return render_template('add_news.html', title='Добавление новости', form=form)


@app.route('/cs')
def cs_news():
    db_sess = db_session.create_session()
    news_list = db_sess.query(AddNews).filter(AddNews.game == 'cs').all()
    return render_template('cs.html', title='CS:GO', news_list=news_list[::-1])


@app.route('/add_news_cs', methods=['GET', 'POST'])
def add_news_cs():
    form = AddNewsForm()
    if request.method == 'POST':
        if request.files['profile']:
            profile = request.files['profile']
            profile.save(os.path.join(uploads_dir, secure_filename(profile.filename)))
            for file in request.files.getlist('charts'):
                file.save(os.path.join(uploads_dir, secure_filename(file.name)))
        db_sess = db_session.create_session()
        add_new = AddNews()
        add_new.header = form.header.data
        add_new.description = form.description.data
        add_new.game = 'cs'
        add_new.date = datetime.datetime.now().strftime('%d %b %Y')
        add_new.image = f'../static/img/{profile.filename}'
        db_sess.add(add_new)
        db_sess.commit()
        return redirect("/cs")
    return render_template('add_news.html', title='Добавление новости', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/cs_for_new_players')
def cs_for_new_players():
    return render_template('cs_for_new_players.html', title='Кс для новичков')


@app.route('/cs_guns')
def cs_guns():
    return render_template('cs_guns.html', title='Оружие в кс')


@app.route('/cs_economy')
def cs_economy():
    return render_template('cs_economy.html', title='Экономика в кс')


@app.route('/dota_for_new_players')
def dota_for_new_players():
    return render_template('dota_for_new_players.html', title='Дота для новичков')


@app.route('/dota_choice')
def dota_choice():
    return render_template('dota_choice.html', title='Дота для новичков')


@app.route('/dota_heroes_for_new_players')
def dota_heroes_for_new_players():
    return render_template('dota_heroes_for_new_players.html', title='Дота для новичков')


@app.route('/dota_sokrasheniya')
def dota_sokrasheniya():
    return render_template('dota_sokrasheniya.html', title='Сокращения Dota 2')


@app.route('/cs_choice')
def cs_choice():
    return render_template('cs_choice.html', title='Кс для новичков')


if __name__ == '__main__':
    db_session.global_init("db/GameWiki.db")
    app.run()
