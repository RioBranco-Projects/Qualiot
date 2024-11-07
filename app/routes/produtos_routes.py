from flask import Blueprint, request, jsonify
from app import db
from app.models import Produto
from app.schemas import ProdutoSchema
from flask_jwt_extended import jwt_required

bp = Blueprint('produtos', __name__, url_prefix='/produtos')

@bp.route('/', methods=['POST'])
@jwt_required()
def criar_produto():
    """
    Rota para criar um novo produto.
    Recebe dados do produto e salva no banco de dados.
    """
    data = request.get_json()
    produto_schema = ProdutoSchema()
    produto = produto_schema.load(data)
    db.session.add(produto)
    db.session.commit()
    result = produto_schema.dump(produto)
    return jsonify(result), 201

@bp.route('/', methods=['GET'])
@jwt_required()
def listar_produtos():
    """
    Rota para listar todos os produtos.
    """
    produtos = Produto.query.all()
    produto_schema = ProdutoSchema(many=True)
    result = produto_schema.dump(produtos)
    return jsonify(result), 200

@bp.route('/<int:produto_id>', methods=['GET'])
@jwt_required()
def obter_produto(produto_id):
    """
    Rota para obter detalhes de um produto específico.
    """
    produto = Produto.query.get(produto_id)
    if not produto:
        return jsonify({"error": "Produto não encontrado"}), 404

    produto_schema = ProdutoSchema()
    result = produto_schema.dump(produto)
    return jsonify(result), 200

@bp.route('/<int:produto_id>', methods=['PUT'])
@jwt_required()
def atualizar_produto(produto_id):
    """
    Rota para atualizar um produto existente.
    """
    produto = Produto.query.get(produto_id)
    if not produto:
        return jsonify({"error": "Produto não encontrado"}), 404

    data = request.get_json()
    produto_schema = ProdutoSchema()
    produto = produto_schema.load(data, instance=produto, partial=True)
    db.session.commit()
    result = produto_schema.dump(produto)
    return jsonify(result), 200

@bp.route('/<int:produto_id>', methods=['DELETE'])
@jwt_required()
def deletar_produto(produto_id):
    """
    Rota para deletar um produto.
    """
    produto = Produto.query.get(produto_id)
    if not produto:
        return jsonify({"error": "Produto não encontrado"}), 404

    db.session.delete(produto)
    db.session.commit()
    return jsonify({"message": "Produto deletado com sucesso"}), 200
