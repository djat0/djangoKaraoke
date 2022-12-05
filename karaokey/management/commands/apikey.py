from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'set the api key for youtube data api v3'

    def add_arguments(self, parser):
        parser.add_argument('apikey', nargs='+')

    def handle(self, *args, **options):
        apikey = options['apikey'][0]
        print(apikey)
        with open("apikey.txt", "w") as f:
            f.write(apikey)
            print("api key registered")