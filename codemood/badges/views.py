from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .models import BadgeUser


class BadgeUserList(ListView):
    model = BadgeUser
    template_name = 'badges/list.html'
    context_object_name = 'badgeuser_list'

    def get_queryset(self):
        user = self.request.user
        return BadgeUser.objects.filter(user=user).distinct()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BadgeUserList, self).dispatch(*args, **kwargs)