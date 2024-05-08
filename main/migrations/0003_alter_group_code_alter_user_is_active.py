# Generated by Django 5.0.4 on 2024-05-08 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_user_avatar_alter_user_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='code',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
    ]
