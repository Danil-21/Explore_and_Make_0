from rest_framework import serializers
from .models import User, Project, Task


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User"""
    class Meta:
        """Модель и поля для сериализации"""
        model = User
        fields = ['id', 'username', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""
    class Meta:
        """Модель и поля для сериализации"""
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def create(self, validated_data):
        """Создание пользователя"""
        user = User.objects.create_user(**validated_data)
        return user


class ProjectSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Project"""
    creator = UserSerializer(read_only=True)

    class Meta:
        """Модель и поля для сериализации"""
        model = Project
        fields = ['id', 'name', 'description', 'creator', 'members', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Task"""
    author = UserSerializer(read_only=True)

    class Meta:
        """Модель и поля для сериализации"""
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'deadline',
            'project',
            'author',
            'performer',
            'created_at',
        ]

    def validate(self, data):
        """
        Проверка, что исполнитель является участником проекта

        params:
            data (dict): Данные для валидации

        returns:
            dict: Валидированные данные
        """
        project = data.get('project') # or self.instance.project
        performer = data.get('performer')

        if performer not in project.members.all():
            raise serializers.ValidationError("Исполнитель должен быть участником проекта.")
        
        return data
    
