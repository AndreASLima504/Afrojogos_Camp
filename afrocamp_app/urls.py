from django.urls import path
from afrocamp_app import views

urlpatterns = [
    path('login/', views.login)
]