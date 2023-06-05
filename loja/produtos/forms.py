from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators, DecimalField


class Addprodutos(Form):
    name = StringField('Nome :', [validators.DataRequired()])
    price = DecimalField('Preço :', [validators.DataRequired()])
    discount = IntegerField('Desconto :', [validators.DataRequired()])
    stock = IntegerField('Estoque :', [validators.DataRequired()])
    discription = TextAreaField('Descrição :', [validators.DataRequired()])
    colors = TextAreaField('Cor :', [validators.DataRequired()])

    image_1 = FileField('Imagem 1 :' , validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    image_2 = FileField('Imagem 2 :' , validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    image_3 = FileField('Imagem 3 :' , validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])]) 