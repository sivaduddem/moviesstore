#urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='petitions.index'),
    path('create/', views.create, name='petitions.create'),
    path('<int:petition_id>/', views.show, name='petitions.show'),
    path('<int:petition_id>/vote/', views.vote, name='petitions.vote'),
]
