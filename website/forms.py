from django import forms
from website.models import COLOR_CHOICES
from django.utils.translation import ugettext_lazy as _


class InputsTemplates():

    @staticmethod
    def choicefield_input(label, choices):
        return forms.ChoiceField(
            label=label,
            choices=choices,
            widget=forms.Select(attrs={'class': 'form-control'})
        )

    @staticmethod
    def charfield_template(label, max_length, required=True):
        return forms.CharField(
            label=label,
            required=required,
            max_length=max_length,
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )

    @staticmethod
    def code_input(required=True):
        return forms.IntegerField(
            localize=False,
            label=_('Code'),
            required=required,
            widget=forms.NumberInput(attrs={'class': 'form-control'})
        )

    @staticmethod
    def emailfield_template(label, max_length, required=True):
        return forms.EmailField(
            label=label,
            required=required,
            max_length=max_length,
            widget=forms.EmailInput(attrs={'class': 'form-control'})
        )

    @staticmethod
    def coordinatefield_template(label):
        return forms.FloatField(
            label=label,
            required=False,
            widget=forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': True
            })
        )


class CodeForm(forms.Form):
    code = InputsTemplates.code_input()
    color = InputsTemplates.choicefield_input(_('Color'), COLOR_CHOICES)


class MetalForm(forms.Form):
    metal_ring = InputsTemplates.charfield_template(_('Metal ring'), 10)


class MapForm(forms.Form):
    date = forms.DateField(
        label=_('Date'),
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    last_name = InputsTemplates.charfield_template(_('Last name'), 255)
    first_name = InputsTemplates.charfield_template(_('First name'), 255)
    email = InputsTemplates.emailfield_template(_('Email'), 255,)
    town = InputsTemplates.charfield_template(_('Town'), 255)
    department = InputsTemplates.charfield_template(_('Department'), 255)
    country = InputsTemplates.charfield_template(_('Country'), 255)
    locality = InputsTemplates.charfield_template(_('Locality'), 255, False)

    coordinate_x = InputsTemplates.coordinatefield_template(_('X coordinate'))
    coordinate_y = InputsTemplates.coordinatefield_template(_('Y coordinate'))
