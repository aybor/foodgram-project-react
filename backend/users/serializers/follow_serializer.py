from rest_framework import serializers

import api.serializers
from api.models import Recipe
# from api.serializers import MiniRecipeSerializer

from users.models import Follow


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        if isinstance(obj, tuple):
            obj = obj[0]
        return Follow.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        if isinstance(obj, tuple):
            obj = obj[0]
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return api.serializers.MiniRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        if isinstance(obj, tuple):
            obj = obj[0]
        return Recipe.objects.filter(author=obj.author).count()
