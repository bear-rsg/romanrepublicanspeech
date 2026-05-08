from django.db import models
# from django.urls import reverse
from django.db.models.functions import Upper
from ckeditor.fields import RichTextField
import re


# 1. Secondary Models
# 2. Primary Models


class SimpleModelAbstract(models.Model):
    """
    An abstract model for simple models that only include a name field
    See: https://docs.djangoproject.com/en/4.0/topics/db/models/#abstract-base-classes
    """

    name = RichTextField()
    name_clean = models.TextField(blank=True, null=True)  # removes html tags, used for order and search

    def __str__(self):
        return self.name_clean

    def save(self, *args, **kwargs):
        # Set value of name_clean automatically (used for ordering and searching)
        clean_regex = re.compile('<.*?>')
        self.name_clean = re.sub(clean_regex, '', self.name)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = [Upper('name'), 'id']


# 1. Secondary Models


class CiceroAsSource(SimpleModelAbstract):
    """ The different options for whether Cicero is the source of a speech """

    class Meta:
        ordering = [Upper('name'), 'id']
        verbose_name_plural = 'cicero as source'


class CitizenStatus(SimpleModelAbstract):
    """ The status of the citizen, e.g. Roman, Romans, Italian, Foreigner """

    class Meta:
        verbose_name_plural = 'citizen statuses'


class CourtType(SimpleModelAbstract):
    """ The different types of court, e.g. Criminal, Civil """


class OratoricalExemplumType(SimpleModelAbstract):
    """ The type of oratorical examplum, e.g. Roman or External """


class OratorInCiceroBrutusType(SimpleModelAbstract):
    """ The type of orator in Cicero, Brutus """

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'orators in cicero brutus types'


class SpeechType(SimpleModelAbstract):
    """ The type of speech, e.g. Direct or Indirect """


class TimePeriod(SimpleModelAbstract):
    """ A period of time by which other objects can be grouped """


class Venue(SimpleModelAbstract):
    """ A venue/place in which a speech was made """


class VenueType(SimpleModelAbstract):
    """ The type of the venue of a speech, e.g. public or private """


# 2. Primary Models


class Orator(models.Model):
    """
    A public speaker
    """

    name = models.CharField(max_length=1000, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = [Upper('name'), 'id']


class Author(models.Model):
    """
    A creator of Works
    """

    praenomen = models.CharField(max_length=1000, db_index=True, blank=True, null=True)
    nomen = models.CharField(max_length=1000, db_index=True, blank=True, null=True)
    cognomen = models.CharField(max_length=1000, db_index=True, blank=True, null=True)
    agnomen = models.CharField(max_length=1000, db_index=True, blank=True, null=True)

    @property
    def name(self):
        name = ' '.join(
            [n for n in [self.praenomen, self.nomen, self.cognomen, self.agnomen] if n]
        )
        return name

    def __str__(self):
        return self.name

    class Meta:
        ordering = [Upper('cognomen'), Upper('nomen'), 'id']


class Work(models.Model):
    """
    A collection of Passages, created by an Author
    """

    related_name = 'works'

    author = models.ForeignKey(Author, related_name=related_name, on_delete=models.RESTRICT)
    name = models.CharField(max_length=1000, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = [Upper('name'), 'id']


class Passage(models.Model):
    """
    A part/section from a piece of Work
    """

    related_name = 'passages'

    work = models.ForeignKey(Work, related_name=related_name, on_delete=models.RESTRICT)
    name = models.CharField(max_length=1000, db_index=True)
    name_ordering = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name_ordering = re.sub(r'\d+', lambda m: m.group().zfill(3), self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = [Upper('name_ordering'), 'id']


class OratorInPassage(models.Model):
    """
    The main primary model
    Contains data about instances of Orators in Passages
    """

    related_name = 'orators_in_passages'

    passage = models.ForeignKey(Passage, related_name=related_name, on_delete=models.RESTRICT)
    orator = models.ForeignKey(Orator, related_name=related_name, on_delete=models.RESTRICT)
    oratorical_exemplum = models.BooleanField(default=True)
    oratorical_exemplum_type = models.ForeignKey(OratoricalExemplumType, related_name=related_name, on_delete=models.SET_NULL, blank=True, null=True)
    content_summary = RichTextField(blank=True, null=True)
    speeches = RichTextField(blank=True, null=True)
    content = models.BooleanField(default=False)
    context = models.BooleanField(default=False)
    speech_type = models.ForeignKey(SpeechType, related_name=related_name, on_delete=models.SET_NULL, blank=True, null=True)
    venue = models.ForeignKey(Venue, related_name=related_name, on_delete=models.SET_NULL, blank=True, null=True)
    venue_type = models.ForeignKey(VenueType, related_name=related_name, on_delete=models.SET_NULL, blank=True, null=True)
    citizen_status = models.ForeignKey(CitizenStatus, related_name=related_name, on_delete=models.SET_NULL, blank=True, null=True)
    athens = models.BooleanField(default=False, verbose_name='Athens (democratic)')
    non_magistrate_senator = models.BooleanField(default=False, verbose_name='non-magistrate senator')
    time_period = models.ForeignKey(TimePeriod, related_name=related_name, on_delete=models.SET_NULL, blank=True, null=True)
    precise_date = models.CharField(max_length=1000, blank=True, null=True)
    precise_date_order = models.IntegerField(blank=True, null=True, help_text='Number used to sort records by precise date, BC = negative, AD = positive')
    court_type = models.ForeignKey(CourtType, related_name=related_name, on_delete=models.SET_NULL, blank=True, null=True)
    court_type_details = RichTextField(blank=True, null=True)
    liminal_speaker_non_elite = models.BooleanField(default=False)
    liminal_speaker_non_roman = models.BooleanField(default=False)
    liminal_speaker_women = models.BooleanField(default=False)
    cicero_as_source = models.ForeignKey(CiceroAsSource, related_name=related_name, on_delete=models.SET_NULL, blank=True, null=True)
    oratorical_exemplum = models.BooleanField(default=False)
    cicero_work_used = RichTextField(blank=True, null=True)
    research_notes = RichTextField(blank=True, null=True)
    published = models.BooleanField(default=True, help_text='Uncheck this box to hide this record on the public interface')

    def __str__(self):
        return f'{self.passage}: {self.orator}'

    # def get_absolute_url(self):
    #     return reverse('researchdata:story-detail', args=[str(self.id)])

    class Meta:
        ordering = ['passage', 'orator', 'id']
        verbose_name_plural = 'orators in passages'
        constraints = [
            models.UniqueConstraint(
                fields=['passage', 'orator'],
                name='unique_passage_per_orator'
            )
        ]


class OratorInCiceroBrutus(models.Model):
    """
    An orator in Cicero, Brutus (treated separately from main Orators)
    """

    related_name = 'orators_in_cicero_brutus'

    name = models.CharField(max_length=1000)
    type = models.ForeignKey(OratorInCiceroBrutusType, related_name=related_name, on_delete=models.SET_NULL, blank=True, null=True)
    presented_as_an_orator = models.BooleanField(default=False)
    not_in_sumners_register = models.BooleanField(default=False, verbose_name="Not in Sumner's register")
    greek_orators_in_sumner = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = [Upper('name'), 'id']
        verbose_name_plural = 'orators in cicero brutus'
