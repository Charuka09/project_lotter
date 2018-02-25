# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

from simple_history.models import HistoricalRecords

class Project(models.Model):
    company = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=50, blank=True)
    description = models.TextField(max_length=500, blank=True)
    time_added = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.title


class Leader(models.Model):
    DEGREE = [('IT', 'IT'), ('ITM', 'ITM')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    eligibility = models.BooleanField(default=True)
    degree = models.CharField(max_length=5, choices=DEGREE, default='IT')
    history = HistoricalRecords()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Leader.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.leader.save()


class LotteryDraw(models.Model):
    scheduled_time = models.DateTimeField(null=True, blank=True)
    winner = models.OneToOneField(User, editable=False, null=True, on_delete=models.PROTECT)
    enrollments = models.ManyToManyField(User, related_name='+')
    project = models.OneToOneField(Project, on_delete=models.PROTECT)
    finished = models.BooleanField(editable=False, default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.project.title

# TODO: Need to add enrollement audits
