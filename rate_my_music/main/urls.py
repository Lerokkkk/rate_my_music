from django.urls import path
from django.utils.text import slugify

from . import views


urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path(slugify('top albums/'), views.ShowTopAlbums.as_view(), name='albums'),
    path(slugify('musicians/'), views.ShowMusicians.as_view(), name='musicians'),
    path('musicians/<slug:artist_slug>/', views.ShowArtist.as_view(), name='artist'),
    path('albums/<int:composition_id>/<slug:composition_slug>/', views.ShowComposition.as_view(), name='composition'),
    path('add_artist/', views.AddArtist.as_view(), name='add_artist'),
    path('add_composition/', views.AddComposition.as_view(), name='add_composition'),
    path('search/', views.CustomSearchView.as_view(), name='haystack_search'),
]