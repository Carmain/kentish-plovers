from django.core.management.base import BaseCommand
from old_website.models import KentishPlover, Observations
from website.models import Location, Observer, Plover, Observation

from datetime import datetime

OLD_COLORS = {
    "JAUNE": "Y",
    "ROUGE": "R",
    "VERT": "G",
    "ROSE": "P",
    "BLANC": "W"
}

OLD_SEXES = {
    "?": "U",
    "M": "M",
    "F": "F",
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        plovers = KentishPlover.objects.using("old_website").all()
        for plover in plovers:
            locality = plover.locality.strip().capitalize(
            ) if plover.locality is not None else None
            location, location_created = Location.objects.using("default").get_or_create(
                country="France",
                town=plover.town.strip().upper(),
                department=plover.department,
                locality=locality
            )
            observer, observer_created = Observer.objects.using("default").get_or_create(
                last_name=plover.observer.strip().upper(),
                first_name=plover.first_name_observer.strip().capitalize(),
                email=None,
                is_bander=True
            )

            if plover.action == "B":
                time = None
                if plover.banding_time != '' and plover.banding_time is not None:
                    time = plover.banding_time.lower().replace("h", ":")
                    time = datetime.strptime(time, "%H:%M")

                new_plover, new_plover_created = Plover.objects.using("default").get_or_create(
                    bander=observer,
                    location=location,
                    banding_year=plover.banding_year,
                    metal_ring=plover.metal_ring.strip(),
                    code=plover.number,
                    color=OLD_COLORS.get(plover.color),
                    sex=OLD_SEXES.get(plover.sex),
                    age=plover.age,
                    banding_date=datetime.strptime(
                        plover.date, "%d/%m/%Y") if plover.date != "" else None,
                    banding_time=time,
                )
                print(new_plover)

        observations = Observations.objects.using("old_website").all()
        for observation in observations:
            observer, observer_created = Observer.objects.get_or_create(
                last_name=observation.last_name.strip().upper(),
                first_name=observation.first_name.strip().capitalize(),
                email=None
            )
            locality = observation.locality.strip().capitalize(
            ) if observation.locality is not None else None
            location, location_created = Location.objects.using("default").get_or_create(
                country="France",
                town=observation.town.strip().upper(),
                department=observation.department.strip(),
                locality=locality,
            )

            try:
                old_plover = plovers = KentishPlover.objects.using(
                    "old_website").get(id_kentish_plover=observation.fk_plover)
                plover = Plover.objects.using("default").get(
                    metal_ring=old_plover.metal_ring.strip())

                comment = observation.comment.strip() if observation.comment is not None else None
                observation, observation_created = Observation.objects.get_or_create(
                    observer=observer,
                    plover=plover,
                    location=location,
                    date=observation.date,
                    supposed_sex=observation.sex,
                    coordinate_x=observation.map_x if observation.map_x != '' else None,
                    coordinate_y=observation.map_y if observation.map_y != '' else None,
                    comment=comment,
                )
                print(observation)
            except KentishPlover.DoesNotExist:
                print("ERROR : WRONG OLD KENISH PLOVER")
