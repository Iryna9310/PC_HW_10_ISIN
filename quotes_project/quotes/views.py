from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import AuthorForm, QuoteForm
from .models import Author, Quote

def home(request):
    return HttpResponse("Hello, world!")

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Автор успішно доданий!')  # Повідомлення про успішне додавання
            return redirect('home')  # Перенаправлення на домашню сторінку після додавання
    else:
        form = AuthorForm()
    return render(request, 'add_author.html', {'form': form})

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Цитата успішно додана!')  # Повідомлення про успішне додавання
            return redirect('home')  # Перенаправлення на домашню сторінку після додавання
    else:
        form = QuoteForm()
    return render(request, 'add_quote.html', {'form': form})