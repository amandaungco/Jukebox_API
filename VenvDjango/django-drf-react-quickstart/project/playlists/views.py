from django.shortcuts import render
from .models import Playlist
from django.http import HttpResponse
from .serializers import PlaylistSerializer
from django.http import JsonResponse

import spotipy
from spotipy import oauth2
import spotipy.util as util
import string
import random
import json

from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['POST'])
@parser_classes((JSONParser,))
def playlist_save(request):
    # import pdb; pdb.set_trace();
    print(request.META)
    access_token=request.META['HTTP_X_SPOTIFY_TOKEN']
    # access_token = request.session['token_info']['access_token']
    sp = spotipy.Spotify(access_token)
    user = sp.current_user()

    playlist = Playlist()
    playlist.user_id = user['id']
    playlist.playlist_id = request.data['playlistId']
    playlist.access_token = access_token
    playlist.room_code = id_generator()

    playlist.save()

    serializer = PlaylistSerializer(playlist)
    return Response(serializer.data)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def add_track(request):
    body = json.loads(request.body)
    current_playlist = get_playlistDB(body['room_code'])
    sp = spotipy.Spotify(current_playlist.access_token)
    sp.trace = False
    results = sp.user_playlist_add_tracks(current_playlist.user_id,current_playlist.playlist_id, [body['track_id']])
    return JsonResponse(results)

def get_playlistDB(find_room_code):
    current_playlist = Playlist.objects.get(room_code__exact=find_room_code)
    # queryset = self.queryset

    return current_playlist
