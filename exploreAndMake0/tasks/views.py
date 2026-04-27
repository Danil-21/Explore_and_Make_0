from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView, Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from tasks.permissions import ProjectPermission, TaskPermission
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer, RegisterSerializer
from django_filters.rest_framework import DjangoFilterBackend


class RegisterView(APIView):
    """
    Предоставляет операцию регистрации пользователя
    """
    permission_classes = []

    def post(self, request):
        """
        Обработка POST запроса для регистрации нового пользователя
        """
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Create your views here.
class ProjectViewSet(ModelViewSet):
    """
    ViewSet для модели Project
    Предоставляет опереции для проектов
    """
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectPermission]

    def get_queryset(self):
        """
        Какие объекты доступны текущему пользователю
        Пользователь видит только проекты, в которых он является участником

        returns:
            QuerySet: отфильтрованный список проектов
        """
        return Project.objects.filter(members=self.request.user)
    

    def perform_create(self, serializer):
        """
        Создание проекта и назначение текущего пользователя
        его создателем и участником
        """
        project = serializer.save(creator=self.request.user)
        project.members.add(self.request.user)

    
class TaskViewSet(ModelViewSet):
    """
    ViewSet для модели Task
    Предоставляет операции для задач
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, TaskPermission]
    # pagination_class = PageNumberPagination

    filter_backends = [DjangoFilterBackend]
    
    filterset_fields = [
        'project',
        'status',
        'priority',
        'performer',
        'deadline',
    ]

    def get_queryset(self):
        """
        Какие объекты доступны текущему пользователю
        Видит только задачи, которые ему назначены
        """
        return Task.objects.filter(project__members=self.request.user)
    

    def perform_create(self, serializer):
        """
        Создание задачи и назначение текущего пользователя
        ее автором
        """
        serializer.save(author=self.request.user)