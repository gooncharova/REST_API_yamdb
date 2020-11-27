from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly

from .filters import TitlesFilter
from .models import Categories, Genres, Titles
from .permissions import IsAdminUserOrReadOnly
from .serializers import (CategoriesSerializer, GenresSerializer,
                          TitlesReadSerializer, TitlesWriteSerializer)


class CategoriesViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminUserOrReadOnly, )
    filter_backends = [SearchFilter]
    search_fields = ['=name', ]
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class GenresViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminUserOrReadOnly, )
    filter_backends = [SearchFilter]
    search_fields = ['=name', ]
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminUserOrReadOnly, )
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter
    filterset_fields = ['name', ]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitlesReadSerializer
        return TitlesWriteSerializer
