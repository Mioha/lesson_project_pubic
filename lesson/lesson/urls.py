"""lesson URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import LessonAllViewSet, LessonListViewSet, IsAdminViewSet, \
    ProfileViewSet, \
    LessonLogViewSet, CreateUserView, \
    StartLessonViewSet, CompleteLessonViewSet, ReviewListViewSet, \
    ApproveRejectViewSet, LessonDetailViewSet, \
    LessonDetailAdminViewSet, NewLessonViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/register/', CreateUserView.as_view(), name='register'),
    path('api/v1/login/', obtain_auth_token, name='login'),
    path('api/v1/users/me/', IsAdminViewSet.as_view(), name='is_admin'),
    path('api/v1/lessonlogs/', LessonLogViewSet.as_view(), name='lessonlog'),
    path('api/v1/users/me/lessonlogs/', ProfileViewSet.as_view(),
         name='profile'),
    path('api/v1/lessons/', LessonAllViewSet.as_view(), name='lessons_all'),
    path('api/v1/users/me/lessons/', LessonListViewSet.as_view(),
         name='lessons'),
    path('api/v1/users/me/lessons/<int:lesson_id>',
         LessonDetailViewSet.as_view(),
         name='lesson_detail'),
    path('api/v1/lessons_admin/', NewLessonViewSet.as_view(),
         name='lesson_new'),
    path('api/v1/lessons_admin/<int:lesson_id>',
         LessonDetailAdminViewSet.as_view(), name='lessons_admin'),
    path('api/v1/lessons/<int:lesson_id>/start/', StartLessonViewSet.as_view(),
         name='start'),
    path('api/v1/lessons/<int:lesson_id>/comp/',
         CompleteLessonViewSet.as_view(), name='comp'),
    path('api/v1/lessonlogs/under_review/', ReviewListViewSet.as_view(),
         name='review'),
    path('api/v1/lessonlogs/<str:change_status>',
         ApproveRejectViewSet.as_view(), name='approve_reject'),
]
