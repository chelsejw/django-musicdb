
from django_seed import Seed
seeder = Seed.seeder()
from database.models import Organisation, TagCategory, User, Playlist, Tag, Track, TrackTag, Artist, Catalog

seeder.add_artists(Artist, 100, {
    'name': lambda x: seeder.faker.name(),
})

seeder.execute()
