#Spencer Klem 
#Final project
#3 Areas of focus: Spotipy api, file input/output, dictionaries
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import date, timedelta


#Token authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="<ENTER CLIENT ID>",
    client_secret="<ENTER CLIENT SECRET>",
    redirect_uri="http://localhost:<ENTER PORT NUMBER>",
    scope="playlist-modify-public"))

#playlist ID
newreleases_id = '<ENTER PERSONAL PLAYLIST ID>'

#global id list to remove dupes
id_list = []

def get_artist_id(artist_name):
    """
    sig: str -> str
    returns artists uri, given the name 
    and assuming they are the top artist result for that name
    """
    result = sp.search(artist_name, limit=1, offset=0, type='artist', market=None)
    return result['artists']['items'][0]['uri']


def get_artists_songs (artist_id, days_since):
    """
    sig: str -> 2d arr of str
    gets all singles and tracks from albums released in the past 
    'days_since' days, then returns list of these tracks, in form
    ['SONGNAME', 'DATERELEASED', 'SONGID']
    """
    global id_list
    songs = []
    #Extracting tracks from artists albums
    album_songs = sp.artist_albums(artist_id, album_type='album')
    albums = album_songs['items']
    for item in albums:
        album = sp.album_tracks(item['id'])['items']
        #Checks to see if the album was released within given time frame
        if (date.today() - date.fromisoformat(item['release_date']) > timedelta(days_since)):
            break
        for song in album:
            if song['id'] not in id_list:
                id_list.append(song['id'])
                songs.append([song['name'], item['release_date'], song['id']])

    #Extracting songs from singles / EPs
    single_songs = sp.artist_albums(artist_id, album_type='single')
    singles = single_songs['items']
    for item in singles:
        if (date.today() - date.fromisoformat(item['release_date']) > timedelta(days_since)):
            break
        ep = sp.album_tracks(item['id'])['items']
        for song in ep:
            if song['id'] not in id_list:
                id_list.append(song['id'])
                songs.append([song['name'], item['release_date'], song['id']])
    return songs

def make_playlist_of_tracks(playlist_id, song_ids, days_since):
    """
    sig: str, list of strs -> none
    Updates given playlist to include all tracks found, and updates
    name of playlist to today's date
    """
    #gets all current songs in the playlist
    songs_info = sp.playlist_items(playlist_id)
    songs = songs_info['items']

    #deletes all current items in the playlist
    song_ids_to_remove = []
    for song in songs:
        song_ids_to_remove.append(song['track']['id'])
    
    if song_ids_to_remove != []:
        sp.playlist_remove_all_occurrences_of_items(playlist_id, song_ids_to_remove)
    
    #updates name + description of playlist
    sp.playlist_change_details(playlist_id, 
                               name= 'new releases' + ' ('+ date.today().strftime('%m/%d/%Y')+')',
                               description= 'Contains all new releases from ' + (date.today() + timedelta(-1 * days_since)).strftime('%m/%d/%Y') +
                               ' to ' + date.today().strftime('%m/%d/%Y'))
    
    #adds all new items to playlist
    if song_ids != []:
        while len(song_ids) > 99:
            req_ids = song_ids[:99]
            song_ids = song_ids[99:]
            sp.playlist_add_items(playlist_id, req_ids)            
        sp.playlist_add_items(playlist_id, song_ids)

#runs for experienced users
def runner():
    
    input_filename = 'artistnames.txt'
    output_filename = 'output.txt'
    days_since = 7
    #OUTPUT TYPES: VERBOSE, ARTIST_TREE
    output_type = 'ARTIST_TREE'

    #CLI (optional)
    if len(sys.argv) > 2:
        input_filename = sys.argv[2]
        if len(sys.argv) > 3:
            output_filename = sys.argv[3]
            if len(sys.argv) > 4:
                days_since = int(sys.argv[4])
                if len(sys.argv) > 5:
                    output_type = sys.argv[5]

    #reading and writing to files
    f1 = open(input_filename, 'r')
    f2 = open(output_filename, 'w')
    
    #for automatically updating playlist and output file
    song_ids = []
    first = True

    #file output
    for artist in f1:
        songs = get_artists_songs(get_artist_id(artist), days_since)
        
        if output_type == 'ARTIST_TREE':
            if songs != []:
                if first:
                    f2.write(artist)
                    first = False
                else:
                    f2.write('\n' + artist)

        for song_info in songs:
            if artist[-1] == '\n':
                artist = artist[:-1]
            
            if output_type == 'VERBOSE':
                songstr = artist + ' -- ' + song_info[0] + ' -- ' + song_info[1]
                f2.write(songstr + '\n')
            
            elif output_type == 'ARTIST_TREE':
                songstr = ' - ' + song_info[0]
                f2.write(songstr + '\n')

            #adds ids to list for making playlist
            song_ids.append(song_info[2])

    make_playlist_of_tracks(newreleases_id, song_ids, days_since)
    f1.close()
    f2.close()

#runs for beginners
def howto():
    #builds command for beginners
    cmdargs = ''
    c1 = input('would you like to enter an input filename (y/n): ')
    if c1 == 'y':
        cmdargs += input('please enter an input filename: ')
        c2 = input('would you like to enter an output filename (y/n): ')
        if c2 == 'y':
            cmdargs += ' ' + input('please enter an output filename: ')
            c3 = input('would you like to enter how many days of songs you want (y/n): ')
            if c3 == 'y':
                cmdargs += ' ' + input('please enter the number of days of songs: ')
                c4 = input('would you like to enter an output type (y/n): ')
                if c4 == 'y':
                    cmdargs += ' ' + input('please enter VERBOSE or ARTIST_TREE: ')
    print("please type the following command into the terminal:")
    print("make run ARGS='" + cmdargs + "'")

if len(sys.argv) > 1 and sys.argv[1] == 'help':
    howto()
else:
    runner()
