# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
    assignee = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    history = HistoricalRecords()

    def __str__(self):
        return self.title


class Leader(models.Model):
    DEGREE = [('IT', 'IT'), ('ITM', 'ITM')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    eligibility = models.BooleanField(default=True, editable=True)
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
    enrollments = models.ManyToManyField(User, blank=True, related_name='draw_enrollments', through='DrawEnrollments')
    project = models.OneToOneField(Project, on_delete=models.PROTECT)
    finished = models.BooleanField(editable=False, default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.project.title

    def add_enrollment(self, leader):
        draw = DrawEnrollments.objects.get_or_create(leader=leader, draw=self)

    def remove_enrollment(self, leader):
        DrawEnrollments.objects.get(leader=leader, draw=self).delete()


class DrawEnrollments(models.Model):
    leader = models.ForeignKey(User, editable=False, on_delete=models.PROTECT)
    draw = models.ForeignKey(LotteryDraw, editable=False, on_delete=models.PROTECT)
    modified_time = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()