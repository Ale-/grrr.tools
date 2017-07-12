# Import python packages
from datetime import date

# Import django packages
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

# Import app packages
from . import models
from apps.utils import widgets as utils
from apps.utils.fields import GroupedModelChoiceField
from . import categories


class AgreementForm(forms.ModelForm):
    """Form to create/update Agreement objects"""

    class Meta:
        model = models.Agreement
        fields = '__all__'

class NodeCreateForm(forms.ModelForm):
    """Form to create/update Node objects"""

    class Meta:
        model   = models.Node
        exclude = ('users'),
        widgets = {
            'geom'        : utils.GeocodedLeafletWidget(submit_text='Localiza el nodo', provider="google", sources="id_place id_address"),
            'image'       : utils.PictureWithPreviewWidget(),
            'description' : utils.LimitedTextareaWidget(limit=500),
        }

    def __init__(self, *args, **kwargs):
        self.base_fields['manager'].widget.attrs['disabled'] = True
        self.base_fields['manager'].widget.attrs['readonly'] = True
        super(NodeCreateForm, self).__init__(*args, **kwargs)

class NodeUpdateForm(forms.ModelForm):
    """Form to create/update Project objects"""

    class Meta:
        model = models.Node
        fields = '__all__'
        widgets = {
            'geom'        : utils.GeocodedLeafletWidget(submit_text='Localiza el nodo', provider="google", sources="id_place id_address"),
            'image'       : utils.PictureWithPreviewWidget(),
            'description' : utils.LimitedTextareaWidget(limit=500),
        }

    def __init__(self, *args, **kwargs):
        node_users = kwargs['initial'].pop('project_users')
        super(NodeUpdateForm, self).__init__(*args, **kwargs)

class MaterialForm(forms.ModelForm):
    """Form to create/update Node objects"""

    class Meta:
        model   = models.Material
        fields = '__all__'
        widgets = {
            'image'       : utils.PictureWithPreviewWidget(),
            'description' : utils.LimitedTextareaWidget(limit=500),
        }

    def __init__(self, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)

class PostForm(forms.ModelForm):
    """Form to create/update Blog posts"""

    class Meta:
        model   = models.Post
        exclude = ('author'),
        widgets = {
            'image'   : utils.PictureWithPreviewWidget(),
            'summary' : utils.LimitedTextareaWidget(limit=500),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs['initial'].pop('user')
        self.base_fields['space'].queryset = models.Space.objects.filter(nodes__in = user.users.all() )
        self.base_fields['space'].empty_label = None
        super(PostForm, self).__init__(*args, **kwargs)

class SpaceForm(forms.ModelForm):
    """Form to create/update Blog posts"""

    class Meta:
        model   = models.Space
        fields = '__all__'
        widgets = {
            'geom'      : utils.GeocodedLeafletWidget(submit_text='Localiza el reuso', provider="google", sources="id_place id_address"),
            'image'     : utils.PictureWithPreviewWidget(),
            'summary'   : utils.LimitedTextareaWidget(limit=500),
            'agreement' : utils.SelectOrAddMultipleWidget(view_name='models:create_agreement_popup', link_text=_("Añade un acuerdo"))
        }

    def __init__(self, *args, **kwargs):
        self.base_fields['nodes'].queryset = models.Node.objects.all().order_by('name')
        super(SpaceForm, self).__init__(*args, **kwargs)

class SmsForm(forms.ModelForm):
    """Sms modelforms"""

    batch = GroupedModelChoiceField(queryset=models.Batch.objects.order_by('space'),
                                    label=_("Oferta/demanda"),
                                    help_text=_('Si mandas el mensaje en relación a una oferta o demanda puedes especificarla aquí.'),
                                    group_by_field='space',
                                    empty_label=_("El mensaje no está relacionado con ningún lote"), )

    class Meta:
        model   = models.Sms
        fields = '__all__'
        widgets = {
            'body' : utils.LimitedTextareaWidget(limit=500),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs['initial']['user']
        self.base_fields['emissor'].empty_label = None
        nodes = models.Node.objects.filter(users__in=[user])
        user_spaces = models.Space.objects.filter(nodes__in=nodes)
        self.base_fields['emissor'].queryset = user_spaces
        if 'receiver' in kwargs['initial']:
            self.base_fields['receiver'].widget.attrs['readonly'] = True
        else:
            self.base_fields['receiver'].empty_label = None
            self.base_fields['receiver'].queryset = models.Space.objects.all().order_by('name')
        super(SmsForm, self).__init__(*args, **kwargs)

class BatchForm(forms.ModelForm):
    """Batch modelforms"""

    def group_label(material_key):
        return dict(categories.MATERIALS_BY_FAMILY)[material_key]

    material = GroupedModelChoiceField(queryset=models.Material.objects.order_by('family', 'name'),
                                       label=_('Material'),
                                       help_text=_('El material del que se compone el lote.'),
                                       group_by_field='family', group_label=group_label,
                                       empty_label=" ", widget = utils.SelectOrAddWidget(view_name='models:create_material_popup', link_text=_("Añade un material")))

    class Meta:
        model   = models.Batch
        fields = '__all__'
        widgets = {
            'image'        : utils.PictureWithPreviewWidget(),
            'public_info'  : utils.LimitedTextareaWidget(limit=500),
            'private_info' : utils.LimitedTextareaWidget(limit=500)
        }

    def __init__(self, *args, **kwargs):
        user = kwargs['initial']['user']
        self.base_fields['category'].choices = categories.BATCH_FORM_CATEGORIES
        self.base_fields['material'].empty_label = None
        self.base_fields['space'].empty_label = None
        if user.is_staff:
            self.base_fields['space'].queryset = models.Space.objects.all().order_by('name')
        else:
            self.base_fields['space'].queryset = models.Space.objects.filter( nodes__in=user.users.all() ).order_by('name')
        self.base_fields['date'].widget.attrs['placeholder'] = _("Usa el formato dd/mm/aaaa, por ejemplo: 01/05/2015")
        super(BatchForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(BatchForm, self).clean()
        quantity = cleaned_data.get("quantity")
        total    = cleaned_data.get("total")
        category = cleaned_data.get("category")
        if total and category == 'de' :
            raise forms.ValidationError(_("El campo 'Cantidad total' no se usa en demandas, usa sólo el campo 'Cantidad'"))
        if total and quantity and total < quantity:
            raise forms.ValidationError(_("La cantidad total no puede ser inferior a la ofrecida, melón!"))
        if category == 'of' and not total and not quantity:
            raise forms.ValidationError(_("Las entradas de lotes han de tener al menos una cantidad asociada, sea la ofrecida o la total"))
