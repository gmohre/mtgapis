import __future__
import re, json, os, datetime
from django.db import models

from selenium import webdriver                                                                                                                                         
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.support.ui import WebDriverWait

try:
    import urllib2 as urllib
except ModuleNotFoundError:
    import urllib.request as urllib

BASIC_LAND_TYPES = ['Swamp', 'Island', 'Mountain', 'Plains', 'Forest']
CARDSBYNAMEDB = json.loads(open('cardsbynameDB.db','r').read())

CARD_RE = re.compile("(?P<count>[0-9]{1,2}) (?P<set>\[.+?\]) (?P<name>.*[^\r^\n])")

class Card(models.Model):

    name = models.CharField(max_length=2**8)
    multID = models.IntegerField()
    count = models.IntegerField()

    def save(self, *args, **kwargs):
        try:
            self.multID = CARDSBYNAMEDB.get(self.name, -1)
        except:
            self.multID = -1
        super(Card, self).save(*args, **kwargs)


class Deck(models.Model):
    title = models.CharField(blank=False, max_length=2**8) 
    md_cards = models.ForeignKey(Card, on_delete=models.SET_NULL, related_name='md', null=True)
    sb_cards = models.ForeignKey(Card, on_delete=models.SET_NULL, related_name='sb', null=True)
    html = models.TextField(blank=True)
    deckID = models.CharField(max_length=2**6)

    def save(self, *args, **kwargs):
        self._populate_card_lists()
        super(Deck, self).save(*args, **kwargs)

    def _populate_card_lists(self):
        md_cards = [Card.objects.create(**c.groupdict()) for c in CARD_RE.finditer(self.html)]
        sb_cards = [Card.objects.create(**c.groupdict()) for c in CARD_RE.finditer(self.html)]
        if not md_cards:
            return
        def _remove_basics(cardlist):
            return [card for card in cardlist if card.name not in BASIC_LAND_TYPES]
        self.md_cards = _remove_basics(md_cards)
        self.sb_cards = _remove_basics(sb_cards)
        self.save(update_fields=['md_cards','sb_cards'])


class Event(models.Model):
    """
        An Event, with a date, eventID, url, and 
    """
    eventID = models.CharField(max_length=2**7)
    eventTitle = models.CharField(blank=True, max_length=2**8)
    decks = models.ForeignKey(Deck, on_delete=models.SET_NULL, null=True)
    date = models.DateField(null=True)
    format_query = models.ForeignKey('mtg.FormatQuery', null=True)

    def save(self, *args, **kwargs):
        self._populate_decks()
        super(Event, self).save(*args, **kwargs)
    @property
    def format_code(self):
        return self.format_query.event_format.format_code if self.format_query else ''

    def __iter__(self):
        self._iter = iter(self.decks.objects.all())
        return self

    def __next__(self):
        return next(self._iter)


    def _populate_decks(self):
        response = urllib.urlopen(self.url)
        print(response)
        html = response.read().decode("Windows-1250").encode("utf-8")

        if isinstance(html, bytes):
            html = str(html)
        #html = html.replace("\n", "")

        if "data[Deck][cards]" in html:
            deckList = re.findall("\?e=[0-9]+\&d=[0-9]+\&f={}"\
                .format(self.format_code), html)

            self.eventTitle = str(re.search("class=S18 align=center\>.+?\</td\>"\
                ,html).group().replace("class=S18 align=center>","")\
                .replace("</td>", ""))
            
            for deckID in deckList:
                titleSearch = r"d=" + deckID + "&f={}.+?\>.+?\<\/a\>".format(self.format_code)
                deckTitle=re.search(titleSearch, html)
                if deckTitle:
                    deckTitle=str(decktitle.group().\
                        split(">")[1].replace("</a", ""))
                    print(deckTitle)
                else:
                    print('not a deck')
                    continue
                import pdb; pdb.set_trace()
                Deck.objects.create(
                    html=html,
                    event=self,
                    deckID=deckID.split("=")[2].replace("&f", ""),
                    title=deckTitle)
                            
    @property
    def url(self):
        URL_PATTERN = "http://mtgtop8.com/event/?e={}"
        return URL_PATTERN.format(self.eventID)

    @property
    def deckIDs(self):
        return [deckID for deckID, deck in self]

 
#    def __iter__(self):
#        self.card_index = 0
#        self.deck_section = 'md'
#        return self
#
#    def __next__(self):
#        self.card_index += 1
#        if self.deck_section == 'md':
#            if len(self.cards[self.deck_section]) >= self.card_index:
#                return self.cards[self.deck_section][self.card_index - 1]
#            self.deck_section = 'sb'
#        if len(self.cards[self.deck_section]) >= self.card_index:
#            return self.cards[self.deck_section][self.card_index - 1]
#        else:
#            raise StopIteration

#    def default(self):
#        md_cards_json = [json.dumps(card) for card in self.cards.get('md')]
#        sb_cards_json = [json.dumps(card) for card in self.cards.get('sb')]
#        return dict(
#            data=dict(
#                title=self.title,
#                cards=dict(md=md_cards_json, sb=sb_cards.json),
#                url=self.url)
#            )


   


class EventFormat(models.Model):
    format_name = models.CharField(max_length=2*5, default='Standard')
    format_code = models.CharField(max_length=2*1, default='ST', blank=True)


class FormatQuery(models.Model):
    event_format = models.ForeignKey(EventFormat)

    def save(self, *args, **kwargs):
        super(FormatQuery, self).save(*args, **kwargs)
        self._populate_events(*args, **kwargs)

    def __iter__(self):
        self._iter = iter(self.events)
        return self

    def __next__(self):
        return self.events.get(next(self._iter))

    def eventIDs(self):
        return [event.eventID for event in self.events.all()]


    def _populate_events(self, *args, **kwargs):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=chrome_options)
        driver.get('http://mtgtop8.com/search')
        driver.implicitly_wait(2)

        format_sel=driver.find_element_by_css_selector('select[name=format]')         
        format_sel.send_keys(self.event_format.format_name)
        
        search_submit = driver.find_element_by_css_selector('input[value=Search]')    
        search_submit.click()
        driver.implicitly_wait(0)
        
        trs = driver.find_elements_by_class_name('hover_tr')
        event_re = re.compile(r'.*\?e=(?P<eventID>[0-9]+)&f='+self.event_format.format_code)
        for tr_set in trs:
            anchors = [a for a in tr_set.find_elements_by_css_selector('td a')]
            date = tr_set.find_elements_by_css_selector('td')[-1].text
            date = datetime.date(*[int(dig) for dig in date.split('/')])
            hrefs = [a.get_attribute('href') for a in anchors]

            
            event_dicts = [event_re.match(href).groupdict() for href in hrefs if event_re.match(href)]

            if any(event_dicts):
                events = [Event.objects.get_or_create(date=date, format_query=self,**event_dict) for event_dict in event_dicts]
                #events = [self.events.add(event[0]) for event in events if event[0]]
            else:
                print('no events')
#            for event_dict in event_dicts:
#                eventID = event_dict.get('eventID')
#                print(eventID)
#                if not self.events.get(eventID) and eventID:
#                    print(date)
#                    event_dict.update(date=date)
#                    self.events[event_dict.get('eventID')] = Event(**event_dict)
#

