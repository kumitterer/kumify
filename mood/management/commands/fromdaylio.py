from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

from mood.models import Status, Mood, Activity, StatusActivity

import csv
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d %I:%M %p'

class Command(BaseCommand):
    help = 'Import .csv from Daylio'

    def add_arguments(self, parser):
        parser.add_argument('username')
        parser.add_argument('path')

    def handle(self, *args, **options):
        try:
            user = get_user_model().objects.get(username=options["username"])
            with open(options["path"], mode='r', encoding='utf-8-sig') as infile:
                reader = csv.DictReader(infile)
                for row in reader:
                    timestamp = datetime.strptime("%s %s" % (row["full_date"], row["time"]), DATE_FORMAT)
                    activities = [a.strip() for a in row["activities"].split("|")]

                    try:
                        mood = Mood.objects.get(user=user, name__iexact=row["mood"])
                    except Mood.DoesNotExist:
                        mood = Mood.objects.create(user=user, name=row["mood"], value=0)

                    status = Status.objects.create(user=user, timestamp=timestamp, mood=mood, title=row["note_title"], text=row["note"])

                    for activity in activities:
                        if activity:
                            try:
                                aobj = Activity.objects.get(user=user, name__iexact=activity)
                            except Activity.DoesNotExist:
                                aobj = Activity.objects.create(user=user, name=activity)

                            StatusActivity.objects.create(status=status, activity=aobj)

        except FileNotFoundError:
            raise CommandError('File "%s" does not exist' % options["path"])
        except get_user_model().DoesNotExist:
            raise CommandError('User "%s" does not exist' % options["user"])

        self.stdout.write(self.style.SUCCESS('Successfully imported data for user "%s"' % options["username"]))