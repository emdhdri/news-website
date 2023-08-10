from django.test import TestCase
from news.models import News
import lorem


NEWS_TEXT = lorem.paragraph()

class NewsTest(TestCase):
    def setUp(self):
        News.objects.create(title='test news',
                            text=NEWS_TEXT,
                            tags=['tag1', 'tag2', 'tag3'],
                            source='randomsourcehere.com',
                            )
        News.objects.create(title='test news2',
                            text=NEWS_TEXT,
                            tags=['tag1', 'tag5'],
                            source='randomsource2.com',
                            )
    def test_News_data(self):
        news_1 = News.objects.get(title='test news')
        news_2 = News.objects.get(title='test news2')
        self.assertTrue('tag1' in news_1.tags and 'tag1' in news_2.tags)
        self.assertTrue('tag5' not in news_1.tags and 'tag2' not in news_2.tags)
        self.assertEqual(str(news_1), news_1.title)
        self.assertEqual(str(news_2), news_2.title)
        self.assertEqual(news_1.text, NEWS_TEXT)