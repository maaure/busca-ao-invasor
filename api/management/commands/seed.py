from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import hashlib
from api.models import *


class Command(BaseCommand):
    help = 'Popula o banco de dados com usuários e suas matrículas'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        users = [
            ("Ana Célia Baía Araújo", "20221014040009"),
            ("Anna Carolinne Albuquerque de Medeiros", "20201014040053"),
            ("Antônio Fernandes da Cruz Junior", "20211014040033"),
            ("Ariane Silveira Correa", "20212014040001"),
            ("Arthur de Melo Galvão", "20221014040003"),
            ("Bruno Lins Dos Santos Viana", "20221014040010"),
            ("Cibele Regina Barros Diniz", "20221014040018"),
            ("Davi Alessandro Canuto da Silva Gregorio", "20211014040030"),
            ("Debora Lavínia da Silva Melo", "20211014040047"),
            ("Felipe Xavier de Carvalho", "20221014040007"),
            ("Fernanda da Silva Caldas", "20162014040011"),
            ("Igor Gabriel de Araujo Dantas", "20221014040008"),
            ("Italo Mageste Martins Franca", "20211014040024"),
            ("Joana Darc Fernandes Silva", "20191014040076"),
            ("Jose Vilanir de Souza Brito Neto", "20221014040006"),
            ("Lucas Nithael Silva de Souza", "20211014040063"),
            ("Marcus Vinícius Cadete Spencer Chaves", "20221014040001"),
            ("Matheus Duarte de Medeiros", "20211014040022"),
            ("Neemias Renan Santos de Oliveira", "20211014040062"),
            ("Pedro Maure Frutuoso de Andrade", "20221014040013"),
            ("Renato Bernardino da Silva Araújo", "20191014040068"),
            ("Ronaldo Bento Marinho Filho", "20211014040044"),
            ("Sergio Henrique Oliveira de Azevedo", "20182014040007"),
            ("Thiago Magalhaes Lima Oliveira", "20211014040016"),
            ("Virginia Claudia de Lima Menezes", "20191014040004"),
            ("Wagner Amadeus Galvao de Souza", "20211014040028"),
            ("Wemerson Das Chagas Dos Santos", "20172014040035"),
            ("Yuri Thairony Feitosa de Oliveira", "20222014040015"),
        ]

        for nome_completo, matricula in users:
            user, created = User.objects.get_or_create(
                username=matricula
            )
            if created:
                user.set_password('123')
                user.save()

            Informacoes.objects.create(
                usuario=user, nome_completo=nome_completo)

        flag_user = User.objects.create(username="ArthurMelo777")
        Informacoes.objects.create(
            usuario=flag_user, nome_completo="Invasor Secreto")
        Arquivo.objects.create(
            usuario=flag_user, arquivo=None, descricao="Arquivo secreto")

        self.stdout.write(self.style.SUCCESS('Usuários criados com sucesso!'))
