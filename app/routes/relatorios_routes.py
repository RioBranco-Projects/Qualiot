from flask import Blueprint, request, jsonify, Response
from app import db
from app.models import Venda, Despesa, ItemVenda
from flask_jwt_extended import jwt_required
from sqlalchemy import func
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import base64
from io import BytesIO

bp = Blueprint('relatorios', __name__, url_prefix='/relatorios')

@bp.route('/faturamento', methods=['GET'])
@jwt_required()
def calcular_faturamento():
    """
    Rota para calcular o faturamento total.
    Soma o valor total de todas as vendas.
    """
    faturamento = db.session.query(
        func.sum(ItemVenda.quantidade * ItemVenda.valor_unitario)
    ).scalar() or 0
    return jsonify({"faturamento_total": faturamento}), 200

@bp.route('/lucro', methods=['GET'])
@jwt_required()
def calcular_lucro():
    """
    Rota para calcular o lucro total.
    Calcula o faturamento menos as despesas.
    """
    faturamento = db.session.query(
        func.sum(ItemVenda.quantidade * ItemVenda.valor_unitario)
    ).scalar() or 0
    despesas_total = db.session.query(
        func.sum(Despesa.valor)
    ).scalar() or 0
    lucro = faturamento - despesas_total
    return jsonify({"lucro_total": lucro}), 200

@bp.route('/ganho_por_colheita', methods=['GET'])
@jwt_required()
def calcular_ganho_por_colheita():
    """
    Rota para calcular o ganho por colheita.
    Filtra as vendas por período específico.
    """
    data_inicial = request.args.get('data_inicial')  # Formato AAAAMMDD
    data_final = request.args.get('data_final')      # Formato AAAAMMDD

    query = db.session.query(
        func.sum(ItemVenda.quantidade * ItemVenda.valor_unitario)
    ).join(Venda)

    if data_inicial and data_final:
        query = query.filter(Venda.data_venda.between(data_inicial, data_final))

    ganho = query.scalar() or 0
    return jsonify({"ganho_por_colheita": ganho}), 200

@bp.route('/gasto_por_colheita', methods=['GET'])
@jwt_required()
def calcular_gasto_por_colheita():
    """
    Rota para calcular o gasto por colheita.
    Filtra as despesas por período específico e categoria.
    """
    data_inicial = request.args.get('data_inicial')  # Formato AAAAMMDD
    data_final = request.args.get('data_final')      # Formato AAAAMMDD
    categoria = request.args.get('categoria')

    query = db.session.query(
        func.sum(Despesa.valor)
    )

    if data_inicial and data_final:
        query = query.filter(Despesa.data_despesa.between(data_inicial, data_final))

    if categoria:
        query = query.filter(Despesa.categoria == categoria)

    gasto = query.scalar() or 0
    return jsonify({"gasto_por_colheita": gasto}), 200

@bp.route('/exportar_vendas_csv', methods=['GET'])
@jwt_required()
def exportar_vendas_csv():
    """
    Rota para exportar as vendas em formato CSV.
    """
    vendas = Venda.query.all()
    data = []
    for venda in vendas:
        for item in venda.itens:
            data.append({
                'Venda ID': venda.id,
                'Data Venda': venda.data_venda,
                'Cliente ID': venda.cliente_id,
                'Produto ID': item.produto_id,
                'Quantidade': item.quantidade,
                'Valor Unitário': item.valor_unitario,
                'Valor Total': item.quantidade * item.valor_unitario
            })
    df = pd.DataFrame(data)
    csv_data = df.to_csv(index=False)
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=vendas.csv"}
    )

@bp.route('/grafico_faturamento', methods=['GET'])
@jwt_required()
def grafico_faturamento():
    """
    Rota para gerar um gráfico de faturamento por período.
    Retorna uma imagem em base64.
    """
    # Obter dados
    vendas = db.session.query(Venda.data_venda, func.sum(ItemVenda.quantidade * ItemVenda.valor_unitario).label('faturamento')).join(ItemVenda).group_by(Venda.data_venda).all()

    # Preparar dados para o gráfico
    datas = [str(venda.data_venda) for venda in vendas]
    faturamentos = [venda.faturamento for venda in vendas]

    # Gerar gráfico
    plt.figure(figsize=(10,5))
    plt.plot(datas, faturamentos, marker='o')
    plt.title('Faturamento por Data')
    plt.xlabel('Data')
    plt.ylabel('Faturamento')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Converter gráfico para base64
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()

    return jsonify({"grafico": img_base64}), 200
