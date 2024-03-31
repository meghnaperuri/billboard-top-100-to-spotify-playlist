from bs4 import BeautifulSoup
import lxml
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

CLIENT_ID=""
CLIENT_SECRET=""


input=input("which year do you want to travel to? type the date in this format YYYY-MM-DD: ")
# print(input)

response=requests.get(url=f"https://www.billboard.com/charts/hot-100/{input}/")
response.raise_for_status()
top100=response.text
soup=BeautifulSoup(top100,"html.parser")

top100List1=soup.select(selector="li.o-chart-results-list__item > h3.c-title")
top100List=[]
for x in range(0,len(top100List1)):
    top100List.append(str(top100List1[x].getText().strip()))
print(top100List, len(top100List))

song_uris=[]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username="Meghnaperuri",
    )
)

user_id = sp.current_user()["id"]
print(user_id)
# ceaa1y80w1poddimpd7ty1eze
year=input.split("-")[0]

for song in top100List:
    pass
    result=sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri=result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in spotify. Skipped.")


# https://example.com/?code=AQANRPuTHi07wKD00uXKhG6V-269tFu21SCvOJAzDPfo2eAW04hA0OFSQub9sd779ha8yunrj30bEdkTCyPYoQB57ksjoGJ5ZtfdoOYFgqFDnCobnMzM8Re2-a536efDMwxyOnPNHtKA6-ogxpAXZ-By2WOmeNcb4oSg3bepyTcTc5KlFVxS03IF0MDyNSI


playlist = sp.user_playlist_create(user=user_id, name=f"{input} Billboard 100", public=False)
print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
