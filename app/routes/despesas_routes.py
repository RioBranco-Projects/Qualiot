from flask import Blueprint, request, jsonify
from app import db
from app.models import Despesa
from app.schemas import DespesaSchema
from flask_jwt_extended import jwt_required

bp = Blueprint('despesas', __name__, url_prefix='/despesas')

@bp.route('/', methods=['POST'])
@jwt_required()
def criar_despesa():
    """
    Rota para criar uma nova despesa.
    Recebe dados da despesa e salva no banco de dados.
    """
    data = request.get_json()
    despesa_schema = DespesaSchema()
    despesa = despesa_schema.load(data)
    db.session.add(despesa)
    db.session.commit()
    result = despesa_schema.dump(despesa)
    return jsonify(result), 201

@bp.route('/', methods=['GET'])
@jwt_required()
def listar_despesas():
    """
    Rota para listar todas as despesas.
    Retorna uma lista de despesas registradas.
    """
    despesas = Despesa.query.all()
    despesa_schema = DespesaSchema(many=True)
    result = despesa_schema.dump(despesas)
    return jsonify(result), 200

@bp.route('/<int:despesa_id>', methods=['GET'])
@jwt_required()
def obter_despesa(despesa_id):
    """
    Rota para obter detalhes de uma despesa específica.
    """
    despesa = Despesa.query.get(despesa_id)
    if not despesa:
        return jsonify({"error": "Despesa não encontrada"}), 404

    despesa_schema = DespesaSchema()
    result = despesa_schema.dump(despesa)
    return jsonify(result), 200

@bp.route('/<int:despesa_id>', methods=['PUT'])
@jwt_required()
def atualizar_despesa(despesa_id):
    """
    Rota para atualizar uma despesa existente.
    """
    despesa = Despesa.query.get(despesa_id)
    if not despesa:
        return jsonify({"error": "Despesa não encontrada"}), 404

    data = request.get_json()
    despesa_schema = DespesaSchema()
    despesa = despesa_schema.load(data, instance=despesa, partial=True)
    db.session.commit()
    result = despesa_schema.dump(despesa)
    return jsonify(result), 200

@bp.route('/<int:despesa_id>', methods=['DELETE'])
@jwt_required()
def deletar_despesa(despesa_id):
    """
    Rota para deletar uma despesa.
    """
    despesa = Despesa.query.get(despesa_id)
    if not despesa:
        return jsonify({"error": "Despesa não encontrada"}), 404

    db.session.delete(despesa)
    db.session.commit()
    return jsonify({"message": "Despesa deletada com sucesso"}), 200
