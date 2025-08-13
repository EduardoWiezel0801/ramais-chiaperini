from flask import Blueprint, request, jsonify
from src.models.funcao import Funcao, db

funcoes_bp = Blueprint('funcoes', __name__)

@funcoes_bp.route('/funcoes', methods=['GET'])
def listar_funcoes():
    try:
        funcoes = Funcao.query.filter_by(ativo=True).all()
        return jsonify([func.to_dict() for func in funcoes])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@funcoes_bp.route('/funcoes', methods=['POST'])
def criar_funcao():
    try:
        data = request.get_json()
        
        if not data or 'nome' not in data:
            return jsonify({'error': 'Nome é obrigatório'}), 400
        
        # Verificar se já existe
        existe = Funcao.query.filter_by(nome=data['nome']).first()
        if existe:
            return jsonify({'error': 'Função já existe'}), 400
        
        funcao = Funcao(nome=data['nome'])
        db.session.add(funcao)
        db.session.commit()
        
        return jsonify(funcao.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@funcoes_bp.route('/funcoes/<int:id>', methods=['PUT'])
def atualizar_funcao(id):
    try:
        funcao = Funcao.query.get_or_404(id)
        data = request.get_json()
        
        if 'nome' in data:
            # Verificar se já existe outro com o mesmo nome
            existe = Funcao.query.filter(
                Funcao.nome == data['nome'],
                Funcao.id != id
            ).first()
            if existe:
                return jsonify({'error': 'Função já existe'}), 400
            
            funcao.nome = data['nome']
        
        if 'ativo' in data:
            funcao.ativo = data['ativo']
        
        db.session.commit()
        return jsonify(funcao.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@funcoes_bp.route('/funcoes/<int:id>', methods=['DELETE'])
def deletar_funcao(id):
    try:
        funcao = Funcao.query.get_or_404(id)
        
        # Verificar se tem funcionários vinculados
        if funcao.funcionarios:
            return jsonify({'error': 'Não é possível excluir função com funcionários vinculados'}), 400
        
        db.session.delete(funcao)
        db.session.commit()
        
        return jsonify({'message': 'Função excluída com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

