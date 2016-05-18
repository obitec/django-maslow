from django.contrib.admin.sites import site
from django.utils.module_loading import autodiscover_modules


def autodiscover():
    autodiscover_modules('admin', register_to=site)
