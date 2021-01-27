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


class CodeForm(forms.Form):
    code = InputsTemplates.code_input()
    color = InputsTemplates.choicefield_input(_('Color'), COLOR_CHOICES)


class MetalForm(forms.Form):
    metal_ring = InputsTemplates.charfield_template(_('Metal ring'), 10)
