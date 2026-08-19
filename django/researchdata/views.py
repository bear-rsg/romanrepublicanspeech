from django.http import HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.urls import reverse
from datetime import datetime
from . import models
import csv


class DbListHelpTemplateView(TemplateView):
    """
    Class-based view for db list help template
    """
    template_name = 'researchdata/dblisthelp.html'


class OratorsListView(ListView):
    """
    Class-based view for orators list template
    """
    template_name = 'researchdata/dblist-orators.html'
    model = models.Orator


class OratorsDetailView(DetailView):
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


class PassagesListView(ListView):
    """
    Class-based view for passages list template
    """
    template_name = 'researchdata/dblist-passages.html'
    model = models.Passage


class PassagesDetailView(DetailView):
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


class OratorsInPassagesListView(ListView):
    """
    Class-based view for oratorsinpassages list template
    """
    template_name = 'researchdata/dblist-oratorsinpassages.html'
    model = models.OratorInPassage

    def get_queryset(self):
        queryset = self.model.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(published=True)
        return queryset.distinct()


class OratorsInPassagesDetailView(DetailView):
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


class OratorsInCiceroBrutusListView(ListView):
    """
    Class-based view for orators in cicero brutus list template
    """
    template_name = 'researchdata/dblist-oratorsincicerobrutus.html'
    model = models.OratorInCiceroBrutus


class OratorsInCiceroBrutusDetailView(DetailView):
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


def export_csv(request):
    """
    Returns a CSV file containing all OratorInPassage objects
    """

    # Define data
    queryset = models.OratorInPassage.objects.all()
    # Prepare response
    response = HttpResponse(content_type='text/csv')
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    response['Content-Disposition'] = f'attachment; filename="data_export_{now}.csv"'
    # Setup the CSV Writer
    writer = csv.writer(response)

    if queryset is not None:
        # Write header row to CSV file
        field_names = [field.name for field in queryset.model._meta.fields]
        writer.writerow(field_names)
        # Write the data rows to CSV file
        for obj in queryset:
            # Extract the value for each field on the current object
            row = [getattr(obj, field) for field in field_names]
            writer.writerow(row)

    return response
