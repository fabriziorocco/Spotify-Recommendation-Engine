import pandas as pd

df = pd.read_csv("tracks.csv")
tracks = []
for rows in df.itertuples(index = False, name = None):
    for i in rows:
        tracks.append(i)

import requests

client_id = "e17ae75c630f4888a8d57e82e1066888"
client_secret = "6aa3fffa06b64b16a59fc49d6c925335"

# URL for token resource
auth_url = 'https://accounts.spotify.com/api/token'

# request body
params = {'grant_type': 'client_credentials',
          'client_id': client_id,
          'client_secret': client_secret}

# POST the request
auth_response = requests.post(auth_url, params).json()
access_token = auth_response["access_token"]
headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
base_url = 'https://api.spotify.com/v1/'

###############track basic info ###########################
track_endpoint = base_url + "tracks"
tracks_in_batches= []
chunk_size = 50
for i in range(0,len(tracks),chunk_size):
    tracks_in_batches.append(tracks[i:i+chunk_size])

#lists
name = [] #float
popularity = [] #float
artist = []
release_date = []

for o in range(0,len(tracks_in_batches)):
    params_basic = {"ids":",".join(tracks_in_batches[o])}
    tracks_list = requests.get(track_endpoint, headers=headers, params = params_basic).json()

    for i in range(0,len(tracks_in_batches[o])):
        try:
            name.append(str(tracks_list["tracks"][i]["name"]))
        except:
            name.append(None)
        try:
            popularity.append(float(tracks_list["tracks"][i]["popularity"]))
        except:
            popularity.append(None)
        try:
            artist.append(str(tracks_list["tracks"][i]["artists"][0]["name"]))
        except:
            artist.append(None)
        try:
            release_date.append(tracks_list["tracks"][i]["album"]["release_date"])
        except:
            release_date.append(None)
print(len(name))


#################tracks features#######################

tracks_endpoint = base_url + "audio-features"
tracks_in_batches= []
chunk_size = 100
for i in range(0,len(tracks),chunk_size):
    tracks_in_batches.append(tracks[i:i+chunk_size])

#lists
danceability = [] #float
energy = [] #float
loudness = [] #float
mode = [] # int
speechiness = [] #float
acousticness = [] #float
instrumentalness = [] #float&lists
liveness = [] #float
valence = [] #float
tempo = [] #float
duration = [] #float

for o in range(0,len(tracks_in_batches)):
    params_3 = {"ids":",".join(tracks_in_batches[o])}
    tracks_list = requests.get(tracks_endpoint, params = params_3, headers = headers).json()

    for i in range(0,len(tracks_in_batches[o])):
        try:
            danceability.append(float(tracks_list["audio_features"][i]["danceability"]))
        except:
            danceability.append(None)
        try:
            energy.append(float(tracks_list["audio_features"][i]["energy"]))
        except:
            energy.append(None)
        try:
            loudness.append(float(tracks_list["audio_features"][i]["loudness"]))
        except:
            loudness.append(None)
        try:
            mode.append(int(tracks_list["audio_features"][i]["mode"]))
        except:
            mode.append(None)
        try:
            speechiness.append(float(tracks_list["audio_features"][i]["speechiness"]))
        except:
            speechiness.append(None)
        try:
            acousticness.append(float(tracks_list["audio_features"][i]["acousticness"]))
        except:
            acousticness.append(None)
        try:
            instrumentalness.append(tracks_list["audio_features"][i]["instrumentalness"])
        except:
            instrumentalness.append(None)
        try:
            liveness.append(float(tracks_list["audio_features"][i]["liveness"]))
        except:
            liveness.append(None)
        try:
            valence.append(float(tracks_list["audio_features"][i]["valence"]))
        except:
            valence.append(None)
        try:
            tempo.append(float(tracks_list["audio_features"][i]["tempo"]))
        except:
            tempo.append(None)
        try:
            duration.append(float(tracks_list["audio_features"][i]["duration_ms"]))
        except:
            duration.append(None)

print(len(tempo))

#################tracks timbre#######################
# average_timbre = []
# for i in range(0,2):
#     analysis_endpoint = base_url + "audio-analysis/" + tracks[i]
#     analysis_response = requests.get(analysis_endpoint, headers=headers).json()
#     try:
#         a = analysis_response["segments"][0]["timbre"]
#         average_timbre.append(sum(a)/len(a))
#     except:
#         average_timbre.append(None)

################tracks AVERAGE PITCH#######################
# average_pitch = []
# for i in range(0,len(tracks)):
#     analysis_endpoint = base_url + "audio-analysis/" + tracks[i]
#     analysis_response = requests.get(analysis_endpoint, headers=headers).json()
#     try:
#         a = analysis_response["segments"][0]["pitches"]
#         average_pitch.append(sum(a)/len(a))
#     except:
#         average_pitch.append(None)
###########################################################

import pandas as pd

df = pd.DataFrame(data = {"Track_id": tracks, 'Title': name, 'artist': artist, "release_date": release_date, 'duration': duration, 'track_popularity': popularity,
                          "danceability":danceability, "energy":energy, "loudness":loudness, "mode":mode,
                         "speechiness":speechiness, "acousticness":acousticness, "instrumentalness":instrumentalness,
                         "liveness":liveness,  "valence":valence, "tempo":tempo})

df.drop_duplicates(inplace=True)
df.sample(frac = 1)
print(df)
df.to_csv("spotify_raw.csv", index=False)