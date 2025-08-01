from flask import Blueprint, jsonify, request
from src.models.user import User, db

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    
    # Validação básica
    required_fields = ['nome', 'email', 'curso', 'cidade', 'palavras_chave']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Campo {field} é obrigatório'}), 400
    
    # Verificar se email já existe
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'error': 'Email já cadastrado'}), 400
    
    # Processar palavras-chave (converter lista para string)
    palavras_chave_str = ','.join(data['palavras_chave']) if isinstance(data['palavras_chave'], list) else data['palavras_chave']
    
    user = User(
        nome=data['nome'],
        email=data['email'],
        curso=data['curso'],
        cidade=data['cidade'],
        palavras_chave=palavras_chave_str
    )
    
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    
    user.nome = data.get('nome', user.nome)
    user.email = data.get('email', user.email)
    user.curso = data.get('curso', user.curso)
    user.cidade = data.get('cidade', user.cidade)
    
    if 'palavras_chave' in data:
        palavras_chave_str = ','.join(data['palavras_chave']) if isinstance(data['palavras_chave'], list) else data['palavras_chave']
        user.palavras_chave = palavras_chave_str
    
    user.ativo = data.get('ativo', user.ativo)
    
    db.session.commit()
    return jsonify(user.to_dict())

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204


