from rest_framework.viewsets import ReadOnlyModelViewSet

from api.models import Tag
from api.permissions import AdminOrReadOnly
from api.serializers import TagSerializer


class TagViewSet(ReadOnlyModelViewSet):
    permission_classes = (AdminOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
