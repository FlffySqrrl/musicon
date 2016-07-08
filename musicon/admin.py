from django.contrib import admin

from forms import *
from models import *

# ------------------------------------------------------------------------------
# INTERFACE CUSTOMIZATIONS
# ------------------------------------------------------------------------------

class HasArtistInline(admin.StackedInline):
    '''
    Creates HasArtist as a required in-line form.
    '''
    model = HasArtist
    extra = 1
    formset = RequiredInlineFormSet

class HasVenueInline(admin.StackedInline):
    '''
    Creates HasVenue as a required in-line form.
    '''
    model = HasVenue
    max_num = 1
    formset = RequiredInlineFormSet

class EventAdmin(admin.ModelAdmin):
    model = Event
    inlines = [HasArtistInline, HasVenueInline]
    list_display = ['event_id', 'event_type', 'event_name', 'start_date', 'start_time']

class ArtistAdmin(admin.ModelAdmin):
    model = Artist
    list_display = ['artist_id', 'artist_name']

class VenueAdmin(admin.ModelAdmin):
    model = Venue
    list_display = ['venue_id', 'venue_name', 'city']

class HasArtistAdmin(admin.ModelAdmin):
    model = HasArtist
    list_display = ['event_id', 'artist_id', 'artist_order']

class HasVenueAdmin(admin.ModelAdmin):
    model = HasVenue
    list_display = ['event_id', 'venue_id']

class FavEventAdmin(admin.ModelAdmin):
    model = FavEvent
    list_display = ['user_id', 'event_id']

class FavVenueAdmin(admin.ModelAdmin):
    model = FavVenue
    list_display = ['user_id', 'venue_id']

class LastUpdatedAdmin(admin.ModelAdmin):
    model = LastUpdated
    list_display = ['date', 'count']

# ------------------------------------------------------------------------------
# ADMIN INCLUSIONS
# ------------------------------------------------------------------------------

admin.site.register(Event, EventAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(HasArtist, HasArtistAdmin)
admin.site.register(HasVenue, HasVenueAdmin)
admin.site.register(FavEvent, FavEventAdmin)
admin.site.register(FavVenue, FavVenueAdmin)
admin.site.register(LastUpdated, LastUpdatedAdmin)
