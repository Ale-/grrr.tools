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

    def __init__(self, *args, **kwargs):
        self.base_fields['space'].empty_label = None
        self.base_fields['space'].queryset = models.Space.objects.all().order_by('name')
        super(TransferBatchForm, self).__init__(*args, **kwargs)


class ActivateBatchForm(forms.Form):
    date     = forms.DateField(label=_("Fecha"), initial=date.today(),
               help_text=_("Fecha aproximada en que los materiales se reutilizaron"))
    quantity = forms.IntegerField(label=_("Cantidad"), initial=0,
               help_text=_("¿Qué cantidad de materiales del lote se han reutilizado?"))
