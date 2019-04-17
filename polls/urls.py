from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.my_logout,name='logout'),
    path('login/', views.my_login,name='login'),
    path('index/', views.index,name='index'),
    path('detail/<id1>', views.detail,name='detail'),
    path('create/', views.create,name='create'),
    path('comment/', views.comment,name='comment'),
    path('change/', views.change_pass,name='change'),
    path('register/', views.my_register,name='register'),

]