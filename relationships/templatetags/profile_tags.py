from django import template

def person(user):
    """
    Renders a single user object.
    """
    return {'user': user}

register = template.Library()
register.inclusion_tag('relationship/person.html')(person)
