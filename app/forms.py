from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

import os
from werkzeug.utils import secure_filename

from app import db, bcrypt, app
from app.models import Contato, User, Post, PostComentarios


class LoginForm(FlaskForm):
    #Email() para validar o email
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    #criada a confirmação de senha e a verificação de igualdade com o EqualTo()
    senha = PasswordField('Senha', validators=[DataRequired()])
    #botao
    btnSubmit = SubmitField('Login')
    def login(self):
        #recuperar o usuário do e-mail
        user = User.query.filter_by(email=self.email.data).first()
        #verificar se a senha é valida
        if user:
            if bcrypt.check_password_hash(user.senha, self.senha.data.encode('utf-8')):
                #login
                return user
            else:
                return 'Senha incorreta'
        else:
            return 'Usuário não encontrado'
        
#formulario padrao
class UserForm(FlaskForm):
    #todos os campos com obrigação de preenchimento: datarequired
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    #Email() para validar o email
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    #criada a confirmação de senha e a verificação de igualdade com o EqualTo()
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Confirmação de senha', validators=[DataRequired(), EqualTo('senha')])
    #botao
    btnSubmit = SubmitField('Cadastrar')

    
    #validação de ususario ja cadastrado
    def validate_email(self, email):
         # Verifica se o email já existe, excluindo o usuário atual
        if hasattr(self, 'user_id'):  # Se estivermos atualizando
            if User.query.filter(User.email == email.data, User.id != self.user_id).first():
                raise ValidationError('Usuário já cadastrado com esse E-mail!')
        else:  # Se estivermos criando
            if User.query.filter(User.email == email.data).first():
                raise ValidationError('Usuário já cadastrado com esse E-mail!')

    #logica de salvamento no bd
    def save(self):
        ##gera o hash da senha tratando a codificação utf-8
        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))
        #cria o usuario
        user = User(
            nome = self.nome.data,
            sobrenome = self.sobrenome.data,
            email = self.email.data,
            senha = senha
        )
        #passa o usuario para a sessão
        db.session.add(user)
        #salva o ususario no banco
        db.session.commit()
        #retorna o usuario para view
        return user


class UserFormUpdate(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    # Tornar a senha opcional para edição
    senha = PasswordField('Senha (deixe em branco para não alterar)')
    confirmacao_senha = PasswordField('Confirmação de senha', 
                                    validators=[EqualTo('senha', message='As senhas devem ser iguais')])
    btnSubmit = SubmitField('Atualizar')

    def validate_email(self, email):
        if hasattr(self, 'user_id'):
            if User.query.filter(User.email == email.data, User.id != self.user_id).first():
                raise ValidationError('E-mail já está em uso por outro usuário!')

    def update_user(self, user):
        user.nome = self.nome.data
        user.sobrenome = self.sobrenome.data
        user.email = self.email.data
        if self.senha.data:  # Só atualiza senha se foi fornecida
            user.senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))
        db.session.commit()


class ContatoForm(FlaskForm):
    email = SelectField('E-mail', validators=[DataRequired()], choices=[])
    assunto = StringField('Assunto', validators=[DataRequired()])
    mensagem = TextAreaField('Mensagem', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')

    def __init__(self, *args, **kwargs):
        super(ContatoForm, self).__init__(*args, **kwargs)
        # Atualiza as opções do SelectField com os emails do banco de dados
        self.email.choices = [(user.email, user.email) for user in User.query.all()]

    def save(self, email_usuario, nome_usuario):
        contato = Contato(
            nome = nome_usuario,
            email_destino = self.email.data,
            email_usuario = email_usuario,
            assunto = self.assunto.data,
            mensagem = self.mensagem.data
        )


        db.session.add(contato)
        db.session.commit()

class RespostaForm(FlaskForm):
    mensagem = TextAreaField('Resposta', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar Resposta')
    
class PostForm(FlaskForm):
    mensagem = StringField('Mensagem', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')
    imagem = FileField('Imagem')

    def save(self, user_id):
        imagem = self.imagem.data
        nome_seguro = secure_filename(imagem.filename)
        post = Post(
            mensagem = self.mensagem.data,
            user_id = user_id,
            imagem = nome_seguro
        )

        caminho = os.path.join(
            #Pegar a pasta que está o projeto
            os.path.abspath(os.path.dirname(__file__)),
            #Definir a pasta que está configurada
            app.config['UPLOAD_FILES'],
            #A pasta que está os POST
            'post',
            nome_seguro
        )
        if imagem:
            imagem.save(caminho)

        db.session.add(post)
        db.session.commit()

class PostComentarioForm(FlaskForm):
    comentario = StringField('Mensagem', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')

    def save(self, user_id, post_id):
        comentario = PostComentarios(
            comentario = self.comentario.data,
            user_id = user_id,
            post_id = post_id
        )

        db.session.add(comentario)
        db.session.commit()