from loja.admin.rotas import categoria
from flask import redirect, render_template, url_for, flash, request, session, current_app
from .forms import Addprodutos
from loja import db, app, photos
from .models import Marca, Categoria, Addproduto
import secrets,os


@app.route('/addmarca', methods=['GET','POST'])
def addmarca():
    if 'email' not in session:
        flash(f'Favor fazer seu login primeiro.', 'warning')
        return redirect(url_for('login'))

    if request.method == "POST":
        getmarca = request.form.get('marca')
        marca = Marca(name=getmarca)
        db.session.add(marca)
        flash(f'A marca {getmarca} foi cadastrada com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('addmarca'))
    return render_template('/produtos/addmarca.html', marcas='marcas')


@app.route('/updatemarca/<int:id>', methods = ['POST', 'GET'])
def updatemarca(id):
    if 'email' not in session:
        flash(f'Favor fazer seu login primeiro.', 'warning')
        return redirect(url_for('login'))
    updatemarca = Marca.query.get_or_404(id)
    marca = request.form.get('marca')
    if request.method=='POST':
        updatemarca.name = marca
        flash(f'Sua marca foi atualizada com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('marcas'))

    return render_template('/produtos/updatemarca.html',title='Atualizar Marcas',updatemarca=updatemarca)


@app.route('/deletemarca/<int:id>',methods=['POST'])
def deletemarca(id):
    marca = Marca.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(marca)
        db.session.commit()
        flash(f'A Marca {marca.name} Foi Deletada com sucesso', 'success')
        return redirect(url_for('admin'))
    flash(f'A Marca {marca.name} Não foi deletada', 'warning')
    return redirect(url_for('admin'))


@app.route('/addcat', methods=['GET','POST'])
def addcat():
    if 'email' not in session:
        flash(f'Favor fazer seu login primeiro.', 'warning')
        return redirect(url_for('login'))

    if request.method == "POST":
        getmarca = request.form.get('categoria')
        cat = Categoria(name=getmarca)
        db.session.add(cat)
        flash(f'A categoria {getmarca} foi cadastrada com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('/produtos/addmarca.html')


@app.route('/updatecat/<int:id>', methods = ['POST', 'GET'])
def updatecat(id):
    if 'email' not in session:
        flash(f'Favor fazer seu login primeiro.', 'warning')
        return redirect(url_for('login'))
    updatecat = Categoria.query.get_or_404(id)
    categoria = request.form.get('categoria')
    if request.method == 'POST':
        updatecat.name = categoria
        flash(f'Sua categoria foi atualizada com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('categoria'))
    return render_template('/produtos/updatemarca.html', title='Atualizar Categoria', updatecat=updatecat)


@app.route('/addproduto', methods=['GET','POST'])
def addproduto():
    if 'email' not in session:
        flash(f'Favor fazer seu login primeiro.', 'warning')
        return redirect(url_for('login'))

    marcas = Marca.query.all()
    categorias = Categoria.query.all()
    form = Addprodutos(request.form)
    if request.method == "POST":

        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.discription.data
        marca = request.form.get('marca')
        categoria = request.form.get('categoria')

        image_1 = photos.save(request.files.get(
            'image_1'), name=secrets.token_hex(10)+".")
        image_2 = photos.save(request.files.get(
            'image_2'), name=secrets.token_hex(10)+".")
        image_3 = photos.save(request.files.get(
            'image_3'), name=secrets.token_hex(10)+".")

        addpro = Addproduto(name=name, price=price, discount=discount, stock=stock, colors=colors, desc=desc,
                            marca_id=marca, categoria_id=categoria, image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(addpro)
        flash(f'Produto {name} foi cadastrada com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('produtos/addproduto.html', title="Cadastrar Produtos", form=form, marcas=marcas, categorias=categorias)


@app.route('/updateproduto/<int:id>', methods = ['POST', 'GET'])
def updateproduto(id):
    marcas = Marca.query.all()
    categorias = Categoria.query.all()
    produto = Addproduto.query.get_or_404(id)
    marca = request.form.get('marca')
    categoria = request.form.get('categoria')
    form = Addprodutos(request.form)
    if request.method=="POST":
        produto.name = form.name.data
        produto.price = form.price.data
        produto.discount = form.discount.data

        produto.categoria_id = categoria
        produto.marca_id = marca

        produto.stock = form.stock.data
        produto.colors = form.colors.data
        produto.desc = form.discription.data

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/" + produto.image_1))
                produto.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                produto.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/" + produto.image_2))
                produto.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                produto.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/" + produto.image_3))
                produto.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                produto.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
                            
        db.session.commit()
        flash(f'Produto foi atualizado com sucesso', 'success')
        return redirect('/')

    form.name.data = produto.name
    form.price.data = produto.price
    form.discription.data = produto.desc
    form.stock.data = produto.stock
    form.colors.data = produto.colors
    form.discount.data = produto.discount

    return render_template('/produtos/updateproduto.html', title='Atualizar Produtos', form=form,marcas=marcas,categorias=categorias,produto=produto)