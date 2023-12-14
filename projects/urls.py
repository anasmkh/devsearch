from django.urls import path
from projects import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('project/<str:pk>/', views.project, name='project'),
    path('creatproject/', views.creatproject, name='project-form'),
    path('updateproject/<str:pk>/', views.updateproject, name='update-project'),
    path('deleteproject/<str:pk>/', views.deleteproject,name='delete-project')
]
