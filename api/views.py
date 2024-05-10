from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import *
from rest_framework import status
from django.contrib.auth import authenticate, login, logout

from main import models
from . import serializers
from .peremisions import *


@api_view(['POST'])
def user_create(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    password_confirm = request.data.get('password_confirm')
    if password == password_confirm:
        user = models.User.objects.create_user(username=username, email=email, password=password)
        return Response({'user_create': 'success'})
    else:
        return Response({'user_create': 'fail'})


@api_view(["POST"])
def log_in(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return Response({'Login': 'success'})
    return Response({'Login': 'fail'})


@api_view(["POST"])
def log_out(request):
    logout(request)
    return Response('logut qilindi')


@api_view(["PUT"])
@authentication_classes([BasicAuthentication, SessionAuthentication, ])
@permission_classes([IsAuthenticated, IsOwner])
def user_update(request):
    user = request.user
    # Foydalanuvchining ma'lumotlarini o'zgartiramiz
    user.username = request.data.get('username', user.username)
    user.email = request.data.get('email', user.email)
    if request.data.get('first_name'):
        user.first_name = request.data.get('first_name', user.first_name)
    if request.data.get('last_name'):
        user.last_name = request.data.get('last_name', user.last_name)
    if request.data.get('phone'):
        user.phone = request.data.get('phone', user.phone)
    user.save()

    if request.data.get('image'):
        models.UserImage.objects.create(user=user, image=request.data.get('image'), selected=True)

    return Response({'user_update': 'success'}, status=status.HTTP_200_OK)


@api_view(['get'])
@authentication_classes([BasicAuthentication, SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_list(request):
    users = models.User.objects.all()
    serializer = serializers.UserListSerializers(users, many=True)
    return Response(serializer.data)


@api_view(['get'])
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def user_detail(request, pk):
    user = models.User.objects.get(pk=pk)
    serializer = serializers.UserDetailsSerializers(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated, IsOwner])
def user_image_list(request):
    user_images = models.UserImage.objects.filter(user=request.user)
    serializer = serializers.UserImageSerializers(user_images, many=True)
    return Response(serializer.data)


@api_view(['get', 'delete'])
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([IsOwner])
def user_image_delete(request, pk):
    try:
        user_image = models.UserImage.objects.get(pk=pk, user=request.user)
        user_image.delete()
        return Response({'user_image_delete': 'success'})
    except models.UserImage.DoesNotExist:
        return Response({'user_image_delete': 'fail'})


# -----------------Group--------------------------------
@api_view(['POST', 'GET'])
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated, ])
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
        author=request.user,
    )

    return Response({
        'created': True
    })


@api_view(['get'])
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def group_list(request):
    user_group = models.GroupUsers.objects.filter(user=request.user)
    groups = [group_user.group for group_user in user_group]
    serializer = serializers.GroupListSerializers(groups, many=True)
    return Response(serializer.data)


@api_view(['get'])
@authentication_classes([BasicAuthentication, SessionAuthentication])
def group_detail(request, code):
    group = models.Group.objects.get(code=code)
    serializer = serializers.GroupDetailSerializer(group, many=False)
    return Response(serializer.data)


@api_view(['put'])
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([IsGroupOwner])
def group_update(request, code):
    group = models.Group.objects.get(code=code)
    if group.author == request.user:
        group.name = request.data.get('name', group.name)
        group.avatar = request.data.get('avatar', group.avatar)
        group.description = request.data.get('description', group.description)
        group.save()
        return Response({'group_update': 'success'})
    else:
        return Response({'group_update': 'fail'})


class GroupDelete(generics.DestroyAPIView):
    queryset = models.Group.objects.all()
    serializer_class = serializers.GroupDetailSerializer
    lookup_field = 'code'
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsGroupOwner]
    lookup_url_kwarg = 'code'


# -----------------JoinRequest--------------------------------
@api_view(['post'])
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def join_request_create(request):
    group = models.Group.objects.get(code=request.data.get('code'))
    user = request.user
    models.GroupJoinedRequest.objects.create(group=group, user=user, status=1)
    return Response({'join_request_create': 'success'})


@api_view(['get'])
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([IsGroupAdmins])
def join_request_list(request, code):
    group = models.Group.objects.get(code=code)
    join_requests = models.GroupJoinedRequest.objects.filter(group=group)
    serializer = serializers.JoinRequestListSerializer(join_requests, many=True)
    return Response(serializer.data)



# -----------------Message--------------------------------
