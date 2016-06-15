# from django.core.serializers import serialize
# from django.db.models.query import QuerySet, FlatValuesListIterable
from django.utils.safestring import mark_safe
from django.template import Library
import json

register = Library()


def jsonify(querydict, key):
    return json.dumps(mark_safe(list(querydict.values_list(key, flat=True))))


def listify(querydict, key):
    return mark_safe(list(querydict.values_list(key, flat=True)))


@register.filter
def subtract(value, arg):
    try:
        return value - arg
    except:
        return 0


@register.filter
def multiply(value, arg):
    try:
        return value * arg
    except:
        return 0


@register.filter
def divide(value, arg):
    try:
        return value / arg
    except:
        return 0


register.filter('jsonify', jsonify)
register.filter('listify', listify)
jsonify.is_safe = True

register.filter('subtract', subtract)
register.filter('multiply', multiply)
register.filter('divide', divide)

