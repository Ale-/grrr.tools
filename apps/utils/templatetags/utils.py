from django import template
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def css(file):
    return  settings.STATIC_URL + settings.PROJECT_STATIC_FOLDER + '/css/' + file

@register.simple_tag
def js(file):
    return  settings.STATIC_URL + settings.PROJECT_STATIC_FOLDER + '/js/' + file

@register.simple_tag
def angular(file):
    return  mark_safe("<script type='text/javascript' src='" + settings.STATIC_URL + settings.PROJECT_STATIC_FOLDER + "/angular/" + file + "'></script>")

@register.simple_tag
def img(file):
    return  settings.STATIC_URL + settings.PROJECT_STATIC_FOLDER + '/img/' + file

@register.inclusion_tag('fake-breadcrumb.html')
def fake_breadcrumb(text):
    if not text:
        text = _('Volver a la página anterior')
    return { 'text' : text }

@register.inclusion_tag('limited-choices-select.html')
def limited_choices_select(choices=None, select_name=None, select_class=None, all=False, multiple=False):
    options = [{ 'name' : option[1], 'id' : option[0] } for option in choices ]
    return  { 'options' : options, 'select_name' : select_name, 'select_class' : select_class, 'all' : all, 'multiple' : multiple}

@register.filter(name='remove_i18n_prefix')
def remove_i18n_prefix(value):
    if value.startswith('/en') or value.startswith('/es'):
        value = value[3::]
    return value
