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

    # green field is optional
    green_field = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)

    def save(self, *args, **kwargs):
        file_id = kwargs.get('file_id', None)
        chunk_id = kwargs.get('chunk_id', None)
        geometry = json.loads(self.cleaned_data['geometry'].replace("'", '"'))
        try:
            green_field = json.loads(
                self.cleaned_data['green_field'].replace("'", '"'))
        except:
            green_field = None
        json_data = get_feature(
            id=self.cleaned_data['id'], geometry=geometry, green_field=green_field)
        if chunk_id:
            chunk = Chunk.objects.get(id=chunk_id)
            chunk.json = json_data
            chunk.save()
        else:
            return Chunk.objects.create(json=json_data, file=GeoJsonFile.objects.get(id=file_id))
