from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .permissions import IsOwnerOrReadOnly

from users.models import CustomUser
from .serializers import CustomUserSerializer, CreateCustomUserSerializer, MyTokenObtainPairSerializer


@api_view(['POST',])
def register_view(request):
    serializer = CreateCustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)


@api_view(['GET',])
@permission_classes([IsAdminUser])
def account_list_view(request):
    try:
        objects = CustomUser.objects.all()
    except CustomUser.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    serializer = CustomUserSerializer(objects, many = True)
    return Response (serializer.data)

@api_view(['GET','PUT','DELETE'])
@permission_classes([IsOwnerOrReadOnly])
def user_detail_view(request, id):
    try:
        user = CustomUser.objects.get(id=id)
    except CustomUser.DoesNotExist:
        return HttpResponse(status=HTTP_404_NOT_FOUND)
    
    if request.user == user:

        if request.method == 'GET':
            serializer = CustomUserSerializer(user)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = CustomUserSerializer(user,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status =status.HTTP_400_BAD_REQUEST)
            
        elif request.method == "DELETE":
            user.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
    else:
        return Response("Brak uprawnień. Musisz byc zalogowany na tę konto.", status =status.HTTP_204_NO_CONTENT)



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer