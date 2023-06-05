# Spotify_Classification_Capstone_Project

Spotify released an API that reports the audio features of its songs, such as “tempo” or “energy”. Here, we will use these features of 50k randomly picked songs to predict the genre that the song belongs to.

## Data

The data is contained in the file musicData.csv. In this file, the first row represents the column headers. Each row after that represents data from one song.

The columns represent, in order (from left to right):
Column 1: unique Spotify ID of each song
Column 2: artist name
Column 3: song name
Column 4: popularity of the music (what percentage of users know about it, from 0 to 99%)
Column 5: acousticness (an audio feature) on a scale from 0 to 1
Column 6: danceability (an audio feature) on a scale from 0 to 1
Column 7: the duration of the music (in milliseconds)
Column 8: energy (an auditory feature) on a scale from 0 to 1
Column 9: instrumentality (an audio feature) on a scale from 0 to 1
Column 10: key of the song (in musical notation)
Column 11: liveness (an audio feature) on a scale from 0 to 1
Column 12: loudness (in dB relative to some threshold)
Column 13: mode of the song (musical)
Column 14: speechiness (an audio feature), on a scale from 0 to 1
Column 15: tempo (in beats)
Column 16: obtained date (when was this information obtained from Spotify)
Column 17: valence (an audio feature), on a scale from 0 to 1
Column 18: Genre of the song (there are 10 different genres, e.g. “Rock” or “Country”)
