#!/usr/bin/env python3

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app
from src.models.usuario import Usuario, db

def init_database():
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()
        
        # Verificar se já existe usuário admin
        admin = Usuario.query.filter_by(username='admin').first()
        if not admin:
            # Criar usuário admin padrão
            admin = Usuario(username='admin', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Criar usuário comum padrão
            user = Usuario(username='usuario', is_admin=False)
            user.set_password('user123')
            db.session.add(user)
            
            db.session.commit()
            print("✅ Usuários padrão criados:")
            print("   Admin: admin / admin123")
            print("   Usuário: usuario / user123")
        else:
            print("✅ Banco de dados já inicializado")

if __name__ == '__main__':
    init_database()

