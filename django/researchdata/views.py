from django.views.generic import (DetailView, ListView, TemplateView, View)
from django.db.models.functions import Lower
from django.db.models import (Count, Q, CharField, TextField, Prefetch)
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.conf import settings
from functools import reduce
from operator import (or_, and_)
from datetime import datetime
from . import models
import csv


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
