from haystack import indexes
from .models import Artist, Composition


class ArtistIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    photo = indexes.CharField(model_attr='photo')
    url = indexes.CharField(model_attr='get_absolute_url')

    def get_model(self):
        return Artist

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_published=True)


class CompositionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    photo = indexes.CharField(model_attr='photo')
    url = indexes.CharField(model_attr='get_absolute_url')

    def get_model(self):
        return Composition

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_published=True)
