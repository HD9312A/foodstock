from sqlalchemy import func
from models.model_produto import Produto
from datetime import datetime, timedelta

def relatorio_categorias():

    categorias = (
        Produto.query
        .with_entities(
            Produto.categoria,
            func.count(Produto.id)
        )
        .group_by(Produto.categoria)
        .all()
    )

    resultado = []

    for categoria, quantidade in categorias:
        resultado.append({
            "categoria": categoria,
            "quantidade": quantidade
        })

    return resultado

def relatorio_categorias_detalhado():

    produtos = Produto.query.all()

    resultado = {}

    for produto in produtos:

        categoria = produto.categoria

        if categoria not in resultado:
            resultado[categoria] = []

        resultado[categoria].append({
            "id": produto.id,
            "nome": produto.nome,
            "quantidadeAtual": produto.quantidadeAtual,
            "quantidadeMinima": produto.quantidadeMinima,
            "unidade": produto.unidade,
            "validade": produto.dataValidade.strftime("%Y-%m-%d")
        })

    return resultado

def relatorio_resumo():

    produtos = Produto.query.all()

    total_produtos = len(produtos)

    estoque_baixo = sum(
        1
        for produto in produtos
        if produto.quantidadeAtual <= produto.quantidadeMinima
    )

    vencendo = sum(
        1
        for produto in produtos
        if produto.dataValidade <= datetime.today() + timedelta(days=2)
    )

    return {
        "total_produtos": total_produtos,
        "produtos_estoque_baixo": estoque_baixo,
        "produtos_vencendo": vencendo
    }

def relatorio_estoque_baixo():

    produtos = Produto.query.all()

    resultado = []

    for produto in produtos:

        if produto.quantidadeAtual <= produto.quantidadeMinima:

            resultado.append({
                "id": produto.id,
                "nome": produto.nome,
                "categoria": produto.categoria,
                "quantidadeAtual": produto.quantidadeAtual,
                "quantidadeMinima": produto.quantidadeMinima
            })

    return resultado

def relatorio_validade(dias=3):

    produtos = Produto.query.all()

    resultado = []

    limite = datetime.today() + timedelta(days=dias)

    for produto in produtos:

        if produto.dataValidade <= limite:

            resultado.append({
                "id": produto.id,
                "nome": produto.nome,
                "categoria": produto.categoria,
                "dataValidade": produto.dataValidade.strftime("%Y-%m-%d")
            })

    return resultado

def relatorio_quantidade_produtos():

    produtos = Produto.query.all()

    resultado = []

    for produto in produtos:

        resultado.append({
            "id": produto.id,
            "nome": produto.nome,
            "categoria": produto.categoria,
            "quantidadeAtual": produto.quantidadeAtual,
            "unidade": produto.unidade
        })

    return {
        "total_produtos": len(produtos),
        "produtos": resultado
    }

def relatorio_produtos_vencidos():

    produtos = Produto.query.all()

    resultado = []

    for produto in produtos:

        if produto.dataValidade < datetime.today():

            resultado.append({
                "id": produto.id,
                "nome": produto.nome,
                "categoria": produto.categoria,
                "dataValidade": produto.dataValidade.strftime("%Y-%m-%d")
            })

    return resultado