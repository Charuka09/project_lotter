# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.decorators import api_view

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test

from lotter.models import LotteryDraw
from utils import start_draw


@login_required
def index(request):
    past_draws = LotteryDraw.objects.filter(finished=True).order_by('-scheduled_time')
    upcoming_draws = LotteryDraw.objects.filter(finished=False).order_by('-scheduled_time')
    return render(request, 'index.html', {'past_draws': past_draws, 'upcoming_draws': upcoming_draws, 'leader': request.user})


@login_required
@api_view(['GET'])
def modify_enrollments(request, draw_id, status='add'):
    try:
        draw = LotteryDraw.objects.get(id=draw_id)
    except LotteryDraw.DoesNotExist:
        return JsonResponse({'msg': 'error'}, status=404)
    else:
        if status == 'add':
            draw.add_enrollment(request.user)
        elif status == 'remove':
            draw.remove_enrollment(request.user)
        else:
            return JsonResponse({'msg': 'error'}, status=404)
    return JsonResponse({'msg': 'success'}, status=200)


@user_passes_test(lambda u: u.is_superuser)
@api_view(['GET'])
def start_project_draw(request, draw_id):
    winner = None
    try:
        winner = start_draw(draw_id)
    except Exception as ex:
        return JsonResponse({'msg': 'error'}, status=404)

    return JsonResponse({'msg': 'success', 'winner': winner.first_name + ' '+ winner.last_name})
