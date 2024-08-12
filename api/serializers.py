from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    matricula = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class AlterarSenhaSerializer(serializers.Serializer):
    matricula = serializers.CharField(required=True)
    nova_senha = serializers.CharField(required=True)


class InformacoesSerializer(serializers.Serializer):
    nome_completo = serializers.CharField()
    numero_arquivos = serializers.CharField()


class UploadArquivoSerializer(serializers.Serializer):
    arquivo = serializers.FileField()
    descricao = serializers.CharField(required=False, allow_blank=True)
