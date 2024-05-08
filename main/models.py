from django.db import models
from django.contrib.auth.models import AbstractUser

import random, string


class CodeGenerate(models.Model):
    code = models.CharField(max_length=25, blank=True, null=True)

    @staticmethod
    def generate_code():
        return ''.join(random.sample(string.ascii_uppercase + string.digits, 22))

    def save(self, *args, **kwargs):
        if not self.id:
            while True:
                code = self.generate_code()
                if not self.__class__.objects.filter(code=code):
                    self.code = code
                    break
        super(CodeGenerate, self).save(*args, **kwargs)

    class Meta:
        abstract = True

    def __str__(self):
        return self.code


class User(AbstractUser):
    avatar = models.ImageField(upload_to='user/avatar', blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

    def user_groups(self):
        return GroupUsers.objects.filter(user=self)

    def __str__(self):
        return self.username


class Group(CodeGenerate):
    name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='group/avatar')
    description = models.TextField(null=True, blank=True)

    @property
    def group_users(self):
        return GroupUsers.objects.filter(group=self)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Group'


class GroupUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    #
    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.is_admin = True
    #     super(GroupUsers, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} - {self.group}'


class GroupAddRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    joined = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.group} - {self.joined}'


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.group} - {self.text}'
