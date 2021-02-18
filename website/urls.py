from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/<str:method>', views.search, name='search'),
    path('search', views.search, name='search'),
    path('export-to-pdf/<metal_ring>', views.get_report, name='get_report'),
]
