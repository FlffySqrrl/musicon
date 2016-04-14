import datetime
from datetime import date
import json
import sys
import time
import urllib2

from django.core.exceptions import ObjectDoesNotExist

from models import *

def update():

    # Request a JSON object containing the upcoming events located in Vancouver.
    url = 'http://api.songkick.com/api/3.0/events.json?apikey=Pt2W1O3NKByZdwQL&location=ip:23.16.100.157'
    json_obj = urllib2.urlopen(url)
    data = json.load(json_obj)

    # Parse events information.
    event_id = []
    event_type = []
    event_status = []
    event_name = []
    event_date = []
    event_time = []
    event_url = []
    event_popularity = []
    event_age = []

    for event in data['resultsPage']['results']['event']:
        event_id.append(event['id'])
        event_type.append(event['type'])
        event_status.append(event['status'])
        event_name.append(event['displayName'])
        event_date.append(event['start']['date'])
        event_time.append(event['start']['time'])
        event_url.append(event['uri'])
        event_popularity.append(event['popularity'])
        event_age.append(event['ageRestriction'])

    # Parse artists information.
    artist_id = []
    artist_name = []
    artist_url = []
    artist_type = []

    for event in data['resultsPage']['results']['event']:
        temp = []
        for artist in event['performance']:
            temp.append(artist['artist']['id'])
        artist_id.append(temp)
        temp = []
        for artist in event['performance']:
            temp.append(artist['artist']['displayName'])
        artist_name.append(temp)
        temp = []
        for artist in event['performance']:
            temp.append(artist['artist']['uri'])
        artist_url.append(temp)
        temp = []
        for artist in event['performance']:
            temp.append(artist['billing'])
        artist_type.append(temp)
        temp = []

    # Parse venues information.
    venue_id = []
    venue_name = []
    venue_city = []
    venue_lat = []
    venue_lon = []

    for event in data['resultsPage']['results']['event']:
        venue_id.append(event['venue']['id'])
        venue_name.append(event['venue']['displayName'])
        venue_city.append(event['venue']['metroArea']['displayName'])
        venue_lat.append(event['venue']['lat'])
        venue_lon.append(event['venue']['lng'])

    # Add items to the Event table.
    for i in xrange(len(event_id)):
        try:
            e = Event.objects.get(eID = event_id[i])
        except ObjectDoesNotExist:
            if event_id[i] is not None:
                e = Event(eID = event_id[i], eName = event_name[i], eType = event_type[i], eUrl = event_url[i], \
                          startDate = event_date[i], startTime = event_time[i], popularity = event_popularity[i], \
                          status = event_status[i], ageRestriction = event_age[i])
                e.save()
        if event_id[i] is not None:
            e.eName = event_name[i]
            e.eType = event_type[i]
            e.eUrl = event_url[i]
            e.startDate = event_date[i]
            e.startTime = event_time[i]
            e.popularity = event_popularity[i]
            e.status = event_status[i]
            e.ageRestriction = event_age[i]
            e.save()

    # Add items to the Artist table.
    for i in xrange(len(event_id)):
        for j in xrange(len(artist_id[i])):
            try:
                a = Artist.objects.get(aID = artist_id[i][j])
            except ObjectDoesNotExist:
                if artist_id[i][j] is not None:
                    a = Artist(aID = artist_id[i][j], aName = artist_name[i][j], aUrl = artist_url[i][j])
                    a.save()
            if artist_id[i][j] is not None:
                a.aName = artist_name[i][j]
                a.aURL = artist_url[i][j]
                a.save()

    # Add items to the Venue table.
    for i in xrange(len(venue_id)):
        try:
            v = Venue.objects.get(vID = venue_id[i])
        except ObjectDoesNotExist:
            if venue_id[i] is not None:
                v = Venue(vID = venue_id[i], vName = venue_name[i], city = venue_city[i], \
                          lat = venue_lat[i], lon = venue_lon[i])
                v.save()
        if venue_id[i] is not None:
            v.vName = venue_name[i]
            v.city = venue_city[i]
            v.lat = venue_lat[i]
            v.lon = venue_lon[i]
            v.save()

    # Add items to the Has_Artist table.
    for i in xrange(len(event_id)):
        for j in xrange(len(artist_id[i])):
            try:
                ha = Has_Artist.objects.get(eID = Event.objects.get(eID = event_id[i]), aID = Artist.objects.get(aID = artist_id[i][j]))
            except ObjectDoesNotExist:
                if event_id[i] is not None:
                    ha = Has_Artist(eID = Event.objects.get(eID = event_id[i]), aID = Artist.objects.get(aID = artist_id[i][j]), \
                                   aType = artist_type[i][j])
                    ha.save()
            if event_id[i] is not None:
                ha.aID = Artist.objects.get(aID = artist_id[i][j])
                ha.save()

    # Add items to the Has_Venue table.
    for i in xrange(len(event_id)):
        try:
            hv = Has_Venue.objects.get(eID = Event.objects.get(eID = event_id[i]))
        except ObjectDoesNotExist:
            if event_id[i] is not None and venue_id[i] is not None:
                hv = Has_Venue(eID = Event.objects.get(eID = event_id[i]), vID = Venue.objects.get(vID = venue_id[i]))
                hv.save()
        if event_id[i] is not None and venue_id[i] is not None:
            hv.vID = Venue.objects.get(vID = venue_id[i])
            hv.save()

    lu = Last_Updated.objects.order_by('-updateCount')[0]
    lu.date = datetime.date.today()
    lu.updateCount = lu.updateCount + 1
    lu.save()

# Update the database if it hasn't been updated yet.
if len(Last_Updated.objects.order_by('-updateCount')) == 0:
    lu = Last_Updated(date = datetime.date.today(), updateCount = 1)
    lu.save()
    update()

# Update the database everyday.
currDate = datetime.date.today()
lastUpdate = Last_Updated.objects.order_by('-updateCount')[0]
lastUpdate = str(lastUpdate)
lastUpdate = lastUpdate.replace('-', ' ')
lastUpdate = lastUpdate.split(' ')
lastUpdate = [int(x) for x in lastUpdate]
lastDate = datetime.date(lastUpdate[0], lastUpdate[1], lastUpdate[2])
diff = currDate - lastDate

if diff.days >= 1:
    update()
