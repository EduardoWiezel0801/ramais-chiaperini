from flask import Blueprint, request, jsonify
from src.models.funcionario import Funcionario, db
from sqlalchemy import or_

funcionarios_bp = Blueprint('funcionarios', __name__)

@funcionarios_bp.route('/funcionarios', methods=['GET'])
def listar_funcionarios():
    try:
        # Parâmetros de busca e filtro
        busca = request.args.get('busca', '')
        departamento_id = request.args.get('departamento_id')
        funcao_id = request.args.get('funcao_id')
        unidade_id = request.args.get('unidade_id')
        
        query = Funcionario.query.filter_by(ativo=True)
        
        # Aplicar busca por nome, ramal ou email
        if busca:
            query = query.filter(
                or_(
                    Funcionario.nome.ilike(f'%{busca}%'),
                    Funcionario.ramal.ilike(f'%{busca}%'),
                    Funcionario.email.ilike(f'%{busca}%')
                )
            )
        
        # Aplicar filtros
        if departamento_id:
            query = query.filter_by(departamento_id=departamento_id)
        if funcao_id:
            query = query.filter_by(funcao_id=funcao_id)
        if unidade_id:
            query = query.filter_by(unidade_id=unidade_id)
        
        funcionarios = query.all()
        return jsonify([func.to_dict() for func in funcionarios])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@funcionarios_bp.route('/funcionarios', methods=['POST'])
def criar_funcionario():
    try:
        data = request.get_json()
        
        if not data or 'nome' not in data:
            return jsonify({'error': 'Nome é obrigatório'}), 400
        
        funcionario = Funcionario(
            nome=data['nome'],
            ramal=data.get('ramal'),
            email=data.get('email'),
            whatsapp=data.get('whatsapp'),
            departamento_id=data.get('departamento_id'),
            funcao_id=data.get('funcao_id'),
            unidade_id=data.get('unidade_id')
        )
        
        db.session.add(funcionario)
        db.session.commit()
        
        return jsonify(funcionario.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@funcionarios_bp.route('/funcionarios/<int:id>', methods=['PUT'])
def atualizar_funcionario(id):
    try:
        funcionario = Funcionario.query.get_or_404(id)
        data = request.get_json()
        
        # Atualizar campos
        if 'nome' in data:
            funcionario.nome = data['nome']
        if 'ramal' in data:
            funcionario.ramal = data['ramal']
        if 'email' in data:
            funcionario.email = data['email']
        if 'whatsapp' in data:
            funcionario.whatsapp = data['whatsapp']
        if 'departamento_id' in data:
            funcionario.departamento_id = data['departamento_id']
        if 'funcao_id' in data:
            funcionario.funcao_id = data['funcao_id']
        if 'unidade_id' in data:
            funcionario.unidade_id = data['unidade_id']
        if 'ativo' in data:
            funcionario.ativo = data['ativo']
        
        db.session.commit()
        return jsonify(funcionario.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@funcionarios_bp.route('/funcionarios/<int:id>', methods=['DELETE'])
def deletar_funcionario(id):
    try:
        funcionario = Funcionario.query.get_or_404(id)
        db.session.delete(funcionario)
        db.session.commit()
        
        return jsonify({'message': 'Funcionário excluído com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

