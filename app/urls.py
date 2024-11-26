from django.urls import path
from . import views

urlpatterns = [
    path('', views.buscar_ponto_form, name='home'),
    path('buscar/', views.buscar_ponto_form, name='buscar_ponto_form'),
    path('ponto/<str:id_colaborador>/', views.buscar_ponto, name='buscar_ponto'),
]