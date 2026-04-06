# from django.shortcuts import render
import os

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render  # noqa: E501
from django.views.generic import ListView

from utils.pagination import make_pagination

from .models import Recipe

per_page = int(os.environ.get('PER_PAGE', 2))
PER_PAGE = int(os.environ.get('PER_PAGE', 2))


# Base class for home, category and search templates
class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE
        )
        ctx.update(
            {
                'recipes': page_obj,
                'pagination_range': pagination_range
            }
        )

        return ctx


# Class Based View for Home
class RecipeListViewBaseHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        category_id = self.kwargs['category_id']
        qs = qs.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id')

        return get_list_or_404(qs)

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        recipes = ctx.get('recipes')

        ctx.update(
            {
                'title': f'{recipes[0].category.name} - Category | '
            }
        )

        return ctx


# def home(request):
#     recipes = Recipe.objects.filter(is_published=True).order_by('-id')
#     page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)
#     return render(
#         request,
#         'recipes/pages/home.html',
#         context={
#             'recipes': page_obj,
#             'pagination_range': pagination_range,
#         })


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
