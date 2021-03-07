from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from website.models import Plover, Observation, Observer, Location


class DefaultAdminModel(admin.ModelAdmin):
    list_per_page = 25
    ordering = ('id',)


class PloverAdmin(DefaultAdminModel):
    list_display = ('id', 'metal_ring', 'code', 'color', 'sex', 'age')
    search_fields = ('code', 'color', 'metal_ring')
    list_filter = ('code', 'color')


class ObservationAdmin(DefaultAdminModel):
    list_display = ('id', 'date', 'observer', 'plover', 'location',
                    'supposed_sex', 'coordinate_x', 'coordinate_y', 'comment')
    search_fields = ('observer', 'plover', 'date', 'location')
    list_filter = ('plover',)
    ordering = ('-date',)


class ObserverAdmin(DefaultAdminModel):
    list_display = ('id', 'last_name', 'first_name', 'email')
    list_filter = ('last_name', 'first_name')
    search_fields = ('last_name', 'first_name', 'email')


class LocationAdmin(DefaultAdminModel):
    list_display = ('id', 'country', 'town', 'department', 'locality')
    list_filter = ('country', 'town', 'department')
    search_fields = ('country', 'town', 'department')


admin.site.site_header = _('Administration')
admin.site.site_title = _('Kentish plovers')

admin.site.register(Plover, PloverAdmin)
admin.site.register(Observation, ObservationAdmin)
admin.site.register(Observer, ObserverAdmin)
admin.site.register(Location, LocationAdmin)
