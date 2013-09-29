from django.views.generic import TemplateView

from commits.forms import RepositoryForm
from commits.models import Repository, Commit
from social.models import Post

class Index(TemplateView):
    """
    Return different view to authenticated and not.
    """
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return AuthenticatedIndex.as_view()(self.request)
        else:
            return NotAuthenticatedIndex.as_view()(self.request)


class AuthenticatedIndex(TemplateView):
    """
    View to authenticated user
    """
    template_name = 'index/authorized.html'

    def get_context_data(self, **kwargs):
        context = super(AuthenticatedIndex, self).get_context_data(**kwargs)
        
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
    
    
class NotAuthenticatedIndex(TemplateView):
    """
    View to NOT authenticated user
    """
    template_name = 'index/not-authorized.html'
