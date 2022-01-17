from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.serializers import RecipeSerializer, MiniRecipeSerializer
from api.models import Recipe, Favorite, Cart
from api.paginators import CustomPageNumberPagination
from api.filters import RecipeFilter
from api.permissions import AuthorOrReadOnly


class RecipeViewSet(ModelViewSet):
    permission_classes = (AuthorOrReadOnly,)
    queryset = Recipe.objects.all()
    pagination_class = CustomPageNumberPagination
    filter_class = RecipeFilter
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        return self.do_action(request=request, model=Favorite, pk=pk)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        return self.do_action(request=request, model=Cart, pk=pk)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = user.carts.values(
            'recipe__ingredients__name',
            'recipe__ingredients__measurement_unit',
        ).order_by('recipe__ingredients__name').annotate(
            ingredients_sum=Sum('recipe__ingredientamountforrecipe__amount')
        )

        list_for_shopping = ''
        for item in ingredients:
            name = item['recipe__ingredients__name']
            amount = (
                    str(item['ingredients_sum']) +
                    ' ' +
                    item['recipe__ingredients__measurement_unit']
            )
            list_for_shopping += f'{name}: {amount}\n'

        return HttpResponse(list_for_shopping, content_type='text/plain')

    def create_bond(self, model, user, recipe):
        if model.objects.filter(user=user, recipe=recipe).exists():
            return Response({
                'errors': 'Рецепт уже добавлен'
            }, status=status.HTTP_400_BAD_REQUEST)
        model.objects.create(user=user, recipe=recipe)
        serializer = MiniRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_bond(self, model, user, recipe):
        bond = model.objects.filter(user=user, recipe=recipe)
        if bond.exists():
            bond.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'Рецепт уже удалён'
        }, status=status.HTTP_400_BAD_REQUEST)

    def do_action(self, request, model, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'POST':
            return self.create_bond(model=model, user=user, recipe=recipe)
        elif request.method == 'DELETE':
            return self.delete_bond(model=model, user=user, recipe=recipe)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
