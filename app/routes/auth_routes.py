from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models import Usuario
from app.schemas import UsuarioSchema
from flask_jwt_extended import create_access_token

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    """
    Rota para registrar um novo usuário.
    Recebe login e senha, verifica se o usuário já existe,
    criptografa a senha e salva o novo usuário no banco de dados.
    """
    data = request.get_json()
    login = data.get('login')
    senha = data.get('senha')

    # Verificar se o usuário já existe
    if Usuario.query.filter_by(login=login).first():
        return jsonify({"error": "Usuário já existe"}), 400

    # Criptografar a senha
    senha_hash = bcrypt.generate_password_hash(senha).decode('utf-8')

    # Criar novo usuário
    novo_usuario = Usuario(login=login, senha=senha_hash)
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({"message": "Usuário registrado com sucesso"}), 201

@bp.route('/login', methods=['POST'])
def login():
    """
    Rota para autenticar um usuário.
    Recebe login e senha, verifica as credenciais e retorna um token de acesso JWT.
    """
    data = request.get_json()
    login = data.get('login')
    senha = data.get('senha')

    # Verificar se o usuário existe
    usuario = Usuario.query.filter_by(login=login).first()
    if not usuario or not bcrypt.check_password_hash(usuario.senha, senha):
        return jsonify({"error": "Credenciais inválidas"}), 401

    # Gerar token de acesso
    access_token = create_access_token(identity=usuario.id)
    return jsonify({"access_token": access_token}), 200
