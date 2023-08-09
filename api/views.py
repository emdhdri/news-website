from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from .serializers import newsSerializer
from news.models import News
from django.db.models import Q
import operator
from functools import reduce

    
#Retrieve a list of News if tags are provided.
#If no tags are specified in the request, all News data will be retrieved.
class NewsList(APIView):

    def get(self, request):
        params = dict(self.request.GET)
        if('tag' in params.keys()):
            filter_tags = set(params['tag'])
            if((not filter_tags) or (len(filter_tags) == 1 and ('' in filter_tags))):
                news_list = News.objects.all()
            else:
                query = [Q(tags__contains='{}'.format(tag)) for tag in filter_tags]
                news_list = News.objects.filter(reduce(operator.and_, query))   
        else:
            news_list = News.objects.all()

        response_data = newsSerializer(news_list, many=True)
        return Response(data=response_data.data)


#Retreive an specific News based on its primary key.
#if no record exists with the provided primary key then a 404 Not found response will be raised.
class NewsByPrimaryKey(APIView):

    def get_object(self, news_pk):
        try:
            news_instance = News.objects.get(pk=news_pk)
            return news_instance
        except News.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        news_object = self.get_object(pk)
        response_data = newsSerializer(news_object).data
        return Response(response_data)
