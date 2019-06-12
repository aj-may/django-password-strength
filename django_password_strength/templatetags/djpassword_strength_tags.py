import json

from django.template import Library

register = Library()


def jsonify(value):
    return json.dumps(value)


register.filter('jsonify', jsonify)
