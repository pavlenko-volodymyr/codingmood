from django.views.generic import TemplateView

from commits.forms import RepositoryForm
from commits.models import Repository, Commit
from social.models import Post

class Index(TemplateView):

    def get_template_names(self):
        if self.request.user.is_authenticated():
            return 'index/authorized.html'
        else:
            return 'index/not-authorized.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():

            if self.request.method == 'POST':
                repository_form = RepositoryForm(self.request)
            else:
                repository_form = RepositoryForm()

            context['repository_form'] = repository_form
            #add filtering by user
            context['git_activity_list'] = Commit.objects.all()
            context['repositories'] = Repository.objects.all()

            context['fb_activity_list'] = Post.objects.filter(user=self.request.user).order_by('created')
        return context
