from django.template import Library

register = Library()

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)
