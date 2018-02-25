# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from lotter.models import LotteryDraw

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@login_required
def index(request):
    past_draws = LotteryDraw.objects.filter(finished=True).order_by('-scheduled_time')
    upcoming_draws = LotteryDraw.objects.filter(finished=False).order_by('-scheduled_time')
    return render(request, 'index.html', {'past_draws': past_draws, 'upcoming_draws': upcoming_draws, 'leader': request.user})

@login_required
@api_view(['GET'])
def add_enrollment(request, draw_id, status='enroll'):
    try:
        draw = LotteryDraw.objects.get(id=draw_id)
    except LotteryDraw.DoesNotExist:
        return JsonResponse({'msg': 'error'}, status=404)
    else:
        if status == 'enroll':
            draw.enrollments.add(request.user)
            draw.save()
        elif status == 'unenroll':
            draw.enrollments.remove(request.user)
            draw.save()
        else:
            return JsonResponse({'msg': 'error'}, status=404)
    return JsonResponse({'msg': 'success'}, status=200)