from flask import render_template, session, request, redirect, url_for, flash
from loja.produtos.models import Addproduto, Marca, Categoria
from loja import app, db, bcrypt
from .forms import RegistrationForm, LoginFormulario
from .models import User


@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Favor fazer seu login primeiro.','warning')
        return redirect(url_for('login'))
    produtos = Addproduto.query.all()
    return render_template('admin/index.html', title="Página Administrativa", produtos=produtos)

@app.route('/marcas')
def marcas():
    if 'email' not in session:
        flash(f'Favor fazer seu login primeiro.','warning')
        return redirect(url_for('login'))
    marcas = Marca.query.order_by(Marca.id.desc()).all()
    return render_template('admin/marca.html', title="Página Marcas", marcas=marcas)

@app.route('/categoria')
def categoria():
    if 'email' not in session:
        flash(f'Favor fazer seu login primeiro.','warning')
        return redirect(url_for('login'))
    categorias = Categoria.query.order_by(Categoria.id.desc()).all()
    return render_template('admin/marca.html', title='Página Categorias', categorias=categorias)

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Obrigado {form.name.data} por se Registrar', 'success')
        return redirect(url_for('login'))
    return render_template('admin/registrar.html', form=form, title="Página de Registros")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginFormulario(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(
                f'Você está logado com o e-mail: {form.email.data}', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash(f'Usuário não localizado em nossa base de dados.', 'danger')
    return render_template('admin/login.html', form=form, title='Página de Login')
