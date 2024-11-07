from flask import Blueprint, request, jsonify
from app import db
from app.models import Cliente
from app.schemas import ClienteSchema
from flask_jwt_extended import jwt_required

bp = Blueprint('clientes', __name__, url_prefix='/clientes')

@bp.route('/', methods=['POST'])
@jwt_required()
def criar_cliente():
    """
    Rota para criar um novo cliente.
    Recebe dados do cliente e salva no banco de dados.
    """
    data = request.get_json()
    cliente_schema = ClienteSchema()
    cliente = cliente_schema.load(data)
    db.session.add(cliente)
    db.session.commit()
    result = cliente_schema.dump(cliente)
    return jsonify(result), 201

@bp.route('/', methods=['GET'])
@jwt_required()
def listar_clientes():
    """
    Rota para listar todos os clientes.
    """
    clientes = Cliente.query.all()
    cliente_schema = ClienteSchema(many=True)
    result = cliente_schema.dump(clientes)
    return jsonify(result), 200

@bp.route('/<int:cliente_id>', methods=['GET'])
@jwt_required()
def obter_cliente(cliente_id):
    """
    Rota para obter detalhes de um cliente específico.
    """
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return jsonify({"error": "Cliente não encontrado"}), 404

    cliente_schema = ClienteSchema()
    result = cliente_schema.dump(cliente)
    return jsonify(result), 200

@bp.route('/<int:cliente_id>', methods=['PUT'])
@jwt_required()
def atualizar_cliente(cliente_id):
    """
    Rota para atualizar um cliente existente.
    """
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return jsonify({"error": "Cliente não encontrado"}), 404

    data = request.get_json()
    cliente_schema = ClienteSchema()
    cliente = cliente_schema.load(data, instance=cliente, partial=True)
    db.session.commit()
    result = cliente_schema.dump(cliente)
    return jsonify(result), 200

@bp.route('/<int:cliente_id>', methods=['DELETE'])
@jwt_required()
def deletar_cliente(cliente_id):
    """
    Rota para deletar um cliente.
    """
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return jsonify({"error": "Cliente não encontrado"}), 404

    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"message": "Cliente deletado com sucesso"}), 200
