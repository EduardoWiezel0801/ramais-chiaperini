from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import login, logout
from django.db.models import Q

from .models import Usuario, Departamento, Funcao, Unidade, Funcionario
from .serializers import (
    UsuarioSerializer, LoginSerializer, DepartamentoSerializer,
    FuncaoSerializer, UnidadeSerializer, FuncionarioSerializer,
    FuncionarioListSerializer
)


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
    filterset_fields = ['is_admin', 'ativo']
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
            raise PermissionError('Apenas administradores podem criar usuários')
        serializer.save()
    
    def perform_update(self, serializer):
        """Usuários podem editar apenas seus próprios dados, admins podem editar todos"""
        if not self.request.user.is_admin and self.get_object() != self.request.user:
            raise PermissionError('Você só pode editar seus próprios dados')
        serializer.save()
    
    def perform_destroy(self, serializer):
        """Apenas admins podem excluir usuários (soft delete)"""
        if not self.request.user.is_admin:
            raise PermissionError('Apenas administradores podem excluir usuários')
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
    
    def perform_destroy(self, instance):
        """Verificar se tem funcionários vinculados antes de excluir"""
        if instance.funcionarios.filter(ativo=True).exists():
            raise ValueError('Não é possível excluir departamento com funcionários vinculados')
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
    
    def perform_destroy(self, instance):
        """Verificar se tem funcionários vinculados antes de excluir"""
        if instance.funcionarios.filter(ativo=True).exists():
            raise ValueError('Não é possível excluir função com funcionários vinculados')
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
    
    def perform_destroy(self, instance):
        """Verificar se tem funcionários vinculados antes de excluir"""
        if instance.funcionarios.filter(ativo=True).exists():
            raise ValueError('Não é possível excluir unidade com funcionários vinculados')
        instance.delete()


class FuncionarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar funcionários
    """
    queryset = Funcionario.objects.filter(ativo=True)
    serializer_class = FuncionarioSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    queryset = Funcionario.objects.filter(ativo=True)
    search_fields = ['nome', 'ramal', 'email', 'whatsapp']
    ordering_fields = ['nome', 'ramal']
    ordering = ['nome']
    
    def get_serializer_class(self):
        """Usar serializer simplificado para listagem"""
        if self.action == 'list':
            return FuncionarioListSerializer
        return FuncionarioSerializer
    
    def get_queryset(self):
        """Aplicar filtros de busca customizada"""
        queryset = Funcionario.objects.filter(ativo=True)
        
        # Busca customizada que funciona em todos os campos
        busca = self.request.query_params.get('busca', None)
        if busca:
            queryset = queryset.filter(
                Q(nome__icontains=busca) |
                Q(ramal__icontains=busca) |
                Q(email__icontains=busca) |
                Q(whatsapp__icontains=busca) |
                Q(departamento__nome__icontains=busca) |
                Q(funcao__nome__icontains=busca) |
                Q(unidade__nome__icontains=busca)
            )
        
        return queryset.select_related('departamento', 'funcao', 'unidade')
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Endpoint customizado para busca avançada"""
        busca = request.query_params.get('q', '')
        departamento_id = request.query_params.get('departamento_id')
        funcao_id = request.query_params.get('funcao_id')
        unidade_id = request.query_params.get('unidade_id')
        
        queryset = self.get_queryset()
        
        # Aplicar busca por texto
        if busca:
            queryset = queryset.filter(
                Q(nome__icontains=busca) |
                Q(ramal__icontains=busca) |
                Q(email__icontains=busca) |
                Q(whatsapp__icontains=busca)
            )
        
        # Aplicar filtros específicos
        if departamento_id:
            queryset = queryset.filter(departamento_id=departamento_id)
        if funcao_id:
            queryset = queryset.filter(funcao_id=funcao_id)
        if unidade_id:
            queryset = queryset.filter(unidade_id=unidade_id)
        
        # Paginar resultados
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FuncionarioListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = FuncionarioListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def perform_destroy(self, instance):
        """Soft delete - apenas marca como inativo"""
        instance.ativo = False
        instance.save()