# stdlib imports
import collections
import random
from datetime import datetime

# third-party imports
from django.db.models import F
from rest_framework import generics, status
from rest_framework.response import Response

# local imports
from .models import QueuedTrack, QueuedTrackHistory, QueuedTrackVote
from radio_metadata.models import Track


def _add_random_to_queue():
    """
    Selects a track for the "tracks" database table
    and add its to the top of the queue
    """
    # Grab the first 50 tracks with the highest number of votes
    track_ids = Track.objects.order_by('-vote_count').values_list('id', flat=True)[:50]
    # Select a track ID at random
    track_id = random.choice(track_ids)
    track = Track.objects.get(id=track_id)
    # Create the new playlist track, with the track "started"
    QueuedTrack.objects.create(
        track=track,
        position=1,
        started=datetime.now(),
        value=0,
    )
    # Return the track instance
    return track


def _get_track_from_queue():
    """
    Fetches the track in position 1 of the queue
    If the queue is empty then a random track is added
    """
    try:
        # Fetch the top track in a playlist
        queued_track = QueuedTrack.objects.get(position=1)
        # Grab the track data
        track = queued_track.track

        # Ensure the track has not been downvoted to dead
        # If track is dead, then remove from queue,
        # reset postions, and try again
        if queued_track.alive is False:
            queued_track.delete()
            _reset_queue_positions()
            return _get_track_from_queue()

        # Check to see if the track has started
        if queued_track.started:
            # If track has started work out how much time has passed
            now = datetime.now().replace(tzinfo=None)
            started = queued_track.started.replace(tzinfo=None)
            diff = now - started
            diff = diff.total_seconds().__int__() * 1000
            track_len = track.duration_ms
            # If the time difference is greater that then length of the song,
            # remove the track and start the next
            if diff >= track_len:
                queued_track.delete()
                _reset_queue_positions()
                return _get_track_from_queue()
            else:
                # Add the time lapsed param to the track data
                queued_track.time_lapse = diff
        else:
            # If there is a track, but it hasn't started yet, then start track
            queued_track.started = datetime.now()
            queued_track.save()

            queued_track.time_lapse = 0

        queued_track.votes = QueuedTrackVote.objects.filter(
            queued_track_id=queued_track.id
        )

    except:
        # If the playlist is empty, then insert a random track
        track = _add_random_to_queue()
        # Add default time_lapse and votes to the queued track
        queued_track.time_lapse = 0
        queued_track.votes = [0]

    return queued_track


def _reset_queue_positions():
    """
    Once a record has been removed from the queue, reset the postions,
    to move the tracks up a place
    """
    queue_items = QueuedTrack.objects.filter()

    for (i, track) in enumerate(queue_items):
        track.position = i+1
        track.save()


