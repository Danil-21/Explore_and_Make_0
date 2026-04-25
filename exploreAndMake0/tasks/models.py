from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    pass


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_projects'
    )

    members = models.ManyToManyField(
        User,
        related_name='projects'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Task(models.Model):

    # status = models.CharField(max_length=50)
    # priority = models.CharField(max_length=50)
    class Status(models.TextChoices):
        TODO = 'Сделать', 'сделать'
        IN_PROGRESS = 'В процессе', 'в процессе'
        DONE = 'Готово', 'готово'


    class Priority(models.TextChoices):
        LOW = 'Низкий', 'низкий'
        MEDIUM = 'Средний', 'средний'
        HIGH = 'Высокий', 'высокий'

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.TODO
    )

    priority = models.CharField(
        max_length=50,
        choices=Priority.choices,
        # default=Priority.LOW
    )

    deadline = models.DateTimeField(null=True, blank=True)

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_tasks'
    )

    performer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='performed_tasks'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title