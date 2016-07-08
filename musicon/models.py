from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

# ------------------------------------------------------------------------------
# MAIN ENTITY SETS
# ------------------------------------------------------------------------------

class Event(models.Model):
    EVENT_TYPES = (
        ('Concert', 'Concert'),
        ('Festival', 'Festival'),
    )

    event_id   = models.IntegerField('Event ID', primary_key=True)
    event_name = models.CharField('Event Name', max_length=200, null=True)
    event_type = models.CharField('Event Type', max_length=10, null=True, choices=EVENT_TYPES)
    event_url  = models.CharField('Event URL', max_length=200, null=True, blank=True)
    start_date = models.DateField('Start Date', null=True)
    start_time = models.CharField('Start Time', max_length=10, null=True)
    status     = models.CharField('Status', max_length=100, null=True, blank=True)
    popularity = models.FloatField('Popularity', null=True, blank=True)
    age_limit  = models.CharField('Age Limit', max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['start_date', 'start_time']

    def __unicode__(self):
        return self.event_name

class Artist(models.Model):
    artist_id   = models.IntegerField('Artist ID', primary_key=True)
    artist_name = models.CharField('Artist Name', max_length=100, null=True)
    artist_url  = models.CharField('Artist URL', max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['artist_name']

    def __unicode__(self):
        return self.artist_name

class Venue(models.Model):
    venue_id   = models.IntegerField('Venue ID', primary_key=True)
    venue_name = models.CharField('Venue Name', max_length=100, null=True)
    venue_url  = models.CharField('Venue URL', max_length=200, null=True, blank=True)
    city       = models.CharField('City', max_length=100, null=True)
    lat        = models.FloatField('Latitude', null=True)
    lng        = models.FloatField('Longitude', null=True)

    class Meta:
        ordering = ['venue_name']

    def __unicode__(self):
        return self.venue_name

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['event_name']

class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ['lat', 'lng']

# ------------------------------------------------------------------------------
# MAIN-MAIN RELATIONSHIP SETS
# ------------------------------------------------------------------------------

class HasArtist(models.Model):
    event_id     = models.ForeignKey(Event, verbose_name='Event')
    artist_id    = models.ForeignKey(Artist, verbose_name='Artist')
    artist_order = models.IntegerField('Performance Order')

    class Meta:
        ordering = ['event_id', 'artist_order']
        unique_together = ('event_id', 'artist_id')
        verbose_name_plural = 'HasArtist'

    def __unicode__(self):
        return 'Event ' + str(self.event_id_id) + ' - #' + str(self.artist_order) + ' ' + str(self.artist_id.artist_name)

class HasVenue(models.Model):
    event_id = models.ForeignKey(Event, verbose_name='Event')
    venue_id = models.ForeignKey(Venue, verbose_name='Venue')

    class Meta:
        ordering = ['event_id']
        unique_together = ('event_id', 'venue_id')
        verbose_name_plural = 'HasVenue'

    def __unicode__(self):
        return 'Event ' + str(self.event_id_id) + ' at ' + str(self.venue_id.venue_name)

# ------------------------------------------------------------------------------
# USER-MAIN RELATIONSHIP SETS
# ------------------------------------------------------------------------------

class FavEvent(models.Model):
    user_id  = models.ForeignKey(User, verbose_name='User')
    event_id = models.ForeignKey(Event, verbose_name='Event')

    class Meta:
        ordering = ['user_id']
        unique_together = ('user_id', 'event_id')
        verbose_name_plural = 'FavEvents'

    def __unicode__(self):
        return str(self.user_id.username) + ' - ' + str(self.event_id.event_name)

class FavVenue(models.Model):
    user_id  = models.ForeignKey(User, verbose_name='User')
    venue_id = models.ForeignKey(Venue, verbose_name='Venue')

    class Meta:
        ordering = ['user_id']
        unique_together = ('user_id', 'venue_id')
        verbose_name_plural = 'FavVenues'

    def __unicode__(self):
        return str(self.user_id.username) + ' - ' + str(self.venue_id.venue_name)

# ------------------------------------------------------------------------------
# DATABASE UPDATES TRACKER
# ------------------------------------------------------------------------------

class Update(models.Model):
    date  = models.DateField()
    note  = models.CharField('Note', max_length=100, null=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Updates'

    def __unicode__(self):
        return str(self.date)
