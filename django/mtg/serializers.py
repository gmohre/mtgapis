from rest_framework.serializers import ModelSerializer
from .models import Card, Event, FormatQuery, Deck, EventFormat


class CardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = ('__all__')


class DeckSerializer(ModelSerializer):
    class Meta:
        model = Deck
        fields = ('__all__')

class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ('__all__')

class FormatQuerySerializer(ModelSerializer):
    class Meta:
        model = FormatQuery
        fields = ('__all__')

class EventFormatSerializer(ModelSerializer):
    class Meta:
        model = EventFormat
        fields = ('__all__')


