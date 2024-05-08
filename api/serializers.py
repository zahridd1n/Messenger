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
        fields = ['username', 'password', 'first_name', 'last_name', 'avatar', 'email', ]
        extra_kwargs = {'password': {'write_only': False}}


class UserListSerializers(ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'username', 'last_name', 'avatar', 'is_active']


class UserDetailsSerializers(ModelSerializer):
    class Meta:
        model = models.User
        exclude = ['password', 'groups', 'user_permissions']


class GroupListSerializers(ModelSerializer):
    class Meta:
        model = models.Group
        fields = ['id', 'code', 'name', 'avatar']


class GroupDetailSerializer(ModelSerializer):
    class Meta:
        model = models.Group
        fields = '__all__'
