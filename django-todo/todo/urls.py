from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.create_task, name='create_task'),
    path('update/<int:pk>/', views.update_task, name='update_task'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('categories/', views.manage_categories, name='manage_categories'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),
    path('tags/', views.manage_tags, name='manage_tags'),
    path('tags/delete/<int:pk>/', views.delete_tag, name='delete_tag'),
    path('register/', views.register, name='register'),
]