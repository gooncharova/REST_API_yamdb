from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Categories, Genres, Titles


class CategoriesSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=50, validators=[UniqueValidator(
            queryset=Categories.objects.all())])

    class Meta:
        exclude = ('id', )
        lookup_field = 'slug'
        model = Categories


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id', )
        lookup_field = 'slug'
        model = Genres


class TitlesReadSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Titles


class TitlesWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(), slug_field='slug')
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(), slug_field='slug', many=True)

    class Meta:
        fields = '__all__'
        model = Titles
