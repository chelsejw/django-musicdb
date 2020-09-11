import factory
import factory.django
from database.models import Organisation, TagCategory, User, Playlist, Tag, Track, TrackTag, Artist, Catalog, ArtistFactory, OrganisationFactory, UserFactory, CatalogFactory, TrackFactory



## TO ADD RANDOM TAGS
# for i in range(Track.objects.last().id, Track.objects.first().id):
#     t = Track.objects.get(id=i)
#     bpm_tags = Tag.objects.filter(category__description='BPM')
#     t1 = TrackTag(tag=random.choice(bpm_tags), confidence=random.random())
#     t1.track = t
#     energy_tags = Tag.objects.filter(category__description='Energy')
#     t2 = TrackTag(tag=random.choice(energy_tags), confidence=random.random())
#     t2.track = t
#     genre_tags = Tag.objects.filter(category__description='Genre')
#     t3 = TrackTag(tag=random.choice(genre_tags), confidence=random.random())
#     t3.track = t
#     voice_tags = Tag.objects.filter(category__description='Voice Identity')
#     t4 = TrackTag(tag=random.choice(voice_tags), confidence=random.random())
#     t4.track = t
#     t1.save()
#     t2.save()
#     t3.save()
#     t4.save()


# To make user playlists

for i in range(Playlist.objects.last().id, Playlist.objects.first().id):
    playlist = Playlist.objects.get(id=i)
    available = playlist.user.organisation.catalog.tracks.all()
    for i in range(5, 10):
        playlist.tracks.add(random.choice(available))


for i in range(Catalog.objects.first().id, Catalog.objects.last().id):
    catalog = Catalog.objects.get(id=i)
    for i in range(random.randint(20,400)):
        new_track = Track.objects.get(id=random.randint(Track.objects.last().id, Track.objects.first().id))
        catalog.tracks.add(new_track)
    catalog.save()
    
    
