# Import python packages
from datetime import date

# Import django packages
from django import forms
from django.utils.translation import ugettext_lazy as _

# Import app packages
from apps.models import models

class TransferBatchForm(forms.Form):
    date     = forms.DateField(label=_("Fecha"), initial=date.today(),
               help_text=_("Fecha aproximada de transferencia de los materiales"))
    space    = forms.ModelChoiceField(queryset = models.Space.objects.all(),
               label=_("Espacio"), empty_label=None,
               help_text=_("¿A qué espacio de la red se mueven los materiales?"))
    quantity = forms.IntegerField(label=_("Cantidad"), initial=0,
               help_text=_("¿Qué cantidad de materiales del lote se mueven?"))

    def __init__(self, pk, *args, **kwargs):
        self.batch_id = pk
        self.base_fields['space'].empty_label = None
        space = models.Batch.objects.filter(pk=self.batch_id).first().space
        self.base_fields['space'].queryset = models.Space.objects.exclude(pk=space.pk).order_by('name')
        super(TransferBatchForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(TransferBatchForm, self).clean()
        quantity = cleaned_data.get('quantity')
        batch = models.Batch.objects.filter(pk=self.batch_id).first()
        if quantity and quantity > batch.total:
            raise forms.ValidationError(_("No puedes transferir más material del que tienes, Einstein."))


class ActivateBatchForm(forms.Form):
    date     = forms.DateField(label=_("Fecha"), initial=date.today(),
               help_text=_("Fecha aproximada en que los materiales se reutilizaron"))
    quantity = forms.IntegerField(label=_("Cantidad"), initial=0,
               help_text=_("¿Qué cantidad de materiales del lote se han reutilizado?"))

    def __init__(self, pk, *args, **kwargs):
        self.batch_id = pk
        super(ActivateBatchForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ActivateBatchForm, self).clean()
        quantity = cleaned_data.get('quantity')
        batch = models.Batch.objects.filter(pk=self.batch_id).first()
        if quantity and quantity > batch.total:
            raise forms.ValidationError(_("No puedes activar más material del que tienes, huevo."))
