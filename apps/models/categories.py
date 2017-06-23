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

MATERIALS_BY_FAMILY = (
    ('MAD', _('Madera')),
    ('MET', _('Metal')),
    ('PLA', _('Plástico')),
    ('ELE', _('Electrónico')),
    ('TEX', _('Textiles')),
    ('OTR', _('Otros')),
)

MATERIALS_BY_FORM = (
    ( 'LO', _('Longitudinales')),
    ( 'SU', _('Superficiales')),
    ( 'CO', _('Contenedores')),
    ( 'OT', _('Otros')),
)

MATERIAL_UNITS = (
    ( 'UD', _('Unidades')),
    ( 'ML', _('Metros lineales')),
    ( 'M2', _('Metros cuadrados')),
    ( 'M3', _('Metros cúbicos')),
)

MESSAGE_CATEGORIES = (
    ('me', _('Quiero mandar un mensaje genérico')),
    ('of', _('Quiero notificar al nodo que tengo materiales que puede querer')),
    ('de', _('Tengo interés en materiales de este nodo')),
)
