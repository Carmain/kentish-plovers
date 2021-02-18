from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from website.utils.views_snippets import get_or_none
from website.models import Plover
from django.conf import settings
from django.http import HttpResponse
from website.forms import CodeForm, MetalForm

from weasyprint import HTML, CSS


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
            Plover, metal_ring=request.POST.get('metal_ring'))
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
        CSS(f'{static_path}node_modules/bootstrap/dist/css/bootstrap.min.css'),
        CSS(f'{static_path}css/pdf.css')
    ])

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{metal_ring}.pdf"'

    return response
