from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic.base import TemplateView
from django.contrib.auth.views import PasswordResetView

from .forms import GrrrContactForm
from contact_form.views import ContactFormView
from apps.users import views as userviews
from apps.views import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^captcha/', include('captcha.urls'))
]

urlpatterns += i18n_patterns(
    url(r'^$', views.FrontView.as_view(), name='front'),

    # User urls
    url(r'^mi-cuenta$', userviews.UserAccount.as_view(), name='dashboard'),

    # Registration urls
    url(r'^cambia-tu-pass$', PasswordResetView.as_view(), { 'template_name' : 'registration/password_change.html', }, name='password_change'),
    url(r'^pass-cambiado$', TemplateView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    url(r'', include('registration.backends.default.urls')),
    url(r'^codigo-etico$', TemplateView.as_view(template_name="registration/ethic-code.html"), name='ethic-code'),

    # Models urls
    url(r'', include('apps.models.urls', namespace='models')),

    # Static pages
    url(r'^acerca$', TemplateView.as_view(template_name="pages/about.html"), name='about'),
    url(r'^recursos$', views.ResourcesView.as_view(), name='resources'),
    url(r'^glosario$', views.GlossaryView.as_view(), name='glossary'),
    url(r'^como-funciona$', TemplateView.as_view(template_name="pages/how.html"), name='how-it-works'),

    # General views
    url(r'^blog$', views.BlogView.as_view(), name='blog'),
    url(r'^blog/(?P<slug>.+)$', views.BlogItemView.as_view(), name="blogpost"),
    url(r'^comunidad$', views.NodesView.as_view(), name='nodes'),
    url(r'^aspectos-legales$', TemplateView.as_view(template_name="pages/legal-issues.html"), name='legal-issues'),
    url(r'^acuerdos$', views.AgreementsView.as_view(), name='agreements'),
    url(r'^busca$', views.BatchesView.as_view(), name='batches'),
    url(r'^referencias$', views.ReferencesView.as_view(), name='references'),
    url(r'^nodos$', views.ReusesView.as_view(), name='reuses'),
    url(r'^nodo/(?P<slug>.+)$', views.SpaceItemView.as_view(), name="space"),
    url(r'^lote/(?P<pk>[0-9]+)$', views.BatchItemView.as_view(), name="batch"),
    url(r'^transfiere/(?P<pk>[0-9]+)$', views.TransferBatchView.as_view(), name="transfer_batch"),
    url(r'^activa/(?P<pk>[0-9]+)$', views.ActivateBatchView.as_view(), name="activate_batch"),

    # API services
    url(r'^api/', include('apps.api.urls', namespace='api')),

    # Contact form
    # url(r'^contacta$', ContactFormView.as_view(form_class=GrrrContactForm), name='contact_form'),
    # url(r'^contacta/', include('contact_form.urls')),

    # ratings
    url(r'^ratings/', include('star_ratings.urls', 'ratings')),
)

if settings.DEBUG == True:
   urlpatterns += static( settings.STATIC_URL, document_root = settings.STATIC_ROOT )
   urlpatterns += static( settings.MEDIA_URL,  document_root = settings.MEDIA_ROOT )
