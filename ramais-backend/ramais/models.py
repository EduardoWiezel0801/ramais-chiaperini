from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    """
    Modelo de usuário customizado baseado no AbstractUser do Django
    """
    is_admin = models.BooleanField(default=False, verbose_name='É Administrador')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    can_edit = models.BooleanField(default=True, verbose_name='Pode Editar')
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return self.username


class Departamento(models.Model):
    """
    Modelo para departamentos da empresa
    """
    nome = models.CharField(max_length=100, unique=True, verbose_name='Nome')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    
    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Funcao(models.Model):
    """
    Modelo para funções/cargos dos funcionários
    """
    nome = models.CharField(max_length=100, unique=True, verbose_name='Nome')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    
    class Meta:
        verbose_name = 'Função'
        verbose_name_plural = 'Funções'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Unidade(models.Model):
    """
    Modelo para unidades da empresa
    """
    nome = models.CharField(max_length=100, unique=True, verbose_name='Nome')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    
    class Meta:
        verbose_name = 'Unidade'
        verbose_name_plural = 'Unidades'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Funcionario(models.Model):
    """
    Modelo para funcionários com informações de contato
    """
    nome = models.CharField(max_length=200, verbose_name='Nome')
    ramal = models.CharField(max_length=20, blank=True, null=True, verbose_name='Ramal')
    email = models.EmailField(max_length=200, blank=True, null=True, verbose_name='E-mail')
    whatsapp = models.CharField(max_length=20, blank=True, null=True, verbose_name='WhatsApp')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    
    # Relacionamentos com chaves estrangeiras
    departamento = models.ForeignKey(
        Departamento, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='funcionarios',
        verbose_name='Departamento'
    )
    funcao = models.ForeignKey(
        Funcao, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='funcionarios',
        verbose_name='Função'
    )
    unidade = models.ForeignKey(
        Unidade, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='funcionarios',
        verbose_name='Unidade'
    )
    
    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
    
    @property
    def departamento_nome(self):
        """Retorna o nome do departamento ou None"""
        return self.departamento.nome if self.departamento else None
    
    @property
    def funcao_nome(self):
        """Retorna o nome da função ou None"""
        return self.funcao.nome if self.funcao else None
    
    @property
    def unidade_nome(self):
        """Retorna o nome da unidade ou None"""
        return self.unidade.nome if self.unidade else None
    # Relacionamentos com chaves estrangeiras
    departamento = models.ForeignKey(
        Departamento, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='funcionarios',
        verbose_name='Departamento'
    )
    funcao = models.ForeignKey(
        Funcao, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='funcionarios',
        verbose_name='Função'
    )
    unidade = models.ForeignKey(
        Unidade, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='funcionarios',
        verbose_name='Unidade'
    )
    
    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
    
    @property
    def departamento_nome(self):
        """Retorna o nome do departamento ou None"""
        return self.departamento.nome if self.departamento else None
    
    @property
    def funcao_nome(self):
        """Retorna o nome da função ou None"""
        return self.funcao.nome if self.funcao else None
    
    @property
    def unidade_nome(self):
        """Retorna o nome da unidade ou None"""
        return self.unidade.nome if self.unidade else None