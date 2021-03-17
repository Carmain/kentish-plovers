from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from website.utils.views_snippets import get_or_none, flush_session
from website.models import Plover, Observation, Location, Observer
from django.conf import settings
from django.http import HttpResponse
from website.forms import CodeForm, MetalForm, MapForm, PloverForm

from weasyprint import HTML, CSS
from os import getenv
from hashlib import sha1


def index(request):
    return render(request, 'website/home.html')


def search(request, method=None):
    if method is None or (method != 'code' and method != 'metal'):
        return redirect('search', method='code')

    plover = None
    form = None
    if method == 'code':
        plover = get_or_none(
            Plover, code=request.POST.get('code'),
            color=request.POST.get('color'))
        form = CodeForm
    else:
        plover = get_or_none(
            Plover, metal_ring=request.POST.get('metal_ring').strip())
        form = MetalForm

    data = {
        'not_found': False,
        'form_url': request.path
    }

    if request.method == 'POST':
        form = form(request.POST)

        if form.is_valid():
            if plover:
                data['plover'] = plover
            else:
                data['not_found'] = True
    else:
        form = form()

    data['form'] = form
    return render(request, 'website/search.html', data)


def get_report(request, metal_ring):
    plover = get_object_or_404(Plover, metal_ring=metal_ring)
    html_template = get_template('website/pdf_export.html')
    static_path = f'{settings.BASE_DIR}{settings.STATIC_URL}'

    pdf_file = HTML(
        string=html_template.render(
            {'plover': plover}).encode(encoding="UTF-8"),
        base_url=request.build_absolute_uri()
    ).write_pdf(stylesheets=[
        CSS('https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css'),
        CSS(f'{static_path}css/pdf.css')
    ])

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{metal_ring}.pdf"'

    return response


def map(request):
    flush_session(request, ('plovers', 'general'))

    if request.method == 'POST':
        map_form = MapForm(request.POST)

        # check whether it's valid:
        if map_form.is_valid():
            request.session['general'] = {
                'date': request.POST.get('date'),
                'last_name': request.POST.get('last_name').strip().upper(),
                'first_name': request.POST.get('first_name').strip().capitalize(),
                'town': request.POST.get('town').strip().capitalize(),
                'department': request.POST.get('department'),
                'country': request.POST.get('country').strip().capitalize(),
                'locality': request.POST.get('locality').strip().capitalize(),
                'coordinate_x': request.POST.get('coordinate_x'),
                'coordinate_y': request.POST.get('coordinate_y')
            }

            return redirect('observations')
    else:
        map_form = MapForm()

    return render(request, 'website/map.html', {
        'form': map_form,
        'google_map_api_key': getenv("GOOGLE_MAP_API_KEY")
    })


def remove_plover_from_session(request, id):
    plovers = request.session.get('plovers')
    plovers.pop(id, None)
    request.session['plovers'] = plovers

    return redirect('observations')


def observations(request):
    def add_plover_in_session(request, plover):
        if 'plovers' not in request.session or not request.session['plovers']:
            plovers = {}
        else:
            plovers = request.session['plovers']

        plovers[plover.get('id')] = plover
        request.session['plovers'] = plovers

    if request.session.get('general', False):
        data = {
            'general': request.session.get('general')
        }

        if request.method == 'POST':
            plover_form = PloverForm(request.POST)

            if plover_form.is_valid():
                form_data = plover_form.cleaned_data
                id = sha1(f"{form_data['code']}{form_data['color']}".encode())
                plover = {
                    'id': id.hexdigest(),
                    'code': form_data['code'],
                    'color': form_data['color'],
                    'sex': form_data['sex'],
                    'comment': form_data['comment'].strip(),
                }

                add_plover_in_session(request, plover)
                data['plovers'] = request.session.get('plovers').values()
        elif request.session.get('plovers', False):
            data['plovers'] = request.session.get('plovers').values()
            plover_form = PloverForm()
        else:
            plover_form = PloverForm()

        data['form'] = plover_form
        return render(request, 'website/observations.html', data)
    else:
        return redirect('map')


def validate_plovers(request):
    def parse_form_coords(coord):
        coord = coord.strip()
        return float(coord) if coord else None

    general = request.session.get('general')
    observations = request.session.get('plovers').values()
    accepted_observations = []
    rejected_observations = []

    location, location_exist = Location.objects.get_or_create(
        country=general.get('country'),
        town=general.get('town'),
        department=general.get('department'),
        locality=general.get('locality')
    )

    observer, observer_exist = Observer.objects.get_or_create(
        last_name=general.get('last_name'),
        first_name=general.get('first_name'),
        email=general.get('email')
    )

    for observation in observations:
        try:
            plover = Plover.objects.get(
                code=observation.get('code'),
                color=observation.get('color')
            )
        except Plover.DoesNotExist:
            plover = None

        if plover:
            observation_saved, created = Observation.objects.get_or_create(
                observer=observer,
                location=location,
                plover=plover,
                date=general.get('date'),
                supposed_sex=observation.get('sex'),
                comment=observation.get('comment'),
                coordinate_x=parse_form_coords(general.get('coordinate_x')),
                coordinate_y=parse_form_coords(general.get('coordinate_y'))
            )

            accepted_observations.append(plover)
        else:
            rejected_observations.append(observation)

    result = {
        'accepted_observations': accepted_observations,
        'rejected_observations': rejected_observations
    }

    return render(request, 'website/result.html', result)
