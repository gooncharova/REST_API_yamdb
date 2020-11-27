from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=40, unique=True, null=True)

    def __str__(self):
        return f'{self.pk} {self.name}'


class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=40, unique=True, null=True)

    def __str__(self):
        return f'{self.pk} {self.name}'


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField()
    description = models.TextField(null=True)
    genre = models.ManyToManyField(Genres)
    category = models.ForeignKey(
        Categories, on_delete=models.CASCADE, related_name='category')

    def __str__(self):
        return f'{self.pk} {self.name}'
