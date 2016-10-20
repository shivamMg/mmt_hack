import os

from django.core.management.base import BaseCommand

from countries.models import Continent, Country
from bahav.settings.common import DATA_DIR

CONTINENTS_FILE = os.path.join(DATA_DIR, 'continents.csv')
COUNTRIES_FILE = os.path.join(DATA_DIR, 'countries.csv')


def parse_line(line):
    rm_inverted_commas = lambda st: st.strip('"')
    line = line.rstrip().split(',')
    return map(rm_inverted_commas, line)


class Command(BaseCommand):
    help = 'Populate DB with Continents and Countries'

    def handle(self, *args, **options):
        self.stdout.write('Creating continents... ', ending='')
        with open(CONTINENTS_FILE, 'r') as fp:
            # Leave the header
            lines = fp.readlines()[1:]

            for line in lines:
                code, name = parse_line(line)
                Continent.objects.create(code=code, name=name)
            else:
                self.stdout.write(self.style.SUCCESS('DONE'))

        self.stdout.write('Creating countries... ', ending='')
        with open(COUNTRIES_FILE, 'r') as fp:
            # Leave the header
            lines = fp.readlines()[1:]

            for line in lines:
                code, name, _, continent_code = parse_line(line)
                continent = Continent.objects.get(code=continent_code)
                Country.objects.create(code=code,
                                       name=name,
                                       continent=continent)
            else:
                self.stdout.write(self.style.SUCCESS('DONE'))
