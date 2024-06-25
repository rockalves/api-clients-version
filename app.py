from flask import Flask, request, jsonfy, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)
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
@app.route('/users',methods=['POST'])    
def create_user():
  try:
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return make_response(jsonfy({'message': 'usuario criado.'}), 201)
  except e:
    return make_response(jsonfy({'message': 'Erro na criação de usuário'}), 500)

# Retornar todos os Usuários    
@app.route('/users', methods=['GET'])
def get_users():
  try:
    users = User.query.all()
    return make_response(jsonfy({'users': [user.json() for user in users]}), 200)
  except e:
    return make_response(jsonfy({'message': 'Erro na criação de usuário'}), 500)

# Retronar usuário pelo id
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      return make_response(jsonfy({'user': user.json()}), 200)
    return make_response(jsonfy({'message': 'Usuário não encontrado'}), 404)
  except e:
    return make_response(jsonfy({'message': 'Erro ao recuperar o usuário'}),500)

# Atualizar o usuário pelo id
@app.route('/users/<int:id>', methods=['PUT'])
def update_user (id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      data = request.get_json()
      user.username = data['username']
      user.email = data =['email']
      db.session.commit()
      return make_response(jsonfy({'message': 'Usuário atualizado'}), 200)
    return make_response(jsonfy({'message': 'Usuário não encontrado'}), 404)
  except e:
    return make_response(jsonfy({'message': 'Erro ao atualizar o usuário'}), 500)
  
# Deletar o usuário
@app.route ('/users/<int:id>', methods = ['DELETE'])
def delete_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      db.session.delete(user)
      db.session.commit()
      return make_response(jsonfy({'message': 'Usuário deletado'}), 200)
    return make_response(jsonfy({'message': 'Usuário não encontrado'}), 404)
  except e:
    return make_response(jsonfy({'message': 'Erro ao excluir o usuário'}), 500)


#https://www.youtube.com/watch?v=fHQWTsWqBdE&list=PL4-O7mT21E3roXTNDUpfu6BvgV7vgNP9s&t=484s

