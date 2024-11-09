from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .serializers import GetNewsSerializer,CreateNewsSerializer
from news.models import News


@api_view(['GET'])
def get_news(request):
    try:
        objects = News.objects.all()
    except MainSiteText.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    serializer = GetNewsSerializer(objects, many = True)
    return Response (serializer.data)

@api_view(['POST'])
def create_news(request):
        serializer = CreateNewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)


@api_view(['GET','PUT','DELETE'])
def news_detail(request, slug):
    try:
        new = News.objects.get(slug=slug)
    except MainSiteText.DoesNotExist:
        return HttpResponse(status=HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = GetNewsSerializer(new)
        return Response(serializer.data)
    
    elif request.method == 'PUT':

        serializer = CreateNewsSerializer(new,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status =status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        new.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)