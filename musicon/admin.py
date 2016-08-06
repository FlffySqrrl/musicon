from django.contrib import admin
from django.forms.models import BaseInlineFormSet

from models import *

# ------------------------------------------------------------------------------
# FORM CUSTOMIZATIONS
# ------------------------------------------------------------------------------

class RequiredInlineFormSet(BaseInlineFormSet):
    """
    Generate a required in-line form.
    """

    def _construct_form(self, i, **kwargs):
        """
        Overrides the method to set empty_permitted to False.
        """
        form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form


class HasArtistInline(admin.StackedInline):
    """
    Create HasArtist as a required in-line form.
    """
    model = HasArtist
    extra = 1
    formset = RequiredInlineFormSet


class HasVenueInline(admin.StackedInline):
    """
    Create HasVenue as a required in-line form.
    """
    model = HasVenue
    max_num = 1
    formset = RequiredInlineFormSet

# ------------------------------------------------------------------------------
# LIST CUSTOMIZATIONS
# ------------------------------------------------------------------------------

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


class UpdateAdmin(admin.ModelAdmin):
    model = Update
    list_display = ['date', 'note']

# ------------------------------------------------------------------------------
# APPLY CUSTOMIZATIONS
# ------------------------------------------------------------------------------

admin.site.register(Event, EventAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(HasArtist, HasArtistAdmin)
admin.site.register(HasVenue, HasVenueAdmin)
admin.site.register(FavEvent, FavEventAdmin)
admin.site.register(FavVenue, FavVenueAdmin)
admin.site.register(Update, UpdateAdmin)
