from flask import Blueprint, jsonify, request
from src.models.user import User, db
import random
from datetime import datetime

agente_bp = Blueprint('agente', __name__)

# Dados simulados de vagas
VAGAS_SIMULADAS = [
    {
        "titulo": "Estágio em Desenvolvimento Python",
        "empresa": "TechCorp",
        "cidade": "São Paulo",
        "descricao": "Estágio para desenvolvimento de aplicações web com Python e Django",
        "palavras_chave": ["python", "django", "web", "desenvolvimento"],
        "portal": "CIEE"
    },
    {
        "titulo": "Estágio em Suporte Técnico",
        "empresa": "InfoSys",
        "cidade": "Rio de Janeiro", 
        "descricao": "Suporte técnico a utilizadores e manutenção de sistemas",
        "palavras_chave": ["suporte", "técnico", "sistemas", "helpdesk"],
        "portal": "Nube"
    },
    {
        "titulo": "Estágio em Marketing Digital",
        "empresa": "DigitalMax",
        "cidade": "Belo Horizonte",
        "descricao": "Criação de campanhas digitais e gestão de redes sociais",
        "palavras_chave": ["marketing", "digital", "redes sociais", "campanhas"],
        "portal": "LinkedIn"
    },
    {
        "titulo": "Estágio em Análise de Dados",
        "empresa": "DataLab",
        "cidade": "São Paulo",
        "descricao": "Análise de dados com Python e ferramentas de BI",
        "palavras_chave": ["python", "dados", "análise", "bi", "estatística"],
        "portal": "CIEE"
    },
    {
        "titulo": "Estágio em Desenvolvimento Frontend",
        "empresa": "WebStudio",
        "cidade": "Porto Alegre",
        "descricao": "Desenvolvimento de interfaces web com React e JavaScript",
        "palavras_chave": ["react", "javascript", "frontend", "web", "css"],
        "portal": "LinkedIn"
    },
    {
        "titulo": "Estágio em Redes e Infraestrutura",
        "empresa": "NetSolutions",
        "cidade": "Brasília",
        "descricao": "Configuração e manutenção de redes corporativas",
        "palavras_chave": ["redes", "infraestrutura", "cisco", "configuração"],
        "portal": "Nube"
    },
    {
        "titulo": "Estágio em Design Gráfico",
        "empresa": "CreativeAgency",
        "cidade": "São Paulo",
        "descricao": "Criação de materiais gráficos e identidade visual",
        "palavras_chave": ["design", "gráfico", "photoshop", "illustrator", "criativo"],
        "portal": "CIEE"
    },
    {
        "titulo": "Estágio em Administração",
        "empresa": "AdminCorp",
        "cidade": "Curitiba",
        "descricao": "Apoio em processos administrativos e gestão de documentos",
        "palavras_chave": ["administração", "gestão", "processos", "documentos"],
        "portal": "LinkedIn"
    }
]

def filtrar_vagas_por_utilizador(user):
    """Filtra vagas baseado no perfil do utilizador"""
    vagas_correspondentes = []
    user_keywords = [kw.lower().strip() for kw in user.palavras_chave.split(',')]
    
    for vaga in VAGAS_SIMULADAS:
        # Verificar se a cidade corresponde
        if user.cidade.lower() in vaga["cidade"].lower() or vaga["cidade"].lower() in user.cidade.lower():
            # Verificar se alguma palavra-chave corresponde
            for user_kw in user_keywords:
                for vaga_kw in vaga["palavras_chave"]:
                    if user_kw in vaga_kw.lower() or vaga_kw.lower() in user_kw:
                        if vaga not in vagas_correspondentes:
                            vagas_correspondentes.append(vaga)
                        break
    
    return vagas_correspondentes

@agente_bp.route('/executar', methods=['POST'])
def executar_agente():
    """Simula a execução do agente de varredura de vagas"""
    try:
        # Buscar todos os utilizadores ativos
        users = User.query.filter_by(ativo=True).all()
        
        if not users:
            return jsonify({
                'success': False,
                'message': 'Nenhum utilizador ativo encontrado'
            }), 400
        
        resultados = []
        total_vagas_encontradas = 0
        
        for user in users:
            vagas_correspondentes = filtrar_vagas_por_utilizador(user)
            total_vagas_encontradas += len(vagas_correspondentes)
            
            resultado_user = {
                'user_id': user.id,
                'nome': user.nome,
                'email': user.email,
                'vagas_encontradas': len(vagas_correspondentes),
                'vagas': vagas_correspondentes
            }
            resultados.append(resultado_user)
        
        return jsonify({
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'total_users_processados': len(users),
            'total_vagas_encontradas': total_vagas_encontradas,
            'portais_verificados': ['CIEE', 'Nube', 'LinkedIn'],
            'resultados': resultados
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@agente_bp.route('/status', methods=['GET'])
def status_agente():
    """Retorna o status do agente"""
    users_ativos = User.query.filter_by(ativo=True).count()
    total_users = User.query.count()
    
    return jsonify({
        'status': 'online',
        'users_ativos': users_ativos,
        'total_users': total_users,
        'portais_configurados': ['CIEE', 'Nube', 'LinkedIn'],
        'ultima_execucao': 'Simulação - não executado automaticamente'
    })

@agente_bp.route('/vagas-exemplo', methods=['GET'])
def vagas_exemplo():
    """Retorna exemplos de vagas disponíveis"""
    # Retornar uma amostra aleatória de vagas
    amostra = random.sample(VAGAS_SIMULADAS, min(5, len(VAGAS_SIMULADAS)))
    return jsonify({
        'vagas_exemplo': amostra,
        'total_vagas_simuladas': len(VAGAS_SIMULADAS)
    })

