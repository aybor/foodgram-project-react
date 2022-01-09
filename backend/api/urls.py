from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()

router.register('ingredients', views.IngredientsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
