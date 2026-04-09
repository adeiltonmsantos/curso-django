# from django.shortcuts import render
import os

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render  # noqa: E501
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
class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


# Class Based View for Category
class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id'),
            is_published=True,
        ).order_by('-id')

        if not qs:
            raise Http404

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        recipes = ctx.get('recipes')

        ctx.update(
            {
                'title': f'{recipes[0].category.name} - Category | '
            }
        )

        return ctx


# Class Based View for Search
class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        search_item = self.request.GET.get('q', '').strip()

        if not search_item:
            raise Http404()

        qs = Recipe.objects.filter(
            Q(
                Q(title__icontains=search_item) |
                Q(description__icontains=search_item)
            ),
            is_published=True
        ).order_by('title')

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        search_item = self.request.GET.get('q', '').strip()

        ctx.update(
            {
                'page_title': f'Search for "{search_item}" | ',
                'search_term': search_item,
                'aditional_url_query': f'&q={search_item}'
            }
        )

        return ctx


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)

    return render(
        request,
        'recipes/pages/recipe-view.html',
        context={
            'recipe': recipe,
            'is_detail_page': True,
        })
