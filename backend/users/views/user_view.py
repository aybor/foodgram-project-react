from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from djoser.views import UserViewSet

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.paginators import CustomPageNumberPagination
from users.serializers import FollowSerializer
from users.models import Follow

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    pagination_class = CustomPageNumberPagination

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, pk=id)
        if request.method == 'POST':
            if user == author:
                return Response(
                    {
                        'errors': 'Нельзя подписаться на самого себя'
                    }
                )
            follow = Follow.objects.get_or_create(user=user, author=author)
            serializer = FollowSerializer(
                follow, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            follow = Follow.objects.filter(user=user, author=author)
            if follow.exists():
                follow.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {
                    'errors': 'Такой подписки нет'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user
        queryset = user.follower.all()
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
