from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import IngredientSerializer
from api.filters import IngredientSearchFilter
from api.models import Ingredient


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
