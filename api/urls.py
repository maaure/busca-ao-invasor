from django.urls import path
from .views import LoginView, AlterarSenhaView, MeuCadastroView, UploadArquivoView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('alterar-senha/', AlterarSenhaView.as_view(), name='alterar_senha'),
    path('minhas-informacoes/', MeuCadastroView.as_view(),
         name='buscar_informacoes'),
    path('arquivo/', UploadArquivoView.as_view(), name='upload_arquivo'),
]
