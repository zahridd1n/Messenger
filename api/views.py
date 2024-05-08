from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import *
from django.contrib.auth import authenticate

from main import models
from . import serializers


@api_view(['POST'])
def user_register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    user = models.User.objects.create_user(username=username, email=email, password=password)
    token = Token.objects.create(user=user)
    return Response({'token': token.key})


@api_view(["POST"])
def log_in(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response


@api_view(["POST"])
def log_out(request):
    token = Token.objects.get(user=request.user).delete()
    return Response('logut qilindi')


@api_view(['get'])
@authentication_classes([BasicAuthentication, SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_list(request):
    users = models.User.objects.all()
    serializer = serializers.UserListSerializers(users, many=True)
    return Response(serializer.data)


@api_view(['get'])
@authentication_classes([BasicAuthentication, SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_detail(request, pk):
    user = models.User.objects.get(pk=pk)
    serializer = serializers.UserDetailsSerializers(user, many=False)
    return Response(serializer.data)


# -----------------Group--------------------------------
@authentication_classes([BasicAuthentication, SessionAuthentication , TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def group_create(request):
    name = request.data.get('name')
    avatar = request.data.get('avatar')
    description = ''
    if request.data.get('description'):
        description = request.data.get('description')

    group = models.Group.objects.create(
        name=name,
        avatar=avatar,
        description=description,
    )

    models.GroupUsers.objects.create(
        user=request.user,
        group=group,
        is_admin=True,
    )
    return Response({
        'data': True
    })


@api_view(['get'])
@authentication_classes([BasicAuthentication, SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def group_list(request):
    user_group = models.GroupUsers.objects.filter(user=request.user)
    groups = [group_user.group for group_user in user_group]
    serializer = serializers.GroupListSerializers(groups, many=True)
    return Response(serializer.data)
