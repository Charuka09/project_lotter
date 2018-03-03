from datetime import datetime
from random import choice

from django.utils import timezone
from django.contrib.auth.models import User

from background_task import background
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


@background(schedule=60)
def start_draw(draw_id=None):
    from lotter.models import ProjectDraw
    if draw_id is None:
        return True
    draw = ProjectDraw.objects.get(id=draw_id)
    projects = draw.projects.all()
    aware_datetime = datetime.now()
    timezone.get_current_timezone().localize(aware_datetime)
    results = []

    for p in projects:
        eligibles = p.enrollments.filter(leader__eligibility=True)
        if eligibles:
            winner = choice(eligibles)

            winner.leader.eligibility = False
            winner.save()
            p.assignee = winner
            p.save()

            results.append({'project_id':p.id,'project_title': p.title, 'eligibles': eligibles, 'winner': winner})
        else:
            results.append({'project_id': p.id, 'project_title': p.title, 'eligibles': eligibles, 'winner': ''})
    draw.finished = True
    draw.save()
    r = {'draw_id': draw_id, 'time': aware_datetime, 'results': results}
    logger.debug(r)
    print (r)
    send_results_email(r)

def send_password_email(first_name, pw, to):
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import get_template
    from django.template import Context
    plaintext = get_template('email/send_password.txt')
    htmly = get_template('email/send_password.html')

    d = {'first_name': first_name, 'password': pw}

    subject, from_email = 'Project Selector Account Activated', 'fitbatch16@gmail.com'
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    return msg.send()

def send_results_email(result):
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import get_template
    from django.template import Context
    plaintext = get_template('email/send_password.txt')
    htmly = get_template('email/send_password.html')
    print (htmly)
    logger.debug(htmly)
    # from django.core import mail
    # connection = mail.get_connection()
    # connection.open()
    # subject, from_email = 'Project Selector - %s Draw Results'%str(result.get('time','')), 'fitbatch16@gmail.com'
    # for p in result.get('results',[]):
    #     text_content = plaintext.render(p)
    #     html_content = htmly.render(p)
    #     msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    #     msg.attach_alternative(html_content, "text/html")
    #     msg.send()
    #
    #
    # connection.close()