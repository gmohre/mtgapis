# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer

from .serializers import CardSerializer, EventSerializer, DeckSerializer, FormatQuerySerializer, EventFormatSerializer
from .models import Card, Event, Deck, FormatQuery, EventFormat


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    renderer = JSONRenderer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class DeckViewSet(viewsets.ModelViewSet):
    queryset = Deck.objects.all()
    serializer_class = DeckSerializer

class FormatQueryViewSet(viewsets.ModelViewSet):
    queryset = FormatQuery.objects.all()
    serializer_class = FormatQuerySerializer

class EventFormatQueryViewSet(viewsets.ModelViewSet):
    queryset = EventFormat.objects.all()
    serializer_class = EventFormatSerializer


# Create your views here.
