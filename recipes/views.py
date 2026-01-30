# from django.shortcuts import render
import os

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render  # noqa: E501

from utils.pagination import make_pagination

from .models import Recipe

PER_PAGE = os.environ.get('PER_PAGE')


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    page_obj, pagination_obj = make_pagination(request, recipes, PER_PAGE)

    return render(
        request,
        'recipes/pages/home.html',
        context={
            'recipes': page_obj,
            'pagination_obj': pagination_obj,
        })


def category(request, category_id):
    rcps = Recipe.objects.filter(
        category__id=category_id,
        is_published=True,
    ).order_by('-id')

    recipes = get_list_or_404(rcps)
    page_obj, pagination_obj = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/category.html', context={
        'recipes': page_obj,
        'pagination_obj': pagination_obj,
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
    page_obj, pagination_obj = make_pagination(request, recipes, PER_PAGE)
    return render(
        request,
        'recipes/pages/search.html',
        context={
            'page_title': f'Search for "{search_item}" | ',
            'search_term': search_item,
            'recipes': page_obj,
            'pagination_obj': pagination_obj,
            'aditional_url_query': f'&q={search_item}'
        }
    )
