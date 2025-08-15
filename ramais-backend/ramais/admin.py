from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import Usuario, Departamento, Funcao, Unidade, Funcionario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Admin para modelo Usuario customizado
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_admin', 'ativo', 'date_joined','can_edit')
    list_filter = ('is_admin', 'ativo', 'is_staff', 'is_superuser', 'date_joined','can_edit')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
    # Campos no formulário de edição
    fieldsets = UserAdmin.fieldsets + (
        ('Configurações Customizadas', {
            'fields': ('is_admin', 'ativo','can_edit')
        }),
    )
    
    # Campos no formulário de criação
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Configurações Customizadas', {
            'fields': ('is_admin', 'ativo','can_edit')
        }),
    )
    
    def get_queryset(self, request):
        """Mostrar todos os usuários incluindo inativos"""
        return Usuario.objects.all()


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    """
    Admin para modelo Departamento
    """
    list_display = ('nome', 'ativo', 'funcionarios_count', 'funcionarios_ativos_count')
    list_filter = ('ativo',)
    search_fields = ('nome',)
    ordering = ('nome',)
    
    def funcionarios_count(self, obj):
        """Total de funcionários no departamento"""
        return obj.funcionarios.count()
    funcionarios_count.short_description = 'Total Funcionários'
    
    def funcionarios_ativos_count(self, obj):
        """Funcionários ativos no departamento"""
        count = obj.funcionarios.filter(ativo=True).count()
        return format_html('<span style="color: green;">{}</span>', count)
    funcionarios_ativos_count.short_description = 'Funcionários Ativos'
    
    def get_queryset(self, request):
        """Otimizar queries com prefetch_related"""
        return super().get_queryset(request).prefetch_related('funcionarios')


@admin.register(Funcao)
class FuncaoAdmin(admin.ModelAdmin):
    """
    Admin para modelo Funcao
    """
    list_display = ('nome', 'ativo', 'funcionarios_count', 'funcionarios_ativos_count')
    list_filter = ('ativo',)
    search_fields = ('nome',)
    ordering = ('nome',)
    
    def funcionarios_count(self, obj):
        """Total de funcionários na função"""
        return obj.funcionarios.count()
    funcionarios_count.short_description = 'Total Funcionários'
    
    def funcionarios_ativos_count(self, obj):
        """Funcionários ativos na função"""
        count = obj.funcionarios.filter(ativo=True).count()
        return format_html('<span style="color: green;">{}</span>', count)
    funcionarios_ativos_count.short_description = 'Funcionários Ativos'
    
    def get_queryset(self, request):
        """Otimizar queries com prefetch_related"""
        return super().get_queryset(request).prefetch_related('funcionarios')


@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    """
    Admin para modelo Unidade
    """
    list_display = ('nome', 'ativo', 'funcionarios_count', 'funcionarios_ativos_count')
    list_filter = ('ativo',)
    search_fields = ('nome',)
    ordering = ('nome',)
    
    def funcionarios_count(self, obj):
        """Total de funcionários na unidade"""
        return obj.funcionarios.count()
    funcionarios_count.short_description = 'Total Funcionários'
    
    def funcionarios_ativos_count(self, obj):
        """Funcionários ativos na unidade"""
        count = obj.funcionarios.filter(ativo=True).count()
        return format_html('<span style="color: green;">{}</span>', count)
    funcionarios_ativos_count.short_description = 'Funcionários Ativos'
    
    def get_queryset(self, request):
        """Otimizar queries com prefetch_related"""
        return super().get_queryset(request).prefetch_related('funcionarios')


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    """
    Admin para modelo Funcionario
    """
    list_display = (
        'nome', 'ramal', 'email_link', 'whatsapp_link', 
        'departamento', 'funcao', 'unidade', 'ativo_badge'
    )
    list_filter = ('ativo', 'departamento', 'funcao', 'unidade')
    search_fields = ('nome', 'ramal', 'email', 'whatsapp')
    ordering = ('nome',)
    
    # Campos no formulário
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'ativo')
        }),
        ('Contato', {
            'fields': ('ramal', 'email', 'whatsapp')
        }),
        ('Organização', {
            'fields': ('departamento', 'funcao', 'unidade')
        }),
    )
    
    # Filtros horizontais para seleção múltipla (se necessário)
    filter_horizontal = ()
    
    def email_link(self, obj):
        """Criar link clicável para email"""
        if obj.email:
            return format_html('<a href="mailto:{}">{}</a>', obj.email, obj.email)
        return '-'
    email_link.short_description = 'Email'
    
    def whatsapp_link(self, obj):
        """Criar link clicável para WhatsApp"""
        if obj.whatsapp:
            # Remove caracteres não numéricos
            numero = ''.join(filter(str.isdigit, obj.whatsapp))
            if numero:
                return format_html(
                    '<a href="https://wa.me/55{}" target="_blank">{}</a>', 
                    numero, obj.whatsapp
                )
        return '-'
    whatsapp_link.short_description = 'WhatsApp'
    
    def ativo_badge(self, obj):
        """Badge colorido para status ativo"""
        if obj.ativo:
            return format_html('<span style="color: green; font-weight: bold;">✓ Ativo</span>')
        else:
            return format_html('<span style="color: red; font-weight: bold;">✗ Inativo</span>')
    ativo_badge.short_description = 'Status'
    
    def get_queryset(self, request):
        """Otimizar queries com select_related"""
        return super().get_queryset(request).select_related(
            'departamento', 'funcao', 'unidade'
        )
    
    # Ações customizadas
    actions = ['marcar_como_ativo', 'marcar_como_inativo']
    
    def marcar_como_ativo(self, request, queryset):
        """Ação para marcar funcionários selecionados como ativos"""
        updated = queryset.update(ativo=True)
        self.message_user(request, f'{updated} funcionário(s) marcado(s) como ativo(s).')
    marcar_como_ativo.short_description = 'Marcar selecionados como ATIVO'
    
    def marcar_como_inativo(self, request, queryset):
        """Ação para marcar funcionários selecionados como inativos"""
        updated = queryset.update(ativo=False)
        self.message_user(request, f'{updated} funcionário(s) marcado(s) como inativo(s).')
    marcar_como_inativo.short_description = 'Marcar selecionados como INATIVO'


# Customizar o header do admin
admin.site.site_header = 'Administração do Sistema de Ramais'
admin.site.site_title = 'Ramais Admin'
admin.site.index_title = 'Bem-vindo ao Sistema de Ramais'
