from django.urls import path
from . import views 


urlpatterns = [
    path('news/', views.NewsList.as_view(), name='news_list_view'),
    path('news/<int:pk>', views.NewsByPrimaryKey.as_view(), name='news_by_primary_key'),
]
