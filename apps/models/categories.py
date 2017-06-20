from django.utils.translation import ugettext_lazy as _

""" Categories used by models """

AGREEMENT_CATEGORIES = (
    ('PU', _('Cesión de entidad pública a colectivo')),
    ('PR', _('Cesión de entidad privada a colectivo')),
    ('CO', _('Cesión de colectivo a colectivo')),
)

AGREEMENT_LANGUAGES = (
    ('ES', _('Español')),
    ('CA', _('Catalán')),
    ('GA', _('Gallego')),
    ('EU', _('Euskera')),
    ('EN', _('Inglés')),
    ('FR', _('Francés')),
    ('OT', _('Otros'))
)
