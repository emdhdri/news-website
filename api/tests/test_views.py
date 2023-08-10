#from django.test import TestCase, Client
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from news.models import News
from api.serializers import NewsSerializer
import json
import lorem

NEWS_TEXT = lorem.paragraph()

class GetListOfBooks(APITestCase):
    def setUp(self):
        news_instance = News.objects.create(title='text',
                            text=NEWS_TEXT,
                            tags=['specific_tag1', 'tag2'],
                            source='randomsource.ir')
        #self.serialized_news = NewsSerializer(news_instance)
        self.news_id = news_instance.id
    def test_get_all_news(self):
        url = reverse('news_list_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_get_news_by_pk(self):
        url = reverse('news_by_primary_key', args=[self.news_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_get_news_by_invalid_pk(self):
        url = reverse('news_by_primary_key', args=[0])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    def test_filter_by_tags(self):
        url = reverse('news_list_view')
        response = self.client.get(url, data={'tag' : 'specific_tag1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(News.objects.count(), 1)


        