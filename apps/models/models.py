# Import python packages
import time
from datetime import date

# Import django packages
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation

# Import contrib apps
from djgeojson.fields import PointField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from ckeditor_uploader.fields import RichTextUploadingField
from star_ratings.models import Rating

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
    weight        = models.PositiveIntegerField(_("Peso unitario"), blank=True, null=True,
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
    nodes         = models.ManyToManyField(Node, verbose_name="Nodos", blank=False, related_name="Nodos",
                    help_text=_("¿Qué nodos de la red participan en este espacio? Mantén presionado 'Control' o 'Command' en un Mac, para seleccionar más de una opción."))
    image         = models.ImageField(_("Imagen"), blank=False, upload_to="images/news/",
                    help_text=_("Una imagen significativa del espacio para las vistas de resúmenes de contenido y el encabezado de la vista completa. Puedes añadir más imágenes al texto completo del reuso."))
    thumbnail     = ImageSpecField(source="image", processors=[ResizeToFill(200, 200)], format='JPEG', options={'quality': 85})
    agreement     = models.ManyToManyField(Agreement, verbose_name="Acuerdos", related_name="agreement", blank=True,
                    help_text=_("Puedes asociar documentos de acuerdos de cesión al espacio."))
    summary       = models.TextField(_("Resumen"), blank=False,
                    help_text=_("Un resumen de la noticia para las vistas de contenidos, si no lo usas se usará un recorte del cuerpo."))
    place         = models.CharField(_("Localidad"), max_length=128, blank=True, null=True,
                    help_text=_("El nombre de la localidad —ciudad, pueblo, ámbito— donde se hizo el reuso. Aunque es opcional, esta información ayuda al resto de usuari@s a contextualizar la iniciativa rápidamente."))
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
        user_in_groups = self.nodes.filter(users__in = [user]).count() > 0
        return user_in_groups or user.is_staff

class Post(models.Model):
    """News about the GRRR project and the site."""

    title         = models.CharField(_("Título"), max_length=128,
                    help_text=_("El titulo del post."))
    space         = models.ForeignKey(Space, verbose_name=_("Espacio"), null=True,
                    help_text=_("¿Al blog de qué espacio está asociado este post?"))
    slug          = models.SlugField(editable=False, blank=True)
    creation_date = models.DateField(_("Fecha"), default=date.today,
                    help_text=_("Usa el formato dd/mm/aaaa, por ejemplo: 01/05/2015."))
    author        = models.ForeignKey(User, related_name="author", verbose_name=_("Autor-"), null=True, blank=False)
    published     = models.BooleanField(_("Publicado"), default=True, blank=False,
                    help_text=_("Sólo los contenidos publicados serán visibles. Desmarca esta casilla para generar un borrador que podrás publicar más adelante, cuando esté acabado."))
    grrr_blog     = models.BooleanField(_("Blog del GRRR"), default=False, blank=False,
                    help_text=_("Indica si es un post para el blog principal de la web."))
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

class Sms(models.Model):
    """Messages sent to nodes of the network"""

    author   = models.ForeignKey(User, blank=True, null=True, editable=False)
    date     = models.DateField(blank=True, editable=False, default=date.today)
    category = models.CharField(_("Tipo de mensaje"), max_length=2, choices=categories.MESSAGE_CATEGORIES, default='me',
               help_text=_("Elige el tipo de mensaje que quieres enviar."))
    emissor  = models.ForeignKey(Node, verbose_name=_("Remitente"), related_name="emissor", null=True, blank=True,
               help_text=_("Especifica el proyecto que quieres que aparezca como remitente. Esto es aconsejado si el mensaje se manda en relación a un lote."))
    receiver = models.ForeignKey(Node, verbose_name=_("Destinatario"), related_name="receiver", null=True,
               help_text=_("Nodo al que envias el mensaje"))
    body     = models.TextField(_("Mensaje"), blank=False,
               help_text=_("Texto del mensaje. No está permitido usar HTML. Las URLs se convertirán directamente en enlaces."))

    def __str__(self):
        """String representation of model instances."""
        return "Mensaje de " + self.emissor.name + " a " + self.receiver.name + " del " + str(self.date)


class Milestone(models.Model):
    """Milestones register batch transfer between spaces. Created automatically not in forms"""

    date     = models.DateField(null = True)
    space    = models.ForeignKey(Space, null = True)
    category = models.CharField(max_length=2, choices=categories.MILESTONE_CATEGORIES, default='TR')
    quantity = models.PositiveIntegerField(null = True)

    def __str__(self):
        """String representation of model instances."""
        return self.get_category_display() + " | " + self.space.name + " | " + str(self.date)


class Batch(models.Model):
    """Batches of the same material associated to spaces."""

    category     = models.CharField(_("¿Oferta o demanda?"), max_length=2, choices=categories.BATCH_CATEGORIES, default='de',
                   help_text=_("¿Ofreces o necesitas materiales?"))
    space        = models.ForeignKey(Space, verbose_name=_("Espacio"), null=True,
                   help_text=_("¿A qué espacio está asociada la oferta/demanda?"))
    date         = models.DateField(_("Fecha de entrada"), default=date.today,
                   help_text=_("Fecha de entrada del lote en tu inventario"))
    material     = models.ForeignKey(Material, verbose_name=_("Material"), blank=False, null=True, on_delete=models.SET_NULL,
                   help_text=_("El material del que se compone el lote"))
    image        = models.ImageField(_("Imagen"), blank=True, upload_to="images/batches/")
    quantity     = models.PositiveIntegerField(_("Cantidad"), blank=True, null=True,
                   help_text=_("Especifica en las unidades del material cuánto se ofrece o necesita —opcional—."))
    public_info  = models.TextField(_("Información pública"), blank=True, null=True,
                   help_text=_("Informa en este campo de características del lote."))
    private_info = models.TextField(_("Información privada"), blank=True, null=True,
                   help_text=_("Información de carácter privado, sólo para usuari*s de los nodos asociados al espacio."))
    expiration   = models.DateField(_("Fecha de expiración"), blank=True, null=True,
                   help_text=_("Fecha límite opcional para la oferta/demanda."))
    milestones   = models.ManyToManyField(Milestone, blank=True)

    class Meta:
        verbose_name_plural = "Batches"

    def __str__(self):
          """Sets string representation of model instances."""
          return self.space.name + " · Material: " + (self.material.name if self.material else "NULL") + " # " + str(self.id)

    @property
    def material_family(self):
        """Returns the family of the Material object associated with the Batch instance."""
        return self.material.family

    def batch_id(self):
        """Returns the id of the Batch instance."""
        return "%03d" % self.pk

    def edit_permissions(self, user):
        """Returns users allowed to edit an instance of this model."""
        return self.space.edit_permissions(user)

    def save(self, *args, **kwargs):
        """Notifies the creation of the instance to nodes that demand the material of the batch."""
        super(Batch, self).save(*args, **kwargs)

        # Add a new milestone to the list of milestones
        if(self.category == 'of'):
            milestone = Milestone.objects.create(
                date     = self.date,
                space    = self.space,
                category = 'TR',
                quantity = self.quantity,
            )
            self.milestones.add(milestone)

        # TODO:
        # if self.public_quantity is not None and self.public_quantity > 0:
        #     batches = Batch.objects.filter(material=self.material).filter(public_quantity=0)
        #     for batch in batches:
        #         msg = ProjectMessage()
        #         msg.body = "Es un mensaje automático para indicarte que se ha creado un lote que se ajusta a una necesidad tuya"
        #         msg.category = 'of'
        #         msg.emissor = self.project
        #         msg.receiver = batch.project
        #         msg.save()
