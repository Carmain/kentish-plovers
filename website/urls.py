from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/<str:method>', views.search, name='search'),
    path('search', views.search, name='search'),
    path('export-to-pdf/<metal_ring>', views.get_report, name='get_report'),
    path('map', views.map, name='map'),
    path('observations', views.observations, name='observations'),
    path('remove-plover/<str:id>', views.remove_plover_from_session,
         name='remove_plover_from_session'),
    path('validation', views.validate_plovers, name='validate_plovers'),
]
