# third-party imports
from django.db import models

SOURCE_TYPES = [
    ('spotify', 'Spotify'),
    ('soundcloud', 'Soundcloud'),
]


class MetadataBase(models.Model):
    # store source type and ID e.g. spotify, soundcloud, youtube, etc.
    source_type = models.CharField(choices=SOURCE_TYPES, max_length=10)
    source_id = models.CharField(max_length=100)

    # generic metadata
    name = models.CharField(max_length=500)

    class Meta:
        abstract = True
        unique_together = (('source_type', 'source_id'),)

    def __unicode__(self):
        return self.name


class Artist(MetadataBase):
    pass


class Album(MetadataBase):
    pass


class Track(MetadataBase):
    # relationships to other models
    artists = models.ManyToManyField(Artist, related_name='track')
    album = models.ForeignKey(Album, null=True)

    # track metadata
    duration_ms = models.IntegerField()
    preview_url = models.URLField()
    track_number = models.IntegerField()
    image_small = models.URLField(null=True)
    image_medium = models.URLField(null=True)
    image_large = models.URLField(null=True)

    # track stats
    play_count = models.IntegerField(default=0)
    owner = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
