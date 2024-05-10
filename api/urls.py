from django.urls import path
from . import views

urlpatterns = [
    path('user-detail/<str:pk>/', views.user_detail),
    path('user-list/', views.user_list),
    path('user-register/', views.user_create),
    path('log-in/', views.log_in),
    path('user-update/', views.user_update),

    path('user-image/list/', views.user_image_list),
    path('user-image/delete/<str:pk>/', views.user_image_delete),

    path('group-create/', views.group_create),
    path('group-list/', views.group_list),
    path('group-update/<str:code>/', views.group_update),
    path('group-detail/<str:code>/', views.group_detail),
    path('group-delete/<str:code>/', views.GroupDelete.as_view()),
    # path('group-user-delete/<int:id>/', views.GroupUsersDelete.as_view())

    path('join-request-create/', views.join_request_create),
    path('join-request-list/<str:code>/', views.join_request_list),
]
