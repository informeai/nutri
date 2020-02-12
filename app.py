from flask import Flask, request, render_template, redirect, abort
from flask_sqlalchemy import SQLAlchemy


# App Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/nutri.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=True, index=True)
    password = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<User -> id:{self.id}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True, unique=True, index=True)
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

# Funções CRUD PRODUCT
def create_product(product):
    pass

def get_product(product):
    pass

def delete_product(product):
    pass

def update_product(product):
    pass

# Create Tables
db.create_all()

# Views
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    title_login = 'Nutri - Login'
    if request.method == 'POST':
        login_name = request.form.get('name')
        login_pass = request.form.get('pass')
        result = get_user(login_name,login_pass)
        if result != None:
            return redirect('/product')
        else:
            return redirect('/bad')

    return render_template('login.html', login_title=title_login)

@app.route('/cadastrar', methods=['GET','POST'])
def cadastrar():
    if request.method == 'POST':
        user_name = request.form.get('name')
        user_password = request.form.get('pass')
        if user_name and user_password:
            user_created = create_user(user_name, user_password)
            if user_created:
                return redirect('/login')
            else:
                return render_template('user-cadastrado.html')

    return render_template('cadastro.html')

@app.route('/users', methods=['GET','POST'])
def users():
    if request.method == 'POST':
        return f'voltar para users'
    else:
        return render_template('users.html')

@app.route('/bad', methods=['GET'])
def bad():
    return render_template('404.html')


@app.route('/product', methods=['GET','POST'])
def product():
    if request.method == 'POST':
        return f'voltar para products'
    else:
        return render_template('product.html')