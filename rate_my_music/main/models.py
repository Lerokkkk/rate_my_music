from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from datetime import date
from unidecode import unidecode
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=1)


class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Имя')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True, verbose_name='Фото')
    is_published = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = 'Артист'
        verbose_name_plural = "Артисты"
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('artist', kwargs={'artist_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(str(self.name)))
        print(self.slug)
        super().save(*args, **kwargs)


class Composition(models.Model):

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = 'Композиция'
        verbose_name_plural = "Композиции"
        ordering = ['-release_date']

    class CompositionType(models.TextChoices):
        SOLO = "SOLO"
        FEATURE = "FEAT"
        COLLABORATIVE = "COLLAB"
        COLLABORATIVE_FEATURE = "COLLAB_FEAT"

    title = models.CharField(max_length=200, verbose_name='Название')
    release_date = models.DateField(default=date.today, verbose_name='Дата релиза')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True, verbose_name='Фото')
    slug = models.CharField(max_length=255)
    artist = models.ManyToManyField(Artist, related_name='compositions',
                                    verbose_name='Артист (Зажать CTRL чтобы выбрать несколько)')
    composition_type = models.CharField(max_length=11,
                                        choices=CompositionType.choices,
                                        default=CompositionType.SOLO, verbose_name='Тип композиции')
    featured_artist = models.ManyToManyField(Artist, blank=True, related_name='featured_compositions',
                                             verbose_name='Артист на фите (Зажать CTRL чтобы выбрать несколько)')
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('composition', kwargs={'composition_slug': self.slug, 'composition_id': self.pk})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Rate(models.Model):

    class Grades(models.TextChoices):
        APPALLING = "1", "1"
        HORRIBLE = "2", "2"
        VERY_BAD = "3", "3"
        BAD = "4", "4"
        AVERAGE = "5", "5"
        FINE = "6", "6"
        GOOD = "7", "7"
        VERY_GOOD = "8", "8"
        GREAT = "9", "9"
        MASTERPIECE = "10", "10"

    rate = models.CharField(max_length=2, choices=Grades.choices, verbose_name='Оценка')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Юзер', related_name='rate_user')
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE, verbose_name='Композиция', related_name='rate_composition')

