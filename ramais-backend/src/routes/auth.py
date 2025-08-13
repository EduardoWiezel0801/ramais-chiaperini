from flask import Blueprint, request, jsonify, session
from src.models.usuario import Usuario, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username e password são obrigatórios'}), 400
        
        usuario = Usuario.query.filter_by(username=data['username'], ativo=True).first()
        
        if usuario and usuario.check_password(data['password']):
            session['user_id'] = usuario.id
            session['is_admin'] = usuario.is_admin
            
            return jsonify({
                'message': 'Login realizado com sucesso',
                'user': usuario.to_dict()
            })
        else:
            return jsonify({'error': 'Credenciais inválidas'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    try:
        session.clear()
        return jsonify({'message': 'Logout realizado com sucesso'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
def me():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Não autenticado'}), 401
        
        usuario = Usuario.query.get(session['user_id'])
        if not usuario or not usuario.ativo:
            session.clear()
            return jsonify({'error': 'Usuário inválido'}), 401
        
        return jsonify(usuario.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    try:
        # Verificar se é admin
        if 'user_id' not in session:
            return jsonify({'error': 'Não autenticado'}), 401
        
        usuario_logado = Usuario.query.get(session['user_id'])
        if not usuario_logado or not usuario_logado.is_admin:
            return jsonify({'error': 'Acesso negado'}), 403
        
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username e password são obrigatórios'}), 400
        
        # Verificar se já existe
        existe = Usuario.query.filter_by(username=data['username']).first()
        if existe:
            return jsonify({'error': 'Username já existe'}), 400
        
        usuario = Usuario(
            username=data['username'],
            is_admin=data.get('is_admin', False)
        )
        usuario.set_password(data['password'])
        
        db.session.add(usuario)
        db.session.commit()
        
        return jsonify(usuario.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

