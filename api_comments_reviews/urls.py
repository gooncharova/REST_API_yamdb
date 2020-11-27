from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api_comments_reviews.views import CommentViewSet, ReviewViewSet

v1_router = DefaultRouter()
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    viewset=ReviewViewSet, basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    viewset=CommentViewSet, basename='comments'
)


urlpatterns = [
    path('v1/', include(v1_router.urls)),
]