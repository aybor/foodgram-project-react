from rest_framework.viewsets import ModelViewSet

from api.serializers import RecipeSerializer
from api.models import Recipe
from api.paginators import CustomPageNumberPagination


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = CustomPageNumberPagination
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
