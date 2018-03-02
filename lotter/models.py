# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

from simple_history.models import HistoricalRecords
from utils import start_draw
from datetime import datetime, date, time
from django.utils import timezone
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Project(models.Model):
    company = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=50, blank=True)
    description = models.TextField(max_length=500, blank=True)
    time_added = models.DateTimeField(auto_now=True)
    assignee = models.ForeignKey(User, null=True, blank=True, editable=False, on_delete=models.SET_NULL)
    enrollments = models.ManyToManyField(User, editable=False, blank=True, related_name='project_enrollments')
    history = HistoricalRecords()

    def __str__(self):
        return self.title


class Leader(models.Model):
    DEGREE = [('IT', 'IT'), ('ITM', 'ITM')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    eligibility = models.BooleanField(default=True, editable=True)
    degree = models.CharField(max_length=5, choices=DEGREE, default='IT')
    phone = models.CharField(max_length=20, blank=True, null=True)
    history = HistoricalRecords()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Leader.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.leader.save()


class ProjectDraw(models.Model):
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    finished = models.BooleanField(default=False, editable=False)
    projects = models.ManyToManyField(Project, editable=True, blank=True, related_name='+')


@receiver(post_save, sender='lotter.ProjectDraw')
def add_scheduled_draw(sender, instance=None, created=None, update_fields=None, **kwargs):
    if created:
        aware_datetime = datetime.combine(instance.scheduled_date,instance.scheduled_time)
        timezone.get_current_timezone().localize(aware_datetime)
        start_draw(instance.id,schedule=aware_datetime)
        logger.debug('Scheduled draw added in '+str(aware_datetime))

    else:
        pass
    #TODO: Need add this functionality, What happens if we want to change the date time of the draw

