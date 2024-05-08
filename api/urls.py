from django.urls import path
from . import views

urlpatterns = [
    path('user-detail/<str:pk>/', views.user_detail),
    path('user-list/', views.user_list),
    path('user-register/', views.user_register),
    path('log-in/', views.log_in),
    # path('user-update/<str:pk>/',views.user_update),
    # path('user-delete/<str:pk>/',views.user_delete),
    # path('user-login/',views.user_login),
    path('group-create/', views.group_create),
    path('', views.group_list),
]
