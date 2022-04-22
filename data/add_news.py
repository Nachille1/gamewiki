import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class AddNews(SqlAlchemyBase, UserMixin):
    __tablename__ = 'news'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    header = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.Text)
    game = sqlalchemy.Column(sqlalchemy.String)
    date = sqlalchemy.Column(sqlalchemy.String)
