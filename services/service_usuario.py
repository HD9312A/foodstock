from models.model_usuarios import Usuario
from database.db import db
import re

def listar_usuarios():

    usuarios = Usuario.query.all()

    return [
        usuario.to_dict()
        for usuario in usuarios
    ]


def criar_usuario(data):

    campos_obrigatorios = ['nome', 'email', 'senha']
    for campo in campos_obrigatorios:
        if campo not in data:
            raise Exception(f"Campo '{campo}' é obrigatório.")

    if "nome" in data:
        if not re.match(r"^[a-zA-Z\s]+$", data["nome"]):
            raise Exception("Nome deve conter apenas letras e espaços.")    
    if "email" in data:
        if not re.fullmatch(r"^[a-zA-Z]+([._]?[a-zA-Z]+)*@[a-zA-Z]+\.[a-zA-Z]{2,}$", data["email"]):
            raise Exception("E-mail inválido.")
    if "senha" in data:
        if len(data["senha"]) < 8:
            raise Exception("Senha deve conter pelo menos 8 caracteres.")
        if not re.search(r"[A-Z]", data["senha"]):
            raise Exception("Senha deve conter pelo menos uma letra maiúscula.")
        if not re.search(r"[a-z]", data["senha"]):
            raise Exception("Senha deve conter pelo menos uma letra minúscula.")
        if not re.search(r"\d", data["senha"]):
            raise Exception("Senha deve conter pelo menos um número.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", data["senha"]):
            raise Exception("Senha deve conter pelo menos um caractere especial.")
    
        
    perfis_validos = [
        "cozinha",
        "estoquista",
        "gerente"
    ]
        
    if data["perfil"].lower() not in perfis_validos:
        raise Exception(f"Perfil '{data['perfil']}' é inválido. Perfis válidos: {perfis_validos}.")
    
    login_existente = Usuario.query.filter_by(login=data['login']).first()
    if login_existente:
        raise Exception("Login já cadastrado. Escolha outro login.")
    
    usuario = Usuario(
        nome=data['nome'],
        email=data['email'],
        senha=data['senha'],
        perfil=data['perfil']
    )

    db.session.add(usuario)
    db.session.commit()

    return usuario.to_dict()


def buscar_usuario(id):

    usuario = Usuario.query.get(id)

    if not usuario:
        raise Exception("Usuário não encontrado.")
    return usuario.to_dict()


def atualizar_usuario(id, data):
    usuario = Usuario.query.get(id)

    if not usuario:
        raise Exception("Usuário não encontrado.")

    if "perfil" in data:
        perfis_validos = [
            "cozinha",
            "estoquista",
            "gerente"
        ]
        
        if data["perfil"].lower() not in perfis_validos:
            raise Exception(f"Perfil '{data['perfil']}' é inválido. Perfis válidos: {perfis_validos}.")
        
    usuario.nome = data.get('nome', usuario.nome)
    usuario.email = data.get('email', usuario.email)
    usuario.senha = data.get('senha', usuario.senha)
    usuario.perfil = data.get('perfil', usuario.perfil)

    db.session.commit()

    return usuario.to_dict()


def excluir_usuario(id):
    usuario = Usuario.query.get(id)

    if not usuario:
        raise Exception("Usuário não encontrado.")

    db.session.delete(usuario)
    db.session.commit()

    return {"message": "Usuário excluído com sucesso."}