from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import status

# Esquema para login
login_schema = extend_schema(
    request={
        'application/x-www-form-urlencoded': {
            'username': str,
            'password': str
        }
    },
    responses={
        200: {
            'message': str,
            'tokens': {
                'refresh': str,
                'access': str
            }
        },
        401: {
            'error': str
        }
    },
    description="Autentica o usuário e retorna tokens JWT.",
)

# Esquema para meus arquivos
meus_arquivos_schema = extend_schema(
    request={
        'application/x-www-form-urlencoded': {
            'matricula': str
        }
    },
    responses={
        200: {
            'result': str
        }
    },
    description="Retorna a lista de arquivos do usuário com base na matrícula.",
)

# Esquema para alterar senha
alterar_senha_schema = extend_schema(
    request={
        'application/x-www-form-urlencoded': {
            'matricula': str,
            'nova_senha': str
        }
    },
    responses={
        200: {
            'message': str
        },
        404: {
            'error': str
        }
    },
    description="Altera a senha do usuário com base na matrícula.",
)

# Esquema para buscar informações
buscar_informacoes_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            'matricula',
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            description='Matrícula do usuário'
        )
    ],
    responses={
        200: {
            'result': [
                {
                    'nome': str,
                    'hash_secreta': str
                }
            ]
        },
        401: {
            'error': str
        }
    },
    description="Busca informações do usuário autenticado com base na matrícula.",
)

# Esquema para upload de arquivo
upload_arquivo_schema = extend_schema(
    request={
        'multipart/form-data': {
            'arquivo': 'file',
            'descricao': str
        }
    },
    responses={
        200: {
            'message': str,
            'file_name': str
        },
        401: {
            'error': str
        }
    },
    description="Faz o upload de um arquivo para o servidor.",
)
