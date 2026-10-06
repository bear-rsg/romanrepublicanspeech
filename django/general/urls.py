from django.urls import path
from . import views, apps

app_name = apps.app_name

urlpatterns = [
    path('', views.WelcomeTemplateView.as_view(), name='welcome'),
    path('about/', views.AboutTemplateView.as_view(), name='about'),
    path('outputs/presentations/', views.OutputsPresentationsTemplateView.as_view(), name='outputs-presentations'),
    path('outputs/publications/', views.OutputsPublicationsTemplateView.as_view(), name='outputs-publications'),
    path('accessibility/', views.AccessibilityTemplateView.as_view(), name='accessibility'),
    path('cookies/', views.CookiesTemplateView.as_view(), name='cookies'),
]
