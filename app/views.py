from app import app, db
from flask import render_template, url_for, request, redirect
from flask_login import login_user, logout_user, current_user, login_required
import datetime
from app.models import Contato, Post, User
from app.forms import ContatoForm, UserForm, LoginForm, PostForm, PostComentarioForm, UserFormUpdate


@app.route('/', methods=['GET', 'POST'])
def homepage():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)

    print(current_user.is_authenticated)
    return render_template('index.html', form=form)

@app.route('/post/novo', methods=['GET', 'POST'])
@login_required
def PostNovo():
    form = PostForm()
    if form.validate_on_submit():
        form.save(current_user.id)
        return redirect(url_for('PostLista'))

    return render_template('post_novo.html', form=form)

@app.route('/post/lista/')
@login_required
def PostLista():
    
    posts = Post.query.all()
    
    return render_template('post_lista.html', posts=posts)


@app.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def PostDetail(id):
    post = Post.query.get(id)
    form = PostComentarioForm()
    if form.validate_on_submit():
        form.save(current_user.id, id)
        return redirect(url_for('PostDetail', id=id))
    return render_template('post.html', post = post, form = form)


@app.route('/cadastro/', methods=['GET', 'POST'])
def cadastro():
    form = UserForm()
    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template('cadastro.html', form=form)


@app.route('/sair/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/contato/lista/')
@login_required
def contatoLista():
    
    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa', '')

    dados = Contato.query.filter_by(email_destino=current_user.email)
    if pesquisa != '':
        dados = dados.filter_by(nome=pesquisa)
        
    context = {'dados': dados.all()}

    return render_template('contato_lista.html', context=context)

@app.route('/user/')
@login_required
def DadosUsuario():
    return render_template('dados_usuario.html', user=current_user)



@app.route('/user/edit/', methods=['GET', 'POST'])
@login_required
def DadosUsuarioEdit():
    user = current_user
    form = UserFormUpdate(obj=user)
    form.user_id = user.id
    if request.method == 'POST': 
        if form.validate_on_submit():
            form.update_user(user)
            return redirect(url_for('DadosUsuario')) 
        else:
            print("Formulário inválido! Erros:", form.errors)

    return render_template('dados_usuario_edit.html', user=current_user, form=form)


@app.route('/contato/<int:id>/')
@login_required
def contatoDetail(id):
    obj = Contato.query.get(id)
    return render_template('contato_detail.html', obj=obj)



@app.route('/contato/', methods=['GET', 'POST'])
@login_required
def contato():
    form = ContatoForm()
    contatos = User.query.all()
    context = {}
    print(form)
    print(form.email)
    if form.validate_on_submit():
        print(form.email)
        form.save(current_user.email, current_user.nome)
        return redirect(url_for('homepage'))
    return render_template('contato.html', context=context, form=form, contatos=contatos)


#formato não recomendado
@app.route('/contato_old/', methods=['GET', 'POST'])
@login_required
def contato_old():
    context = {}
    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa')
        context.update({'pesquisa': pesquisa})
        print('GET ', pesquisa)
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        assunto = request.form['assunto']
        mensagem = request.form['mensagem']
        
        contato = Contato(
            nome=nome,
            email=email,
            assunto=assunto,
            mensagem=mensagem
        )
        db.session.add(contato)
        db.session.commit()
    return render_template('contato_old.html', context=context)