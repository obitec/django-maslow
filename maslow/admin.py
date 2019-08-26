from django import forms
from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from django.core.exceptions import FieldDoesNotExist
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.forms import FlatpageForm
from django.contrib.flatpages.models import FlatPage
from django.db.models import F, Q
from django.utils.translation import ugettext_lazy
from django.utils.translation import ugettext as _
from guardian.admin import GuardedModelAdmin
from import_export.admin import ImportExportActionModelAdmin
from mptt.forms import MPTTAdminForm
from reversion.admin import VersionAdmin
from mptt.admin import DraggableMPTTAdmin
from .views import TestView


class SuperAdmin(ImportExportActionModelAdmin, VersionAdmin, GuardedModelAdmin):
    pass


class CustomAdminSite(admin.AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('Django site admin')

    # Text to put in each page's <h1>.
    site_header = ugettext_lazy('Django administration')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('Site administration')

    # URL for the "View site" link at the top of each admin page.
    site_url = '/'

    def get_urls(self):
        from django.conf.urls import url

        urls = super(CustomAdminSite, self).get_urls()
        urls += [
            url(r'^my_view/$', self.admin_view(TestView.as_view()))
        ]
        return urls


admin_site = CustomAdminSite(name='custom_admin')
admin.site.unregister(FlatPage)
admin.site.register(ContentType)
admin.site.register(Permission)


class FlatPageAdminForm(FlatpageForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = FlatPage
        fields = '__all__'


@admin.register(FlatPage)
class MyFlatPageAdmin(FlatPageAdmin):
    form = FlatPageAdminForm


def auto_register(app_name: str = '', admin_site=None):
    app_models = apps.get_app_config(app_name).get_models()
    for model in app_models:
        try:
            if getattr(model, '_mptt_meta', None):
                classes = [DraggableMPTTAdmin, SuperAdmin, ]
            else:
                classes = [SuperAdmin, ]

            class DefaultAdmin(*classes):
                list_display = ['__str__',]
                if getattr(model, 'Admin', None):
                    list_display = model.Admin.list_display
                    list_filter = model.Admin.list_filter
                if getattr(model, '_mptt_meta', None):
                    list_display = ['indented_title', ] + list_display
                else:
                    try:
                        model._meta.get_field('name')
                        model._meta.get_field('description')
                    except FieldDoesNotExist:
                        pass
                    else:
                        list_display = ['name', 'description']
                        search_fields = ['name', ]

            if not admin_site:
                admin.site.register(model, DefaultAdmin)
            else:
                admin_site.register(model, DefaultAdmin)

        except AlreadyRegistered:
            pass


# admin.site.register(FlatPage, MyFlatPageAdmin)

# @admin.register(ContentType)
# class ContentTypeAdmin(admin.ModelAdmin):
#     pass

def update_node_positions(node, mode):
    """
    Procedure to update the node positions
    Three different modes available
    1 = insert node
    2 = update position, parent stays the same
    3 = update position and change parent
    4 = trashed
    """
    if mode == 1 or mode == 3:
        # if node has been inserted at the beginning
        if node.position == 1:
            node.get_siblings().update(position=F('position') + 1)
        # if node has been inserted not at beginning and not at the last position
        elif node.position != node.get_siblings().count() + 1:
            # update positions of siblings right of node by one
            node.get_siblings().filter(
                position__gte=node.position).update(position=F('position') + 1)

        if mode == 3:
            # since we removed the node from a parent,
            # we have to decrement the positions of the former siblings
            # right of the node by one
            if node._original_parent is not None:
                # do updates only for nodes which had a parent before.
                # will not be executed for root nodes
                node._original_parent.get_children().filter(
                    position__gt=node._original_position).update(position=F('position') - 1)
    if mode == 2:
        # if old position is left of new position -> decrement position by 1
        # for nodes which have
        # position <= node.position AND > node.original_position
        if node.position > node._original_position:
            node.get_siblings().filter(
                Q(position__lte=node.position) &
                Q(position__gt=node._original_position)
            ).update(position=F('position') - 1)
        # if old position is right of new position -> increment position by 1
        # for nodes which have position >= node.
        # position AND < node.original_position
        if node.position < node._original_position:
            node.get_siblings().filter(
                Q(position__gte=node.position) &
                Q(position__lt=node._original_position)
            ).update(position=F('position') + 1)
    if mode == 4:
        # decrement position by 1 for nodes which
        # have position > node.position
        node.get_siblings().filter(Q(position__gt=node.position)).update(
            position=F('position') - 1)
