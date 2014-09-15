# third-party imports
from django.core.cache import cache
from django.db import models

# local imports
from radio.utils.cache import build_key

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


class AlbumManager(models.Manager):
    def cached_get_or_create(self, album):
        """Get or create an album record from db,
        Returns an Album model reference.
        """
        cache_key = build_key(
            'album', album['source_type'], album['source_id'])
        record = cache.get(cache_key)

        if record is None:
            record, created = self.get_or_create(
                source_id=album['source_id'],
                source_type=album['source_type'],
                name=album['name'],
            )
            cache.set(cache_key, record)
        return record


class Album(MetadataBase):
    objects = AlbumManager()


class ArtistManager(models.Manager):
    def cached_get_or_create(self, artists):
        """Get or create artist records from db.
        Returns a list of artist json objects
        """
        records = []
        for (i, artist) in enumerate(artists):
            cache_key = build_key(
                'artist', artist['source_type'], artist['source_id'])
            record = cache.get(cache_key)

            if record is None:
                record, created = self.get_or_create(
                    source_id=artist['source_id'],
                    source_type=artist['source_type'],
                    name=artist['name'],
                )
                cache.set(cache_key, record)
            records.append(record)

        return records


class Artist(MetadataBase):
    objects = ArtistManager()


class TrackManager(models.Manager):
    def cached_get_or_create(self, track, owner):
        """Saves a track to the db, unless one already exists.
        Returns a track json object
        """
        cache_key = build_key(
            'track', track['source_type'], track['source_id'])
        record = cache.get(cache_key)

        if record is None:
            try:
                record = self.get(
                    source_id=track['source_id'],
                    source_type=track['source_type'],
                )
            except:
                if track['album']:
                    album = Album.objects.cached_get_or_create(
                        track['album'])

                record = self.create(
                    source_id=track['source_id'],
                    source_type=track['source_type'],
                    name=track['name'],
                    duration_ms=track['duration_ms'],
                    preview_url=track['preview_url'],
                    uri=track['uri'],
                    track_number=track['track_number'],
                    album=album,
                    image_small=track['image_small'],
                    image_medium=track['image_medium'],
                    image_large=track['image_large'],
                    owner=owner
                )

                artists = Artist.objects.cached_get_or_create(track['artists'])
                for artist in artists:
                    record.artists.add(artist)

            cache.set(cache_key, record)

        return record


class Track(MetadataBase):
    # relationships to other models
    artists = models.ManyToManyField(Artist, related_name='track')
    album = models.ForeignKey(Album, null=True)

    # track metadata
    duration_ms = models.IntegerField()
    preview_url = models.URLField()
    uri = models.CharField(max_length=500)
    track_number = models.IntegerField()
    image_small = models.URLField(null=True)
    image_medium = models.URLField(null=True)
    image_large = models.URLField(null=True)

    # Additional information
    play_count = models.IntegerField(default=0)
    owner = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = TrackManager()
