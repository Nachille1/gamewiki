from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, IntegerField, PasswordField
from wtforms.validators import DataRequired


class SettingsForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    address = StringField('Адрес')
    about = StringField('О себе')
    submit = SubmitField('Сохранить')
