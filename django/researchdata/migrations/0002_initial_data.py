from django.db import migrations, transaction, IntegrityError
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
    for name in ['Roman', 'External']:
        models.OratoricalExemplumType.objects.create(name=name)


    for name in [
        "Is not listed as an orator in Sumner's orator register, nor in the Facta et dicta",
        "Is not in Sumner's orator register but is mentioned in the Brutus and has a match in the Facta et dicta's list of orators",
        "Is listed as an orator in Sumner's orator register but not in the Facta et dicta's list of orators",
        "Is listed as an orator in Sumner's orator register and in the Facta et dicta's list of orators"
    ]:
        models.OratorInCiceroBrutusType.objects.create(name=name)

    # Author & Work
    author = models.Author.objects.create(nomen='Valerius', cognomen='Maximus')
    models.Work.objects.create(name='Facta et dicta memorabilia', author=author)


def insert_initial_orator_in_passage(apps, schema_editor):
    """
    Inserts the initial OratorInPassage objects from a csv file
    """

    try:
        csv_filepath = os.path.join(settings.BASE_DIR, 'researchdata', 'migrations', 'data', 'initial_orator_in_passage.csv')
        with open(csv_filepath, mode='r', encoding='utf-8-sig', newline='') as f:
            # Convert data to list of dicts
            reader = csv.DictReader(f)
            records = list(reader)

            # Get the Work object that all created Passage objects belong to
            work = models.Work.objects.get(name='Facta et dicta memorabilia')

            for record in records:
                # Create the OratorInPassage object, if mandatory data exists
                passage = record['passage']
                orator = record['orator']
                if passage and orator:
                    try:
                        # Create with mandatory fields
                        with transaction.atomic():
                            oip_object = models.OratorInPassage.objects.create(
                                passage=models.Passage.objects.get_or_create(name=passage, work=work)[0],
                                orator=models.Orator.objects.get_or_create(name=orator)[0]
                            )
                            # Add data for optional fields
                            oip_object.oratorical_exemplum_type = models.OratoricalExemplumType.objects.get_or_create(name=record['oratorical_exemplum_type'])[0]
                            oip_object.content_summary = record['content_summary']
                            oip_object.speeches = record['speeches']
                            if len(record['context']):
                                oip_object.context = record['context']
                            if len(record['content']):
                                oip_object.content = record['content']
                            oip_object.speech_type = models.SpeechType.objects.get_or_create(name=record['speech_type'])[0]
                            oip_object.venue = models.Venue.objects.get_or_create(name=record['venue'])[0]
                            oip_object.venue_type = models.VenueType.objects.get_or_create(name=record['venue_type'])[0]
                            oip_object.citizen_status = models.CitizenStatus.objects.get_or_create(name=record['citizen_status'])[0]
                            if len(record['athens']):
                                oip_object.athens = record['athens']
                            if len(record['non_magistrate_senator']):
                                oip_object.non_magistrate_senator = record['non_magistrate_senator']
                            oip_object.time_period = models.TimePeriod.objects.get_or_create(name=record['time_period'])[0]
                            oip_object.precise_date = record['precise_date']
                            if len(record['precise_date_order']):
                                oip_object.precise_date_order = int(record['precise_date_order'])
                            oip_object.court_type = models.CourtType.objects.get_or_create(name=record['court_type'])[0]
                            oip_object.court_type_details = record['court_type_details']
                            if len(record['liminal_speaker_non_elite']):
                                oip_object.liminal_speaker_non_elite = record['liminal_speaker_non_elite']
                            if len(record['liminal_speaker_non_roman']):
                                oip_object.liminal_speaker_non_roman = record['liminal_speaker_non_roman']
                            if len(record['liminal_speaker_women']):
                                oip_object.liminal_speaker_women = record['liminal_speaker_women']
                            oip_object.cicero_as_source = models.CiceroAsSource.objects.get_or_create(name=record['cicero_as'])[0]
                            if len(record['oratorical_exemplum']):
                                oip_object.oratorical_exemplum = record['oratorical_exemplum']
                            oip_object.cicero_work_used = record['cicero_work_used']
                            oip_object.research_notes = record['research_notes']
                            # Apply changes to object in db
                            oip_object.save()

                    except IntegrityError:
                        continue  # ignore duplicate records

    except FileNotFoundError as err:
        print(err)


def insert_initial_orator_in_cicero_brutus(apps, schema_editor):
    """
    Inserts the initial OratorInCiceroBrutus objects from a csv file
    """

    try:
        csv_filepath = os.path.join(settings.BASE_DIR, 'researchdata', 'migrations', 'data', 'initial_orator_in_cicero_brutus.csv')
        with open(csv_filepath, mode='r', encoding='utf-8-sig', newline='') as f:
            # Convert data to list of dicts
            reader = csv.DictReader(f)
            records = list(reader)

            for record in records:
                with transaction.atomic():
                    # Create object with mandatory field
                    oicb_object = models.OratorInCiceroBrutus.objects.create(name=record['orator'])
                    # Optional fields
                    for i in [1, 2, 3, 4]:
                        if record[f'type_{i}'] == 'x':
                            oicb_object.type_id = i
                    if record['presented_as_an_orator'] == 'x':
                        oicb_object.presented_as_an_orator = True
                    if record['not_in_sumners_register'] == 'x':
                        oicb_object.not_in_sumners_register = True
                    if record['greek_orators_in_sumner'] == 'x':
                        oicb_object.greek_orators_in_sumner = True
                    # Apply changes to object in db
                    oicb_object.save()


    except FileNotFoundError as err:
        print(err)


class Migration(migrations.Migration):

    dependencies = [
        ('researchdata', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_new_data),
        migrations.RunPython(insert_initial_orator_in_passage),
        migrations.RunPython(insert_initial_orator_in_cicero_brutus),
    ]
