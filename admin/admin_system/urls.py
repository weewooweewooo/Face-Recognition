from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('documentation/', views.documentation, name='documentation'),
]
