from django.urls import path
from users import views

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('', views.profiles, name='profiles'),
    path('userprofile/<str:pk>/', views.userProfile, name='user-profile'),
    path('account/',views.userAccount,name='account'),
    path('updateProfile/',views.updateProfile,name='update_profile'),
    path('createSkill/',views.createSkill,name='create-skill'),
    path('deleteSkill/<str:pk>/',views.deleteSkill,name='delete-skill'),
    path('updateSkill/<str:pk>/',views.updateSkill,name='update-skill'),
]
