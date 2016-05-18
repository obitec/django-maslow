from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class NaturalManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


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

