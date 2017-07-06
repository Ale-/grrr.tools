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

fake_breadcrumb_default_text = _('Volver a la página anterior')

@register.inclusion_tag('fake-breadcrumb.html')
def fake_breadcrumb(text=fake_breadcrumb_default_text):
    return { 'text' : text }

@register.inclusion_tag('view.html')
def view(items=None, user=None, title=None, classname_modifier=None, view_id=None):
    view_class = 'empty'
    if len(items)>0:
        view_class = items[0].__class__.__name__.lower()
    template   = view_class + "-item"
    if classname_modifier:
        template += ("--" + classname_modifier)
    return locals()

@register.inclusion_tag('limited-choices-select.html')
def limited_choices_select(choices=None, select_name=None, select_class=None, all=False, multiple=False):
    options = [{ 'name' : option[1], 'id' : option[0] } for option in choices ]
    return  { 'options' : options, 'select_name' : select_name, 'select_class' : select_class, 'all' : all, 'multiple' : multiple}

@register.filter(name='remove_i18n_prefix')
def remove_i18n_prefix(value):
    if value.startswith('/en') or value.startswith('/es'):
        value = value[3::]
    return value

@register.inclusion_tag("share.html")
def share(title, url):
    return({ "title" : title, "url" : url })

@register.inclusion_tag("icon.html")
def icon(icon, text):
    return({ "icon" : icon, "text" : text })

@register.filter(name='has_permissions')
def has_permissions(user, node):
    return node.edit_permissions(user)

@register.simple_tag
def jquery():
    return  mark_safe("<script type='text/javascript' src='" + settings.STATIC_URL + "/admin/js/vendor/jquery/jquery.min.js'></script>")

@register.inclusion_tag("breadcrumb.html")
def breadcrumb(url_2=None, txt_2=None, url_3=None, txt_3=None, txt_4=None):
    return locals()

@register.inclusion_tag("user-actions.html")
def user_actions(object, user):
    return {
        'object' : object,
        'model'  : object.__class__.__name__.lower(),
        'user'   : user
    }
