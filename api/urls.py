from django.urls import path
from .views import LoginView, MeusArquivosView, AlterarSenhaView, MeuCadastroView, UploadArquivoView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('meus-arquivos/', MeusArquivosView.as_view(), name='meus_arquivos'),
    path('alterar-senha/', AlterarSenhaView.as_view(), name='alterar_senha'),
    path('minha-hash/', MeuCadastroView.as_view(), name='buscar_informacoes'),
    path('upload-arquivo/', UploadArquivoView.as_view(), name='upload_arquivo'),
]
