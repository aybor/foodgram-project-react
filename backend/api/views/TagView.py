from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import TagSerializer
from api.models import Tag


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
