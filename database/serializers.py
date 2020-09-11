from .models import Organisation, TagCategory, User, Playlist, Tag, Track, TrackTag, Artist, Catalog
from rest_framework import serializers


class OrganisationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organisation
        fields = ['created', 'title']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['organisation', 'created', 'updated', 'username', 'role']

class TagCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TagCategory
        fields = ['description']

class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    # tracks = TrackSerializer(read_only=True, many=True)
    
    class Meta:
        model = Artist
        fields = ['name']


class TagSerializer(serializers.HyperlinkedModelSerializer):
    category = TagCategorySerializer(read_only=True)

    class Meta:
        model = Tag
        fields = ['category', 'details']

class TrackSerializer(serializers.HyperlinkedModelSerializer):
    artists = ArtistSerializer(read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Track
        fields = ['title', 'created', 'updated',
                  'duration', 'released', 'artists', 'tags']

class CatalogSerializer(serializers.HyperlinkedModelSerializer):

    organisation = OrganisationSerializer(read_only=True)
    tracks = TrackSerializer(read_only=True, many=True)

    class Meta:
        model = Catalog
        fields = ['organisation', 'tracks']
