from django import forms
from .models import *



class AssetTypeModelForm(forms.ModelForm):

    class Meta:
        model = AssetType
        fields = ["type", "description"]
        widget = {
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'})
        }


class AssetModelForm(forms.ModelForm):

    # this custom init to limit types to those only created by logged-in user
    def __init__(self, *args, **kwargs):

        # Get the user from the keyword arguments
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # filter queryset based on logged-in user
        if user:
            self.fields['type'].queryset = AssetType.objects.filter(created_by=user)

    class Meta:
        model = Asset
        fields = ["name", "alloted_to", "current_allocation_status", "type", "is_active"]
        widget = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }



