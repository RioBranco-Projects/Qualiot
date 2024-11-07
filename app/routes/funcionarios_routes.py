from flask import Blueprint, request, jsonify
from app import db
from app.models import Funcionario
from app.schemas import FuncionarioSchema
from flask_jwt_extended import jwt_required

bp = Blueprint('funcionarios', __name__, url_prefix='/funcionarios')

@bp.route('/', methods=['POST'])
@jwt_required()
def criar_funcionario():
    """
    Rota para criar um novo funcionário.
    """
    data = request.get_json()
    funcionario_schema = FuncionarioSchema()
    funcionario = funcionario_schema.load(data)
    db.session.add(funcionario)
    db.session.commit()
    result = funcionario_schema.dump(funcionario)
    return jsonify(result), 201

@bp.route('/', methods=['GET'])
@jwt_required()
def listar_funcionarios():
    """
    Rota para listar todos os funcionários.
    """
    funcionarios = Funcionario.query.all()
    funcionario_schema = FuncionarioSchema(many=True)
    result = funcionario_schema.dump(funcionarios)
    return jsonify(result), 200

@bp.route('/<int:funcionario_id>', methods=['GET'])
@jwt_required()
def obter_funcionario(funcionario_id):
    """
    Rota para obter detalhes de um funcionário específico.
    """
    funcionario = Funcionario.query.get(funcionario_id)
    if not funcionario:
        return jsonify({"error": "Funcionário não encontrado"}), 404

    funcionario_schema = FuncionarioSchema()
    result = funcionario_schema.dump(funcionario)
    return jsonify(result), 200

@bp.route('/<int:funcionario_id>', methods=['PUT'])
@jwt_required()
def atualizar_funcionario(funcionario_id):
    """
    Rota para atualizar um funcionário existente.
    """
    funcionario = Funcionario.query.get(funcionario_id)
    if not funcionario:
        return jsonify({"error": "Funcionário não encontrado"}), 404

    data = request.get_json()
    funcionario_schema = FuncionarioSchema()
    funcionario = funcionario_schema.load(data, instance=funcionario, partial=True)
    db.session.commit()
    result = funcionario_schema.dump(funcionario)
    return jsonify(result), 200

@bp.route('/<int:funcionario_id>', methods=['DELETE'])
@jwt_required()
def deletar_funcionario(funcionario_id):
    """
    Rota para deletar um funcionário.
    """
    funcionario = Funcionario.query.get(funcionario_id)
    if not funcionario:
        return jsonify({"error": "Funcionário não encontrado"}), 404

    db.session.delete(funcionario)
    db.session.commit()
    return jsonify({"message": "Funcionário deletado com sucesso"}), 200
