from django.conf import settings

def site_info_processor(request):
    """Injects into global context information about the site"""

    default_html_title       = settings.DEFAULT_HTML_TITLE
    default_html_description = settings.DEFAULT_HTML_DESCRIPTION

    return locals()

def debug_processor(request):
    """Injects debug flag into context"""

    debug    = settings.DEBUG
    debug_js = settings.DEBUG_JS

    return locals()
