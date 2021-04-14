from django.contrib.auth.models import User
from .models import Relationship

def get_people_user_follows(user):
    """
    Returns a ``QuerySet`` representing the users that the given user follows.
    """
    ul = Relationship.objects.filter(from_user=user).values_list('to_user', 
        flat=True)
    return User.objects.filter(id__in=ul)


def get_people_following_user(user):
    """
    Returns a ``QuerySet`` representing the users that follow the given user.
    """
    ul = Relationship.objects.filter(to_user=user).values_list('from_user', 
        flat=True)
    return User.objects.filter(id__in=ul)

  