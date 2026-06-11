from datetime import datetime
from enums.unidade import Unidade
from database.db import db



class Produto(db.Model):
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    unidade = db.Column(db.Enum(Unidade), nullable=False)
    quantidadeMinima = db.Column(db.Integer, nullable=False)
    dataValidade = db.Column(db.Date, nullable=False)

    def __init__(self, id, nome, categoria, quantidade, unidade, quantidadeMinima, dataValidade):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.quantidade = quantidade
        self.unidade = Unidade(unidade)
        self.quantidadeMinima = quantidadeMinima
        self.dataValidade = dataValidade

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "categoria": self.categoria,
            "quantidade": self.quantidade,
            "unidade": self.unidade.value,
            "quantidadeMinima": self.quantidadeMinima,
            "dataValidade": self.dataValidade.strftime("%Y-%m-%d") # formato: "YYYY-MM-DD"

        }