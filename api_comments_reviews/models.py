from django.contrib.auth import get_user_model
from django.db import models

from api_titles_genres_categories.models import Titles, Genres

User = get_user_model()


class Review(models.Model):
    title = models.ForeignKey(Titles, on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.CharField(max_length=400)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews')
    score = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('author', 'title')
        ordering = ['pub_date']

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')
    text = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.text
