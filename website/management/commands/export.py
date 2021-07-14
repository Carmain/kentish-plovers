from django.core.management.base import BaseCommand
from website.models import Observation
from website.templatetags.template_filters import color_to_string, sex_to_string
from django.utils import translation
import xlsxwriter


class Command(BaseCommand):
    def handle(self, *args, **options):
        translation.activate('fr')

        workbook = xlsxwriter.Workbook('gravelots.xlsx')
        bold = workbook.add_format({'bold': True})
        date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
        time_format = workbook.add_format({'num_format': 'hh:mm'})

        worksheet = workbook.add_worksheet('observations')

        observations = Observation.objects.all()
        headers = [
            'Code',
            'Couleur',
            'Bague métal',
            'Sexe',
            'Bagueur',
            'Lieu',
            'Année de baguage',
            'Date de bagugage',
            'Heure de baguage',
            'âge du gravelot',
            'Observateur',
            'Lieu d\'observation',
            'Date d\'observation',
            'Sexe supposé',
            'Coordonnée X',
            'Coordonnée Y',
            'Commentaire'
        ]
        for key, header in enumerate(headers):
            worksheet.write(0, key, header, bold)

        row = 1
        col = 0
        for observation in observations:
            print(observation)
            plover = observation.plover

            worksheet.write(row, col, plover.code)
            worksheet.write(row, col + 1, plover.get_color_display())
            worksheet.write(row, col + 2, plover.metal_ring)
            worksheet.write(row, col + 3, plover.get_sex_display())
            worksheet.write(row, col + 4, plover.bander.full_name)
            worksheet.write(row, col + 5, plover.location.minimal_location)
            worksheet.write(row, col + 6, plover.banding_year)
            worksheet.write(row, col + 7, plover.banding_date, date_format)
            worksheet.write(row, col + 8, plover.banding_time, time_format)
            worksheet.write(row, col + 9, plover.age)
            worksheet.write(
                row, col + 10, observation.observer.full_name)
            worksheet.write(
                row, col + 11, observation.location.minimal_location)
            worksheet.write(
                row, col + 12, observation.date.strftime("%d/%m/%Y"))
            worksheet.write(row, col + 13, observation.supposed_sex)
            worksheet.write(row, col + 14, observation.coordinate_x)
            worksheet.write(row, col + 15, observation.coordinate_y)
            worksheet.write(row, col + 16, observation.comment)

            row += 1
        workbook.close()
