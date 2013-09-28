from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .models import Badge


class BadgesList(ListView):
    model = Badge
    template_name = 'badges/list.html'
    context_object_name = 'bage_list'

    def get_queryset(self):
        user = self.request.user
        return Badge.objects.filter(badgeuser__user=user).distinct()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BadgesList, self).dispatch(*args, **kwargs)