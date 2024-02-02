from django import forms
from .models import *





class AssetTypeModelForm(forms.ModelForm):

    class Meta:
        model = AssetType
        fields = ["type", "description"]


class AssetModelForm(forms.ModelForm):

    type = forms.ModelChoiceField(queryset=AssetType.objects.all())

    class Meta:
        model = Asset
        fields = ["name", "alloted_to", "current_allocation_status", "type", "is_active"]



