# chillhop-live-rpc 🦝

This is a simple little script to show track info from Chillhop Music's livestreams on your Discord status. It uses the same API that [chillhop.com/live](https://chillhop.com/live) uses internally to display track information.

`chillhop.py` handles the API, and `rpc.py` (as the name suggests) does all the *\~cool\~* rich presence things.

## Usage

The only dependencies are **`requests`** (for the API) and **`pypresence`** (for Discord). You can install them with `pip install requests pypresence`.

Do a good ol' `git clone https://github.com/dmgrstuff/chillhop-live-rpc && cd chillhop-live-rpc`, then run `python rpc.py` and choose a stream. If you don't have Discord open, the script will run normally without rich presence functionality.