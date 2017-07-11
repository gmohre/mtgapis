
#!/usr/bin/env python
import re, json

from selenium import webdriver                                                                                                                                         
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.support.ui import WebDriverWait

try:
    import urllib2 as urllib
except ModuleNotFoundError:
    import urllib.request as urllib

BASIC_LAND_TYPES = ['Swamp', 'Island', 'Mountain', 'Plains', 'Forest']
CARDSBYNAMEDB = json.loads(open('cardsbynameDB.db', 'r').read())


class Event(dict):
    def __init__(self, *args, **kwargs):
        self.URL_PATTERN = "http://mtgtop8.com/event/?e={}"
        self.decks = {}
        self.eventID = kwargs.get('eventID', 'NIL')
        self.url = self.URL_PATTERN.format(self.eventID)
        self.date = kwargs.get('date', 'NIL')
        self.populate_decks()
        dict.__init__(self, decks=self.decks, eventID=self.eventID, url=self.url, date=self.date, deckIDs=[deckID for deckID, deck in self.decks.items()])

    def __iter__(self):
        self._iter = iter(self.decks)
        return self

    def __next__(self):
        return next(self._iter)

    def default(self):
        return dict(
                data=dict(
                    decks=json.dumps(self.decks),
                    deckIDs=self.deckIDS,
                    date=self.date,
                    eventID=self.eventID,
                    url=self.url))


    def populate_decks(self):
        response = urllib.urlopen(self.url)
        html = response.read().decode("Windows-1250").encode("utf-8")

        if isinstance(html, bytes):
            html = str(html)
        # Remove newline as their HTML sometimes splits titles
        html     = html.replace("\n", "")

        if "data[Deck][cards]" not in html:
            pass
        else:
            # Parse deckID's from each event
            deckList   = re.findall("\?e=[0-9]+\&d=[0-9]+\&f=[A-Z]{2,3}", html)
            self.eventTitle = str(re.search("class=S18 align=center\>.+?\</td\>", html).group().replace("class=S18 align=center>","").replace("</td>", ""))
            for deckID in deckList:
                deckID      = deckID.split("=")[2].replace("&f", "")
                titleSearch = r"d=" + deckID + "&f=[A-Z].+?\>.+?\<\/a\>"
                deckTitle   = str(re.search(titleSearch, html).group().split(">")[1].replace("</a", ""))
                self.decks[deckID] = Deck(deckID, self.eventID, deckTitle)

class FormatQuery(dict):

    def __init__(self, format_name='Standard', format_code='ST'):
        try:
            f = open('deck_db.db', 'r').read()
            d = json.loads(f.read())
            dict(self, **json.loads(f))
        except:
            self.format_name = format_name
            self.format_code = format_code
            self.events = {}
            self.pages = 0
            self.populate_events()
            dict.__init__(self, format_name=format_name, format_code=self.format_code, events=self.events, eventIDs=[eventID for eventID, event in self.events.items()])
            f = open('deck_db.db', 'w')
            f.write(json.dumps(self))


    def __iter__(self):
        self._iter = iter(self.events)
        return self

    def __next__(self):
        return self.events.get(next(self._iter))

#    def default(self):
#        return dict(
#                data=dict(
#                    events=[json.dumps(ev) for ev in self.events],
#                    format_name=self.format_name,
#                    format_code=self.format_code))

    def populate_events(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=chrome_options)
        driver.get('http://mtgtop8.com/search')
        driver.implicitly_wait(2)

        format_sel=driver.find_element_by_css_selector('select[name=format]')         
        format_sel.send_keys(self.format_name)
        
        search_submit = driver.find_element_by_css_selector('input[value=Search]')    
        search_submit.click()
        driver.implicitly_wait(0)
        
        trs = driver.find_elements_by_class_name('hover_tr')
        event_re = re.compile(r'.*\?e=(?P<eventID>[0-9]+)&f=ST')
        for tr_set in trs:
            anchors = [a for a in tr_set.find_elements_by_css_selector('td a')]
            date = tr_set.find_elements_by_css_selector('td')[-1].text
            hrefs = [a.get_attribute('href') for a in anchors]
            event_dicts = [event_re.match(href).groupdict() for href in hrefs if event_re.match(href)]
            for event_dict in event_dicts:
                eventID = event_dict.get('eventID')
                if not self.events.get(eventID) and eventID:
                    event_dict.update(date=date)
                    self.events[event_dict.get('eventID')] = Event(**event_dict)

class Card(dict):

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        try:
            self.multID = CARDSBYNAMEDB.get(self.name, -1)
        except:
            self.multID = -1
        self.count = kwargs.get('count')
        dict.__init__(self, name=self.name, multID=self.multID, count=self.count)

    def __repr__(self):
        return "{}:{}:{}".format(self.multID, self.name, self.count)

#    def default(self):
#        return dict(data=dict(
#                        name=self.name,
#                        count=self.count,
#                        multID=self.multID))

class Deck(dict):
    
    def __init__(self, deckID, eventID, title):
        self.title = title
        self.URL_PATTERN = 'http://mtgtop8.com/dec?d={}&f=ST'
        self.EVENT_PATTERN = 'http://mtgtop8.com/event?e={}&d={}&f=ST'
        self.url = self.URL_PATTERN.format(deckID)
        self.event_url = self.EVENT_PATTERN.format(eventID, deckID)
        self.CARD_RE = re.compile("(?P<count>[0-9]{1,2}) (?P<set>\[.+?\]) (?P<name>.*[^\r^\n])")
        self.cards = {}
        self.populate_card_lists()
        
        dict.__init__(self, 
                title=self.title,
                url=self.url,
                cards=self.cards,
                mbcardIDs=list(set(
                    [card.multID for card in self.cards['md']]+\
                    [card.multID for card in self.cards['sb']]
                    ))
                )

    def __iter__(self):
        self.card_index = 0
        self.deck_section = 'md'
        return self

    def __next__(self):
        self.card_index += 1
        if self.deck_section == 'md':
            if len(self.cards[self.deck_section]) >= self.card_index:
                return self.cards[self.deck_section][self.card_index - 1]
            self.deck_section = 'sb'
        if len(self.cards[self.deck_section]) >= self.card_index:
            return self.cards[self.deck_section][self.card_index - 1]
        else:
            raise StopIteration

#    def default(self):
#        md_cards_json = [json.dumps(card) for card in self.cards.get('md')]
#        sb_cards_json = [json.dumps(card) for card in self.cards.get('sb')]
#        return dict(
#            data=dict(
#                title=self.title,
#                cards=dict(md=md_cards_json, sb=sb_cards.json),
#                url=self.url)
#            )


    def populate_card_lists(self):
        response = urllib.urlopen(self.url)
        html = str(response.read().decode('Windows-1250'))
        if 'SB:' in html:
            md_cards = [Card(**c.groupdict()) for c in self.CARD_RE.finditer(html)]
            sb_cards = [Card(**c.groupdict()) for c in self.CARD_RE.finditer(html)]
        else:
            md_cards = [Card(**c.groupdict()) for c in self.CARD_RE.finditer(html)]
            sb_cards = []
        def _remove_basics(cardlist):
            return [card for card in cardlist if card.name not in BASIC_LAND_TYPES]
        md_cards = _remove_basics(md_cards)
        sb_cards = _remove_basics(sb_cards)

        self.cards = {'md':md_cards, 'sb':sb_cards}
    


