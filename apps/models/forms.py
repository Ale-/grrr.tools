from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from . import models
from apps.utils import widgets as utils
from apps.utils.fields import GroupedModelChoiceField
from . import categories

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
        super(PostForm, self).__init__(*args, **kwargs)

class SpaceForm(forms.ModelForm):
    """Form to create/update Blog posts"""

    class Meta:
        model   = models.Space
        fields = '__all__'
        widgets = {
            'geom'    : utils.GeocodedLeafletWidget(submit_text='Localiza el reuso', provider="google", sources="id_place id_address"),
            'image'   : utils.PictureWithPreviewWidget(),
            'summary' : utils.LimitedTextareaWidget(limit=500),
        }

    def __init__(self, *args, **kwargs):
        super(SpaceForm, self).__init__(*args, **kwargs)

class SmsForm(forms.ModelForm):
    """Sms modelforms"""

    class Meta:
        model   = models.Sms
        fields = '__all__'
        widgets = {
            'body' : utils.LimitedTextareaWidget(limit=500),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs['initial']['user']
        self.base_fields['emissor'].empty_label = None
        self.base_fields['emissor'].queryset = models.Node.objects.filter(users__in=[user])
        if 'receiver' in kwargs['initial']:
            self.base_fields['receiver'].widget.attrs['disabled'] = True
            self.base_fields['receiver'].widget.attrs['readonly'] = True
        else:
            self.base_fields['receiver'].empty_label = None
            self.base_fields['receiver'].queryset = models.Node.objects.all().order_by('name')
        super(SmsForm, self).__init__(*args, **kwargs)

class BatchForm(forms.ModelForm):
    """Batch modelforms"""

    def group_label(material_key):
        return dict(categories.MATERIALS_BY_FAMILY)[material_key]

    material = GroupedModelChoiceField(queryset=models.Material.objects.order_by('family', 'name'),
                                       label='Material',
                                       help_text=_('El material del que se compone el lote.'),
                                       group_by_field='family', group_label=group_label,
                                       empty_label=" ", widget = utils.SelectOrAddWidget(view_name='models:create_material_popup', link_text=_("Añade un material")) )

    class Meta:
        model   = models.Batch
        fields = '__all__'
        widgets = {
            'image'       : utils.PictureWithPreviewWidget(),
            'public_info' : utils.LimitedTextareaWidget(limit=500),
            'private_info' : utils.LimitedTextareaWidget(limit=500)
        }

    def __init__(self, *args, **kwargs):
        user = kwargs['initial']['user']
        self.base_fields['material'].empty_label = None
        self.base_fields['space'].empty_label = None
        self.base_fields['space'].queryset = models.Space.objects.filter( nodes__in=user.users.all() ).order_by('name')
        self.base_fields['space'].widget.attrs['placeholder'] = _("dd/mm/aaaa, por ejemplo: 01/05/2015")
        super(BatchForm, self).__init__(*args, **kwargs)
