from rest_framework.serializers import ModelSerializer
from main import models


class UserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'
        # exclude = ['password']


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', ]
        extra_kwargs = {'password': {'write_only': False}}


class UserListSerializers(ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'username', 'first_name', 'is_active']


class UserDetailsSerializers(ModelSerializer):
    class Meta:
        model = models.User
        exclude = ['password', 'groups', 'user_permissions']


class UserImageSerializers(ModelSerializer):
    class Meta:
        model = models.UserImage
        fields = '__all__'


class GroupUserListSerializers(ModelSerializer):
    user = UserListSerializers()

    class Meta:
        model = models.GroupUsers
        fields = ['id', 'is_admin', 'joined_at', 'group', 'user']


class GroupListSerializers(ModelSerializer):
    class Meta:
        model = models.Group
        fields = ['id', 'code', 'name', 'avatar']
        depth = 2


class GroupDetailSerializer(ModelSerializer):
    group_users = GroupUserListSerializers(many=True)

    class Meta:
        model = models.Group
        fields = ['id', 'code', 'name', 'avatar', 'description', 'author', 'group_users']


class JoinRequestListSerializer(ModelSerializer):
    user = UserListSerializers()
    group = GroupListSerializers()
    class Meta:
        model = models.GroupJoinedRequest
        fields = ['id', 'status', 'group', 'user']
        depth = 2
