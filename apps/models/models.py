# Import python packages
import time
from datetime import date
from twitter import Twitter, OAuth, TwitterHTTPError

# Import django packages
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.urls import reverse

# Import contrib apps
from djgeojson.fields import PointField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from ckeditor_uploader.fields import RichTextUploadingField
from star_ratings.models import Rating

# Import site apps
from apps.models import categories
from grrr import private_settings as tw
from django.conf import settings

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


class Material(models.Model):
    """Taxonomy terms to handle the materials that compose the batches."""

    name          = models.CharField(_("Nombre"), max_length=128)
    creation_date = models.DateField(editable=False, blank=True, null=True)
    slug          = models.SlugField(editable=False, blank=True)
    image         = models.ImageField(_("Imagen"), blank=True, upload_to="images/materials/")
    thumbnail     = ImageSpecField(source='image', processors=[ResizeToFill(200, 200)], format='JPEG', options={'quality': 85})
    family        = models.CharField(_("Familia"), max_length=3, choices=categories.MATERIALS_BY_FAMILY, default='MAD',
                    help_text=_("Específica la familia del material."))
    subfamily     = models.CharField(_("Tipo"), max_length=2, choices=categories.MATERIALS_BY_FORM, default='LO',
                    help_text=_("Específica el tipo de material."))
    description   = models.TextField(_("Descripción"), blank=True)
    unit          = models.CharField(_("Unidad"), max_length=2, choices=categories.MATERIAL_UNITS, default="Unidades", blank=True,
                    help_text=_("Especifica la unidad a usar cuando se cuantifica este material."))
    weight        = models.FloatField(_("Peso unitario"), blank=True, null=True,
                    help_text=_("Especifica el peso por unidad en kilogramos de manera aproximada. Se usará para hacer cálculos de materiales recuperados y puestos en uso"))


    def __str__(self):
        """String representation of model instances."""
        return self.name

    def material_id(self):
        """Returns the ID of the Material object formatted."""
        return "%03d" % self.pk

    def save(self, *args, **kwargs):
        """Custom save functions that populates automatically 'slug' and 'creation_date' fields"""
        self.slug = slugify(self.name)
        # Set creation date only when node is saved and hasn't an ID yet, therefore
        if not self.id:
            self.creation_date = date.today()
        super(Material, self).save(*args, **kwargs)

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

class Space(models.Model):
    """Spaces of the network."""

    name          = models.CharField(_("Nombre"), max_length=128,
                    help_text=_("Ponle un nombre significativo al espacio."))
    slug          = models.SlugField(editable=False, blank=True)
    creation_date = models.DateField(_("Fecha de alta en la plataforma"), default=date.today, blank=True)
    reuse         = models.BooleanField(_("¿Es un reuso"), default=True, blank=False,
                    help_text=_("¿Es el espacio el escenario de un reuso?"))
    active        = models.BooleanField(_("Activo"), default=True, blank=False,
                    help_text=_("¿Este reuso es un proceso en marcha o se da por finalizado? Los proyectos en marcha tienen mayor visibilidad en la plataforma."))
    published     = models.BooleanField(_("Publicado"), default=True, blank=False,
                    help_text=_("Sólo los contenidos 'publicados' son visibles. Desmarca esta casilla para generar un contenido provisional que podrás hacer público más adelante."))
    nodes         = models.ManyToManyField(Node, verbose_name="Nodos", blank=False, related_name="spaces",
                    help_text=_("¿Qué nodos de la red participan en este espacio? Mantén presionado 'Control' o 'Command' en un Mac, para seleccionar más de una opción."))
    image         = models.ImageField(_("Imagen"), blank=False, upload_to="images/news/",
                    help_text=_("Una imagen significativa del espacio para las vistas de resúmenes de contenido y el encabezado de la vista completa. Puedes añadir más imágenes al texto completo del reuso."))
    thumbnail     = ImageSpecField(source="image", processors=[ResizeToFill(200, 200)], format='JPEG', options={'quality': 85})
    agreement     = models.ManyToManyField(Agreement, verbose_name="Acuerdos", related_name="agreement", blank=True,
                    help_text=_("Puedes asociar documentos de acuerdos de cesión al espacio."))
    summary       = models.TextField(_("Resumen"), blank=False,
                    help_text=_("Un resumen de la noticia para las vistas de contenidos, si no lo usas se usará un recorte del cuerpo."))
    place         = models.CharField(_("Localidad"), max_length=128, blank=False, null=True,
                    help_text=_("El nombre de la localidad —ciudad, pueblo, ámbito— donde se sitúa el espacio."))
    address       = models.CharField(_("Dirección"), max_length=128, blank=True, null=True,
                    help_text=_("Dirección del nodo. No es necesario que incluyas la localidad anterior."))
    geom          = PointField(_("Ubicación"), blank=False, null=True,
                    help_text=_("Usa el botón inferior para localizar el espacio a partir de los valores de los campos anteriores, 'Localidad' y 'Dirección'."))
    ratings       = GenericRelation(Rating, related_query_name='reuses')

    def __str__(self):
        """String representation of model instances."""
        return self.name

    def save(self, *args, **kwargs):
        """Custom save functions that populates automatically 'slug' field"""
        self.slug = slugify(self.name)
        super(Space, self).save(*args, **kwargs)

    def edit_permissions(self, user):
        """Returns users allowed to edit an instance of this model."""
        if user.is_anonymous:
            return False
        user_in_groups = self.nodes.filter(users__in = [user]).count() > 0
        return user_in_groups or user.is_staff

