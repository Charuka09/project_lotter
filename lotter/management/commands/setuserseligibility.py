from django.core.management import BaseCommand, CommandError
from django.contrib.auth.models import User


# The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):


    # Show this when the user types help
    help = "Set users eligibility"

    def add_arguments(self, parser):
        parser.add_argument(
            '--degree', dest='degree', required=True,
            help='the url to process',
        )
        parser.add_argument(
            '--status', dest='status', required=True,
            help='the url to process',
        )

    # A command must define handle()
    def handle(self, *args, **options):
        users = User.objects.filter(leader__degree=options['degree'])
        for u in users:
            try:
                u.leader.eligibility = True if options['status'] == 'true' or options['status'] == 'True' else False
                u.save()
            except Exception as ex:
                print 'Error in modifying ' + u.username