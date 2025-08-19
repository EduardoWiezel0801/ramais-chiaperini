from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Criar o router e registrar os ViewSets
router = DefaultRouter()
router.register(r'usuarios', views.UsuarioViewSet)
router.register(r'departamentos', views.DepartamentoViewSet)
router.register(r'funcoes', views.FuncaoViewSet)
router.register(r'unidades', views.UnidadeViewSet)
router.register(r'funcionarios', views.FuncionarioViewSet)

# URLs do app ramais
urlpatterns = [
    # URLs da API REST (CRUD automático)
    path('', include(router.urls)),
    
    # URL para obter CSRF token
    path('csrf/', views.CSRFTokenView.as_view(), name='csrf-token'),
    
    # URLs de autenticação
    path('auth/login/', views.AuthViewSet.as_view({'post': 'login'}), name='auth-login'),
    path('auth/logout/', views.AuthViewSet.as_view({'post': 'logout'}), name='auth-logout'),
    path('auth/me/', views.AuthViewSet.as_view({'get': 'me'}), name='auth-me'),
    path('auth/csrf/', views.AuthViewSet.as_view({'get': 'csrf'}), name='auth-csrf'),
]