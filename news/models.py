from django.db import models
from django_mysql.models import ListCharField


TAGS_MAX_COUNT = 50
TAG_MAX_LENGTH = 50

class News(models.Model):
    title = models.CharField(verbose_name='title', max_length=200)
    text = models.TextField(verbose_name='news text')
    tags = ListCharField(base_field=models.CharField(max_length=TAG_MAX_LENGTH),
                         max_length = (TAGS_MAX_COUNT * TAG_MAX_LENGTH),
                         )
    source = models.URLField(verbose_name='source of news url')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'news'