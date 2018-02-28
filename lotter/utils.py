from datetime import datetime
from random import choice

from lotter.models import ProjectDraw
from django.contrib.auth.models import User

from background_task import background
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


@background(schedule=60)
def start_draw(draw_id=None):
    if draw_id is None:
        return True
    draw = ProjectDraw.objects.get(id=draw_id)
    projects = draw.projects.all()
    results = []
    for p in projects:
        eligibles = p.enrollments.filter(leader__eligibility=True)
        winner = choice(eligibles)

        winner.eligibility = False
        winner.save()
        p.assignee = winner
        p.save()
        draw.finished = True
        draw.save()
        results.append({'project_id':p.id,'project_title': p.title, 'eligibles': eligibles, 'winner':winner})
    logger.debug(results)


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


def send_password_email(first_name, pw, to):
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import get_template
    from django.template import Context
    plaintext = get_template('email/send_password.txt')
    htmly = get_template('email/send_password.html')

    d = Context({'first_name': first_name, 'password': pw})

    subject, from_email = 'Project Selector Account Activated', 'fitbatch16@gmail.com'
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()