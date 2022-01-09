from django.db import models


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
