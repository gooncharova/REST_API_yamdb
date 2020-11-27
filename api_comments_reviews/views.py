from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ValidationError

from api_comments_reviews.models import Review
from api_comments_reviews.permissions import HasPermissionsOrReadOnly
from api_comments_reviews.serializers import CommentSerializer, ReviewSerializer
from api_titles_genres_categories.models import Titles


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          HasPermissionsOrReadOnly)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'],
                                   title_id=self.kwargs['title_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        get_object_or_404(Review, id=self.kwargs['review_id'])
        get_object_or_404(Titles, id=self.kwargs['title_id'])
        return serializer.save(author=self.request.user,
                               review_id=self.kwargs['review_id'],)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          HasPermissionsOrReadOnly)
    ordering = ['pub_date']

    def get_queryset(self):
        title = get_object_or_404(Titles, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, id=self.kwargs['title_id'])
        if title.reviews.filter(author=self.request.user).exists():
            raise ValidationError("You can't review same title twice")
        return serializer.save(author=self.request.user,
                               title=title)
