from django.shortcuts import render

# Create your views here.
from .models import Organisation, TagCategory, User, Playlist, Tag, Track, TrackTag, Artist, Catalog
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import OrganisationSerializer, UserSerializer, TrackSerializer, ArtistSerializer, TagSerializer, CatalogSerializer, PlaylistSerializer


class OrganisationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TrackViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    # queryset = Track.objects.all()
    serializer_class = TrackSerializer
    queryset = Track.objects.all()

    def get_queryset(self):
        queryset = Track.objects.all()
        tag_id = self.request.query_params.get('tag_id', None)
        if tag_id is not None:
            queryset = queryset.filter(tags__id=tag_id)
        return queryset


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    

class ArtistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
