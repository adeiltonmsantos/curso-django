from django.contrib import admin  # type: ignore

from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'is_published'
    list_display_links = 'id',
    search_fields = 'title', 'description', 'slug', 'preparation_steps'
