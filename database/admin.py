from django.contrib import admin
from database.models import Organisation, TagCategory, User, Playlist, Tag, Track, TrackTag, Artist, Catalog
admin.site.register(Organisation)
admin.site.register(User)  
admin.site.register(Playlist)
admin.site.register(Track)
admin.site.register(Tag)
admin.site.register(TrackTag)
admin.site.register(Artist)
admin.site.register(Catalog)
admin.site.register(TagCategory)

# Register your models here.
