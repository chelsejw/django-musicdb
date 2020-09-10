from django.db import models
from datetime import timedelta

# Create your models here.


class Organisation(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']


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


class Artist(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


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

    def get_artists(self):
        qs = self.artists.all()
        artists = list(qs)
        names = []
        for artist in artists:
            names.append(artist.name)
        return ", ".join(names)

    def __str__(self):
        return f"{self.title} by {self.get_artists()}"

    class Meta:
        ordering = ['-created']


class Catalog(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    # Each organisation can only have one catalog
    organisation = models.OneToOneField(Organisation, on_delete=models.CASCADE)
    tracks = models.ManyToManyField(Track)

    def __str__(self):
        return self.organisation.title


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tracks = models.ManyToManyField(Track)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']


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
