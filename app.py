from flask import Flask, request, render_template, redirect, abort, session
from flask_sqlalchemy import SQLAlchemy
import pyqrcode
import os
import random
import time
from datetime import datetime

# App Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/nutri.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secret key
app.secret_key = b'nutri-informeai'

# Database
db = SQLAlchemy(app)

# Logger
def log(msg:str,tipo:str):
    with open('log/logger.log','a') as file_log:
        if tipo == 'INFO':
            file_log.write('{0}:{1}:{2}:{3}:{4}:{5}:{6}\n'.format(time.asctime(),tipo,request.remote_addr,request.method,'/'+request.endpoint,msg,request.user_agent))
            file_log.close()



# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(20), unique=True, nullable=True, index=True)
    password = db.Column(db.String(200), nullable=False, unique=False)
    create_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    last_login = db.Column(db.DateTime, nullable=False, default=datetime.now)

    
    def __repr__(self):
        return f'<User -> id:{self.id}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True, unique=True)
    pug = db.Column(db.String(50), nullable=True, unique=True, index=True)
    porcao = db.Column(db.String(10))
    calorias = db.Column(db.String(10))
    proteinas = db.Column(db.String(10))
    carboidratos = db.Column(db.String(10))
    gordurasTrans = db.Column(db.String(10))
    gordurasTotais = db.Column(db.String(10))
    porcentagemDia = db.Column(db.String(10))

    def __repr__(self):
        return f'<Product -> id:{self.id}, name:{self.name}>'

# Funcões CRUD USER
def create_user(user_name, user_password):
    
    user = User(name=user_name, password=user_password)
    verify_user = get_user(user_name,user_password)
    if verify_user == None:
        db.session.add(user)
        db.session.commit()
        return True
    else:
        return False
        
def get_user(user_name,user_password):
    user = User.query.filter_by(name=user_name).first()
    if user and user.name == user_name and user.password == user_password:
        return user
    else:
        return None

def delete_user(user_name):
    user = User.query.filter_by(name=user_name).first()
    if user and user.name != 'admin':
        db.session.delete(user)
        db.session.commit()
        return True
    else:
        return False

def update_user(user_name, user_password):
    user = User.query.filter_by(name=user_name).first()
    if user and user.name != 'admin':
        db.session.delete(user)
        user_updated = User(name=user_name, password=user_password)
        db.session.add(user_updated)
        db.commit()
        return True
    else:
        return False

# Funções CRUD PRODUCT
def create_product(product):
    prod = get_product(product)
    
    if not prod:
        product_new = Product(name=product.name, pug=product.pug, porcao=product.porcao, calorias=product.calorias, 
        proteinas=product.proteinas,carboidratos=product.carboidratos,gordurasTrans=product.gordurasTrans, 
        gordurasTotais=product.gordurasTotais,porcentagemDia=product.porcentagemDia)

        db.session.add(product_new)
        db.session.commit()
        return True
    else:
        return False

def get_product(product):
    prod = Product.query.filter_by(pug=product.pug).first()
    if prod:
        return prod
    else:
        return None

def delete_product(product):
    product = get_product(product)
    if product:
        db.session.delete(product)
        db.session.commit()
        return True
    else:
        return False

def update_product(product):
    prod = get_product(product)
    if prod:
        product_updated = Product(name=product.name, porcao=product.porcao, calorias=product.calorias, 
        proteinas=product.proteinas,carboidratos=product.carboidratos,gordurasTrans=product.gordurasTrans, 
        gordurasTotais=product.gordurasTotais,porcentagemDia=product.porcentagemDia)
        db.session.delete(prod)
        db.session.add(product_updated)
        db.session.commit()
        return True
    else:
        return False


# Create Tables
db.create_all()

# Views
@app.route('/')
def index():
    log('Acesso a pagina principal','INFO')
    if 'username' in session and 'password' in session:
        return redirect('/product')
    else:
        return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    log('Acesso a pagina login', 'INFO')
    title_login = 'Nutri - Login'
    if request.method == 'POST':
        login_name = request.form.get('name')
        login_pass = request.form.get('pass')
        user = get_user(login_name,login_pass)
        if user != None:
            session['username'] = user.name
            session['password'] = user.password
            return redirect('/product')
        else:
            log('Usuario não logou','INFO')
            return redirect('/bad')
    if 'username' in session and 'password' in session:
        return redirect('/product')
    else:
        return render_template('login.html', login_title=title_login)

@app.route('/cadastrar', methods=['GET','POST'])
def cadastrar():
    if request.method == 'POST':
        log('Acesso a pagina cadastrar via post', 'INFO')
        user_name = request.form.get('name')
        user_password = request.form.get('pass')
        if user_name and user_password:
            user_created = create_user(user_name, user_password)
            if user_created:
                return redirect('/login')
            else:
                return render_template('user-cadastrado.html')
    if 'username' in session and 'password' in session:
        log('Usuario logado', 'INFO')
        return render_template('cadastro.html')
    else:
        log('Usuario não logado', 'INFO')
        return redirect('/login')

@app.route('/users', methods=['GET','POST'])
def users():
    if request.method == 'POST':
        return f'voltar para users'
    else:
        if 'username' in session and 'password' in session:
            log('Usuario logado na pagina users','INFO')
            return render_template('users.html')
        else:
            log('Usuario não logado','INFO')
            return redirect('/login')

@app.route('/bad', methods=['GET'])
def bad():
    log('Pagina não encontrada','WARNING')
    return render_template('404.html')


@app.route('/product', methods=['GET','POST'])
def product():
    if request.method == 'POST':
        log('Usuario logado na pagina product via post','INFO')
        prod_name = request.form['name']
        prod_porcao = request.form['porcao']
        prod_calorias = request.form['calorias']
        prod_proteinas = request.form['proteinas']
        prod_carboidratos = request.form['carboidratos']
        prod_gordurasTrans = request.form['gordurasTrans']
        prod_gordurasTotais = request.form['gordurasTotais']
        prod_porcentagemDia = request.form['porcentagemDia']
        
        # Criar o Produto
        product.name = prod_name
        product.porcao = prod_porcao
        product.calorias = prod_calorias
        product.proteinas = prod_proteinas
        product.carboidratos = prod_carboidratos
        product.gordurasTrans = prod_gordurasTrans
        product.gordurasTotais = prod_gordurasTotais
        product.porcentagemDia = prod_porcentagemDia
        product.pug = str(product.name).replace(' ','').lower().strip()
        # Add ao Banco
        result = create_product(product)
        if result:
            return render_template('prod-cadastrado.html')
        else:
            return render_template('prod-ja-cadastrado.html')
    else:
        if 'username' in session and 'password' in session:
            log('Usuario logado na pagina product','INFO')
            return render_template('product.html')
        else:
            log('Usuario não logado','INFO')
            return redirect('/login')

    
@app.route('/products/<prod>', methods=['GET'])
def products(prod):
    listColors = ['#6610f2','#007bff','#e83e8c','#fd7e14','#20c997','#17a2b8']
    # Verificar se existe o produto no database
    prd = Product.query.filter_by(pug=prod).first()
    if prd:
        log('Usuario logado com acesso ao produto {0}'.format(prd.name),'INFO')
        return render_template('products.html',product=prd, colors=listColors, rand=random)
    else:
        log('Pagina não encontrada','INFO')
        return render_template('404.html')

def main():
    port = int(os.environ.get('PORT',5000))
    host = '0.0.0.0'
    app.run(host=host,port=port,debug=False)


if __name__ == '__main__':
    main()