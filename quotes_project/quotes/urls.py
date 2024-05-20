# quotes/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Базовий маршрут для додатку quotes
    path('add_author/', views.add_author, name='add_author'),  # Шлях для сторінки додавання автора
    path('add_quote/', views.add_quote, name='add_quote'),  # Шлях для сторінки додавання цитати
]