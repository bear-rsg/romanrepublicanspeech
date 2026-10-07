from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.apps import apps
from datetime import datetime
from . import models
import csv
import json


class DbListHelpTemplateView(LoginRequiredMixin, TemplateView):
    """
    Class-based view for db list help template
    """
    template_name = 'researchdata/dblisthelp.html'


class OratorsListView(LoginRequiredMixin, ListView):
    """
    Class-based view for orators list template
    """
    template_name = 'researchdata/dblist-orators.html'
    model = models.Orator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'Orator'
        return context


class OratorsDetailView(LoginRequiredMixin, DetailView):
    """
    Class-based view for orators detail template
    """
    template_name = 'researchdata/dbdetail.html'
    model = models.Orator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_url'] = reverse('admin:researchdata_orator_change', args=(self.object.id,))
        context['details'] = [
            {'label': 'Name', 'value': self.object.name},
        ]
        return context


class PassagesListView(LoginRequiredMixin, ListView):
    """
    Class-based view for passages list template
    """
    template_name = 'researchdata/dblist-passages.html'
    model = models.Passage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'Passage'
        return context


class PassagesDetailView(LoginRequiredMixin, DetailView):
    """
    Class-based view for passages detail template
    """
    template_name = 'researchdata/dbdetail.html'
    model = models.Passage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_url'] = reverse('admin:researchdata_passage_change', args=(self.object.id,))
        context['details'] = [
            {'label': 'Name', 'value': self.object.name},
            {'label': 'Work', 'value': self.object.work},
        ]
        return context


class OratorsInPassagesListView(LoginRequiredMixin, ListView):
    """
    Class-based view for oratorsinpassages list template
    """
    template_name = 'researchdata/dblist-oratorsinpassages.html'
    model = models.OratorInPassage
    # paginate_by = 250

    def get_queryset(self):
        queryset = self.model.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(published=True)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'OratorInPassage'
        return context


class OratorsInPassagesDetailView(LoginRequiredMixin, DetailView):
    """
    Class-based view for oratorsinpassages detail template
    """
    template_name = 'researchdata/dbdetail.html'
    model = models.OratorInPassage

    def get_queryset(self):
        queryset = self.model.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(published=True)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_url'] = reverse('admin:researchdata_oratorinpassage_change', args=(self.object.id,))
        context['details'] = [
            {'label': 'Passage', 'value': self.object.passage},
            {'label': 'Orator', 'value': self.object.orator},
            {'label': 'Oratorical exemplum', 'value': self.object.oratorical_exemplum},
            {'label': 'Oratorical exemplum type', 'value': self.object.oratorical_exemplum_type},
            {'label': 'Content summary', 'value': self.object.content_summary},
            {'label': 'Speeches', 'value': self.object.speeches},
            {'label': 'Content', 'value': self.object.content},
            {'label': 'Context', 'value': self.object.context},
            {'label': 'Speech type', 'value': self.object.speech_type},
            {'label': 'Venue', 'value': self.object.venue},
            {'label': 'Venue type', 'value': self.object.venue_type},
            {'label': 'Citizen status', 'value': self.object.citizen_status},
            {'label': 'Athens', 'value': self.object.athens},
            {'label': 'Forensic', 'value': self.object.forensic},
            {'label': 'Non-magistrate senator', 'value': self.object.non_magistrate_senator},
            {'label': 'Time period', 'value': self.object.time_period},
            {'label': 'Precise date', 'value': self.object.precise_date},
            {'label': 'Court type', 'value': self.object.court_type},
            {'label': 'Court type details', 'value': self.object.court_type_details},
            {'label': 'Liminal speaker (non-elite)', 'value': self.object.liminal_speaker_non_elite},
            {'label': 'Liminal speaker (non-Roman)', 'value': self.object.liminal_speaker_non_roman},
            {'label': 'Liminal speaker (women)', 'value': self.object.liminal_speaker_women},
            {'label': 'Cicero as source', 'value': self.object.cicero_as_source},
            {'label': 'Oratorical exemplum', 'value': self.object.oratorical_exemplum},
            {'label': 'Cicero work used', 'value': self.object.cicero_work_used},
            {'label': 'Research notes', 'value': self.object.research_notes},
        ]
        return context


class OratorsInCiceroBrutusListView(LoginRequiredMixin, ListView):
    """
    Class-based view for orators in cicero brutus list template
    """
    template_name = 'researchdata/dblist-oratorsincicerobrutus.html'
    model = models.OratorInCiceroBrutus

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'OratorInCiceroBrutus'
        return context


class OratorsInCiceroBrutusDetailView(LoginRequiredMixin, DetailView):
    """
    Class-based view for orators in cicero brutus detail template
    """
    template_name = 'researchdata/dbdetail.html'
    model = models.OratorInCiceroBrutus

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_url'] = reverse('admin:researchdata_oratorincicerobrutus_change', args=(self.object.id,))
        context['details'] = [
            {'label': 'Name', 'value': self.object.name},
            {'label': 'Type', 'value': self.object.type},
            {'label': 'Presented as an Orator', 'value': self.object.presented_as_an_orator},
            {'label': 'Not in Sumner\'s register', 'value': self.object.not_in_sumners_register},
            {'label': 'Greek Orator in Sumner', 'value': self.object.greek_orators_in_sumner},
        ]
        return context


@require_POST
def download_csv(request):
    """
    Functional view to download data as a CSV file for the specified model
    """

    try:
        data = json.loads(request.body)
        model = data.get('model', None)
        object_ids = data.get('objects', [])
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    if not model:
        return JsonResponse({"error": "No model provided"}, status=400)
    if not object_ids:
        return JsonResponse({"error": "No object IDs provided"}, status=400)

    # Get model class from model string
    model_class = apps.get_model(f'researchdata.{model}')

    # Filter the Record model by the extracted IDs
    records = model_class.objects.all()
    if not request.user.is_staff:
        records = records.filter(published=True)
    if type(object_ids) is list:
        records = records.filter(id__in=object_ids)

    # Set up the HTTP response to act as a downloadable CSV
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="RRS_{model}_{timestamp}.csv"'},
    )

    writer = csv.writer(response)

    # Dynamically get all field names (headers) from the Record model
    field_names = [field.name for field in model_class._meta.fields]
    writer.writerow(field_names)

    # Loop through the queryset and write each record's data to the CSV
    for record in records:
        writer.writerow([getattr(record, field) for field in field_names])

    return response
