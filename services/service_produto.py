from database.db import estoque
from models.model_produto import Produto
from datetime import datetime, timedelta
from enums.unidade import Unidade
from database.db import db


def listar_produtos():
    produtos = Produto.query.all()

    return [
        produto.to_dict()
        for produto in produtos
    ]

def criar_produto(data):
    try:
        unidade = Unidade(data["unidade"])
    except ValueError:
        raise ValueError(f"Unidade '{data['unidade']}' inválida. Use uma das seguintes: {[u.value for u in Unidade]}")

    novo = Produto(
        id=len(estoque) + 1,
        nome=data["nome"],
        categoria=data["categoria"],
        quantidade=data["quantidade"],
        unidade=data["unidade"],
        quantidadeAtual=data["quantidadeAtual"],
        quantidadeMinima=data["quantidadeMinima"],
        dataValidade=data["dataValidade"]
    )
    db.session.add(novo)
    db.session.commit()
    db.session.add(novo)
    db.session.commit()

def dar_saida(id, quantidade):
        produto = Produto.query.get(id)
        produto.quantidade -= quantidade
        db.session.commit()



def alertaEstoqueBaixo():
    produtos = Produto.query.filter(Produto.quantidadeAtual <= Produto.quantidadeMinima).all()
    return produtos

def alertaValidade(dias=2):
    produtos_vencendo = []
    hoje = datetime.today()


    for produto in estoque:
        validade = datetime.strptime(produto.dataValidade, "%Y-%m-%d")
        if validade - hoje <= timedelta(days=dias):
            produtos_vencendo.append(produto.to_dict())
    return produtos_vencendo