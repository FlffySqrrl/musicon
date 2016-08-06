import datetime
import urllib2

from django.contrib import auth
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import Context
from django.template import RequestContext
from django.template import loader
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect

from forms import *
from models import *
from parse import *

# ------------------------------------------------------------------------------
# MAIN PAGE
# ------------------------------------------------------------------------------

def events(request):
    """
    Display all upcoming events.
    """
    events = []

    # Get all upcoming events.
    upcoming = Event.objects.filter(start_date__gte=datetime.date.today)
    upcoming = upcoming.order_by('start_date')

    for e in upcoming:
        events.append(e)

    context = collect_events(events)
    return render(request, 'events.html', context)

# ------------------------------------------------------------------------------
# SEARCH
# ------------------------------------------------------------------------------

def search(request):
    """
    Filter events based on the search criteria.
    """
    events = []

    # Parse URL query string.
    by, q, start, end, pop = None, None, None, None, None
    if 'by' in request.GET:
        by = request.GET['by']
    if 'q' in request.GET and request.GET['q'].strip():
        q = request.GET['q']
    if 'start' in request.GET:
        start = request.GET['start']
        if start:
            start = [int(x) for x in str(start).split('-')]
            start = datetime.date(start[0], start[1], start[2])
    if 'end' in request.GET:
        end = request.GET['end']
        if end:
            end = [int(x) for x in str(end).split('-')]
            end = datetime.date(end[0], end[1], end[2])
    if 'pop' in request.GET:
        pop = request.GET['pop']

    # Get all upcoming events.
    upcoming = Event.objects.filter(start_date__gte=datetime.date.today)
    upcoming = upcoming.order_by('start_date')

    # Find matching events if a search string was entered.
    # 1. Look up artists/venues with matching names.
    # 2. Get matching artist/venue IDs.
    # 3. Get matching event IDs.
    event_ids = []
    if q:
        if by == 'artist':
            artist_ids = []
            artists = list(Artist.objects.filter(artist_name__icontains=q))
            for a in artists:
                artist_ids.append(a.artist_id)
            for id in artist_ids:
                has_artist = list(HasArtist.objects.filter(artist_id=id))
                for ha in has_artist:
                    event_ids.append(ha.event_id_id)
        elif by == 'venue':
            venue_ids = []
            venues = list(Venue.objects.filter(venue_name__icontains=q))
            for v in venues:
                venue_ids.append(v.venue_id)
            for id in venue_ids:
                has_venue = list(HasVenue.objects.filter(venue_id=id))
                for hv in has_venue:
                    event_ids.append(hv.event_id_id)
        elif by == 'any':
            artist_ids = []
            artists = list(Artist.objects.filter(artist_name__icontains=q))
            for a in artists:
                artist_ids.append(a.artist_id)
            for id in artist_ids:
                has_artist = list(HasArtist.objects.filter(artist_id=id))
                for ha in has_artist:
                    event_ids.append(ha.event_id_id)
            venue_ids = []
            venues = list(Venue.objects.filter(venue_name__icontains=q))
            for v in venues:
                venue_ids.append(v.venue_id)
            for id in venue_ids:
                has_venue = list(HasVenue.objects.filter(venue_id=id))
                for hv in has_venue:
                    if hv.event_id_id not in event_ids:
                        event_ids.append(hv.event_id_id)
            upcoming = list(upcoming.filter(event_name__icontains=q))
            for e in upcoming:
                if e.event_id not in event_ids:
                    event_ids.append(e.event_id)

    # Filter events by date(s).
    if start and end:
        upcoming = upcoming.filter(start_date__gte=start, start_date__lte=end)
    elif start:
        upcoming = upcoming.filter(start_date__gte=start)
    elif end:
        upcoming = upcoming.filter(start_date__lte=end)

    # Sort by popularity if checked.
    if pop:
        upcoming = upcoming.order_by('-popularity')

    # Add an event if:
    # 1. It is a matching event.
    # 2. The search string is empty.
    for e in upcoming:
        if (e.event_id in event_ids) or (not q):
            events.append(e)

    context = collect_events(events)
    context['by'] = by
    context['q'] = q
    context['start'] = start
    context['end'] = end
    context['count'] = len(events)
    return render(request, 'events.html', context)

# ------------------------------------------------------------------------------
# ADDING USER FAVOURITES
# ------------------------------------------------------------------------------

