import factory
import factory.django
from database.models import Organisation, TagCategory, User, Playlist, Tag, Track, TrackTag, Artist, Catalog, ArtistFactory, OrganisationFactory, UserFactory

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Artist

    name = factory.Faker('name')
    address = factory.Faker('address')
    phone_number = factory.Faker('phone_number')
