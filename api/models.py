import os
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("O campo 'username' é obrigatório.")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("O superusuário deve ter is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("O superusuário deve ter is_superuser=True.")

        return self.create_user(username, password, **extra_fields)


class Usuario(AbstractUser):
    matricula = models.TextField(max_length=14, null=True, blank=False)
    numero_arquivos = models.IntegerField(
        default=0)
    objects = UserManager()

    first_name = None
    last_name = None

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = 'Usuários'


def user_directory_path(instance, filename):
    return "{0}/{1}".format(instance.usuario.username, filename)


class Arquivo(models.Model):
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='arquivos')
    arquivo = models.FileField(upload_to=user_directory_path)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.descricao or "Arquivo"} de {self.usuario.username}'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.usuario.numero_arquivos += 1
            self.usuario.save()
        super().save(*args, **kwargs)


@receiver(post_delete, sender=Arquivo)
def decrement_numero_arquivos(sender, instance, **kwargs):
    instance.usuario.numero_arquivos -= 1
    instance.usuario.save()


class Informacoes(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nome_completo = models.TextField(max_length=200, blank=True, null=True)
