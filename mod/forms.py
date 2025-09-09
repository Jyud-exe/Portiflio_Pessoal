from wtforms import StringField, PasswordField, SubmitField, DateField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, ValidationError
from mod.models import User, db, comentarios
from werkzeug.security import generate_password_hash, check_password_hash


class cadForm(FlaskForm):
    nome_completo = StringField('Nome Completo', validators=[DataRequired()])
    data_nascimento = DateField('Data de Nascimento', validators=[DataRequired()])
    UF = StringField('UF', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired()])
    btn = SubmitField('Cadastrar')

    def save(self):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            raise ValidationError('Email ja cadastrado!')
        else:
            senha = generate_password_hash(self.senha.data)
            novo_usuario = User(
                nome=self.nome_completo.data,
                data_nascimento=self.data_nascimento.data,
                UF=self.UF.data,
                email=self.email.data,
                senha=senha
            )

            db.session.add(novo_usuario)
            db.session.commit()
            return novo_usuario
        
class loginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    btnsubmit = SubmitField('Entrar')

    def login(self):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            if check_password_hash(user.senha, self.senha.data):
                return user
            else:
                raise ValidationError('Senha Incorreta!')
        else:
            raise ValidationError('Usuario Invalido!')
        
class feedForms(FlaskForm):
    comentario = StringField('Comentário')
    btncom = SubmitField('Enviar')

    def save(self, user_id):
        feedback = comentarios(
            coment=self.comentario.data,
            user_id=self.user_id.data
        )

        db.session.add(feedback)
        db.session.commit()
        return feedback