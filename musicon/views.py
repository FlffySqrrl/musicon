import datetime
import urllib2

from django.contrib import auth
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import Context, loader, RequestContext
from django.utils import timezone

from forms import RegistrationForm
from models import *
from parse import *

#-------------------------------------------------------------------------------
# Homepage
#-------------------------------------------------------------------------------

def events(request):
    """
    Displays all upcoming events.
    """
    Events = []

    # Sort upcoming events by date.
    upcoming_events = Event.objects.filter(startDate__gte = datetime.date.today)
    upcoming_events = upcoming_events.order_by('-startDate').reverse()

    for event in upcoming_events:
        Events.append(event)

    context = collect_events(Events)
    return render(request, 'events.html', context)

#-------------------------------------------------------------------------------
# Search
#-------------------------------------------------------------------------------

def search(request):
    """
    Filters out events based on the search criteria.
    """
    query_type, query_string, start_date, end_date, sort_by_pop = False, False, False, False, False
    Events, query_type_ids, matching_event_ids = [], [], []
    
    # Get query information entered by the user.
    query_type = request.GET['query_type'] if 'query_type' in request.GET else None
    query_string = request.GET['query_string'] if 'query_string' in request.GET and request.GET['query_string'].strip() else None
    start_date = request.GET['start_date'] if 'start_date' in request.GET else None
    end_date = request.GET['end_date'] if 'end_date' in request.GET else None
    sort_by_pop = request.GET['sort_by_pop'] if 'sort_by_pop' in request.GET else None

    # Display all events if the query type is empty.
    if not query_type:
        return events(request)

    # Get all upcoming events.
    upcoming_events = Event.objects.filter(startDate__gte = datetime.date.today)
    upcoming_events = upcoming_events.order_by('-startDate').reverse()

    # Find matching events if a query string was entered.
    # Step 1. Look up artists/venues with names containing the query string.
    # Step 2. Get the IDs of those artists/venues.
    # Step 3. Get the IDS of matching events.
    if query_string:
        if query_type == 'artist':
            similar_artists = list(Artist.objects.filter(aName__icontains = query_string))
            for artist in similar_artists:
                query_type_ids.append(artist.aID)
            for artist_id in query_type_ids:
                has_artist = list(Has_Artist.objects.filter(aID = artist_id))
                for event in has_artist:
                    matching_event_ids.append(event.eID_id)
        elif query_type == 'venue':
            similar_venues = list(Venue.objects.filter(vName__icontains = query_string))
            for venue in similar_venues:
                query_type_ids.append(venue.vID)
            for venue_id in query_type_ids:
                has_venue = list(Has_Venue.objects.filter(vID = venue_id))
                for event in has_venue:
                    matching_event_ids.append(event.eID_id)

    # Parse date range and filter events by dates.
    if start_date:
        start_date = [int(x) for x in str(start_date).split('-')]
        start_date = datetime.date(start_date[0], start_date[1], start_date[2])
    if end_date:
        end_date = [int(x) for x in str(end_date).split('-')]
        end_date = datetime.date(end_date[0], end_date[1], end_date[2])

    if start_date and end_date:
        upcoming_events = upcoming_events.filter(startDate__gte = start_date, startDate__lte = end_date)
    elif start_date:
        upcoming_events = upcoming_events.filter(startDate__gte = start_date)
    elif end_date:
        upcoming_events = upcoming_events.filter(startDate__lte = end_date)

    # Sort by popularity if checked.
    if sort_by_pop:
        upcoming_events = upcoming_events.order_by('-popularity').reverse()

    # Add an event to Events if it's a matching event or the query string
    # is empty, for the case where the user is only filtering by dates.
    for event in upcoming_events:
        if (event.eID in matching_event_ids) or (not query_string):
            Events.append(event)

    context = collect_events(Events)
    context['query_type'] = query_type
    context['query_string'] = query_string
    context['start_date'] = start_date
    context['end_date'] = end_date
    return render(request, 'events.html', context)

#-------------------------------------------------------------------------------
# Adding User Favourites
#-------------------------------------------------------------------------------

def add_fav_event(request):
    """
    Adds the matching event to Fav_Event when the user clicks on "Add Event". 
    """
    temp_events = []
    if request.user.is_authenticated():
        uID = request.user.id
        fav_events = Fav_Event.objects.filter(uID = uID)
        for event in fav_events:
             e = Event.objects.get(eName = event.eID)
             temp_events.append(e)
        if request.method == 'GET':
            eName = request.GET.get('eName', '')
            if "&#39;" in eName:
                eName = eName.replace("&#39;", "'")
            try:
                event = Event.objects.get(eName = eName)
            except ObjectDoesNotExist:
                event = None
            else:
                user = User.objects.get(id = uID)
                if event not in temp_events:
                    fe = Fav_Event(uID = user, eID = event)
                    fe.save()
    return fav_event(request)

