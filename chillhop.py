from datetime import datetime
import requests
import json
import time

class live:
    def __init__(self, stream_index=0, log_bad_response=False): # default value if no index is passed
        self.streams = [{'name': 'Chillhop Radio 🐾', 'id': '5yx6BWlEVcY', 'appid': '889847839662956615'}, {'name': 'lofi hip hop radio 🐾', 'id': '7NOSDKb0HlU', 'appid': '890420933280550922'}]
        self.stream_index = stream_index
        self.log_bad_response = log_bad_response # will remove this eventually

    def parse_response(self, response): # you can easily add variables to grab from the json here
        result = []
        
        for i in response: # iterates over a list of multiple tracks, useful for get_track_history()
            title = i["title"]    
            artists = []
            for artist in i["artists"]:
                artists.append(artist["name"])
            artists = ', '.join(artists)
            track_id = i["id"]
            post_id = i["post_id"]
            spotify_url = f"https://spotify.com/track/{i['spot_id']}"
            last_play = i["last_play"]
            duration = i["duration"]
            img = i["img"]
            result.append({'title': title, 'artists': artists, 'track_id': track_id, 'post_id': post_id, 'spotify_url': spotify_url, 'last_play': last_play, 'duration': duration, 'img': img})

        return result

    def get_track_info(self):
        data = {'action': 'player_get_livestream_tracks', 'youtubeid': self.streams[self.stream_index]['id'], 'type': 'history', 'lastPull': (str(int(time.time()))), 'offset': '0'}

        while True:
            response = json.loads(requests.post('https://chillhop.com/wp-admin/admin-ajax.php', data=data).content)
            try:  
                result = self.parse_response(response["livetracks"])[0] # returned list should only contain one dict
                break
            except IndexError: # Chillhop's API sometimes returns nothing for a few seconds between songs - this handles that
                if self.log_bad_response == True:
                    print("Encountered IndexError - waiting a bit...")
                    print('Response received:')
                    print(response)
                time.sleep(4) # spam it until it works lol

        return result

    def get_track_history(self, offset):
        # -- WIP --
        # Chillhop's API returns information on the 20 last-played tracks at a time
        # Offset 0 will actually only return the currently playing track, but get_track_info() is provided as a more convenient function for this

        if offset < 0:
            raise ValueError("Offset passed to API cannot be negative") # invalid offsets don't return anything useful
        data = {'action': 'player_get_livestream_tracks', 'youtubeid': self.streams[self.stream_index]['id'], 'type': 'history', 'lastPull': (str(int(time.time()))), 'offset': str(offset)}
        while True:
            response = json.loads(requests.post('https://chillhop.com/wp-admin/admin-ajax.php', data=data).content)
            try:  
                result = self.parse_response(response["livetracks"])
                break
            except IndexError:
                if self.log_bad_response == True:
                    print("Encountered IndexError - waiting a bit...")
                    print(f"Response received:")
                    print(response)
                time.sleep(4) # spam it until it works lol
        return result

    def get_current_views(self): # BUG: this request 404s even on Chillhop's website, maybe a change in the API?
        response = requests.get(f'https://chillhop.com/fetch3/?action=get_current_views&youtube_id={self.streams[self.stream_index]["id"]}')
        result = json.loads(response.content)["viewers"]
        return result