from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import IngredientSerializer
from api.filters import IngredientSearchFilter
from api.models import Ingredient
from api.permissions import AdminOrReadOnly


class IngredientsViewSet(ReadOnlyModelViewSet):
    permission_classes = (AdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
