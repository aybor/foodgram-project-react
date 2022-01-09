from django.core import validators
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Ingredient(models.Model):

    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique ingredient'
            )
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    COLOR_CHOICES = [
        ('#DB4035', 'Красный'),
        ('#FAD000', 'Желтый'),
        ('#299438', 'Зелёный'),
        ('#4073FF', 'Синий'),
        ('#AF38EB', 'Фиолетовый'),
    ]
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Имя тега',
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        choices=COLOR_CHOICES,
        verbose_name='Цвет',
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='slug',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    image = models.ImageField(
        verbose_name='Фото',
        upload_to='recipes/',
        blank=False,
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmountForRecipe',
        related_name='recipes',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )
    cooking_time = models.PositiveIntegerField(
        validators=(
            validators.MinValueValidator(
                1,
                message='Время не меньше минуты'
            ),
        ),
        verbose_name='Время приготовления'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientAmountForRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    amount = models.PositiveIntegerField(
        validators=(
            validators.MinValueValidator(
                1,
                message='Минимальное количество: 1'
            ),
        )
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'ingredient',
                    'recipe',
                ],
                name='unique ingredient for recipe'
            )
        ]
