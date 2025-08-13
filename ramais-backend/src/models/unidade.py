from src.models.user import db

class Unidade(db.Model):
    __tablename__ = 'unidades'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    ativo = db.Column(db.Boolean, default=True)
    
    # Relacionamento com funcionários
    funcionarios = db.relationship('Funcionario', backref='unidade_rel', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'ativo': self.ativo
        }
    
    def __repr__(self):
        return f'<Unidade {self.nome}>'

