# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics

from .models import Card, VendorQuote, WatchedCard
from .serializers import CardSerializer, VendorQuoteSerializer,\
        WatchedCardSerializer


class CardList(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class VendorQuoteList(generics.ListCreateAPIView):
    queryset = VendorQuote.objects.all()
    serializer_class = VendorQuoteSerializer


class WatchedCardList(generics.ListCreateAPIView):
    queryset = WatchedCard.objects.all()
    serializer_class = WatchedCardSerializer
