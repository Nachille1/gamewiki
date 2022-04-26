from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class AddNewsRandomGame(FlaskForm):
    game = StringField('Название игры', validators=[DataRequired()])
    header = StringField('Заголовок', validators=[DataRequired()])
    description = TextAreaField('Описание')
    submit = SubmitField('Сохранить')