def add_fav_event(request):
    """
    Add the matching event to FavEvent when the user clicks on 'Add Event'.
    """
    curr_fav_events = []

    if request.user.is_authenticated():
        user_id = request.user.id
        fav_events = FavEvent.objects.filter(user_id=user_id)
        for fe in fav_events:
            event = Event.objects.get(event_id=fe.event_id_id)
            curr_fav_events.append(event)
        if request.method == 'GET':
            event_name = request.GET.get('event_name', '')
            try:
                event = Event.objects.get(event_name=event_name)
            except ObjectDoesNotExist:
                event = None
            else:
                user = User.objects.get(id=user_id)
                if event not in curr_fav_events:
                    this_fav_event = FavEvent(user_id=user, event_id=event)
                    this_fav_event.save()

    return disp_fav_events(request)


def add_fav_venue(request):
    """
    Add the matching venue to FavVenue when the user clicks on 'Add Venue'.
    """
    curr_fav_venues = []

    if request.user.is_authenticated():
        user_id = request.user.id
        fav_venues = FavVenue.objects.filter(user_id=user_id)
        for fv in fav_venues:
            venue = Venue.objects.get(venue_id=fv.venue_id_id)
            curr_fav_venues.append(venue)
        if request.method == 'GET':
            lat = request.GET.get('lat', '')
            lng = request.GET.get('lng', '')
            venue = Venue.objects.get(lat=float(lat), lng=float(lng))
            user = User.objects.get(id=user_id)
            if venue not in curr_fav_venues:
                this_fav_venue = FavVenue(user_id=user, venue_id=venue)
                this_fav_venue.save()

    return disp_fav_venues(request)

# ------------------------------------------------------------------------------
# DISPLAYING USER FAVOUITES
# ------------------------------------------------------------------------------

def disp_fav_events(request):
    """
    Display a user's favourite events.
    """
    events = []

    fav_events = FavEvent.objects.filter(user_id=request.user.id)
    for fe in fav_events:
        event = Event.objects.get(event_id=fe.event_id_id)
        events.append(event)

    context = collect_events(events)
    return render(request, 'events.html', context)


def disp_fav_venues(request):
    """
    Display events at a user's favourite venues.
    """
    events = []

    fav_venues = FavVenue.objects.filter(user_id=request.user.id)
    for fv in fav_venues:
        has_venue = HasVenue.objects.filter(venue_id=fv.venue_id_id)
        for hv in has_venue:
            event = Event.objects.get(event_id=hv.event_id_id)
            events.append(event)

    context = collect_events(events)
    return render(request, 'events.html', context)

# ------------------------------------------------------------------------------
# EVENT LISTING
# ------------------------------------------------------------------------------

def collect_events(events):
    """
    Collect event information to be fed to events.html.
    """

    # Main entities
    # events = events
    artists = []
    venues = []

    # Event details
    e_ids = []
    e_artists, e_venues, e_types, e_urls, e_dates, e_times, e_pops = {}, {}, {}, {}, {}, {}, {}

    # Forms
    event_form = EventForm()
    venue_form = VenueForm()

    for e in events:

        # Get artist(s).
        lineup = []
        lineup_names = []
        has_artist = list(HasArtist.objects.filter(event_id=e.event_id).order_by('artist_order'))
        if e.event_type == 'Festival':
            lineup_names.append(e.event_name)
        if e.event_type == 'Concert':
            for ha in has_artist:
                artist = Artist.objects.get(artist_id=ha.artist_id_id)
                lineup.append(artist)
                lineup_names.append(artist.artist_name)

        # Get venue.
        try:
            has_venue = HasVenue.objects.get(event_id=e.event_id)
        except ObjectDoesNotExist:
            venue = None
        else:
            venue = Venue.objects.get(venue_id=has_venue.venue_id_id)

        artists.append(lineup)
        venues.append(venue)

        e_ids.append(e.event_id)

        e_artists[e.event_id] = lineup_names
        e_venues[e.event_id] = venue.venue_name if venue else None
        e_types[e.event_id] = e.event_type
        e_urls[e.event_id] = e.event_url
        e_dates[e.event_id] = e.start_date
        e_times[e.event_id] = e.start_time[:5] if e.start_time else None
        e_pops[e.event_id] = e.popularity

    context = Context({
        'events'    : events,
        'artists'   : artists,
        'venues'    : venues,

        'e_ids'     : e_ids,
        'e_artists' : e_artists,
        'e_venues'  : e_venues,
        'e_types'   : e_types,
        'e_urls'    : e_urls,
        'e_dates'   : e_dates,
        'e_times'   : e_times,
        'e_pops'    : e_pops,

        'event_form': event_form,
        'venue_form': venue_form,
    })
    return context

# ------------------------------------------------------------------------------
# AUTHENTICATION SYSTEM
# ------------------------------------------------------------------------------

@csrf_protect
def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'signup_success.html')
        else:
            return render(request, 'signup.html', {'error': True})
    return render(request, 'signup.html')


@csrf_protect
def signin(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'signin.html', {'error': True})
    return render(request, 'signin.html')


@csrf_protect
def signout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
