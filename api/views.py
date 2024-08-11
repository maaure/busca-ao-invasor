from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import GenericAPIView

from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Usuario, Arquivo
import os
import sqlite3
from .serializers import *


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginView(GenericAPIView):

    def get_serializer_class(self):
        return LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('matricula')
            password = serializer.validated_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                tokens = get_tokens_for_user(user)
                return Response({"message": "Login realizado com sucesso!", "tokens": tokens})
            else:
                return Response({"error": "Credenciais inválidas"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='matricula',
                             description='Número de Matrícula', type=str),
        ]
    )
)
class MeusArquivosView(GenericAPIView):

    def get_serializer_class(self):
        return super().get_serializer_class()

    def get(self, request):
        matricula = request.data.get('matricula')
        result = os.popen(f"ls ~/arquivos/{matricula}").read()
        return Response({"result": result})


class AlterarSenhaView(GenericAPIView):
    def get_serializer_class(self):
        return AlterarSenhaSerializer

    def post(self, request):
        serializer = AlterarSenhaSerializer(data=request.data)
        if serializer.is_valid():
            matricula = serializer.validated_data.get('matricula')
            nova_senha = serializer.validated_data.get('nova_senha')
            try:
                user = Usuario.objects.get(username=matricula)
                user.set_password(nova_senha)
                user.save()
                return Response({"message": "Senha alterada com sucesso"})
            except Usuario.DoesNotExist:
                return Response({"error": "Usuário não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='matricula',
                             description='Número de Matrícula', type=str),
        ]
    )
)
class MeuCadastroView(GenericAPIView):

    def get_serializer_class(self):
        return MeuCadastroSerializer

    def get(self, request):
        usuario = request.user
        if not usuario.is_authenticated:
            return Response({"error": "Usuário não autenticado"}, status=status.HTTP_401_UNAUTHORIZED)

        matricula = request.query_params.get('matricula')
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        query = f"""
        SELECT i.minha_hash, i.nome_completo
        FROM api_informacoes i
        JOIN api_usuario u ON u.id = i.usuario_id
        WHERE u.username = {matricula}
        """
        cursor.execute(query)
        result = cursor.fetchall()

        informacoes = [InformacoesSerializer(
            {"nome": r[1], "hash_secreta": r[0]}).data for r in result]
        return Response({"result": informacoes})


class UploadArquivoView(GenericAPIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        return UploadArquivoSerializer

    def post(self, request):
        serializer = UploadArquivoSerializer(data=request.data)
        if serializer.is_valid():
            usuario = request.user
            if not usuario.is_authenticated:
                return Response({"error": "Usuário não autenticado"}, status=status.HTTP_401_UNAUTHORIZED)

            arquivo = serializer.validated_data.get('arquivo')
            descricao = serializer.validated_data.get('descricao')

            arquivo_obj = Arquivo(
                usuario=usuario, arquivo=arquivo, descricao=descricao
            )
            arquivo_obj.save()

            return Response({"message": "Arquivo enviado com sucesso", "file_name": arquivo_obj.arquivo.name})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)