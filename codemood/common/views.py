from django.views.generic import TemplateView


class Index(TemplateView):

    def get_template_names(self):
        if self.request.user.is_authenticated():
            return 'index/authorized.html'
        else:
            return 'index/not-authorized.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['git_activity_list'] = None
            context['fb_activity_list'] = None
        return context