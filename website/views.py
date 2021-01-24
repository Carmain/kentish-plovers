from django.shortcuts import render, redirect
from website.utils.views_snippets import get_or_none
from website.models import Plover
from website.forms import CodeForm, MetalForm


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