class Post(models.Model):
    """News about the GRRR project and the site."""

    title         = models.CharField(_("Título"), max_length=128,
                    help_text=_("El titulo del post."))
    space         = models.ForeignKey(Space, verbose_name=_("Espacio"), blank=True, null=True,
                    help_text=_("¿Al blog de qué espacio está asociado este post?"))
    slug          = models.SlugField(editable=False, blank=True)
    creation_date = models.DateField(_("Fecha"), default=date.today,
                    help_text=_("Usa el formato dd/mm/aaaa, por ejemplo: 01/05/2015."))
    author        = models.ForeignKey(User, related_name="author", verbose_name=_("Autor-"), null=True, blank=False)
    published     = models.BooleanField(_("Publicado"), default=True, blank=False,
                    help_text=_("Sólo los contenidos publicados serán visibles. Desmarca esta casilla para generar un borrador que podrás publicar más adelante, cuando esté acabado."))
    grrr_blog     = models.BooleanField(_("Destacado"), default=False, blank=False,
                    help_text=_("Indica si es un post del equipo editorial. La selección de espacio se ignora si marcas esta opción."))
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

class Milestone(models.Model):
    """Milestones register batch transfer between spaces. Created automatically not in forms"""

    date     = models.DateField(null = True)
    space    = models.ForeignKey(Space, null = True)

    def __str__(self):
        """String representation of model instances."""
        return self.space.name + " | " + str(self.date)


