from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

#-------------------------------------------------------------------------------
# Main entity sets.
#-------------------------------------------------------------------------------

class Event(models.Model):
    EVENT_TYPES = (
        ('Concert', 'Concert'),
        ('Festival', 'Festival'),
    )
    eID = models.IntegerField('Event ID', primary_key = True)
    eName = models.CharField('Event name', max_length = 200, null = True)
    eType = models.CharField('Event type', choices = EVENT_TYPES, max_length = 20, null = True)
    eUrl = models.CharField('Songkick page', max_length = 200, null = True)
    startDate = models.DateField('Date', null = True)
    startTime = models.CharField('Time', max_length = 10, null = True)
    popularity = models.FloatField(null = True, blank = True)
    status = models.CharField(max_length = 100, null = True, blank = True)
    ageRestriction = models.CharField('Age restriction', max_length = 100, null = True, blank = True)

    class Meta:
        ordering = ['startDate']
    
    def __unicode__(self):
        return self.eName

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['eName']

class Artist(models.Model):
    aID = models.IntegerField('Artist ID', primary_key = True)
    aName = models.CharField('Artist name', max_length = 100, null = True)
    aUrl = models.CharField('Songkick page', max_length = 200, null = True, blank = True)

    class Meta:
        ordering = ['aName']

    def __unicode__(self):
        return self.aName

class Venue(models.Model):
    vID = models.IntegerField('Venue ID', primary_key = True)
    vName = models.CharField('Venue name', max_length = 100, null = True)
    city = models.CharField(max_length = 100, null = True, blank = True)
    lat = models.FloatField('Latitude', null = True)
    lon = models.FloatField('Longitude', null = True)

    class Meta:
        ordering = ['vName']

    def __unicode__(self):
        return self.vName

class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ['lat', 'lon']

#-------------------------------------------------------------------------------
# Relationships between main entity sets.
#-------------------------------------------------------------------------------

class Has_Artist(models.Model):
    ARTIST_TYPES = (
        ('headline', 'headline'),
        ('support', 'support'),
    )
    eID = models.ForeignKey(Event, verbose_name = u'Event ID')
    aID = models.ForeignKey(Artist, verbose_name = u'Artist ID')
    aType = models.CharField('Artist type', choices = ARTIST_TYPES, max_length = 20, null = True)

    class Meta:
        ordering = ['eID']
        unique_together = ('eID', 'aID',)
        verbose_name_plural = 'Has_Artist'

    def __unicode__(self):
        return str(self.eID_id) + " - " + str(self.aID.aName) + " - " + str(self.aType)

class Has_Venue(models.Model):
    eID = models.ForeignKey(Event, verbose_name = u'Event ID')
    vID = models.ForeignKey(Venue, verbose_name = u'Venue ID')
    
    class Meta:
        ordering = ['eID']
        unique_together = ('eID', 'vID',)
        verbose_name_plural = 'Has_Venue'

    def __unicode__(self):
        return str(self.eID_id) + " - " + str(self.vID.vName)

#-------------------------------------------------------------------------------
# Relationships between users and main entity sets.
#-------------------------------------------------------------------------------

class Fav_Event(models.Model):
    uID = models.ForeignKey(User, verbose_name = u'User ID')
    eID = models.ForeignKey(Event, verbose_name = u'Event ID')

    class Meta:
        ordering = ['uID']
        unique_together = ('uID', 'eID',)
        verbose_name_plural = 'Fav_Events'

    def __unicode__(self):
        return str(self.uID.username) + " - " + str(self.eID_id)

class Fav_Venue(models.Model):
    uID = models.ForeignKey(User, verbose_name = u'User ID')
    vID = models.ForeignKey(Venue, verbose_name = u'Venue ID')

    class Meta:
        ordering = ['uID']
        unique_together = ('uID', 'vID',)
        verbose_name_plural = 'Fav_Venues'

    def __unicode__(self):
        return str(self.uID.username) + " - " + str(self.vID.vName)

#-------------------------------------------------------------------------------
# Keeps track of when the database was last updated.
#-------------------------------------------------------------------------------

class Last_Updated(models.Model):
    date = models.DateField()
    updateCount = models.IntegerField('Update count')
    
    class Meta:
        verbose_name_plural = 'Last_Updated'

    def __unicode__(self):
        return u'%s' % self.date
