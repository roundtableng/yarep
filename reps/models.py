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

    @property
    def representative(self):
        return self.constituency.representative_set.all()[0]

    @property
    def senator(self):
        return self.district.senator_set.all()[0]


class Representative(models.Model):
    name = models.CharField(max_length=200)
    constituency = models.ForeignKey('Constituency')
    join_date = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    @property
    def is_active(self):
        if not self.join_date:
            return False
        return True


class Senator(models.Model):
    name = models.CharField(max_length=200)
    district = models.ForeignKey('District')
    join_date = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    @property
    def is_active(self):
        if not self.join_date:
            return False
        return True
