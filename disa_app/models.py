# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint, uuid
from django.conf import settings as project_settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponseRedirect

from django.db.models.signals import post_save
from django.dispatch import receiver


log = logging.getLogger(__name__)


class UserProfile( models.Model ):
    """
    - from <https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone>
    - reminder: if I know I'll need to access UserProfile entries...
      `users = User.objects.all().select_related('profile')`
      ...to minimize extra db queries.
    """
    user = models.OneToOneField( User, on_delete=models.SET_NULL, related_name='profile', null=True, blank=True )  # null=True so I can pre-create the user-profile entries if desired
    uu_id = models.UUIDField( default=uuid.uuid4, editable=False )
    email = models.EmailField( default='', blank=True )
    old_db_id = models.IntegerField( null=True, blank=True )
    last_logged_in = models.DateTimeField( null=True, blank=True )


## auto create and save UserProfile entries

@receiver( post_save, sender=User )
def create_user_profile(sender, instance, created, **kwargs):
    log.debug( f'starting create_user_profile(); created, ```{created}```; kwargs, ```{kwargs}```' )
    if created:  # meaning a User object was created
        log.debug( '`created` was True' )
        log.debug( f'instance, ```{pprint.pformat(instance.__dict__)}```' )
        try:  # see if there is an existing user-profile to associate -- this allows for user-profiles to be pre-created, and associated with the correct user-id when the user first logs in.
            prfl = UserProfile.objects.get( email=instance.email )
            if prfl.user != instance:
                prfl.user = instance
                prfl.save()
                log.debug( 'pre-existing user-profile has been matched to user' )
        except:
            log.exception( 'user has no matching user-profile, so one will be created (traceback follows; processing will continue)' )
            UserProfile.objects.create( user=instance )

@receiver( post_save, sender=User )
def save_user_profile(sender, instance, **kwargs):
    log.debug( f'starting save_user_profile(); kwargs, ```{kwargs}```' )
    log.debug( f'instance, ```{pprint.pformat(instance.__dict__)}```' )
    instance.profile.email = instance.email  # in case preferred shib email is updated.
    instance.profile.last_logged_in = datetime.datetime.now()
    instance.profile.save()
