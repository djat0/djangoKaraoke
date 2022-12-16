# djangoKaraoke
A karaoke web application that uses [youtube data api](https://developers.google.com/youtube/v3/quickstart/python) for karaoke song library. Uses django channels to implement websockets to make an open connection between pages for realtime song queuing and controls.

## Features
- Search karaoke songs and will return top 5 result which the user can select the preferred video
* Queue songs and play, pause, and skip controls on video playback using the songbook page
+ Display karaoke songs, now playing, and song queue on lyrics page

## Installation 

### Requirements
Install [python3](https://www.python.org/downloads/) and django channels 
```
python -m pip install -U channels["daphne"]
```
Install google api python client
```
pip install --upgrade google-api-python-client
```
### Clone project
clone this repository using `git clone https://github.com/djat0/djangoKaraoke.git`
### Setting up api key
Create your Youtube Data API v3 key on [API console](https://console.cloud.google.com/)

Once an api key is created configure your api key on the project using
```
python manage.py apikey your-api-key-here
```
And finally run
```
python manage.py runserver 8000
```
open the [http://localhost/8000/songbook](http://localhost/8000/songbook) to search and queue songs and [http://localhost/8000/lyrics](http://localhost/8000/lyrics) to display the karaoke videos. Happy singing