from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from reps.models import LGA


class Account(models.Model):
    user = models.OneToOneField(User)
    lga = models.ForeignKey(LGA, null=True)

    def __unicode__(self):
        return self.user.username


def user_creation_callback(sender, **kwargs):
    if kwargs['created']:
        try:
            account, _ = Account.objects.get_or_create(user=kwargs['instance'])
        except:
            pass


post_save.connect(user_creation_callback, sender=User)
