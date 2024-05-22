from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('author/<int:pk>/', views.author_detail, name='author_detail'),  # Залиште цей шлях
    path('quotes/', views.all_quotes, name='all_quotes'),
    path('accounts/', include('allauth.urls')),
]
