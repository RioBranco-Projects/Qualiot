from flask import Blueprint, request, jsonify
from app import db
from app.models import Venda, ItemVenda, Produto
from app.schemas import VendaSchema, ItemVendaSchema
from flask_jwt_extended import jwt_required

bp = Blueprint('vendas', __name__, url_prefix='/vendas')

@bp.route('/', methods=['POST'])
@jwt_required()
def criar_venda():
    """
    Rota para criar uma nova venda.
    Recebe dados do cliente, data da venda e itens.
    Salva a venda e os itens associados no banco de dados.
    """
    data = request.get_json()
    cliente_id = data.get('cliente_id')
    data_venda = data.get('data_venda')
    endereco_envio_id = data.get('endereco_envio_id')
    frete = data.get('frete', 0)
    itens_data = data.get('itens')

    # Criar nova venda
    nova_venda = Venda(
        cliente_id=cliente_id,
        data_venda=data_venda,
        endereco_envio_id=endereco_envio_id,
        frete=frete
    )
    db.session.add(nova_venda)
    db.session.flush()  # Para obter o ID da venda

    # Adicionar itens à venda
    for item in itens_data:
        produto_id = item.get('produto_id')
        quantidade = item.get('quantidade')
        valor_unitario = item.get('valor_unitario')

        # Atualizar quantidade em estoque do produto
        produto = Produto.query.get(produto_id)
        if produto:
            if produto.quantidade_estoque >= quantidade:
                produto.quantidade_estoque -= quantidade
            else:
                return jsonify({"error": f"Estoque insuficiente para o produto ID {produto_id}"}), 400
        else:
            return jsonify({"error": f"Produto ID {produto_id} não encontrado"}), 404

        novo_item = ItemVenda(
            venda_id=nova_venda.id,
            produto_id=produto_id,
            quantidade=quantidade,
            valor_unitario=valor_unitario
        )
        db.session.add(novo_item)

    db.session.commit()
    venda_schema = VendaSchema()
    result = venda_schema.dump(nova_venda)
    return jsonify(result), 201

@bp.route('/', methods=['GET'])
@jwt_required()
def listar_vendas():
    """
    Rota para listar todas as vendas.
    Retorna uma lista de vendas com detalhes dos itens.
    """
    vendas = Venda.query.all()
    venda_schema = VendaSchema(many=True)
    result = venda_schema.dump(vendas)
    return jsonify(result), 200

@bp.route('/<int:venda_id>', methods=['GET'])
@jwt_required()
def obter_venda(venda_id):
    """
    Rota para obter detalhes de uma venda específica.
    Retorna as informações da venda e seus itens.
    """
    venda = Venda.query.get(venda_id)
    if not venda:
        return jsonify({"error": "Venda não encontrada"}), 404

    venda_schema = VendaSchema()
    result = venda_schema.dump(venda)
    return jsonify(result), 200

@bp.route('/<int:venda_id>', methods=['PUT'])
@jwt_required()
def atualizar_venda(venda_id):
    """
    Rota para atualizar uma venda existente.
    Permite atualizar dados da venda e dos itens.
    """
    venda = Venda.query.get(venda_id)
    if not venda:
        return jsonify({"error": "Venda não encontrada"}), 404

    data = request.get_json()
    venda.cliente_id = data.get('cliente_id', venda.cliente_id)
    venda.data_venda = data.get('data_venda', venda.data_venda)
    venda.endereco_envio_id = data.get('endereco_envio_id', venda.endereco_envio_id)
    venda.frete = data.get('frete', venda.frete)

    # Atualizar itens da venda
    if 'itens' in data:
        # Remover itens antigos e restituir estoque
        for item in venda.itens:
            produto = Produto.query.get(item.produto_id)
            if produto:
                produto.quantidade_estoque += item.quantidade
            db.session.delete(item)

        # Adicionar novos itens e atualizar estoque
        for item_data in data['itens']:
            produto_id = item_data.get('produto_id')
            quantidade = item_data.get('quantidade')
            valor_unitario = item_data.get('valor_unitario')

            produto = Produto.query.get(produto_id)
            if produto:
                if produto.quantidade_estoque >= quantidade:
                    produto.quantidade_estoque -= quantidade
                else:
                    return jsonify({"error": f"Estoque insuficiente para o produto ID {produto_id}"}), 400
            else:
                return jsonify({"error": f"Produto ID {produto_id} não encontrado"}), 404

            novo_item = ItemVenda(
                venda_id=venda.id,
                produto_id=produto_id,
                quantidade=quantidade,
                valor_unitario=valor_unitario
            )
            db.session.add(novo_item)

    db.session.commit()
    venda_schema = VendaSchema()
    result = venda_schema.dump(venda)
    return jsonify(result), 200

@bp.route('/<int:venda_id>', methods=['DELETE'])
@jwt_required()
def deletar_venda(venda_id):
    """
    Rota para deletar uma venda.
    Remove a venda e os itens associados do banco de dados.
    """
    venda = Venda.query.get(venda_id)
    if not venda:
        return jsonify({"error": "Venda não encontrada"}), 404

    # Restituir estoque dos produtos
    for item in venda.itens:
        produto = Produto.query.get(item.produto_id)
        if produto:
            produto.quantidade_estoque += item.quantidade

    db.session.delete(venda)
    db.session.commit()
    return jsonify({"message": "Venda deletada com sucesso"}), 200
