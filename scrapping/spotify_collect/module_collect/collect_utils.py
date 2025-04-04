import pandas as pd
import requests
from . import spotify_dataclass as sd


def collect_info(artist, headers):
    artist = artist.replace(" ", "")

    url = f"https://api.spotify.com/v1/search?q={artist}&type=artist&market=FR&limit=1"
    response = requests.get(url, headers=headers)
    artist_id = (
        response.json().get("artists", None).get("items", None)[0].get("id", None)
    )

    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    response = requests.get(url, headers=headers)
    artist_data = response.json()

    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=FR"
    response = requests.get(url, headers=headers)
    artist_toptrack = response.json()

    return artist_id, artist_data, artist_toptrack


def artist_stats(artists_list, headers):
    artist_stats_concat = pd.DataFrame(columns=sd.ArtistStats.__match_args__)
    top_tracks_concat = pd.DataFrame(columns=sd.TopTracks.__match_args__)

    for artist in artists_list:
        _, artist_data, artist_toptrack = collect_info(artist, headers)
        try:
            artist_stats_line = sd.ArtistStats(
                id=artist_data.get("id"),
                name=artist_data.get("name"),
                genres=artist_data.get("genres", None),
                popularity=artist_data.get("popularity", None),
                followers=artist_data.get("followers", None).get("total", None),
                image=artist_data.get("images")[0].get("url", None),
            )

            artist_stats = pd.DataFrame([artist_stats_line])
            artist_stats_concat = pd.concat([artist_stats_concat, artist_stats], axis=0)
        except Exception as e:
            print(f"for {artist_data.get('name')} : {e}")

        for track in artist_toptrack["tracks"]:
            try:
                top_tracks_line = sd.TopTracks(
                    main_artist=track.get("artists")[0].get("name"),
                    id_artist=track.get("artists")[0].get("id"),
                    feat_artists=[i["name"] for i in track.get("artists")],
                    track_name=track.get("name"),
                    album_name=track.get("album").get("name"),
                    album_releasedate=track.get("album").get("release_date"),
                    album_totaltracks=track.get("album").get("total_tracks"),
                    track_duration=track.get("duration_ms"),
                    track_popularity=track.get("popularity"),
                    track_number=track.get("track_number"),
                )
                top_tracks = pd.DataFrame([top_tracks_line])
                top_tracks_concat = pd.concat([top_tracks_concat, top_tracks], axis=0)
            except Exception as e:
                print(f"for {artist_data.get('name')} : {e}")

    return (
        artist_stats_concat.reset_index()[artist_stats_concat.columns],
        top_tracks_concat.reset_index()[top_tracks_concat.columns],
    )
