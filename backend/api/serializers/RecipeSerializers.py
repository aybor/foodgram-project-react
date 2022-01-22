from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from api.models import Ingredient, IngredientAmountForRecipe, Recipe
from api.serializers import IngredientAmountForRecipeSerializer, TagSerializer
from users.serializers import CustomUserSerializer


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientAmountForRecipeSerializer(
        source='ingredientamountforrecipe_set',
        many=True,
        read_only=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Recipe.objects.filter(
                favorites__user=user,
                id=obj.id
            ).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Recipe.objects.filter(carts__user=user, id=obj.id).exists()
        return False

    def validate(self, data):

        self.check_required_field('ingredients')
        self.check_required_field('tags')

        ingredients = self.initial_data.get('ingredients')
        ingredient_list = []
        for ingredient in ingredients:
            ingredient_item = get_object_or_404(
                Ingredient,
                id=ingredient['id']
            )
            if ingredient_item in ingredient_list:
                raise serializers.ValidationError(
                    {'ingredients': 'Указаны повторяющиеся ингредиенты'}
                )
            ingredient_list.append(ingredient_item)
            if int(ingredient['amount']) < 0:
                raise serializers.ValidationError(
                    {'ingredients': 'Количество должно быть положительным'}
                )
        data['ingredients'] = ingredients
        return data

    def check_required_field(self, field):
        checking_field = self.initial_data.get(field)
        if not checking_field:
            raise serializers.ValidationError(
                {
                    field: 'This field is required.'
                }
            )

    def create_ingredients(self, ingredients, recipe):
        ingredients_list = []
        for ingredient in ingredients:
            ingredients_list.append(
                IngredientAmountForRecipe(
                    recipe=recipe,
                    ingredient_id=ingredient.get('id'),
                    amount=ingredient.get('amount')
                )
            )
        IngredientAmountForRecipe.objects.bulk_create(ingredients_list)

    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(image=image, **validated_data)
        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        self.create_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        IngredientAmountForRecipe.objects.filter(
            recipe=instance
        ).all().delete()
        self.create_ingredients(validated_data.get('ingredients'), instance)
        instance.save()
        return instance


class MiniRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')
