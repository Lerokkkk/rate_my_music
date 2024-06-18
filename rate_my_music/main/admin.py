from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from .models import Artist, Composition


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_photo', 'slug', 'is_published')
    list_display_links = ('name', 'slug')
    actions = ['toggle_published']
    search_fields = ('name', )
    list_filter = ['is_published']
    prepopulated_fields = {"slug": ("name", )}
    save_on_top = True

    def toggle_published(self, request, queryset):
        for obj in queryset:
            obj.is_published = not obj.is_published
            obj.save()

    @admin.display(description='Фото')
    def get_photo(self, artist: Artist):
        if artist.photo:
            return mark_safe(f"<img src='{artist.photo.url}' width=50>")
        else:
            return "Без фото"


@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    list_display = ('get_collab_artists', 'title', 'get_photo', 'release_date', 'composition_type', 'get_featured_artists', 'is_published')
    search_fields = ('title', 'artist__name', 'slug')
    actions = ['toggle_published']
    list_display_links = ('title', 'get_collab_artists', 'get_collab_artists')
    prepopulated_fields = {"slug": ("title", )}
    list_filter = ('composition_type', 'is_published')
    filter_horizontal = ['artist', 'featured_artist']
    save_on_top = True

    @admin.display(description='Фит артисты')
    def get_featured_artists(self, compos: Composition):
        return ' '.join(str(obj) for obj in compos.featured_artist.all())

    @admin.display(description='Артисты')
    def get_collab_artists(self, compos: Composition):
        return ' '.join(str(obj) for obj in compos.artist.all())

    @admin.display(description='Фото')
    def get_photo(self, compos: Composition):
        if compos.photo:
            return mark_safe(f"<img src='{compos.photo.url}' width=50>")
        else:
            return "Без фото"

    def toggle_published(self, request, queryset):
        for obj in queryset:
            obj.is_published = not obj.is_published
            obj.save()