class Batch(models.Model):
    """Batches of the same material associated to spaces."""

    category     = models.CharField(_("¿Oferta o demanda?"), max_length=2, choices=categories.BATCH_CATEGORIES, default='of',
                   help_text=_("¿Ofreces o necesitas materiales?"))
    space        = models.ForeignKey(Space, verbose_name=_("Espacio"), null=True,
                   help_text=_("¿Qué espacio ofrece o demanda?"))
    date         = models.DateField(_("Fecha de entrada"), default=date.today,
                   help_text=_("Fecha de entrada del lote en tu inventario"))
    material     = models.ForeignKey(Material, verbose_name=_("Material"), blank=False, null=True, on_delete=models.SET_NULL,
                   help_text=_("El material del que se compone el lote"))
    image        = models.ImageField(_("Imagen"), blank=True, upload_to="images/batches/")
    total        = models.PositiveIntegerField(_("Cantidad total"), blank=True, null=True,
                   help_text=_("En caso de lotes de oferta puedes especificar aquí una cantidad total mayor a la ofertada si se da el caso."))
    quantity     = models.PositiveIntegerField(_("Cantidad"), blank=True, null=True,
                   help_text=_("Especifica en las unidades del material cuánto se ofrece o necesita (opcional en este último caso)."))
    public_info  = models.TextField(_("Información pública"), blank=True, null=True,
                   help_text=_("Informa en este campo de características del lote."))
    private_info = models.TextField(_("Información privada"), blank=True, null=True,
                   help_text=_("Información de carácter privado, sólo para usuari*s de los nodos asociados al espacio."))
    expiration   = models.DateField(_("Fecha de expiración"), blank=True, null=True,
                   help_text=_("Fecha límite opcional para la oferta/demanda."))
    periodicity  = models.CharField(_("Periodicidad"), max_length=2, choices=categories.BATCH_PERIODICITY, default='no',
                   help_text=_("¿Es uan oferta única o tiene periodicidad?"))
    milestones   = models.ManyToManyField(Milestone, verbose_name=_("Movimientos"), blank=True)
    # Only for recovered materials, to store target space
    target       = models.ForeignKey(Space, verbose_name="Objectivo", related_name="source", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Batches"

    def batch_id(self):
        """Returns the id of the Batch instance."""
        return "%04d" % self.pk

    def __str__(self):
          """Sets string representation of model instances."""
          return self.material.name  + ", ref.: " + self.batch_id()

    @property
    def material_family(self):
        """Returns the family of the Material object associated with the Batch instance."""
        return self.material.family

    def edit_permissions(self, user):
        """Returns users allowed to edit an instance of this model."""
        return self.space.edit_permissions(user)

    def save(self, *args, **kwargs):
        """Notifies the creation of the instance to nodes that demand the material of the batch."""

        milestone = {}
        # If creating a new batch and it's an offer, add a new milestone to the list of milestones
        if not self.id and self.category == 'of':
            milestone = Milestone.objects.create(
                date     = self.date,
                space    = self.space,
            )
        if self.category == 'of' and self.quantity and not self.total:
            self.total = self.quantity
        super(Batch, self).save(*args, **kwargs)
        if milestone:
            self.milestones.add(milestone)


class Sms(models.Model):
    """Messages sent to nodes of the network"""

    author       = models.ForeignKey(User, blank=True, null=True, editable=False)
    datetime     = models.DateTimeField(blank=True, default=now)
    batch        = models.ForeignKey(Batch, verbose_name=_("Lote"), null=True, blank=True,
                   help_text=_("Si mandas el mensaje en relación a una oferta/demanda puedes especificarla aquí."))
    emissor      = models.ForeignKey(Space, verbose_name=_("Remitente"), related_name="emissor", null=True, blank=True,
                   help_text=_("Especifica el espacio al que representas."))
    receiver     = models.ForeignKey(Space, verbose_name=_("Destinatario"), related_name="receiver", null=True,
                   help_text=_("Espacio al que envias el mensaje"))
    body         = models.TextField(_("Mensaje"), blank=False,
                   help_text=_("Texto del mensaje. No está permitido usar HTML. Las URLs se convertirán directamente en enlaces."))
    replies      = models.ForeignKey('self', blank=True, null=True)
    notification = models.BooleanField(default=False)

    def __str__(self):
        """String representation of model instances."""
        if self.emissor:
            return "Mensaje de " + self.emissor.name + " a " + self.receiver.name + " #" + str(self.datetime)
        return "Notificación a " + self.receiver.name + " #" + str(self.datetime)

@receiver(post_save, sender=Batch)
def notify_batch(sender, instance, **kwargs):
    # Notify to Space users of related activity
    msg = Sms()
    msg.body = _("Es un mensaje automático para indicarte que se ha creado un lote en uno de tus espacios")
    msg.emissor = None
    msg.receiver = instance.space
    msg.batch = instance
    msg.notification = True
    msg.save()
    # Notify matches
    if instance.category == 'of':
        match = 'de'
        sms = _("Es un mensaje automático para indicarte que se ha creado una oferta de materiales que se ajusta a las necesidades de uno de tus espacios")
    else:
        match = 'of'
        sms = _("Es un mensaje automático para indicarte que se ha creado una demanda de materiales que se ofertan en uno de tus espacios")
    batches = Batch.objects.filter(category=match, material=instance.material)
    matches = Space.objects.distinct().filter(batch__in=batches)
    if len(matches)>0:
        for space in matches:
            msg = Sms()
            msg.body = sms
            msg.emissor = None
            msg.receiver = space
            msg.batch = instance
            msg.notification = True
            msg.save()

    # Twitter notifications
    if settings.TWITTER_NOTIFICATIONS:
        try:
            t = Twitter(auth=OAuth(tw.TWITTER_ACCESS_TOKEN, tw.TWITTER_ACCESS_TOKEN_SECRET, tw.TWITTER_API_KEY, tw.TWITTER_API_SECRET))
            url = 'https://grrr.tools' + reverse('batch',args=(instance.pk,))
            material = instance.material.name.lower()
            cat = "oferta de " if instance.category == 'of' else "demanda de "
            tuit = "Se ha creado una " + cat + material + " en " + instance.space.place + ". Ver en: " + url
            t.statuses.update(status=tuit)
        except:
            print("Parece que hay un error en la conexión a Twitter")
