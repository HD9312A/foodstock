from flask import Blueprint, request, jsonify
from services.service_relatorio import relatorio_categorias, relatorio_categorias_detalhado, relatorio_resumo, relatorio_estoque_baixo, relatorio_validade, relatorio_quantidade_produtos, relatorio_produtos_vencidos

relatorios_bp = Blueprint('relatorios', __name__)

@relatorios_bp.route('/relatorios/categorias', methods=['GET'])
def get_relatorio_categorias():
    return jsonify(relatorio_categorias())

@relatorios_bp.route('/relatorios/categorias/detalhado', methods=['GET'])
def get_relatorio_categorias_detalhado():
    return jsonify(relatorio_categorias_detalhado())

@relatorios_bp.route('/relatorios/resumo', methods=['GET'])
def get_relatorio_resumo():
    return jsonify(relatorio_resumo())

@relatorios_bp.route('/relatorios/estoque-baixo', methods=['GET'])
def get_relatorio_estoque_baixo():  
    return jsonify(relatorio_estoque_baixo())

@relatorios_bp.route('/relatorios/validade', methods=['GET'])
def get_relatorio_validade():
    return jsonify(relatorio_validade())

@relatorios_bp.route('/relatorios/quantidade-produtos', methods=['GET'])
def get_relatorio_quantidade_produtos():
    return jsonify(relatorio_quantidade_produtos())

@relatorios_bp.route('/relatorios/produtos-vencidos', methods=['GET'])
def get_relatorio_produtos_vencidos():
    return jsonify(relatorio_produtos_vencidos())