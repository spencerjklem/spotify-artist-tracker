# Spotify Artist Tracker
Creates playlist of all released music from given artists in past week


## How To Run
Go to [spotify for developers](https://developer.spotify.com/dashboard) to create an app. This will provide you with a Client ID and Cient Secret. You will then replace these where it is specified in the program, as well as replace where it asks for a port with an open port (such as 1234 or 8888). 

Create a new empty playlist on your spotify, and get its playlist id. Copy the link to the playlist and it is in that link (see below)

```https://open.spotify.com/playlist/PLAYLIST_ID?si=OTHER_STUFF```

Then, just add the artist names you want to artistnames.txt (one per line), and you will be good to go.

use ```make help``` to learn how to build a command, otherwise you can use ```make run ARGS='<ENTER INPUT FILENAME> <ENTER OUTPUT FILENAME> <ENTER NUMBER OF DAYS SINCE RELEASE> VERBOSE'```


## Why Did I Make This?
This was the final project submission for my Intro to Programming class. I also really enjoy music and having done some minor work with API requests on a previous project, I wanted to expand my knowledge.
