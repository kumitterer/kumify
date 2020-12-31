from django.core.management.base import BaseCommand, CommandError

from dbsettings.functions import dbsettings

class Command(BaseCommand):
    help = 'Set your Telegram token'

    def handle(self, *args, **options):
        token = input("Enter the token you received from the @BotFather: ")

        dbsettings["TELEGRAM_TOKEN"] = token

        self.stdout.write(self.style.SUCCESS('Telegram token set successfully.'))