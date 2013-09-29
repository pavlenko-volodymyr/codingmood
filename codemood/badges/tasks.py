from celery import task
from django.contrib.auth.models import User

from commits.models import Commit
from .models import Badge, BadgeUser

@task
def give_badges(user_id):
    user = User.objects.get(id=user_id)
    badges = Badge.objects.exclude(badgeuser__user=user)

    for badge in badges:
        q = badge.get_commit_query()
        commits = Commit.objects.filter(repository__user=user).filter(q)

        if commits.count() > 0:
            BadgeUser.objects.create(user=user, badge=badge, commit=commits[0])