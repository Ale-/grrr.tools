# Import python packages
import time
from datetime import date

# Import django packages
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils.text import slugify

# Import contrib apps
from djgeojson.fields import PointField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from ckeditor_uploader.fields import RichTextUploadingField

# Import site apps
from apps.models import categories

class Node(models.Model):
    """Nodes of the GRRR network, participated by users."""

    name          = models.CharField(_("Nombre del nodo"), max_length=128, unique=True,
                    help_text=_("El nombre con el que nos referiremos al nodo en la plataforma"))
    manager       = models.ForeignKey(User, related_name="manager", verbose_name=_("Coordinador"), null=True, blank=True,
                    help_text=_("El usuario que crea el nodo es el manager por defecto del mismo. Puedes cambiarlo posteriormente editando el nodo."))
    creation_date = models.DateField(editable=False, blank=True, null=True)
    place         = models.CharField(_("Localidad"), max_length=128, blank=True, null=True,
                    help_text=_("El nombre de la localidad —ciudad, pueblo, ámbito— donde se ubica el nodo."))
    address       = models.CharField(_("Dirección"), max_length=128, blank=True, null=True,
                    help_text=_("Dirección del nodo. No es necesario que incluyas la localidad anterior."))
    slug          = models.SlugField(editable=False, blank=True)
    image         = models.ImageField(_("Imagen"), blank=True, upload_to="images/projects/",
                    help_text=_("Sube una imagen representativa del nodo: un logo, una foto..."))
    thumbnail     = ImageSpecField(source="image", processors=[ResizeToFill(200, 200)], format='JPEG', options={'quality': 85})
    description   = models.TextField(_("Descripción"), blank=True,
                    help_text=_("Una descripción corta de la actividad del nodo. Se usará de resumen en el perfil del nodo."))
    geom          = PointField(_("Ubicación"), blank=False, null=True,
                    help_text=_("Añade la ubicación del nodo. Usa el botón inferior para localizar el punto a partir de la localidad y dirección introducidos anteriormente. Podrás ajustar posteriormente el punto arrastrándolo."))
    members       = models.PositiveIntegerField(_("Número de miembros"), default=1,
                    help_text=_("Cuánta gente trabaja en el nodo."))
    users         = models.ManyToManyField(User, related_name="users", verbose_name=_("Usuarios del proyecto"), blank=True,
                    help_text=_("Especifica aquí a usuari-s de la red que pertenecen a este Proyecto. Mantén presionado 'Control' o 'Command' en un Mac, para seleccionar más de una opción."))


    def __str__(self):
        """String representation of model instances."""
        return self.name

    def save(self, *args, **kwargs):
        """Custom save functions that populates automatically 'slug' and 'creation_date' fields"""
        self.slug = slugify(self.name)
        # Set creation date only when node is saved and hasn't an ID yet, therefore
        if not self.id:
            self.creation_date = date.today()
        super(Node, self).save(*args, **kwargs)

    def edit_permissions(self, user):
        """Returns users allowed to edit an instance of this model."""
        return user in self.users.all() or user.is_staff


class Post(models.Model):
    """News about the GRRR project and the site."""

    title         = models.CharField(_("Título"), max_length=128,
                                     help_text=_("El titulo del post."))
    slug          = models.SlugField(editable=False, blank=True)
    creation_date = models.DateField(_("Fecha"), default=date.today,
                    help_text=_("Usa el formato dd/mm/aaaa, por ejemplo: 01/05/2015."))
    author        = models.ForeignKey(User, related_name="author", verbose_name=_("Autor-"), null=True, blank=False)
    published     = models.BooleanField(_("Publicado"), default=True, blank=False,
                    help_text=_("Sólo los contenidos publicados serán visibles. Desmarca esta casilla para generar un borrador que podrás publicar más adelante, cuando esté acabado."))
    image         = models.ImageField(_("Imagen"), blank=True, upload_to="images/blog/",
                                      help_text="Una imagen representativa para las vistas de contenido y para la cabecera de la vista del post completo.")
    thumbnail     = ImageSpecField(source="image", processors=[ResizeToFill(200, 200)], format='JPEG', options={'quality': 85})
    summary       = models.TextField(_("Resumen"), blank=True,
                    help_text=_("Un resumen de la noticia para las vistas de contenidos, si no lo usas se usará un recorte del cuerpo."))
    wysiwyg       = RichTextUploadingField(_("Texto"), blank=False,
                    help_text=_("El texto completo de la noticia."))

    def __str__(self):
        """Uses Material title as string representation of model instances."""
        return self.title

    def save(self, *args, **kwargs):
        """Custom save functions that populates automatically 'slug' field"""
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def edit_permissions(self, user):
        """Returns users allowed to edit an instance of this model."""
        return user.is_staff


class Agreement(models.Model):
    """Agreement documents"""

    title         = models.CharField(_("Título"), max_length=128,
                    help_text=_("Un título significativo para el documento."))
    creation_date = models.DateField(editable=False)
    category      = models.CharField(_("Tipo de acuerdo"), max_length=2, choices=categories.AGREEMENT_CATEGORIES, default='me',
                    help_text=_("Entre qué entidades se ha firmado el acuerdo."))
    summary       = models.TextField(_("Resumen"), blank=False,
                    help_text=_("Resume en uno o dos párrafos el contenido del acuerdo."))
    language      = models.CharField(_("Idioma"), max_length=2, choices=categories.AGREEMENT_LANGUAGES, default='ES',
                    help_text=_("¿En qué idioma en que está redactado el documento? Si crees necesario añadir algún idioma contacta con nosotras."))
    document      = models.FileField(_("Documento"), upload_to='documents',
                    help_text=_("Adjunta el documento en PDF o ODT preferentemente."))

    def __str__(self):
        """String representation of model instances."""
        return self.title

    def save(self, *args, **kwargs):
        """Custom save functions that populates automatically 'slug' field"""
        # Set creation date only when node is saved and hasn't an ID yet, therefore
        if not self.id:
            self.creation_date = date.today()
        super(Agreement, self).save(*args, **kwargs)


class Reference(models.Model):
    """References linked to site's goals"""

    name      = models.CharField(_("Título"), max_length=128,
                help_text=_("Nombre de la referencia."))
    summary   = models.TextField(_("Resumen"), blank=False,
                help_text=_("Resume en uno o dos párrafos la referencia."))
    image     = models.ImageField(_("Imagen"), blank=True, upload_to="images/blog/",
                help_text="Una imagen representativa de la referencia.")
    thumbnail = ImageSpecField(source="image", processors=[ResizeToFill(480, 480)], format='JPEG', options={'quality': 85})
    link      = models.URLField(_("Enlace"), blank=False,
                help_text=_("Enlace para ampliar la información sobre la referencia"))

    def __str__(self):
        """String representation of model instances."""
        return self.name
