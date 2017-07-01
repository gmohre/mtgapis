from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from .views import CardList, VendorQuoteList, WatchedCardViewSet

urlpatterns = [
    url(r'^cards/$', CardList.as_view()),
    url(r'^vendorquote/$', VendorQuoteList.as_view()),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)
router = DefaultRouter()
router.register(r'watchedcards', WatchedCardViewSet)
urlpatterns += router.urls