class QueueList(generics.GenericAPIView):
    """
    List of all the tracks in the queue
    """
    def get(self, request, *args, **kwargs):
        results = []
        # Fetch all tracks in the queue
        try:
            queued_tracks = QueuedTrack.objects.all()
        except:
            response = {
                'message': 'No queued tracks found',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        # Build a response for each track found
        for (i, queued_track) in enumerate(queued_tracks):
            track = queued_track.track
            artists = track.artists.all()
            votes = QueuedTrackVote.objects.filter(
                queued_track_id=queued_track.id
            )
            # Build the track url given its source
            if (track.source_type == 'spotify'):
                album_name = track.album.name
            elif (track.source_type == 'soundcloud'):
                album_name = 'soundcloud'

            # Data to be returned
            results.append(collections.OrderedDict([
                ('id', queued_track.id),
                ('track_id', track.id),
                ('source_id', track.source_id),
                ('source_type', track.source_type),
                ('track_name', track.name),
                ('album_name', album_name),
                ('artists', [x.name for x in artists]),
                ('votes', votes.values()),
                ('total_votes', sum(votes.values_list('value', flat=True))),
                ('alive', queued_track.alive),
                ('image_small', track.image_small),
                ('image_medium', track.image_medium),
                ('image_large', track.image_large),
            ]))

        queueObj = collections.OrderedDict([
            ('count', len(results)),
            ('next', None),
            ('previous', None),
            ('results', results),
        ])

        return Response(queueObj)


class QueueNextTrack(generics.GenericAPIView):
    """
    Fetchs a track to be played
    """
    def get(self, request, *args, **kwargs):
        # Fetch the track in position 1
        try:
            queued_track = _get_track_from_queue()
            track = queued_track.track
            artists = track.artists.all()
        except:
            response = {
                'message': 'No queued tracks found',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        # Build the track url given its source
        if (track.source_type == 'spotify'):
            trackUrl = 'spotify:track:' + queued_track.track.source_id
            album_name = track.album.name
        elif (track.source_type == 'soundcloud'):
            trackUrl = 'soundcloud:song/' + track.name + '.' + track.source_id
            album_name = 'soundcloud'

        # Data to be returned
        response = collections.OrderedDict([
            ('id', queued_track.id),
            ('track_id', track.id),
            ('source_id', track.source_id),
            ('source_type', track.source_type),
            ('track_name', track.name),
            ('album_name', album_name),
            ('artists', [x.name for x in artists]),
            ('votes', queued_track.votes.values()),
            ('total_votes', sum(
                queued_track.votes.values_list('value', flat=True)
            )),
            ('alive', queued_track.alive),
            ('image_small', track.image_small),
            ('image_medium', track.image_medium),
            ('image_large', track.image_large),
            ('url', trackUrl),
        ])

        # Return the url for mopidy, and set CORS headers for ajax
        return Response(
            response,
            headers={'Access-Control-Allow-Origin': '*'}
        )


class QueueAddTrack(generics.GenericAPIView):
    """
    Add a playlist track to the queue.
    Will be placed at the bottom of the queue
    """
    def get(self, request, *args, **kwargs):
        # Count number of tracks in queue
        queued_tracks = QueuedTrack.objects.all()
        current_num_records = queued_tracks.count()
        current_num_user_records = queued_tracks.filter().count()

        # Users are only permitted to have 3 active tracks in the queue at any one time
        if current_num_user_records > 3:
            response = {
                'message': 'Max number of tracks reached from this user',
            }
            return Response(response)

        # Fetch track and update the tracks play count
        try:
            track = Track.objects.get(id=kwargs['track_id'])
            track.play_count = F('play_count') + 1
            track.save()
        except:
            response = {
                'message': 'Track not found',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        # Add track to queue
        try:
            QueuedTrack.objects.create(
                track=track,
                position=current_num_records+1,
                owner=self.request.user,
            )
        except:
            response = {
                'message': 'Failed to add track to queue',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        # Make a note of who added the track to the playlist
        try:
            QueuedTrackHistory.objects.create(
                track=track,
                owner=self.request.user,
            )
        except:
            response = {
                'message': 'Failed to save track history',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        return Response({'msg': 'Track successfully added to queue'})


class QueueTrackVote(generics.GenericAPIView):
    """
    Vote on a track in the queue
    """
    def get(self, request, *args, **kwargs):
        track_id = kwargs['track_id']
        vote = kwargs['vote']
        # Fetch queued track
        try:
            queued_track = QueuedTrack.objects.get(id=track_id)
        except:
            response = {
                'message': 'Could not find queued track with id ' + track_id,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        try:
            # Add track to queue
            queued_track_vote, created = QueuedTrackVote.objects.get_or_create(
                queued_track=queued_track,
                owner=self.request.user,
            )

            if created:
                queued_track_vote.value = vote
                queued_track_vote.save()

                # Update the tracks total vote
                track = queued_track.track
                track.vote_count = F('vote_count') + vote
                track.save()
            else:
                response = {
                    'message': 'User has already voted on this track',
                }
                return Response(response)

        except:
            response = {
                'message': 'Failed to save vote',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        # When a tracks voting total reachs -3 votes, then remove from queue
        votes = QueuedTrackVote.objects.filter(
            queued_track_id=queued_track.id
        ).values_list('value', flat=True)

        # If a track is upvoted from being dead, then toggle alive
        if sum(votes) > -3 and queued_track.alive is False:
            queued_track.alive = True
            queued_track.save()

        # If a queued track's total votes gets to -3, then Kill queued track
        if sum(votes) <= -3:
            if queued_track.position != 1:
                queued_track.alive = False
                queued_track.save()

        return Response({'message': 'Your vote has been saved'})
