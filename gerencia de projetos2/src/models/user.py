from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    curso = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    palavras_chave = db.Column(db.Text, nullable=False)  # Armazenado como string separada por vírgulas
    ativo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'curso': self.curso,
            'cidade': self.cidade,
            'palavras_chave': self.palavras_chave.split(',') if self.palavras_chave else [],
            'ativo': self.ativo
        }
