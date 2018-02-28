# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.decorators import api_view

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test

from lotter.models import ProjectDraw, Project
from utils import start_draw
from datetime import datetime, date, time
from django.utils import timezone
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


@login_required
@user_passes_test(lambda u: not u.is_superuser)
def index(request):
    next_draw = ProjectDraw.objects.filter(finished=False).order_by('-scheduled_date').first()
    projects = next_draw.projects.all().order_by('id') if next_draw else []
    return render(request, 'index.html', {'next_draw': next_draw, 'projects':projects, 'user': request.user})


@login_required
@user_passes_test(lambda u: not u.is_superuser)
@api_view(['GET'])
def modify_enrollments(request, pid, status='add'):
    try:
        project = Project.objects.get(id=pid)
    except ProjectDraw.DoesNotExist:
        return JsonResponse({'msg': 'error'}, status=404)
    else:
        if status == 'add':
            project.enrollments.add(request.user)
            project.save()
        elif status == 'remove':
            project.enrollments.remove(request.user)
            project.save()
        else:
            return JsonResponse({'msg': 'error'}, status=404)
    return JsonResponse({'msg': 'success'}, status=200)


#@user_passes_test(lambda u: u.is_superuser)
@api_view(['GET'])
def start_project_draw(request, draw_id):
    results = None
    logger.debug('start_project_draw called')
    try:
        draw = ProjectDraw.objects.get(id=draw_id)
        aware_datetime = datetime.combine(draw.scheduled_date, draw.scheduled_time)
        timezone.get_current_timezone().localize(aware_datetime)
        print aware_datetime
        start_draw(1, schedule=aware_datetime)
    except Exception as ex:
        return JsonResponse({'msg': 'error', 'results': []}, status=404)

    return JsonResponse({'msg': 'success', 'results': results})


def all_projects(request):
    projects = Project.objects.all()
    return render(request, 'all_projects.html',{'projects':projects})