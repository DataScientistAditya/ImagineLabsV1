from pyexpat import model
from attr import field
from django import forms
from .models import PptData

class PptForm(forms.ModelForm):
    
    class Meta:
        model = PptData
        fields = ('Query','isLayman')
        layman_choices = (
            (" ","Select"),
            (True,"Yes"),
            (False,"No"),
        )
        labels = {
            "Query": "Search Tags",
            "isLayman": "Layman Term ?"
        }
        widgets = {
            'Query': forms.TextInput(attrs={"class":"email", "placeholder":"Search your documnents here...","type":"text"}),
            'isLayman': forms.Select(choices= layman_choices,attrs={'class': 'laymanfield',"type":"text"}),
        }