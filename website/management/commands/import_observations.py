from django.core.management.base import BaseCommand
from website.models import Plover, Observation, Location, Observer

import csv


class Command(BaseCommand):
    def handle(self, *args, **options):

        def parse_form_coords(coord):
            coord = coord.strip()
            return float(coord.replace(',', '.'))

        with open('import.csv', 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            for row in reader:
                location, location_created = Location.objects.get_or_create(
                    country="France",
                    town=row[1],
                    department=row[3],
                    locality=row[2]
                )

                observer, observer_created = Observer.objects.get_or_create(
                    last_name=row[9],
                    first_name=row[10],
                    email=None
                )

                try:
                    plover = Plover.objects.get(
                        metal_ring=row[6]
                    )
                except Plover.DoesNotExist:
                    plover = None

                if plover:
                    observation_saved, created = Observation.objects.get_or_create(
                        observer=observer,
                        location=location,
                        plover=plover,
                        date=row[0],
                        supposed_sex='U',
                        comment=None,
                        coordinate_x=parse_form_coords(row[4]),
                        coordinate_y=parse_form_coords(row[5])
                    )
                    
                    if created:
                        print("CREATED", observation_saved)
                    else:
                        print("SAVED", observation_saved)
                    
                else:
                    print("REJECTION", row)
