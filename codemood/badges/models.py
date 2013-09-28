from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models

from commits.models import Commit
from social.models import Post
from common.path_utils import make_upload_path


class Badge(models.Model):
    """
    Badges that user can get
    """

    title = models.CharField(_('Title'), max_length=250)
    description = models.TextField(_('Description'))
    image = models.ImageField(_('Image'), upload_to=make_upload_path)

    qs = models.TextField(_('Badge query'))


class BadgeUser(models.Model):
    """
    Badge that user get
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    badge = models.ForeignKey(Badge)
    commit = models.ForeignKey(Commit, blank=True, null=True)
    post = models.ForeignKey(Post, blank=True, null=True)
    created = models.DateTimeField(_('When got a badge'), auto_now_add=True)