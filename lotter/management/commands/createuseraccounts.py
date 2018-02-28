from django.core.management import BaseCommand, CommandError
from django.contrib.auth.models import User
from lotter.utils import send_password_email

# The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):


    # Show this when the user types help
    help = "Create user accounts using given file"

    def add_arguments(self, parser):
        parser.add_argument(
            '--file', dest='file', required=True,
            help='the url to process',
        )

    # A command must define handle()
    def handle(self, *args, **options):
        lines = []
        try:
            with open(options['file']) as f:
                lines = f.readlines()
        except Exception:
            raise CommandError('Error in reading file')
        users = []
        for l in lines:
            users.append([i.strip()for i in l.strip().split(',')])
        for u in  users:
            try:
                pw = generate_password()
                user = User.objects.create_user(username=u[3],
                                                email=u[4],
                                                first_name=u[2],
                                                last_name=u[1],
                                                password=pw)
                user.save()
                user = User.objects.get(username=u[3])
                user.leader.degree = u[0]
                user.leader.phone = u[5]
                user.save()
                print user.username + ' '+pw
                send_password_email(u[2], pw, u[4])
            except Exception as ex:
                print 'Error in creating ' + u[3]


def generate_password(length=10):
    import os, random, string
    chars = string.ascii_letters + string.digits + '!@#$%&*'
    random.seed = (os.urandom(1024))
    return ''.join(random.choice(chars) for i in range(length))