from django.urls import path, include
from rest_framework import routers

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/all', views.BooksAllView.as_view(), name='books'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
]
