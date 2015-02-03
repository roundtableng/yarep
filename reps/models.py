from django.db import models


class State(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Constituency(models.Model):
    name = models.CharField(max_length=255)
    state = models.ForeignKey('State')

    class Meta:
        verbose_name_plural = 'Constituencies'

    def __unicode__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=255)
    state = models.ForeignKey('State')

    def __unicode__(self):
        return self.name


class LGA(models.Model):
    name = models.CharField(max_length=200)
    state = models.ForeignKey('State')
    constituency = models.ForeignKey('Constituency')
    district = models.ForeignKey('District')

    def __unicode__(self):
        return self.name


class Representative(models.Model):
    name = models.CharField(max_length=200)
    constituency = models.ForeignKey('Constituency')

    def __unicode__(self):
        return self.name


class Senator(models.Model):
    name = models.CharField(max_length=200)
    district = models.ForeignKey('District')

    def __unicode__(self):
        return self.name
