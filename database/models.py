from django.db import models
from datetime import timedelta
import factory
import factory.django
# Create your models here.

import random

class Organisation(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']


class OrganisationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organisation
    title = factory.Faker('company')

class User(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=30, unique=True)
    role = models.CharField(max_length=10)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-created']


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: 'user{}'.format(n))
    organisation = factory.LazyFunction(lambda: Organisation.objects.get(id=random.randint(Organisation.objects.last().id, Organisation.objects.first().id)))
    role = factory.LazyFunction(lambda: random.choice(['admin', 'standard']))


class Artist(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def get_tracks(self):
        return Track.objects.filter(artist_id=self.id)

class ArtistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Artist
    name = factory.Faker('name')

class TagCategory(models.Model):
    description = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.description


class Tag(models.Model):
    # BPM, instruments, vocals, mood, energy, etc
    category = models.ForeignKey(TagCategory, on_delete=models.CASCADE)
    # 90bpm, cymbals, female, thrilling, etc.
    details = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.category.description}: {self.details}"

    class Meta:
        ordering = ['category']

class Track(models.Model):
    artists = models.ManyToManyField(Artist)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    duration = models.DurationField(default=timedelta(minutes=5))
    title = models.CharField(max_length=50)
    released = models.DateField()
    tags = models.ManyToManyField(Tag, through='TrackTag', blank=True)

    # def get_artists(self):
    #     qs = self.artists.all()
    #     artists = list(qs)
    #     names = []
    #     for artist in artists:
    #         names.append(artist.name)
    #     return ", ".join(names)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ['-created']

        
class TrackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Track   
        
    duration = factory.LazyFunction(lambda: timedelta(minutes=random.randint(1,6)))
    title = factory.LazyFunction(lambda: f"{factory.Faker('first_name_nonbinary').generate()} {factory.Faker('safe_color_name').generate()}")
    released = factory.Faker('date')

    @factory.post_generation
    def artists(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.groups.add(group)

class Catalog(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    # Each organisation can only have one catalog
    organisation = models.OneToOneField(Organisation, on_delete=models.CASCADE)
    tracks = models.ManyToManyField(Track, blank=True)

    def __str__(self):
        return self.organisation.title


class CatalogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Catalog
    organisation = factory.Sequence(lambda x: Organisation.objects.get(id=x))

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tracks = models.ManyToManyField(Track, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']



    #CLEAN would only work in a form -- not here
    def clean(self):
        for track in self.tracks.all():
            if self.user.organisation.catalog.tracks.filter(id=track.id):
                raise ValidationError("There is a track that is not available to your organisation's catalog.")

class PlaylistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Playlist
    organisation = factory.Sequence(lambda x: Organisation.objects.get(id=x))


class TrackTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    # Eg (0.9999 = 99.99%, 0.1725 = 17.25%, 1.0000 = 100%)
    confidence = models.DecimalField(max_digits=5, decimal_places=4)

    def __str__(self):
        return f"{self.track}: {self.tag}"

    class Meta:
        ordering = ['-created']
