from flask import Blueprint, request, jsonify
from src.models.unidade import Unidade, db

unidades_bp = Blueprint('unidades', __name__)

@unidades_bp.route('/unidades', methods=['GET'])
def listar_unidades():
    try:
        unidades = Unidade.query.filter_by(ativo=True).all()
        return jsonify([unid.to_dict() for unid in unidades])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@unidades_bp.route('/unidades', methods=['POST'])
def criar_unidade():
    try:
        data = request.get_json()
        
        if not data or 'nome' not in data:
            return jsonify({'error': 'Nome é obrigatório'}), 400
        
        # Verificar se já existe
        existe = Unidade.query.filter_by(nome=data['nome']).first()
        if existe:
            return jsonify({'error': 'Unidade já existe'}), 400
        
        unidade = Unidade(nome=data['nome'])
        db.session.add(unidade)
        db.session.commit()
        
        return jsonify(unidade.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@unidades_bp.route('/unidades/<int:id>', methods=['PUT'])
def atualizar_unidade(id):
    try:
        unidade = Unidade.query.get_or_404(id)
        data = request.get_json()
        
        if 'nome' in data:
            # Verificar se já existe outro com o mesmo nome
            existe = Unidade.query.filter(
                Unidade.nome == data['nome'],
                Unidade.id != id
            ).first()
            if existe:
                return jsonify({'error': 'Unidade já existe'}), 400
            
            unidade.nome = data['nome']
        
        if 'ativo' in data:
            unidade.ativo = data['ativo']
        
        db.session.commit()
        return jsonify(unidade.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@unidades_bp.route('/unidades/<int:id>', methods=['DELETE'])
def deletar_unidade(id):
    try:
        unidade = Unidade.query.get_or_404(id)
        
        # Verificar se tem funcionários vinculados
        if unidade.funcionarios:
            return jsonify({'error': 'Não é possível excluir unidade com funcionários vinculados'}), 400
        
        db.session.delete(unidade)
        db.session.commit()
        
        return jsonify({'message': 'Unidade excluída com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

