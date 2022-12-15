"""karaokey/karaokey/consumer.py"""
import json
from urllib.error import HTTPError
from googleapiclient.discovery import build
from django.db import IntegrityError
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from karaokey.models import Song

api_service_name = "youtube"
api_version = "v3"

with open("apikey.txt", "r") as f:
    api_key = f.read()

yt_api = build('youtube', 'v3', developerKey=api_key)


def filter_embeddable(songs):
    filtered_songs = []
    for song in songs['items']:

        video_id = song['id']['videoId']

        request = yt_api.videos().list(
            part="status",
            id=video_id,
            fields="items(status(embeddable))"
        )

        try:
            response = request.execute()
        except HTTPError as e:
            print('Error response status code : {0}, reason : {1}'.format(
                e.status_code, e.error_details))

        if response['items'][0]['status']['embeddable']:
            filtered_songs.append(song)

    return filtered_songs


class SongLyricsConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'karaoke-room'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if 'song_name' in text_data_json:
            song_name = text_data_json['song_name']

            request = yt_api.search().list(
                part="snippet",
                maxResults=5,
                q=song_name,
                type="video",
                videoSyndicated="true",
                fields="items(id(videoId),snippet(title,thumbnails(medium),channelTitle))"
            )

            try:
                response = request.execute()
            except HTTPError as e:
                print('Error response status code : {0}, reason : {1}'.format(
                    e.status_code, e.error_details))

            embeddable_songs = filter_embeddable(response)

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'song_list',
                    'songs': embeddable_songs
                }
            )
        elif 'button' in text_data_json:
            button = text_data_json['button']

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'player_control',
                    'button': button
                }
            )
        elif 'song_data' in text_data_json:
            song_data = text_data_json['song_data']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'save_queue_song',
                    'song_data': song_data
                }
            )

    def song_list(self, event):
        songs = event['songs']

        self.send(text_data=json.dumps({
            'type': 'song_list',
            'songs': songs
        }))

    def player_control(self, event):
        button = event['button']

        self.send(text_data=json.dumps({
            'type': 'button',
            'button': button
        }))

    def save_queue_song(self, event):
        song_data = event['song_data']

        song = Song(videoId=song_data['videoData']['videoId'], title=song_data['videoData']
                    ['videoName'], ytChannel=song_data['videoData']['ytChannel'], imgSrc=song_data['videoImgUrl'])

        try:
            song.save()
        except IntegrityError:
            print('duplicate song')
        else:
            print('song saved')

        self.send(text_data=json.dumps({
            'type': 'queue_song',
            'song_data': song_data
        }))
