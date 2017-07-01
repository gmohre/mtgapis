# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import WatchedCard, Card, VendorQuote

admin.site.register(Card)
admin.site.register(VendorQuote)
admin.site.register(WatchedCard)

# Register your models here.
