from django import template
import re

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, '')


@register.filter
def truncatewords_custom(value, word_limit):
    words = re.findall(r'\w+', value)
    if len(words) > word_limit:
        return ' '.join(words[:word_limit]) + '...'
    return value