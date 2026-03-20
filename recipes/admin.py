from django.contrib import admin  # type: ignore

from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'author', 'is_published'
    list_display_links = 'id',
    list_editable = 'is_published',
    ordering = '-id',
    prepopulated_fields = {
        'slug': ('title',)
    }
    list_per_page = 8
    list_filter = 'category', 'author', 'is_published', 'preparation_steps_is_html'  # noqa: E501
    search_fields = 'title', 'description', 'slug', 'preparation_steps'
