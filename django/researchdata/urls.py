from django.urls import path
from . import views, apps

app_name = apps.app_name

urlpatterns = [

    # Export Data
    path('export/csv/', views.export_csv, name='export-csv'),

]
