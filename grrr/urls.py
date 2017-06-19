from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic.base import TemplateView

from apps.users import views as userviews
from apps.views import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += i18n_patterns(
    url(r'^$', views.FrontView.as_view(), name='front'),

    # User urls
    url(r'^mi-cuenta$', userviews.UserAccount.as_view(), name='dashboard'),

    # Registration urls
    url(r'', include('registration.backends.default.urls')),
    url(r'^codigo-etico$', TemplateView.as_view(template_name="registration/ethic-code.html"), name='ethic-code'),

    # Models urls
    url(r'', include('apps.models.urls', namespace='models')),

    # Static pages
    url(r'^acerca$', TemplateView.as_view(template_name="pages/about.html"), name='about'),

    # General views
    url(r'^blog$', views.BlogView.as_view(), name='blog'),
    url(r'^blog/(?P<slug>.+)$', views.BlogItemView.as_view(), name="blogpost"),
    url(r'^nodos$', views.NodesView.as_view(), name='nodes'),
    url(r'^nodo/(?P<slug>.+)$', views.NodeItemView.as_view(), name="node"),

    # API services
    url(r'^api/', include('apps.api.urls', namespace='api')),
)

if settings.DEBUG == True:
   urlpatterns += static( settings.STATIC_URL, document_root = settings.STATIC_ROOT )
   urlpatterns += static( settings.MEDIA_URL,  document_root = settings.MEDIA_ROOT )
