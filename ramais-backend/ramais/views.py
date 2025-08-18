from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied, ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import login, logout
from django.db.models import Q

from .models import Usuario, Departamento, Funcao, Unidade, Funcionario
from .serializers import (
    UsuarioSerializer, LoginSerializer, DepartamentoSerializer,
    FuncaoSerializer, UnidadeSerializer, FuncionarioSerializer,
    FuncionarioListSerializer
)


def check_edit_permission(user):
    """Verifica se o usuário tem permissão para editar"""
    return user.is_admin or user.can_edit


class AuthViewSet(viewsets.ViewSet):
    """
    ViewSet para autenticação - login, logout, me
    """
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """Endpoint para login de usuário"""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({
                'message': 'Login realizado com sucesso',
                'user': UsuarioSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Endpoint para logout de usuário"""
        logout(request)
        return Response({'message': 'Logout realizado com sucesso'})
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Endpoint para obter dados do usuário logado"""
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar usuários
    """
    queryset = Usuario.objects.filter(ativo=True)
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_admin', 'ativo', 'can_edit']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering_fields = ['username', 'first_name', 'date_joined']
    ordering = ['username']
    
    def get_queryset(self):
        """Apenas admins podem ver todos os usuários"""
        if self.request.user.is_admin:
            return Usuario.objects.all()
        return Usuario.objects.filter(id=self.request.user.id)
    
    def perform_create(self, serializer):
        """Apenas admins podem criar usuários"""
        if not self.request.user.is_admin:
            raise PermissionDenied('Apenas administradores podem criar usuários')
        serializer.save()
    
    def perform_update(self, serializer):
        """Usuários podem editar apenas seus próprios dados, admins podem editar todos"""
        if not self.request.user.is_admin and self.get_object() != self.request.user:
            raise PermissionDenied('Você só pode editar seus próprios dados')
        serializer.save()
    
    def perform_destroy(self, serializer):
        """Apenas admins podem excluir usuários (soft delete)"""
        if not self.request.user.is_admin:
            raise PermissionDenied('Apenas administradores podem excluir usuários')
        # Soft delete - apenas marca como inativo
        usuario = self.get_object()
        usuario.ativo = False
        usuario.save()


class DepartamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar departamentos
    """
    queryset = Departamento.objects.filter(ativo=True)
    serializer_class = DepartamentoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome']
    ordering_fields = ['nome']
    ordering = ['nome']
    
    def perform_create(self, serializer):
        """Verificar se usuário pode editar antes de criar"""
        if not check_edit_permission(self.request.user):
            raise PermissionDenied('Você não tem permissão para criar departamentos')
        serializer.save()
    
    def perform_update(self, serializer):
        """Verificar se usuário pode editar antes de atualizar"""
        if not check_edit_permission(self.request.user):
            raise PermissionDenied('Você não tem permissão para editar departamentos')
        serializer.save()
    
    def perform_destroy(self, instance):
        """Verificar se tem funcionários vinculados antes de excluir"""
        if not check_edit_permission(self.request.user):
            raise PermissionDenied('Você não tem permissão para excluir departamentos')
        if instance.funcionarios.filter(ativo=True).exists():
            raise ValidationError('Não é possível excluir departamento com funcionários vinculados')
        instance.delete()


class FuncaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar funções
    """
    queryset = Funcao.objects.filter(ativo=True)
    serializer_class = FuncaoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome']
    ordering_fields = ['nome']
    ordering = ['nome']
    
    def perform_create(self, serializer):
        """Verificar se usuário pode editar antes de criar"""
        if not check_edit_permission(self.request.user):
            raise PermissionDenied('Você não tem permissão para criar funções')
        serializer.save()
    
    def perform_update(self, serializer):
        """Verificar se usuário pode editar antes de atualizar"""
        if not check_edit_permission(self.request.user):
            raise PermissionDenied('Você não tem permissão para editar funções')
        serializer.save()
    
    def perform_destroy(self, instance):
        """Verificar se tem funcionários vinculados antes de excluir"""
        if not check_edit_permission(self.request.user):
            raise PermissionDenied('Você não tem permissão para excluir funções')
        if instance.funcionarios.filter(ativo=True).exists():
            raise ValidationError('Não é possível excluir função com funcionários vinculados')
        instance.delete()


class UnidadeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar unidades
    """
    queryset = Unidade.objects.filter(ativo=True)
    serializer_class = UnidadeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome']
    ordering_fields = ['nome']
    ordering = ['nome']
    
    def perform_create(self, serializer):
        """Verificar se usuário pode editar antes de criar"""
        if not check_edit_permission(self.request.user):
            raise PermissionDenied('Você não tem permissão para criar unidades')
        serializer.save()
    
    def perform_update(self, serializer):
        """Verificar se usuário pode editar antes de atualizar"""
        if not check_edit_permission(self.request.user):
            raise PermissionDenied('Você não tem permissão para editar unidades')
        serializer.save()
    
    def perform_destroy(self, instance):
        """Verificar se tem funcionários vinculados antes de excluir"""
        if not check_edit_permission(self.request.user):
            raise PermissionDenied('Você não tem permissão para excluir unidades')
        if instance.funcionarios.filter(ativo=True).exists():
            raise ValidationError('Não é possível excluir unidade com funcionários vinculados')
        instance.delete()


class FuncionarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar funcionários
    """
    queryset = Funcionario.objects.filter(ativo=True)
    serializer_class = FuncionarioSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['departamento', 'funcao', 'unidade', 'ativo']
    search_fields = ['nome', 'ramal', 'email', 'whatsapp']
    ordering_fields = ['nome', 'ramal']
    ordering = ['nome']
    
    def perform_create(self, serializer):
        """Verificar se usuário pode editar antes de criar"""
        if not check_edit_permission(self.request.user):
            raise PermissionDenied('Você não tem permissão para criar funcionários')
        serializer.save()
    
    def perform_update(self, serializer):
        """Verificar se usuário pode editar antes de atualizar"""
        if not check_edit_permission(self.request.user):
            raise PermissionDenied('Você não tem permissão para editar funcionários')
        serializer.save()
    
    def get_serializer_class(self):
        """Usar serializer simplificado para listagem"""
        if self.action == 'list':
            return FuncionarioListSerializer
        return FuncionarioSerializer
    
    def get_queryset(self):
        """Aplicar filtros de busca customizada"""
        # Começar com queryset base
        queryset = Funcionario.objects.filter(ativo=True).select_related('departamento', 'funcao', 'unidade')
        
        # Aplicar filtros apenas se existirem
        try:
            # Busca customizada
            busca = self.request.query_params.get('busca')
            if busca and busca.strip():
                queryset = queryset.filter(
                    Q(nome__icontains=busca) |
                    Q(ramal__icontains=busca) |
                    Q(email__icontains=busca) |
                    Q(whatsapp__icontains=busca) |
                    Q(departamento__nome__icontains=busca) |
                    Q(funcao__nome__icontains=busca) |
                    Q(unidade__nome__icontains=busca)
                )
            
            # Filtros específicos
            departamento_id = self.request.query_params.get('departamento_id')
            if departamento_id and departamento_id.strip():
                queryset = queryset.filter(departamento_id=departamento_id)
                
            funcao_id = self.request.query_params.get('funcao_id')
            if funcao_id and funcao_id.strip():
                queryset = queryset.filter(funcao_id=funcao_id)
                
            unidade_id = self.request.query_params.get('unidade_id')
            if unidade_id and unidade_id.strip():
                queryset = queryset.filter(unidade_id=unidade_id)
                
        except Exception as e:
            # Se der erro nos filtros, retornar queryset base
            print(f"Erro ao aplicar filtros: {e}")
            queryset = Funcionario.objects.filter(ativo=True).select_related('departamento', 'funcao', 'unidade')
        
        return queryset
    
    def perform_destroy(self, instance):
        """Soft delete - apenas marca como inativo"""
        if not check_edit_permission(self.request.user):
            raise PermissionDenied('Você não tem permissão para excluir funcionários')
        instance.ativo = False
        instance.save()