from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()

router.register('ingredients', views.IngredientsViewSet)
router.register('tags', views.TagViewSet)
router.register('recipes', views.RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
