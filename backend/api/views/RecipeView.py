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


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = CustomPageNumberPagination
    filter_class = RecipeFilter
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
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

    def create_bond(self, model, user, recipe):
        model.objects.get_or_create(user=user, recipe=recipe)
        serializer = MiniRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_bond(self, model, user, recipe):
        bond = model.objects.filter(user=user, recipe=recipe)
        if bond.exists():
            bond.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {
                "detail": "Объект уже удалён"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def do_action(self, request, model, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'POST':
            return self.create_bond(model=model, user=user, recipe=recipe)
        elif request.method == 'DELETE':
            return self.delete_bond(model=model, user=user, recipe=recipe)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
