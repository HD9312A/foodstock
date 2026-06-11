from flask import Blueprint, request, jsonify
from services.service_produto import criar_produto, dar_saida, dar_entrada, listar_produtos, alertaValidade, alertaEstoqueBaixo, buscar_produto, deletar_produto, atualizar_produto

produtos_bp = Blueprint('produtos', __name__)

@produtos_bp.route('/produtos', methods=['GET'])
def listar():
    produtos = listar_produtos()
    return jsonify(produtos)

@produtos_bp.route('/produtos', methods=['POST'])
def criar():
    data = request.json
    try:
        produto = criar_produto(data)
        return jsonify(produto), 201
    except Exception as erro:
        return {"erro": str(erro)}, 400 #400 (Bad Request) = o servidor não pode processar a solicitação devido a algo que é percebido como um erro do cliente (ex: dados inválidos)
    
@produtos_bp.route('/produtos/<int:id>', methods=['GET'])
def buscar(id):
    try:
        produto = buscar_produto(id)
        return jsonify(produto)
    except ValueError as erro:
        return jsonify({
            "erro": str(erro)}), 404
    
@produtos_bp.route('/produtos/<int:id>', methods=["PUT"])
def atualizar(id):
    try:
        produto = atualizar_produto(id, request.json)
        return jsonify(produto)
    except ValueError as erro:
        return jsonify({
            "erro": str(erro)}), 400

@produtos_bp.route('/produtos/<int:id>/entrada', methods=['POST'])
def entrada(id):
    try:
        data = request.json
        produto = dar_entrada(id, data["quantidade"])
        return jsonify(produto)
    except ValueError as erro:
        return jsonify({
            "erro": str(erro)}), 404

 
@produtos_bp.route('/produtos/<int:id>/saida', methods=['POST'])
def saida(id):
    data = request.json
    produto = dar_saida(id, data["quantidade"])

    if produto:
        return jsonify(produto)
    return {"erro": "Produto não encontrado"}, 404 #404 (Not Found) = o servidor não pode encontrar o recurso solicitado

@produtos_bp.route(
    "/produto/<int:id>", methods=["DELETE"])
def deletar(id):
    try:
        resultado = deletar_produto(id)
        return jsonify(resultado)
    except ValueError as erro:
        return jsonify({
            "erro": str(erro)}), 404

@produtos_bp.route('/produtos/alerta/estoque-baixo', methods=['GET'])
def get_alerta_estoque_baixo():
    return jsonify(alertaEstoqueBaixo())

@produtos_bp.route('/produtos/alerta/validade', methods=['GET'])
def get_alerta_validade():
    dias = request.args.get('dias', default=2, type=int)
    return jsonify(alertaValidade(dias))

