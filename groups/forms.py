from django import forms
from groups.models import CustomGroup



class GroupCreateForm(forms.ModelForm):
    name = forms.CharField(label='Group Name')
    about = forms.CharField(label='About Group', widget=forms.Textarea(attrs={'rows': 2}))
    
    class Meta:
        model = CustomGroup
        fields = ['name', 'about',]