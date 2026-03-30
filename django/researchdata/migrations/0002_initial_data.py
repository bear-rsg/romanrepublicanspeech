from django.db import migrations
from django.conf import settings
from researchdata import models
import csv
import os


def insert_new_data(apps, schema_editor):
    """
    Inserts new data, that isn't included in the old csv data file so must be manually specified here
    """

    # CourtType
    for name in ['criminal', 'civil']:
        models.CourtType.objects.create(name=name)

    # OratoricalExemplumType
    for name in ['Roman', 'external']:
        models.OratoricalExemplumType.objects.create(name=name)

    # Author & Work
    author = models.Author.objects.create(nomen='Valerius', cognomen='Maximus')
    models.Work.objects.create(name='Facta et dicta memorabilia', author=author)


def insert_old_data(apps, schema_editor):
    """
    Inserts data from the old csv data file
    """

    try:
        csv_filepath = os.path.join(settings.BASE_DIR, 'researchdata', 'migrations', 'data', 'old_data_cleaned.csv')
        with open(csv_filepath, mode='r', encoding='utf-8-sig', newline='') as f:
            # Convert data to list of dicts
            reader = csv.DictReader(f)
            records = list(reader)

            # Get the Work object that all created Passage objects belong to
            work = models.Work.objects.get(name='Facta et dicta memorabilia')

            for record in records:
                # Create the OratorInPassage object, if mandatorydata exists
                passage = record['passage']
                orator = record['orator']
                if passage and orator:
                    # Create with mandatory fields
                    oip_object = models.OratorInPassage.objects.create(
                        passage=models.Passage.objects.get_or_create(name=passage, work=work)[0],
                        orator=models.Orator.objects.get_or_create(name=orator)[0]
                    )
                    # Add data for optional fields
                    # oip_object.oratorical_exemplum = record['oratorical_exemplum']
                    # oip_object.oratorical_exemplum_type = record['oratorical_exemplum_type']
                    oip_object.content_summary = record['content_summary']
                    oip_object.speeches = record['speeches']
                    oip_object.context = record['context']
                    oip_object.content = record['content']
                    oip_object.speech_type = models.SpeechType.objects.get_or_create(name=record['speech_type'])[0]
                    oip_object.venue = models.Venue.objects.get_or_create(name=record['venue'])[0]
                    oip_object.venue_type = models.VenueType.objects.get_or_create(name=record['venue_type'])[0]
                    oip_object.citizen_status = models.CitizenStatus.objects.get_or_create(name=record['citizen_status'])[0]
                    # oip_object.non_magistrate_senator = record['non_magistrate_senator']
                    # oip_object.time_period = record['time_period']
                    # oip_object.court = record['court']
                    # oip_object.court_type = record['court_type']
                    # oip_object.court_type_details = record['court_type_details']
                    # oip_object.cicero_as_source = record['cicero_as_source']
                    oip_object.research_notes = record['research_notes']
                    # Apply changes to object in db
                    oip_object.save()

    except FileNotFoundError as err:
        print(err)


class Migration(migrations.Migration):

    dependencies = [
        ('researchdata', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_new_data),
        migrations.RunPython(insert_old_data)
    ]
