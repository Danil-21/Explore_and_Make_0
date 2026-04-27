from rest_framework.permissions import BasePermission


class TaskPermission(BasePermission):
    """
    Класс для проверки прав доступа к задачам
    """
    def has_object_permission(self, request, view, obj):
        """Проверка прав доступа к задаче"""
        user = request.user

        if obj.project.creator == user:
            return True
        
        if request.method in ['GET']:
            return True
        
        if obj.performer == user:
            if request.method in ['PUT', 'PATCH']:
                allowed_fields = ['status', 'priority']

                if set(request.data.keys()).issubset(allowed_fields):
                    return True
            
        if obj.author == user:
            if request.method in ['PUT', 'PATCH', 'DELETE']:
                return True
        
        return False
    

class ProjectPermission(BasePermission):
    """Класс для проверки прав доступа к проектам"""
    def has_object_permission(self, request, view, obj):
        """Проверка прав доступа к проекту"""
        if obj.creator == request.user:
            return True
        
        if request.method in ['GET']:
            return True
        
        return False
    
