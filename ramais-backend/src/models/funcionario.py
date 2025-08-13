from src.models.user import db

class Funcionario(db.Model):
    __tablename__ = 'funcionarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    ramal = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(200), nullable=True)
    whatsapp = db.Column(db.String(20), nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    
    # Chaves estrangeiras
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamentos.id'), nullable=True)
    funcao_id = db.Column(db.Integer, db.ForeignKey('funcoes.id'), nullable=True)
    unidade_id = db.Column(db.Integer, db.ForeignKey('unidades.id'), nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'ramal': self.ramal,
            'email': self.email,
            'whatsapp': self.whatsapp,
            'ativo': self.ativo,
            'departamento_id': self.departamento_id,
            'departamento': self.departamento_rel.nome if self.departamento_rel else None,
            'funcao_id': self.funcao_id,
            'funcao': self.funcao_rel.nome if self.funcao_rel else None,
            'unidade_id': self.unidade_id,
            'unidade': self.unidade_rel.nome if self.unidade_rel else None
        }
    
    def __repr__(self):
        return f'<Funcionario {self.nome}>'

