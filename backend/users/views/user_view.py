from django.contrib.auth import get_user_model
from djoser.views import UserViewSet

from api.paginators import CustomPageNumberPagination

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    pagination_class = CustomPageNumberPagination
