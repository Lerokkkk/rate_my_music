import django
from django.http.response import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.views.generic.edit import ModelFormMixin, FormMixin
from .forms import AddPostArtistForm, CompositionForm, RateForm, CustomSearchForm
from .models import Artist, Composition
from .utils import MenuMixin
from django import forms
from .models import Rate
from django.db.models import Avg, Subquery, OuterRef
from haystack.generic_views import SearchView


class CustomSearchView(SearchView):
    form_class = CustomSearchForm
    # template_name = 'base.html'
    template_name = 'main/search_results.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = f'Результаты поиска: {context["query"]}'
        # print('context is', context)
        # print('object list is', context['object_list'])
        # for obj in context['object_list']:
        #     print(obj.__dict__)
        #     if obj.model_name == 'artist':
        #         print(obj.object.photo)
        #     elif obj.model_name == 'composition':
        #         print(obj.title)
        return context


class Index(MenuMixin, ListView):
    template_name = 'main/index.html'
    title = 'Главная страница'
    queryset = Composition.objects.annotate(
        r=Subquery(Rate.objects.filter(composition=OuterRef('pk')).values('composition').annotate(avg_rate=Avg('rate'))
                   .values('avg_rate'))).order_by('-r').first()
    context_object_name = 'q'

    def get_last_release(self):
        return Composition.published.order_by('-release_date').first()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_release'] = self.get_last_release()
        return context


class ShowTopAlbums(MenuMixin, ListView):
    template_name = 'main/albums_of_the_month.html'
    queryset = Composition.objects.annotate(
        r=Subquery(Rate.objects.filter(composition=OuterRef('pk')).values('composition').annotate(avg_rate=Avg('rate'))
                   .values('avg_rate'))).order_by('-r').prefetch_related('artist')
    context_object_name = "Compos"
    title = 'Лучшие альбомы'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_context_mixin(context)


class ShowMusicians(MenuMixin, ListView):
    template_name = 'main/musicians.html'
    # model = Artist
    queryset = Artist.published.all()
    ordering = 'name'
    context_object_name = 'n'
    title = 'Музыканты'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_context_mixin(context)


class ShowArtist(MenuMixin, DetailView):
    template_name = 'main/artist.html'
    slug_url_kwarg = 'artist_slug'
    context_object_name = 'artist'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        artist = context['artist']
        context['published_compositions'] = artist.compositions.filter(is_published=True)
        return self.get_context_mixin(context, title=context['artist'].name)

    def get_object(self, queryset=None):
        return get_object_or_404(Artist.published, slug=self.kwargs[self.slug_url_kwarg])


class ShowComposition(MenuMixin, FormMixin, DetailView):
    model = Composition
    template_name = 'main/composition.html'
    slug_url_kwarg = 'composition_slug'
    pk_url_kwarg = 'composition_id'
    context_object_name = 'composition'
    form_class = RateForm
    # query_pk_and_slug = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['Rate'] = self.avg_rate()
        print(context)
        return self.get_context_mixin(context, title=self.object.title, form=self.get_form())

    def avg_rate(self):
        composition = self.get_object()
        rate = Rate.objects.filter(composition=composition).aggregate(Avg('rate'))
        if rate['rate__avg']:
            return round(rate['rate__avg'], 2)
        else:
            return 'Еще не оценивали'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_authenticated:
            kwargs['user'] = self.request.user
        kwargs['composition'] = self.get_object()
        return kwargs

    def get_object(self, queryset=None):
        composition = self.model.published.prefetch_related('artist')
        return get_object_or_404(composition, slug=self.kwargs[self.slug_url_kwarg], id=self.kwargs[self.pk_url_kwarg])

    def get_success_url(self):
        composition = self.get_object()
        return reverse('composition', kwargs={
            'composition_slug': composition.slug,
            'composition_id': composition.id
        })

    def delete_rate(self):
        rate = Rate.objects.filter(composition=self.get_object(), user=self.request.user).first()
        rate.delete()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        if 'delete_rating' in request.POST:
            return self.delete_rate()
        else:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def form_valid(self, form: forms):
        composition = self.get_object()
        user = self.request.user
        rate = Rate.objects.filter(composition=composition, user=user).first()
        if rate:
            rate.rate = form.cleaned_data['rate']
            rate.save()
        else:
            form.instance.composition = composition
            form.instance.user = user
            form.save()

        return super().form_valid(form)


class AddArtist(LoginRequiredMixin, MenuMixin, CreateView):
    form_class = AddPostArtistForm
    template_name = 'main/add_artist.html'
    success_url = reverse_lazy('home')
    title = 'Добавление артиста'


class AddComposition(LoginRequiredMixin, MenuMixin, CreateView):
    form_class = CompositionForm
    template_name = 'main/add_composition.html'
    success_url = reverse_lazy('home')
    title = 'Добавление композиции'






