from rest_framework.serializers import ModelSerializer
from news.models import News

class newsSerializer(ModelSerializer):

    class Meta:
        model = News
        fields = (
            'title',
            'text',
            'tags',
            'source',
        )