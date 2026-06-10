from flask import (
    Blueprint,
    jsonify,
    request
)

from services.service_usuario import (
    listar_usuarios,
    criar_usuario,
    buscar_usuario,
    atualizar_usuario,
    excluir_usuario
)

usuarios_bp = Blueprint(
    "usuarios",
    __name__
)

@usuarios_bp.route("/usuarios", methods=["GET"])
def listar():
    usuarios = listar_usuarios()
    return jsonify(usuarios)

@usuarios_bp.route("/usuarios", methods=["POST"])
def criar():
    dados = request.get_json()
    usuario = criar_usuario(dados)
    return jsonify(usuario), 201

@usuarios_bp.route("/usuarios/<int:id>", methods=["GET"])
def buscar(id):
    usuario = buscar_usuario(id)
    return jsonify(usuario)

@usuarios_bp.route("/usuarios/<int:id>", methods=["PUT"])
def atualizar(id):
    dados = request.get_json()
    usuario = atualizar_usuario(id, dados)
    return jsonify(usuario)

@usuarios_bp.route("/usuarios/<int:id>", methods=["DELETE"])
def excluir(id):
    resultado = excluir_usuario(id)
    return jsonify(resultado)