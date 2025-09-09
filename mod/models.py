from mod import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def loder_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=True)
    data_nascimento = db.Column(db.Integer, nullable=True)
    UF = db.Column(db.String, default='Konoha')
    email = db.Column(db.String, nullable=True)
    senha = db.Column(db.String, nullable=True)

class comentarios(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(db.Date, default=datetime.utcnow())
    mensagem = db.Column(db.String)
    
    