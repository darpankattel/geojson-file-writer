from django import forms
from .models import GeoJsonFile, Chunk
from .utils import get_feature
import json


class GeoJsonFileForm(forms.ModelForm):
    class Meta:
        model = GeoJsonFile
        fields = ['title', 'description', 'type_of_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'type_of_file': forms.Select(attrs={'class': 'form-control'}),
        }


class ChunkForm(forms.Form):
    id = forms.IntegerField(label='ID', required=True,
                            widget=forms.NumberInput(attrs={'class': 'form-control'}))
    geometry = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}))

    def save(self, *args, **kwargs):
        file_id = kwargs.pop('file_id')
        json_data = get_feature(
            id=self.cleaned_data['id'], geometry=json.loads(self.cleaned_data['geometry']))
        return Chunk.objects.create(json=json_data, file=GeoJsonFile.objects.get(id=file_id))
