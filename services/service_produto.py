from models.model_produto import Produto
from datetime import date, datetime, timedelta
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

    if data["quantidade"] < 0 or data["quantidadeMinima"] < 0:
        raise ValueError("As quantidades não podem ser negativas.")
    
    try:

        validade = datetime.strptime(
            data["dataValidade"],
            "%Y-%m-%d"
        )

    except ValueError:

        raise ValueError(
            "Formato de data inválido. Use YYYY-MM-DD"
        )

    novo = Produto(
        id=len(Produto.query.all()) + 1,
        nome=data["nome"],
        categoria=data["categoria"],
        quantidade=data["quantidade"],
        unidade=data["unidade"],
        quantidadeMinima=data["quantidadeMinima"],
        dataValidade=datetime.strptime(data["dataValidade"], "%Y-%m-%d").date()
    )
    db.session.add(novo)
    db.session.commit()
    db.session.add(novo)
    db.session.commit()

    return novo.to_dict()


def buscar_produto(id):
    produto = Produto.query.get(id)
    if not produto:
        raise ValueError("Produto não encontrado.")
    return produto.to_dict()


def atualizar_produto(id, data):
    produto = Produto.query.get(id)
    if not produto:
        raise ValueError("Produto não encontrado.")
    if "nome" in data:
        produto.nome = data["nome"]

    if "categoria" in data:
        produto.categoria = data["categoria"]

    if "quantidadeAtual" in data:

        if data["quantidadeAtual"] < 0:
            raise ValueError("Quantidade atual não pode ser negativa.")

        produto.quantidadeAtual = data["quantidadeAtual"]

    if "quantidadeMinima" in data:

        if data["quantidadeMinima"] < 0:
            raise ValueError("Quantidade mínima não pode ser negativa.")

        produto.quantidadeMinima = data["quantidadeMinima"]

    if "unidade" in data:
        produto.unidade = Unidade(data["unidade"])

    if "dataValidade" in data:
        try:
            produto.dataValidade = datetime.strptime(data["dataValidade"], "%Y-%m-%d").date()
        except ValueError:
            raise ValueError ("Data inválida. Utilize o formato YYYY-MM-DD.")

    db.session.commit()

    return produto.to_dict()


def dar_entrada(id, quantidade):
    produto = Produto.query.get(id)
    if not produto:
        raise ValueError("Produto não encontrado.")
    if quantidade <= 0:
        raise ValueError("Quantidade deve ser maior que zero.")
    
    produto.quantidade += quantidade
    db.session.commit()
    return produto.to_dict()


def dar_saida(id, quantidade):
        produto = Produto.query.get(id)
        if not produto:
            raise ValueError("Produto não encontrado.")
        if produto.quantidade <= 0:
            raise ValueError("Quantidade não pode ser negativa ou igual a zero.")
        if quantidade > produto.quantidade:
            raise ValueError("Quantidade insuficiente em estoque.")
        
        produto.quantidade -= quantidade
        db.session.commit()
        return produto.to_dict()

def deletar_produto(id):
    produto = Produto.query.get(id)
    if not produto:
        raise ValueError("Produto não encontrado.")

    db.session.delete(produto)
    db.session.commit()
    return {
        "mensagem": "Produto removido com sucesso."}

def alertaEstoqueBaixo():
    produtos = Produto.query.filter(Produto.quantidade <= Produto.quantidadeMinima).all()
    return [produto.to_dict() for produto in produtos]


def alertaValidade(dias=2):
    produtos_vencendo = []
    hoje = date.today()


    for produto in Produto.query.all():
        validade = produto.dataValidade
        if validade - hoje <= timedelta(days=dias):
            produtos_vencendo.append(produto.to_dict())
    return produtos_vencendo