def add_fav_venue(request):
    """
    Adds the matching venue to Fav_Venue when the user clicks on "Add Venue".
    """
    temp_venues = []
    if request.user.is_authenticated():
        uID = request.user.id
        fav_venues = Fav_Venue.objects.filter(uID = uID)
        for venue in fav_venues:
            v = Venue.objects.get(vName = venue.vID)
            temp_venues.append(v)
        if request.method == 'GET':
            lat = request.GET.get('lat', '')
            lon = request.GET.get('lon', '')
            venue = Venue.objects.get(lat = float(lat), lon = float(lon))
            user = User.objects.get(id = uID)
            if venue not in temp_venues:
                fv = Fav_Venue(uID = user, vID = venue)
                fv.save()
    return fav_venue(request)

#-------------------------------------------------------------------------------
# Displaying User Favourites
#-------------------------------------------------------------------------------

def fav_event(request):
    """
    Displays a user's favourite events.
    """
    Events = []

    # Get the user's favourite events.
    fav_events = Fav_Event.objects.filter(uID = request.user.id)

    # Add the user's favourite events to Events.    
    for event in fav_events:
        Events.append(Event.objects.get(eName = event.eID))

    context = collect_events(Events)
    return render(request, 'events.html', context)

def fav_venue(request):
    """
    Displays events at a user's favourite venues.
    """
    Events = []

    # Get the user's favourite venues.
    fav_venues = Fav_Venue.objects.filter(uID = request.user.id)

    # Add events at the user's favourite venues to Events.
    for venue in fav_venues:
        events = Has_Venue.objects.filter(vID = venue.vID)
        for event in events:
            Events.append(Event.objects.get(eName = event.eID))

    context = collect_events(Events)
    return render(request, 'events.html', context)

#-------------------------------------------------------------------------------
# Helpers
#-------------------------------------------------------------------------------

def collect_events(Events):
    """
    Collects information to be fed to the events list 
    and events map given an array of Event objects.
    """
    # For events list.
    event_ids = []
    artists, venues, dates, types, times, urls, pops = {}, {}, {}, {}, {}, {}, {}

    # For events map.
    Artists, Venues = [], []
    event_form = EventForm()
    venue_form = VenueForm()

    # Populate the arrays and the dictionaries.
    for event in Events:

        # Get the artists.
        # The headliner will be the first element in the arrays, 
        # followed by the supporting artists. If the event is a 
        # festival, then the festival name will be the "headliner".
        artist_names, artist_objs = [], []
        if event.eType == 'Festival':
            artist_names.append(event.eName)
        lineup = list(Has_Artist.objects.filter(eID = event.eID).order_by('-aType').reverse())
        for artist in lineup:
            artist = Artist.objects.get(aID = artist.aID_id)
            artist_names.append(artist.aName)
            artist_objs.append(artist)

        # Get the venue.
        # Assign None if the event doesn't have a venue yet.
        try:
            venue = Has_Venue.objects.get(eID = event.eID)
        except ObjectDoesNotExist:
            venue = None
        else:
            venue = Venue.objects.get(vID = venue.vID_id)

        Artists.append(artist_objs)
        Venues.append(venue)

        event_ids.append(event.eID)
        artists[event.eID] = artist_names
        venues[event.eID] = venue.vName if venue is not None else None
        dates[event.eID] = event.startDate
        types[event.eID] = event.eType
        times[event.eID] = event.startTime[:5] if event.startTime is not None else None
        urls[event.eID] = event.eUrl
        pops[event.eID] = event.popularity

    context = Context({'event_ids': event_ids, 'artists': artists, 'venues': venues, 
                       'dates': dates, 'types': types, 'times': times, 'urls': urls, 'pops': pops,
                       'Events': Events, 'Artists': Artists, 'Venues': Venues, 
                       'form_e': event_form, 'form_v': venue_form,})
    return context

#-------------------------------------------------------------------------------
# User Registration & Authentication
#-------------------------------------------------------------------------------

def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)

def auth_view(request):
    # GET username, if there is no valid data, return ''.
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username = username, password = password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/accounts/loggedin')
    else:
        return HttpResponseRedirect('/accounts/invalid_login')

def loggedin(request):
    c = {}
    c.update(csrf(request))
    c['username'] = request.user.username
    test = request.POST.get('title', '')
    return HttpResponseRedirect('/')

def invalid_login(request):
    return render_to_response('invalid_login.html')

def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/register_success')
        else:
            return render_to_response('register.html', {'form': form})
    args = {}
    args.update(csrf(request))
    args['form'] = RegistrationForm()
    return render(request, 'register.html', args)

def register_success(request):
    return render_to_response('register_success.html')
