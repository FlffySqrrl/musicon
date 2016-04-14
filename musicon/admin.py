from django.contrib import admin

from forms import *
from models import *

class Has_ArtistInline(admin.StackedInline):
    """
    Includes Has_Artist as a required in-line form.
    """
    model = Has_Artist
    extra = 1
    formset = RequiredInlineFormSet

class Has_VenueInline(admin.StackedInline):
    """
    Includes Has_Venue as a required in-line form.
    """
    model = Has_Venue
    max_num = 1
    formset = RequiredInlineFormSet

class EventAdmin(admin.ModelAdmin):
    """
    Options for the add event form.
    """
    inlines = [Has_ArtistInline, Has_VenueInline]

admin.site.register(Event, EventAdmin)
admin.site.register(Artist)
admin.site.register(Venue)
admin.site.register(Has_Artist)
admin.site.register(Has_Venue)
admin.site.register(Fav_Event)
admin.site.register(Fav_Venue)
admin.site.register(Last_Updated)
