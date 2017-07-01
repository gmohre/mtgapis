from django.db import models
from django.utils.timezone import now

PRICE_MAX_DIGITS = 6
NAME_MAX_LENGTH = 255


class Card(models.Model):
    """
    Card Base class
    """
    name = models.CharField(verbose_name="Card Name", max_length=255)
    expansion = models.CharField(verbose_name="Card Expansion", max_length=255)

    def __str__(self):
        return "{} - {}".format(self.name, self.expansion)


class VendorQuote(models.Model):
    """
    Vendor for item
    """
    quote = models.DecimalField(decimal_places=2, max_digits=6)
    vendor_name = models.CharField(max_length=255)
    date = models.DateTimeField(default=now())

    def __str__():
        return "${} from {} on {}".format(
            (self.quote, self.vendor_name, self.date))


class WatchedCard(models.Model):
    """
    API-accessible Item to watch for purchase.
    """
    api_url = models.URLField(verbose_name="API URL")
    vendor_quote = models.ManyToManyField(VendorQuote)
    card = models.ForeignKey(Card)

    def __str__(self):
        return "{} {}".format(
            [api_url, vendor_quote])
