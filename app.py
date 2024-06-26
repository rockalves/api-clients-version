from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)
class ClientEnvVersion(db.Model):
  __tablename__ = 'client_versions'
  id = db.Column(db.Integer, primary_key=True)
  env = db.Column(db.Integer, nullable=False)
  unimed = db.Column(db.Integer, unique=True, nullable=False)
  url = db.Column(db.String(150), unique=True, nullable=False)
  modify_date = db.Column(db.Date, nullable=False, default=date.today)
  version_reg_date = db.Column(db.Date)
  last_version = db.Column(db.String(20))

  def __init__(self, env, unimed, url, modify_date, version_reg_date, last_version):
    self.env = env
    self.unimed = unimed
    self.url = url
    self.modify_date = modify_date
    self.version_reg_date = version_reg_date
    self.last_version = last_version
      
  def json(self):
    return{'id': self.id, 'env': self.env, 'unimed': self.unimed, 'url': self.url, 'modify_date': self.modify_date, 'version_reg_date': self.version_reg_date, 'last_version':self.last_version} 

db.create_all()

# implementa rota de teste
@app.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message':'teste ok, subiu'}), 200)

# Criar cliente
@app.route('/client_version',methods=['POST'])    
def create_client_env():
  try:
    data = request.get_json()
    new_client_env = ClientEnvVersion(env=data['env'], unimed=data['unimed'], url=data['url'], modify_date=data['modify_date'], version_reg_date=data['version_reg_date'], last_version=data['last_version'])
    db.session.add(new_client_env)
    db.session.commit()
    return make_response(jsonify({'message': 'Cliente / Ambiente criado.'}), 201)
  except e:
    return make_response(jsonify({'message': 'Erro na criação do ambiente / cliente'}), 500)

# Retornar todos os clientes    
@app.route('/client_version', methods=['GET'])
def get_clients():
  try:
    client_versions = ClientEnvVersion.query.all()
    return make_response(jsonify([client_version.json() for client_version in client_versions ]), 200)
  except e:
    return make_response(jsonify({'message': 'Erro ao retornar clientes'}), 500)

# Retronar cliente pelo id
@app.route('/client_version/<int:id>', methods=['GET'])
def get_client(id):
  try:
    client_version = ClientEnvVersion.query.filter_by(id=id).first()
    if client_version:
      return make_response(jsonify({'client_version': client_version.json()}), 200)
    return make_response(jsonify({'message': 'Cliente não encontrado'}), 404)
  except e:
    return make_response(jsonify({'message': 'Erro ao recuperar o cliente'}),500)


# Atualizar o cliente pelo id
@app.route('/client_version/<int:id>', methods=['PUT'])
def update_client (id):
  try:
    client_version = ClientEnvVersion.query.filter_by(id=id).first()
    if client_version:
      data = request.get_json()
      client_version.env = data['env']
      client_version.unimed = data['unimed']
      client_version.url = data['url']
      client_version.modify_date = data['modify_date']
      client_version.version_reg_date = data['version_reg_date']
      client_version.last_version = data['last_version']
      db.session.commit()
      return make_response(jsonify({'message': 'Cliente atualizado'}), 200)
    return make_response(jsonify({'message': 'Cliente não encontrado'}), 404)
  except e:
    return make_response(jsonify({'message': 'Erro ao atualizar o cliente'}), 500)
  
# Deletar o cliente
@app.route ('/client_version/<int:id>', methods = ['DELETE'])
def delete_client(id):
  try:
    client_version  = ClientEnvVersion.query.filter_by(id=id).first()
    if client_version:
      db.session.delete(client_version)
      db.session.commit()
      return make_response(jsonify({'message': 'Cliente deletado'}), 200)
    return make_response(jsonify({'message': 'Cliente não encontrado'}), 404)
  except e:
    return make_response(jsonify({'message': 'Erro ao excluir o cliente'}), 500)