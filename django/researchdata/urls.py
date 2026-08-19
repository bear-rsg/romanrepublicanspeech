from django.urls import path
from . import views, apps

app_name = apps.app_name

urlpatterns = [
    # Help Guide
    path('help/', views.DbListHelpTemplateView.as_view(), name='dblist-help'),
    # Orators
    path('orators/', views.OratorsListView.as_view(), name='dblist-orators'),
    path('orators/<pk>/', views.OratorsDetailView.as_view(), name='dbdetail-orators'),
    # Passages
    path('passages/', views.PassagesListView.as_view(), name='dblist-passages'),
    path('passages/<pk>/', views.PassagesDetailView.as_view(), name='dbdetail-passages'),
    # Orators in Passages
    path('oratorsinpassages/', views.OratorsInPassagesListView.as_view(), name='dblist-oratorsinpassages'),
    path('oratorsinpassages/<pk>/', views.OratorsInPassagesDetailView.as_view(), name='dbdetail-oratorsinpassages'),
    # Orators in Cicero Brutus
    path('oratorsincicerobrutus/', views.OratorsInCiceroBrutusListView.as_view(), name='dblist-oratorsincicerobrutus'),
    path('oratorsincicerobrutus/<pk>/', views.OratorsInCiceroBrutusDetailView.as_view(), name='dbdetail-oratorsincicerobrutus'),
    
    # Export data
    path('export/csv/', views.export_csv, name='export-csv'),
]
