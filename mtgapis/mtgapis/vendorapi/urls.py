from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CardList

urlpatterns = [
    url(r'^cards/$', CardList.as_view()),
    ]
urlpatterns = format_suffix_patterns(urlpatterns)
