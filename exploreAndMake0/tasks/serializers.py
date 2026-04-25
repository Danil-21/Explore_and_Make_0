from rest_framework import serializers
from .models import User, Project, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ProjectSerializer(serializers.ModelSerializer):

    creator = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'creator', 'members', 'created_at']


class TaskSerializer(serializers.ModelSerializer):

    author = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fielad = [
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
        project = data.get('project') # or self.instance.project
        performer = data.get('performer')

        if performer not in project.members.all():
            raise serializers.ValidationError("Исполнитель должен быть участником проекта.")
        
        return data
    
