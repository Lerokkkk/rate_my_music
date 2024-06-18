from django import forms
from .models import Artist, Composition, Rate
from django.core.exceptions import ValidationError
from haystack.forms import SearchForm


class AddPostArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'photo']


class CompositionForm(forms.ModelForm):
    class Meta:
        model = Composition
        fields = ['title', 'photo', 'release_date', 'composition_type', 'artist', 'featured_artist']

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        composition_type = cleaned_data.get("composition_type")
        featured_artist = cleaned_data.get("featured_artist")
        artist = cleaned_data.get("artist")
        if any(i in artist for i in featured_artist):
            raise ValidationError("Artist can`t be main and feat artist at the same time")
        if composition_type == 'SOLO':
            if len(artist) + len(featured_artist) > 1:
                raise ValidationError("Can`t be more then 1 artist for SOLO composition")
        if composition_type == "COLLAB":
            if len(featured_artist) != 0:
                raise ValidationError("Featured artist cannot be present for COLLAB composition")
            if len(artist) < 2:
                raise ValidationError("For COLLAB composition need at least 2 artists")
        if composition_type == 'FEAT':
            if len(artist) > 1:
                raise ValidationError('For FEAT composition need 1 main artist')
            if len(featured_artist) < 1:
                raise ValidationError("For FEAT composition need at least 1 featured artists")
        if composition_type == 'COLLAB_FEAT':
            if len(artist) < 2 or len(featured_artist) < 1:
                raise ValidationError('FOR COLLABORATIVE FEATURE composition need at least 2 main artists and 1 featured')


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ['rate', ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        composition = kwargs.pop('composition', None)
        super().__init__(*args, **kwargs)
        if user and composition:
            last_rate = Rate.objects.filter(user=user, composition=composition).first()
            if last_rate:
                self.initial['rate'] = last_rate.rate


class CustomSearchForm(SearchForm):
    q = forms.CharField(label='', widget=forms.TextInput(attrs=
            {'placeholder': 'Поиск...', 'class': 'search-input',
             'type': 'text', 'name': 'query'}), required=False)

    def search(self):
        sqs = super().search()

        if not self.is_valid():
            return self.no_query_found()

        return sqs
