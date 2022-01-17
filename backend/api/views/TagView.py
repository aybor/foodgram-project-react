from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import TagSerializer
from api.models import Tag
from api.permissions import AdminOrReadOnly


class TagViewSet(ReadOnlyModelViewSet):
    permission_classes = (AdminOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
