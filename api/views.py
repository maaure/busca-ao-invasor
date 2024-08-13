from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import action

from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema, extend_schema_view

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
                user_data = UsuarioSerializer(user).data
                return Response({
                    "message": "Login realizado com sucesso!",
                    "tokens": tokens,
                    "user": user_data
                })
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

    def get(self, request):
        usuario = request.user
        if not usuario.is_authenticated:
            return Response({"error": "Usuário não autenticado"}, status=status.HTTP_401_UNAUTHORIZED)

        matricula = request.query_params.get('matricula')
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        query = f"""
        SELECT u.numero_arquivos, i.nome_completo
        FROM api_informacoes i
        JOIN api_usuario u ON u.id = i.usuario_id
        WHERE u.username = {matricula}
        """
        cursor.execute(query)
        result = cursor.fetchall()

        informacoes = [InformacoesSerializer(
            {"nome_completo": r[1], "numero_arquivos": r[0]}).data for r in result]
        return Response({"result": informacoes})


@extend_schema_view(
    delete=extend_schema(
        parameters=[
            OpenApiParameter(name='nome',
                             description='Nome do arquivo', type=str),
        ]
    ),
    responses={
        200: OpenApiTypes.STR,
    }
)
class UploadArquivoView(GenericAPIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = UploadArquivoSerializer

    def get_serializer_class(self):
        return UploadArquivoSerializer

    def get(self, request):
        usuario = request.user
        if not usuario.is_authenticated:
            return Response({"error": "Usuário não autenticado"}, status=status.HTTP_401_UNAUTHORIZED)
        arquivos = Arquivo.objects.filter(usuario=usuario)
        serializer = self.get_serializer(arquivos, many=True)
        return Response(serializer.data)

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

    def delete(self, request):
        usuario = request.user
        if not usuario.is_authenticated:
            return Response({"error": "Usuário não autenticado"}, status=status.HTTP_401_UNAUTHORIZED)

        nome_arquivo = request.query_params.get('nome', None)
        if not nome_arquivo:
            return Response({"error": "Nome do arquivo não fornecido"}, status=status.HTTP_400_BAD_REQUEST)

        command = f"ls media/{usuario.username}/{nome_arquivo}"

        result = os.popen(command).read()

        return Response({"message": f"Arquivo '{nome_arquivo}' excluído com sucesso", "response": result}, status=status.HTTP_200_OK)
