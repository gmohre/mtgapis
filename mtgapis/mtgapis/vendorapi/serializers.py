from rest_framework import serializers
from .models import Card, VendorQuote, WatchedCard

class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ('__all__')

class VendorQuoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorQuote
        fields = ('__all__')

class WatchedCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = WatchedCard
        fields = ('__all__')

#class CardSerializers(serializers.Serializer):
#    id = serializers.IntegerField(read_only=True)
#    name = serializers.CharField(max_length=NAME_MAX_LENGTH)
#    expansion = serializers.CharField(max_length=NAME_MAX_LENGTH)
#
#    def create(self, validated_data):
#        return Card.objects.create(**validated_data)
#
#    def update(self, instance, validated_data):
#        instance.name = validated_data.get('name', instance.name)
#        instance.expansion = validated_data.get('name', instance.expansion)
#        instance.save()
#        return instance
#
#
#class VendorQuoteSerializer(serializers.Serializer):
#    id = serializers.IntegerField(read_only=True)
#    quote = serializers.DecimalField(decimal_places=2, max_digits=PRICE_MAX_DIGITS)
#    date = serializers.DateTimeField()
#
#    def create(self, validated_data):
#        return VendorQuote.objects.create(**validated_data)
#
#    def update(self, instance, validated_data):
#        instance.quote = validated_data.get('quote', instance.quote)
#        instance.vendor_name = validated_data.get('vendor_name', instance.vendor_name)
#        instance.date = validated_data.gat('date', instance.date)
#        instance.save()
#        return instance
#
#
#class ItemWatcher(serializers.Serializer):
#    id = serializers.IntegerField(read_only=True)
#    api_url = serializers.URLField()
#    vendor_quote = VendorQuoteSerializer()
#
#    def create(self, validated_data):
#        return ItemWatcher.objects.create(**validated_data)
#
#    def update(self, instance, validated_data):
#        instance.api_url = validated_data.get('quote', instance.api_url)
#        instance.vendor_quote = validated_data.get('vendor_quote', instance.vendor_quote)
#        instance.save()
#        return instance
