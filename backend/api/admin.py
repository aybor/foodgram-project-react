from django.contrib import admin
from django.forms import ModelForm
from django.forms.widgets import TextInput

from .models import (Cart,
                     Favorite,
                     Ingredient,
                     Recipe,
                     Tag,
                     IngredientAmountForRecipe,)


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)
    list_filter = ('measurement_unit',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    form = TagForm
    list_display = (
        'pk',
        'name',
        'color',
        'slug',
    )
    search_fields = (
        'name',
        'slug',
    )
    list_filter = (
        'color',
        'name',
        'slug',
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'author',
        'count_favorites',
        'slug',
    )
    search_fields = (
        'name',
        'author',
    )
    list_filter = ('tags',)

    def count_favorites(self, obj):
        return obj.favorites.count()

    count_favorites.short_description = 'Количество добавлений в избранное'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    search_fields = (
        'user',
        'recipe',
    )
    list_filter = ('user',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    search_fields = (
        'user',
        'recipe',
    )
    list_filter = ('user',)


@admin.register(IngredientAmountForRecipe)
class IngredientAmountForRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'ingredient',
        'recipe',
        'amount',
    )

    search_fields = (
        'ingredient',
        'recipe',
    )
