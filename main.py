
############################################################################################################
# CLIENT SECRETS AND CLIENT ID ARE NOT TO BE SHARED. KEEP THEM SAFE AND DO NOT SHARE THEM WITH ANYONE.    #
############################################################################################################
# client id = 'a52cca8810dc4b7881fc75daada45fd3'
# client secret (dont share dumbass) = '10649a4e964a48a492510404fe35fd32'

#function of the programs

#1: find the top artists, genres, tracks, and albums from a user and make a playlist based on them. the variety of track can be adjusted by changing the top uses (e.g instead of the users top
# 10 genres tracks albums etc. use only 5 download to the computer aswell

#2 download all playlists from a users account

#download any playlist, album, track onto your pc

#import needed libraries
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import random
import spotipy.util as util
import pprint
from time import sleep
from pytube import YouTube 
import os
from pytube import Search
import time
username = "skkrt"
scope = "user-top-read, user-modify-playback-state, playlist-modify-public, playlist-modify-private"
redirect_uri = "http://127.0.0.1:9090"
#authenticate with spotify
token = util.prompt_for_user_token(username, scope, "a52cca8810dc4b7881fc75daada45fd3", "10649a4e964a48a492510404fe35fd32", redirect_uri)
sp = spotipy.Spotify(auth=token)


############################################################
# RECOMMEND SONGS, ADD TO QUEUE, CREATE PLAYLIST, DOWNLOAD #
############################################################
#create a playlist based off of top artists, genres, and genrex
#first, define default variables

timeRange = "medium_term" #can be short_term, medium_term, or long_term
songs = 10 #number of songs in the playlist (max 100)
variability = 10 #variability of the playlist (amount of tracks, artists, and genres to sample)

#ask user for input
timeRange = input("Enter the time range (short_term, medium_term, long_term): ")
#add check so that the input is valid
while timeRange not in ["short_term", "medium_term", "long_term"]:
    timeRange = input("Invalid input. Enter the time range (short_term, medium_term, long_term): ")
songs = int(input("Enter the number of songs in the playlist (max 100): "))
#add check so that the input is valid
while songs > 100 or songs < 1:
    songs = int(input("Invalid input. Enter the number of songs in the playlist (min 1, max 100): "))
variability = int(input("Enter the variability of the playlist (amount of tracks, artists, and genres to sample): "))
#add check so that the input is valid
while variability < 1:
    variability = int(input("Invalid input. Enter the variability of the playlist (min 1): "))

#find the top 5 short term artists and make a list of their names
topArtists = sp.current_user_top_artists(time_range=timeRange, limit=5)
artistIDs = []
for i, item in enumerate(topArtists['items']):
    #add the id of each artist to a list called "artistIDs"
    artistIDs.append(item['id'])

#find the top 5 short term tracks and make a list of their ids
topTracks = sp.current_user_top_tracks(time_range=timeRange, limit=5)
trackIDs = []
for i, item in enumerate(topTracks['items']):
    #add the id of each track to a list called "trackIDs"
    trackIDs.append(item['id'])

#take the list of the top 5 artists and take their genres and add to a list
genres = []
for artist in artistIDs:
    #get the artists from the list of artistIDs
    artist = sp.artist(artist)
    #add the genres of the artist to the list "genres"
    genres += artist['genres']

#before creating the playlist, pick 1 genre, 2 artists and 2 tracks form the lists randomly to determine the seeding of the playlist
seedGenres = random.sample(genres, 1)
seedArtists = random.sample(artistIDs, 2)
seedTracks = random.sample(trackIDs, 2)

#create a recommendation based off of the seeds (genres, tracks, artists)
recom = sp.recommendations(seed_artists=seedArtists, seed_tracks=seedTracks, seed_genres=seedGenres, limit=songs)

for track in recom['tracks']:
    print(track['name'], '-', track['artists'][0]['name'])

#ask user if they want to add those songs to their listening queue
addQueue = input("Would you like to add these songs to your queue? (y/n): ")
#add check so that the input is valid
while addQueue not in ["y", "n"]:
    addQueue = input("Invalid input. Would you like to add these songs to your queue? (y/n): ")
if addQueue == "y":
    for track in recom['tracks']:
        #add each track to the users queue
        sp.add_to_queue(track['uri'])
    print("Songs added to queue.")

#ask user if they want to create a playlist with the songs
createPlaylist = input("Would you like to create a playlist with these songs? (y/n): ")
#add check so that the input is valid
while createPlaylist not in ["y", "n"]:
    createPlaylist = input("Invalid input. Would you like to create a playlist with these songs? (y/n): ")
if createPlaylist == "y":
    #create a playlist with the songs
    playlistName = input("Enter the name of the playlist: ")
    #add check so that the input is valid
    while playlistName == "":
        playlistName = input("Invalid input. Enter the name of the playlist: ")
    #create the playlist
    playlist = sp.user_playlist_create(sp.me()['id'], playlistName, public=False)
    #add the songs to the playlist
    songURIs = [track['uri'] for track in recom['tracks']]
    sp.playlist_add_items(playlist['id'], songURIs)
    print("Playlist created.")
else:
    playlistName = "none"

#ask user if they want to download the songs to their computer
downloadSongs = input("Would you like to download these songs to your computer? (y/n): ")
#add check so that the input is valid
while downloadSongs not in ["y", "n"]:
    downloadSongs = input("Invalid input. Would you like to download these songs to your computer? (y/n): ")
if downloadSongs == "y":
    #take each track and put its name into a list in the format "artist - track"
    trackNames = [track['artists'][0]['name'] + ' - ' + track['name'] for track in recom['tracks']]
    #use pytube to search each track on youtube and download the first video as mp3 into a folder called "downloads" in current directory
    for track in trackNames:
        #search for the track on youtuibe and get ONE url. dont use a list
        s = Search(track + ' audio')
        searchResults = []
        for v in s.results:
            searchResults.append(v.watch_url)
        #shorten the list to 1 result
        searchResults = searchResults[0]
        #download the video as mp3
        yt = YouTube(searchResults)
        #check if playlistName exists, if not default the folder to "(time and date) - Spotify Downloads"
        if playlistName == "none":
            playlistName = time.strftime("%Y-%m-%d %H-%M") + " - Spotify Downloads"
        yt.streams.filter(only_audio=True).first().download(filename=track + '.mp3', output_path=playlistName)
        print(track + " downloaded.")
        #reset the search results list
        searchResults = []
            
