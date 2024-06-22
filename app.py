from flask import Flask, request, jsonfy, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

# implementa a tabela users e define a classe User
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def __init__(self, username, email):
        self.username = username
        self.email = email
        
    def json(self):
        return{'id': id, 'username': self.username,'email': self.email}
    
    db.create_all()
    
# implementa rota de teste
@app.route('/test', methods=['GET'])
def test():
    return make_response(jsonfy({'message':'teste ok, subiu'}), 200)

# Criar Usuário
@app.route('/users',methos=['POST'])    
def create_user():
    try:
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonfy({'message': 'usuario criado.'}),201)
    except e:
        return make_response(jsonfy({'message': 'Erro na criação de usuário'}),500)
    
#to-do get users // 08:04 https://youtu.be/fHQWTsWqBdE?list=PL4-O7mT21E3roXTNDUpfu6BvgV7vgNP9s&t=484



        