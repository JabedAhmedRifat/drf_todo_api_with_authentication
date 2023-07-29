from django.shortcuts import render
from rest_framework.response import Response
from .serializers import TaskSerializer
from .models import Task
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from knox.auth import TokenAuthentication
from rest_framework import generics
from knox.models import AuthToken
from knox.settings import CONSTANTS



# Create your views here.

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List' : '/task-list/',
        'Detail View' : '/task-detail/<str:pk>/',
        'Create' : '/task-create/',
        'Update' : '/task-update/<str:pk>/',
        'Delete' : '/task-delete/<str:pk>/',
    }
    return Response(api_urls)


def get_user_from_token(token):
    objs = AuthToken.objects.filter(token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH])
    if len(objs) == 0:
        return None
    return objs.first().user


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def taskList(request):
    # token  =request.auth
    # if not token:
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)
    # user = get_user_from_token(request.auth.token)
    # if not user:
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)

    tasks = Task.objects.filter(user=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)




@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def taskDetail(request, pk):
    tasks = Task.objects.get(id=pk)
    serializer = TaskSerializer(tasks, many = False)
    return Response(serializer.data)



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def taskCreate(request):
    if request.method == 'POST':
        data = {
            'user': request.user.id,
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'completed': request.data.get('completed', False),
            'deadline': request.data.get('deadline'),
            'priority': request.data.get('priority'),
        }
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def taskUpdate(request, pk):
    task = Task.objects.get(id = int(pk))
    serializer = TaskSerializer(instance=task, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
def taskDelete(request, pk):
    task = Task.objects.get(id = pk )
    task.delete()
    return Response("Task deleted successfully.")

