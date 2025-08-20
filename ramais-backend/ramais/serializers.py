from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Usuario, Departamento, Funcao, Unidade, Funcionario


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para modelo Usuario
    """
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_admin', 'ativo','can_edit', 'date_joined', 'last_login',
            'password', 'password_confirm'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True},
        }
    
    def validate(self, attrs):
        """Validação customizada para confirmação de senha"""
        if 'password_confirm' in attrs:
            if attrs['password'] != attrs['password_confirm']:
                raise serializers.ValidationError({
                    'password_confirm': 'As senhas não conferem.'
                })
        return attrs
    
    def create(self, validated_data):
        """Criar usuário com senha criptografada"""
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password')
        user = Usuario(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        """Atualizar usuário, incluindo senha se fornecida"""
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    """
    Serializer para login de usuário
    """
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            
            if not user:
                raise serializers.ValidationError('Credenciais inválidas.')
            
            if not user.ativo:
                raise serializers.ValidationError('Usuário inativo.')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Username e password são obrigatórios.')


class DepartamentoSerializer(serializers.ModelSerializer):
    """
    Serializer para modelo Departamento
    """
    funcionarios_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Departamento
        fields = ['id', 'nome', 'ativo', 'funcionarios_count']
    
    def get_funcionarios_count(self, obj):
        """Retorna quantidade de funcionários ativos no departamento"""
        return obj.funcionarios.filter(ativo=True).count()
    
    def validate_nome(self, value):
        """Validação para nome único (case insensitive)"""
        # Verificar se já existe outro departamento com mesmo nome
        instance = self.instance
        if Departamento.objects.filter(
            nome__iexact=value
        ).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError('Já existe um departamento com este nome.')
        return value


class FuncaoSerializer(serializers.ModelSerializer):
    """
    Serializer para modelo Funcao
    """
    funcionarios_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Funcao
        fields = ['id', 'nome', 'ativo', 'funcionarios_count']
    
    def get_funcionarios_count(self, obj):
        """Retorna quantidade de funcionários ativos na função"""
        return obj.funcionarios.filter(ativo=True).count()
    
    def validate_nome(self, value):
        """Validação para nome único (case insensitive)"""
        instance = self.instance
        if Funcao.objects.filter(
            nome__iexact=value
        ).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError('Já existe uma função com este nome.')
        return value


class UnidadeSerializer(serializers.ModelSerializer):
    """
    Serializer para modelo Unidade
    """
    funcionarios_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Unidade
        fields = ['id', 'nome', 'ativo', 'funcionarios_count']
    
    def get_funcionarios_count(self, obj):
        """Retorna quantidade de funcionários ativos na unidade"""
        return obj.funcionarios.filter(ativo=True).count()
    
    def validate_nome(self, value):
        """Validação para nome único (case insensitive)"""
        instance = self.instance
        if Unidade.objects.filter(
            nome__iexact=value
        ).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError('Já existe uma unidade com este nome.')
        return value


class FuncionarioSerializer(serializers.ModelSerializer):
    """
    Serializer para modelo Funcionario - usado para CREATE/UPDATE
    """
    # Campos read-only para mostrar nomes dos relacionamentos
    departamento_nome = serializers.CharField(source='departamento.nome', read_only=True)
    funcao_nome = serializers.CharField(source='funcao.nome', read_only=True)
    unidade_nome = serializers.CharField(source='unidade.nome', read_only=True)
    
    class Meta:
        model = Funcionario
        fields = [
            'id', 'nome', 'ramal', 'email', 'whatsapp', 'teams', 'ativo',
            'departamento', 'departamento_nome',
            'funcao', 'funcao_nome',
            'unidade', 'unidade_nome'
        ]
    
    def validate_email(self, value):
        """Validação de email único se fornecido"""
        if value:
            instance = self.instance
            if Funcionario.objects.filter(
                email__iexact=value
            ).exclude(pk=instance.pk if instance else None).exists():
                raise serializers.ValidationError('Já existe um funcionário com este email.')
        return value
    
    def validate_ramal(self, value):
        """Validação de ramal único se fornecido"""
        if value:
            instance = self.instance
            if Funcionario.objects.filter(
                ramal=value
            ).exclude(pk=instance.pk if instance else None).exists():
                raise serializers.ValidationError('Já existe um funcionário com este ramal.')
        return value


class FuncionarioListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listagem de funcionários
    """
    departamento_nome = serializers.SerializerMethodField()
    funcao_nome = serializers.SerializerMethodField()
    unidade_nome = serializers.SerializerMethodField()
    
    class Meta:
        model = Funcionario
        fields = [
            'id', 'nome', 'ramal', 'email', 'whatsapp', 'teams',
            'departamento', 'departamento_nome',
            'funcao', 'funcao_nome', 
            'unidade', 'unidade_nome'
        ]
    
    def get_departamento_nome(self, obj):
        """Retorna o nome do departamento ou None"""
        return obj.departamento.nome if obj.departamento else None
    
    def get_funcao_nome(self, obj):
        """Retorna o nome da função ou None"""
        return obj.funcao.nome if obj.funcao else None
    
    def get_unidade_nome(self, obj):
        """Retorna o nome da unidade ou None"""
        return obj.unidade.nome if obj.unidade else None