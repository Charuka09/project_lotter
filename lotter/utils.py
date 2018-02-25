from datetime import datetime
from random import choice

from lotter.models import LotteryDraw
from django.contrib.auth.models import User


def start_draw(draw_id=None):
    if draw_id is None:
        return True
    draw = LotteryDraw.objects.get(id=draw_id)
    time = datetime.now()
    enrolls = draw.enrollments.all()

    elegibiles = enrolls.filter(leader__eligibility=True)
    not_eligibles = enrolls.filter(leader__eligibility=False)

    winner = choice(elegibiles)
    return winner


def make_not_eligible_all(degree='IT'):
    leaders = User.objects.filter(leader__degree=degree)
    for l in leaders:
        try:
            l.leader.eligibility = False
            l.save()
        except Exception as ex:
            print ex
            return False
    return True

