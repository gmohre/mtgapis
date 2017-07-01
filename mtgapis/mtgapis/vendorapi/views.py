# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, AdminRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Card, VendorQuote, WatchedCard
from .serializers import CardSerializer, VendorQuoteSerializer,\
        WatchedCardSerializer

class WatchedCardViewSet(ModelViewSet):
    queryset = WatchedCard.objects.all()
    serializer_class = WatchedCardSerializer

class CardList(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class VendorQuoteList(generics.ListCreateAPIView):
    queryset = VendorQuote.objects.all()
    serializer_class = VendorQuoteSerializer

