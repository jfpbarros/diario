from django.urls import path
from .import views

urlpatterns = [
    path('',views.home, name='home'),
    path('escrever/', views.escrever, name='escrever'),
    path('cadastrar_pessoa/', views.cadastrar_pessoa, name='cadastrar_pessoa'),
    path('dia/', views.dia, name='dia'),
    path('excluir/dia', views.excluir_dia, name='excluir_dia'),
    path('manter_tag', views.manter_tag, name='manter_tag')
]
