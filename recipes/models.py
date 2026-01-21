from django.contrib.auth.models import User  # type: ignore
from django.db import models  # type: ignore


class Category(models.Model):
    name = models.CharField(max_length=65)  # type: ignore

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=65)  # type: ignore
    description = models.CharField(max_length=165)  # type: ignore
    slug = models.SlugField()  # type: ignore
    preparation_time = models.IntegerField()  # type: ignore
    preparation_time_unit = models.CharField(max_length=65)  # type: ignore
    servings = models.IntegerField()  # type: ignore
    servings_unit = models.CharField(max_length=65)  # type: ignore
    preparation_steps = models.TextField()  # type: ignore
    preparation_steps_is_html = models.BooleanField(
        default=False)  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)  # type: ignore
    updated_at = models.DateTimeField(auto_now=True)  # type: ignore
    is_published = models.BooleanField(default=False)  # type: ignore
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )   # type: ignore
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )   # type: ignore

    def __str__(self):
        return self.title
