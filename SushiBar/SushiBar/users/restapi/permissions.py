from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import status
from rest_framework.response import Response
from users.models import CustomUser
class IsOwnerOrReadOnly(BasePermission):
    message = 'Musisz byc zalogowany na to konto, by wyświetlić'
    
    def has_object_permission(self,request,view,obj):
        return obj == request.user
