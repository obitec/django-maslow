from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.flatpages.models import FlatPage
from django.contrib.postgres.fields import JSONField
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from mptt.managers import TreeManager
from reversion import revisions as reversion


class NaturalManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class ThingManager(models.Manager):
    def get_by_natural_key(self, name, parent):
        return self.get(name=name, parent__name=parent)


class NaturalModel(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def natural_key(self):
        return self.name,

    objects = NaturalManager()

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class DataForm(NaturalModel):
    form = models.TextField(blank=True, verbose_name=_('Data form'))

    # calculated_values = ArrayField(models.CharField(max_length=100))
    # action = models.CharField()

    class Meta:
        abstract = True


class DataMixin(models.Model):
    description = models.TextField(verbose_name=_('Description'), blank=True)
    extra_data = JSONField(verbose_name=_('Extra data'), null=True, blank=True)

    # data_form = models.ForeignKey(DataForm, null=True, blank=True)

    class Meta:
        abstract = True


class AuditMixin(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # created_on = models.DateTimeField(default=timezone.now)
    # updated_on = models.DateTimeField()

    # def save(self, *args, **kwargs):
    #     self.updated_on = timezone.now()
    #     super().save(*args, **kwargs)

    class Meta:
        abstract = True


class NaturalDataModel(DataMixin, NaturalModel):
    class Meta:
        abstract = True


class MPTTMetaBase:
    """Base Meta class for MPTT models

    """
    ordering = ('position', 'tree_id', 'lft')
    unique_together = ('name', 'parent')


class Thing(MPTTModel):
    """ AbstractThing as an abstract base class for all MPTT based
    hierarchical models. It also defines a structural link type and
    a jsonb datafield and form to extend models.

    """
    name = models.CharField(max_length=250)
    display_name = models.CharField(max_length=254, blank=True, default="")
    description = models.TextField(blank=True, default='')

    AP = 'AP'
    EC = 'EC'
    GS = 'GS'
    CI = 'CI'
    SL = 'SL'
    STRUCTURAL_LINK_OPTIONS = (
        (AP, _('part')),  # _('Aggregation Participation')),
        (EC, _('characteristic')),  # _('Exhibition Characterization')),
        (GS, _('type')),  # _('Generalization Specialization')),
        (CI, _('instance')),  # _('Classification Instantiation')),
        (SL, _('state')))  # _('State')),)
    link_type = models.CharField(
        max_length=2, choices=STRUCTURAL_LINK_OPTIONS,
        default=GS, verbose_name=_('Structural Link Type'),
        help_text=_('https://en.wikipedia.org/wiki/Object_Process_Methodology#Structural_and_Procedural_Links'))

    PHYSICAL = 'physical'
    INFORMATIONAL = 'informational'
    ESSENCE_OPTIONS = (
        (PHYSICAL, _('physical')),
        (INFORMATIONAL, _('informational')))
    essence = models.CharField(
        max_length=15, choices=ESSENCE_OPTIONS,
        default=INFORMATIONAL, verbose_name=_('Is the object physical or informatical?'),
        help_text=_('https://en.wikipedia.org/wiki/Object_Process_Methodology#OPM_Things'))

    parent = TreeForeignKey(
        'self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.CASCADE)

    data = JSONField(blank=True, null=True)
    data_form = models.ForeignKey(
        FlatPage, null=True, blank=True, related_name='%(class)s_data_form', on_delete=models.CASCADE)

    # TODO: Make order mean something.
    position = models.PositiveIntegerField(blank=True, default=0)

    image = models.ImageField(null=True, blank=True)

    # def get_absolute_url(self):
    #     return reverse('assessment:thing_detail', kwargs={'pk': str(self.id)})

    def __str__(self):
        return self.display_name or self.name

    def save(self, *args, **kwargs):
        with reversion.create_revision():
            reversion.set_comment('Import or backend changes')
            super().save(*args, **kwargs)

    objects = models.Manager()
    tree = TreeManager()

    class MPTTMeta:
        order_insertion_by = ['position']

    class Meta:
        abstract = True


ONE = 1
HUNDRED = 100
THOUSAND = 1000
# HUNDRED_THOUSAND = 100000
MILLION = 1000000
# BILLION = '1 000 000'

MULTIPLIER_OPTIONS = (
    (ONE, _('one')),
    (HUNDRED, _('hundred')),
    (THOUSAND, _('thousand')),
    # (HUNDRED_THOUSAND, _('hundred thousand')),
    (MILLION, _('million')),
    # (BILLION, _('hundred million')),
)
