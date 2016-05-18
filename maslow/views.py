from django.views.generic import TemplateView


class TestView(TemplateView):
    template_name = 'admin_template.html'

    def get_context_data(self, **kwargs):
        context = super(TestView, self).get_context_data(**kwargs)

        if self.request.user:
            context['has_permission'] = True
        return context
