from src.models.user import db

class Funcao(db.Model):
    __tablename__ = 'funcoes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    ativo = db.Column(db.Boolean, default=True)
    
    # Relacionamento com funcionários
    funcionarios = db.relationship('Funcionario', backref='funcao_rel', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'ativo': self.ativo
        }
    
    def __repr__(self):
        return f'<Funcao {self.nome}>'

