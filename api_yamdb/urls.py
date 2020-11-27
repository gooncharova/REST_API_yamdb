from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

import api_users.urls,\
    api_comments_reviews.urls,\
    api_titles_genres_categories.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('redoc/', TemplateView.as_view(template_name='redoc.html'), name='redoc'),
    path('api/', include(api_users.urls)),
    path('api/', include(api_comments_reviews.urls)),
    path('api/', include(api_titles_genres_categories.urls)),
    path('auth/', include('django.contrib.auth.urls')),
]

