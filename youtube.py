from googleapiclient.discovery import build

api_key = '' #Enter your own api key
CLIENT_ID = "" #Enter your own id
CLIENT_SECRET = "" #Enter your own secret
scopes = ['https://www.googleapis.com/auth/youtube']

import google.oauth2.credentials
import google_auth_oauthlib.flow
client_secrets_file = "CLIENT_SECRET.json"

flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
credentials =  flow.run_console()
api_service_name = 'youtube'
api_version = 'v3'
youtube = build(api_service_name, api_version, credentials=credentials)     #handling user data
ytobj = build(api_service_name,api_version,developerKey=api_key)            #used just to search for song 

def readFile():
    song_list = []
    with open('listSong.txt', 'r') as filehandle:
        filecontents = filehandle.readlines()
        for line in filecontents:
            current_place = line[:-1]                                       # remove linebreak which is the last character of the string
            song_list.append(current_place)                                 # add item to the list
    return song_list
    
def createPlayList():
    request = youtube.playlists().insert(
            part="snippet,status",
            body={
              "snippet": {
                "title": playlist_name,
                "description": "We got this here from spotify",
                "tags": [
                  "sample playlist",
                  "API call"
                ],
                "defaultLanguage": "en"
              },
              "status": {
                "privacyStatus": "public"
              }
            }
        )
    response = request.execute()
    return response

def insertYT(video_id):
    youtube.playlistItems().insert(part='snippet',body={
            'snippet': {
                'playlistId': playlistId_Target,
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': video_id
                }
            }
    }).execute()
   

def searchYt(name_song):
    search_response = ytobj.search().list(q=name_song,part="id,snippet",maxResults=25).execute()
    flag=True 
    i=0
    while flag:   
        if(search_response['items'][i]['id']['kind']=='youtube#video'):
            flag= False
        elif i==100:
            flag=False
            print("Not found")
        else:
            i+=1
    video_id=search_response['items'][i]['id']['videoId']
    return video_id


song_list=readFile()
song_list
playlist_name= song_list[0]+" from spotify" #We had stored the name of paylist at the first index  
response= createPlayList()
playlistId_Target = response['id']
for i in range(1,len(song_list)):
    video_id=searchYt(song_list[i])
    insertYT(video_id)
    
print("Playlist added to YouTube")