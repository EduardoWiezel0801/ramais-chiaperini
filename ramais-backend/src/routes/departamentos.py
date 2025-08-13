from flask import Blueprint, request, jsonify
from src.models.departamento import Departamento, db

departamentos_bp = Blueprint('departamentos', __name__)

@departamentos_bp.route('/departamentos', methods=['GET'])
def listar_departamentos():
    try:
        departamentos = Departamento.query.filter_by(ativo=True).all()
        return jsonify([dept.to_dict() for dept in departamentos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@departamentos_bp.route('/departamentos', methods=['POST'])
def criar_departamento():
    try:
        data = request.get_json()
        
        if not data or 'nome' not in data:
            return jsonify({'error': 'Nome é obrigatório'}), 400
        
        # Verificar se já existe
        existe = Departamento.query.filter_by(nome=data['nome']).first()
        if existe:
            return jsonify({'error': 'Departamento já existe'}), 400
        
        departamento = Departamento(nome=data['nome'])
        db.session.add(departamento)
        db.session.commit()
        
        return jsonify(departamento.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@departamentos_bp.route('/departamentos/<int:id>', methods=['PUT'])
def atualizar_departamento(id):
    try:
        departamento = Departamento.query.get_or_404(id)
        data = request.get_json()
        
        if 'nome' in data:
            # Verificar se já existe outro com o mesmo nome
            existe = Departamento.query.filter(
                Departamento.nome == data['nome'],
                Departamento.id != id
            ).first()
            if existe:
                return jsonify({'error': 'Departamento já existe'}), 400
            
            departamento.nome = data['nome']
        
        if 'ativo' in data:
            departamento.ativo = data['ativo']
        
        db.session.commit()
        return jsonify(departamento.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@departamentos_bp.route('/departamentos/<int:id>', methods=['DELETE'])
def deletar_departamento(id):
    try:
        departamento = Departamento.query.get_or_404(id)
        
        # Verificar se tem funcionários vinculados
        if departamento.funcionarios:
            return jsonify({'error': 'Não é possível excluir departamento com funcionários vinculados'}), 400
        
        db.session.delete(departamento)
        db.session.commit()
        
        return jsonify({'message': 'Departamento excluído com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

