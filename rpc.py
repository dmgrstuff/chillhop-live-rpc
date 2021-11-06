from chillhop import live
from pypresence import Presence, InvalidPipe
from datetime import datetime
import time

index = int(input("""Which stream?
[1] Chillhop Radio
[2] lofi hip hop radio
> """))

ch = live(stream_index=index-1) # since Python list indices start at 0
rpc = Presence(ch.streams[ch.stream_index]['appid'])

def time_fmt(num): # the "naive" way
    mins = int(num // 60)
    secs = int(num % 60)
    if secs < 10:
        secs = "0" + str(secs) # leading 0 (there's probably a better way)
    return f"{str(mins)}:{str(secs)}"

try: rpc.connect()
except InvalidPipe as e: # gracefully handle Discord not being open
    print("[warning] Exception \"InvalidPipe\" raised; disabling rich presence functions. (Do you have Discord open?)")
    rpc_enabled = False
else: rpc_enabled = True

while True:
    # welcome to one liner hell, enjoy your stay
    track = ch.get_track_info() # fetch current track info (returns dict)
    time_str = str(int(time.time()))
    last_play = datetime.strptime(track['last_play'], '%Y-%m-%d %H:%M:%S').timestamp()
    duration = int(track['duration']) / 1000
    duration_str = time_fmt(duration)
    next_track_time = last_play + duration # converting from ms

    if rpc_enabled == True:
        viewers = ch.get_current_views() # gets the current viewer count
        track_url = f'https://chillhop.com/?p={track["post_id"]}'
        rpc.update( 
          details=f"{track['title']} ({duration_str})",
          state=track["artists"],
          large_image="radio_1",
          large_text=f"{viewers} viewers",
          buttons=[
            {"label": "View release", "url": track_url},
            {"label": "View artist", "url": f'{track_url}&type=artists'} # well that's convenient!
            ],
          start=time_str
        )
    else: 
        pass

    timestamp_now = datetime.now().strftime('%H:%M:%S') # get the system timestamp
    sleep_duration = (next_track_time - datetime.utcnow().timestamp()) # avoid excessively spamming Discord and Chillhop's APIs :)
    
    try: # text formatting
        first_run
    except NameError:
        first_run = True
        duration_str = f"~{time_fmt(sleep_duration)} left" # probably imprecise

    if sleep_duration >= 0: print(f"[{timestamp_now}] Now playing on {ch.streams[ch.stream_index]['name']} - {track['title']} by {track['artists']} ({duration_str})")
    while True:
        try: 
            time.sleep(sleep_duration)
            break
        except ValueError:
            time.sleep(1) # try again until it works lol
            break