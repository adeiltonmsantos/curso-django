# from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render  # noqa: E501

from .models import Recipe


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    current_page = request.GET.get('page', 1)
    paginator = Paginator(recipes, 9)
    page = paginator.get_page(current_page)

    return render(
        request,
        'recipes/pages/home.html',
        context={
            'recipes': page
        })


def category(request, category_id):
    rcps = Recipe.objects.filter(
        category__id=category_id,
        is_published=True,
    ).order_by('-id')

    recipes = get_list_or_404(rcps)

    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'{recipes[0].category.name} - Category | '
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)

    return render(
        request,
        'recipes/pages/recipe-view.html',
        context={
            'recipe': recipe,
            'is_detail_page': True,
        })


def search(request):
    search_item = request.GET.get('q', '').strip()
    if not search_item:
        raise Http404()
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_item) |
            Q(description__icontains=search_item)
        ),
        is_published=True
    ).order_by('title')
    return render(
        request,
        'recipes/pages/search.html',
        context={
            'page_title': f'Search for "{search_item}" | ',
            'search_term': search_item,
            'recipes': recipes
        }
    )
