from django.contrib import admin
from django.db.models import ManyToManyField, ForeignKey
from . import models


# Actions


def publish(modeladmin, request, queryset):
    """
    Sets all selected objects in queryset to published
    """
    queryset.update(published=True)


publish.short_description = "Publish selected items (will appear on main site)"


def unpublish(modeladmin, request, queryset):
    """
    Sets all selected objects in queryset to not published
    """
    queryset.update(published=False)


unpublish.short_description = "Unpublish selected items (will not appear on main site)"



#
# 1. Reusable code
#


def get_manytomany_fields(model, exclude=[]):
    """
    Returns a list of strings containing the field names of many to many fields of a model
    To ignore certain fields, provide a list of such field names (as strings) using the exclude parameter
    """
    return list(f.name for f in model._meta.get_fields() if type(f) is ManyToManyField and f.name not in exclude)


def get_foreignkey_fields(model, exclude=[]):
    """
    Returns a list of strings containing the field names of foreign key fields of a model
    To ignore certain fields, provide a list of such field names (as strings) using the exclude parameter
    """
    return list(f.name for f in model._meta.get_fields() if type(f) is ForeignKey and f.name not in exclude)


class GenericAdminView(admin.ModelAdmin):
    """
    This is a generic class that can be applied to most models to customise their inclusion in the Django admin.

    This class can either be inherited from to customise, e.g.:
    class [ModelName]AdminView(GenericAdminView):

    Or if you don't need to customise it just register a model, e.g.:
    admin.site.register([model name], GenericAdminView)
    """
    list_display = ('name',)
    list_display_links = ('name',)
    list_per_page = 100
    search_fields = ('name',)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set all many to many fields to display the filter_horizontal widget
        self.filter_horizontal = get_manytomany_fields(self.model)
        # Set all foreign key fields to display the autocomplete widget
        self.autocomplete_fields = get_foreignkey_fields(self.model)


# Simple ModelAdmins


admin.site.register(models.CiceroAsSource, GenericAdminView)
admin.site.register(models.CitizenStatus, GenericAdminView)
admin.site.register(models.CourtType, GenericAdminView)
admin.site.register(models.OratoricalExemplumType, GenericAdminView)
admin.site.register(models.Speaker, GenericAdminView)
admin.site.register(models.SpeechType, GenericAdminView)
admin.site.register(models.TimePeriod, GenericAdminView)
admin.site.register(models.Venue, GenericAdminView)
admin.site.register(models.VenueType, GenericAdminView)


# Custom ModelAdmins


@admin.register(models.Orator)
class OratorAdminView(GenericAdminView):
    """ Customise the admin interface for Orator model """

    list_display = ('name',)
    search_fields = ('name',)


@admin.register(models.Author)
class AuthorAdminView(GenericAdminView):
    """ Customise the admin interface for Author model """

    list_display = ('id', 'praenomen', 'nomen', 'cognomen', 'agnomen')
    list_display_links = ('id',)
    search_fields = ('id', 'praenomen', 'nomen', 'cognomen', 'agnomen')


@admin.register(models.Work)
class WorkAdminView(GenericAdminView):
    """ Customise the admin interface for Work model """

    list_display = ('name', 'author')
    search_fields = ('name',)


@admin.register(models.Passage)
class PassageAdminView(GenericAdminView):
    """ Customise the admin interface for Passage model """

    list_display = ('name', 'work')
    search_fields = ('name', 'work__name')


@admin.register(models.OratorInPassage)
class OratorInPassageAdminView(GenericAdminView):
    """ Customise the admin interface for OratorInPassage model """

    list_display = ('id', 'passage', 'orator', 'content_summary')
    list_display_links = ('id',)
    search_fields = ('name', 'work__name', 'orator__name', 'content_summary')
    list_filter = (
        'published',
        'oratorical_exemplum',
        'oratorical_exemplum_type',
        'speech_type',
        'context',
        'content',
        'court_type',
        'non_magistrate_senator'
    )
    actions = (publish, unpublish)
