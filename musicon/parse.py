import datetime
import json
import sys
import time
import urllib2

from django.core.exceptions import ObjectDoesNotExist

from models import *

# ------------------------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------------------------

API_KEY = 'Pt2W1O3NKByZdwQL' # FlffySqrrl's
IP_ADDR = '23.16.100.157'    # VANCITY BABY

# ------------------------------------------------------------------------------
# IMPORT JSON
# ------------------------------------------------------------------------------

def get_events_by_ip(api_key, ip):
    '''
    Returns events from the Songkick upcoming events calendar localized based
    on an IP address as a JSON object.
    '''
    json_url = 'http://api.songkick.com/api/3.0/events.json?apikey=' + api_key + '&location=ip:' + ip
    json_file = urllib2.urlopen(json_url)
    json_obj = json.load(json_file)
    return json_obj

# ------------------------------------------------------------------------------
# PARSE JSON
# ------------------------------------------------------------------------------

def parse_events(calendar):
    events = []
    for e in calendar['resultsPage']['results']['event']:
        this_event = {
            'id'   : e['id'],
            'name' : e['displayName'],
            'type' : e['type'],
            'url'  : e['uri'],
            'date' : e['start']['date'],
            'time' : e['start']['time'],
            'stat' : e['status'],
            'pop'  : e['popularity'],
            'age'  : e['ageRestriction'],
        }
        events.append(this_event)
    return events

def parse_artists(calendar):
    artists = []
    for e in calendar['resultsPage']['results']['event']:
        for p in e['performance']:
            this_artist = {
                'id'    : p['artist']['id'],
                'name'  : p['artist']['displayName'],
                'url'   : p['artist']['uri'],
                'order' : p['billingIndex'],
                'e_id'  : e['id'],
            }
            artists.append(this_artist)
    return artists

def parse_venues(calendar):
    venues = []
    for e in calendar['resultsPage']['results']['event']:
        this_venue = {
            'id'   : e['venue']['id'],
            'name' : e['venue']['displayName'],
            'url'  : e['venue']['uri'],
            'city' : e['venue']['metroArea']['displayName'],
            'lat'  : e['venue']['lat'],
            'lng'  : e['venue']['lng'],
            'e_id' : e['id'],
        }
        venues.append(this_venue)
    return venues

# ------------------------------------------------------------------------------
# UPDATE ENTITY TABLES
# ------------------------------------------------------------------------------

def update_event(events):
    for e in events:
        try:
            this_event = Event.objects.get(event_id = e['id'])
        except ObjectDoesNotExist:
            if e['id']:
                this_event = Event(
                    event_id   = e['id'],
                    event_name = e['name'],
                    event_type = e['type'],
                    event_url  = e['url'],
                    start_date = e['date'],
                    start_time = e['time'],
                    status     = e['stat'],
                    popularity = e['pop'],
                    age_limit  = e['age']
                )
                this_event.save()
        if e['id']:
            this_event.event_name = e['name']
            this_event.event_type = e['type']
            this_event.event_url  = e['url']
            this_event.start_date = e['date']
            this_event.start_time = e['time']
            this_event.status     = e['stat']
            this_event.popularity = e['pop']
            this_event.age_limit  = e['age']
            this_event.save()

def update_artist(artists):
    for a in artists:
        try:
            this_artist = Artist.objects.get(artist_id = a['id'])
        except ObjectDoesNotExist:
            if a['id']:
                this_artist = Artist(
                    artist_id   = a['id'],
                    artist_name = a['name'],
                    artist_url  = a['url']
                )
                this_artist.save()
        if a['id']:
            this_artist.artist_name = a['name']
            this_artist.artist_url  = a['url']
            this_artist.save()

def update_venue(venues):
    for v in venues:
        try:
            this_venue = Venue.objects.get(venue_id = v['id'])
        except ObjectDoesNotExist:
            if v['id']:
                this_venue = Venue(
                    venue_id   = v['id'],
                    venue_name = v['name'],
                    venue_url  = v['url'],
                    city       = v['city'],
                    lat        = v['lat'],
                    lng        = v['lng']
                )
        if v['id']:
            this_venue.venue_name = v['name']
            this_venue.venue_url  = v['url']
            this_venue.city       = v['city']
            this_venue.lat        = v['lat']
            this_venue.lng        = v['lng']
            this_venue.save()

# ------------------------------------------------------------------------------
# UPDATE RELATIONSHIP TABLES
# ------------------------------------------------------------------------------

def update_has_artist(events, artists):
    for e in events:
        for a in artists:
            if e['id'] == a['e_id']:
                try:
                    this_has_artist = HasArtist.objects.get(
                        event_id  = Event.objects.get(event_id = e['id']),
                        artist_id = Artist.objects.get(artist_id = a['id'])
                    )
                except ObjectDoesNotExist:
                    if e['id']:
                        this_has_artist = HasArtist(
                            event_id     = Event.objects.get(event_id = e['id']),
                            artist_id    = Artist.objects.get(artist_id = a['id']),
                            artist_order = a['order']
                        )
                        this_has_artist.save()
                if e['id']:
                    this_has_artist.artist_id    = Artist.objects.get(artist_id = a['id'])
                    this_has_artist.artist_order = a['order']
                    this_has_artist.save()

def update_has_venue(events, venues):
    for e in events:
        for v in venues:
            if e['id'] == v['e_id']:
                try:
                    this_has_venue = HasVenue.objects.get(
                        event_id = Event.objects.get(event_id = e['id']),
                        venue_id = Venue.objects.get(venue_id = v['id'])
                    )
                except ObjectDoesNotExist:
                    if e['id'] and v['id']:
                        this_has_venue = HasVenue(
                            event_id = Event.objects.get(event_id = e['id']),
                            venue_id = Venue.objects.get(venue_id = v['id'])
                        )
                if e['id'] and v['id']:
                    this_has_venue.venue_id = Venue.objects.get(venue_id = v['id'])
                    this_has_venue.save()

# ------------------------------------------------------------------------------
# UPDATE DATABASE
# ------------------------------------------------------------------------------

def update_database():
    cal = get_events_by_ip(API_KEY, IP_ADDR)

    e = parse_events(cal)
    a = parse_artists(cal)
    v = parse_venues(cal)

    update_event(e)
    update_artist(a)
    update_venue(v)
    update_has_artist(e, a)
    update_has_venue(e, v)

# ------------------------------------------------------------------------------
# CHECK FOR UPDATE
# ------------------------------------------------------------------------------

if len(Update.objects.order_by('-date')) == 0:
    this_update = Update(date=datetime.date.today(), note='First update')
    this_update.save()
    update_database()
else:
    last_update = Update.objects.order_by('-date')[0]
    last_update = str(last_update).replace('-', ' ').split(' ')
    last_update = [int(x) for x in last_update]
    last_update_date = datetime.date(last_update[0], last_update[1], last_update[2])
    this_update_date = datetime.date.today()
    diff = this_update_date - last_update_date
    if diff.days >= 1:
        this_update = Update(date=this_update_date, note='Daily update')
        this_update.save()
        update_database()
