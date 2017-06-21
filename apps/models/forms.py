from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from . import models
from apps.utils import widgets as utils

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
        super(PostForm, self).__init__(*args, **kwargs)
