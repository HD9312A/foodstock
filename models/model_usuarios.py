from database.db import db


class Usuario(db.Model):

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    perfil = db.Column(db.String(100), nullable=False)

    def __init__(self, id, nome, login, senha, perfil):
        self.id = id
        self.nome = nome
        self.login = login 
        self.senha = senha 
        self.perfil = perfil 

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "login": self.login,
            "senha": self.senha,
            "perfil": self.perfil

        }