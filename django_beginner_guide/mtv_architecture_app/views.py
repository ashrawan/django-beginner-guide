from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from django.views.generic import ListView, DetailView
from .models import Book

# Create your views here.
def index(request):
    request_path = request.path
    html = """<p>Hello, We have some pages for books. <br/> 
    1) <a href="{}books/all"/>All Books</a>, <br/> 
    2) <a href="{}books/1"/>Book By Id</a>. 
    </p>""".format(request_path, request_path)
    return HttpResponse(html)

# Book List view
class BooksAllView(ListView):
    template_name = 'books.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        return Book.objects.all()

# Book detail view
class BookDetailView(DetailView):
    model = Book
    template_name = 'book-detail.html'