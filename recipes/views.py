# from django.shortcuts import render
from django.shortcuts import render  # type: ignore


def home(request):
    return render(request, 'recipes/pages/home.html')


def recipe(request):
    return render(request, 'recipes/pages/recipe-view.html')
