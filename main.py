import requests

# documentation needed to connect to the Spotify API
CLIENT_ID='a1211eeec3424ffca8fc6f8dbee1b6ca'
CLIENT_SECRET='a668e7d0f7fd42d9940f6d33b12c820d'

AUTH_URL='https://accounts.spotify.com/api/token'

auth_response=requests.post(AUTH_URL, {
    'grant_type' : 'client_credentials',
    'client_id'  : CLIENT_ID,
    'client_secret' : CLIENT_SECRET,

})

auth_response_data=auth_response.json()

access_token = auth_response_data['access_token']

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

BASE_URL='https://api.spotify.com/v1/'

# entire program is in a loop until the user expresses that they would not like to continue
while True:
    # user chooses category they would like to search from
    choice=int(input("\nWhat would you like to search up?\n\t1 - Track\n\t2 - Album\n\t3 - Artist\n\t4 - All\n"))
    while(True):
        if(not(choice==1 or choice==2 or choice==3 or choice==4)):
            choice=int(input("Please type a number between 1 and 4: "))
        else:
            break
    
    # once the category is decided, the user is prompted to enter the search value of their choice
    search=str(input("\nWhat would you like to search up?\n"))

    def inputDecider(choice):
        switcher={
            1: 'track',
            2: 'album',
            3: 'artist'
        }
        return switcher.get(choice)

    # based on the user's choice, a query is executed using the API and the result is stored as a JSON object
    if(1<=choice<=3):
        query='q=%s&type=%s&limit=10' %(search, inputDecider(choice))
        r=requests.get(BASE_URL + 'search?' + query, headers=headers)
        r=r.json()
    elif(choice==4):
        query1='q=%s&type=track&limit=10' %search
        r1=requests.get(BASE_URL + 'search?' + query1, headers=headers)
        r1=r1.json()
        query2='q=%s&type=album&limit=10' %search
        r2=requests.get(BASE_URL + 'search?' + query2, headers=headers)
        r2=r2.json()
        query3='q=%s&type=artist&limit=10' %search
        r3=requests.get(BASE_URL + 'search?' + query3, headers=headers)
        r3=r3.json()

    # the result of the query is then printed in a format depending on if a song, album, or artist was searched
    if choice==1:
        print("\n")
        for x in range(len(r.get('tracks').get('items'))):
            artist = r.get('tracks').get('items')[x].get('album').get('artists')[0].get('name')
            title = r.get('tracks').get('items')[x].get('name')
            album = r.get('tracks').get('items')[x].get('album').get('name')
            print('%s by %s from the album %s' %(title, artist, album))
    if choice==2:
        print("\n")
        for x in range(len(r.get('albums').get('items'))):
            artist = r.get('albums').get('items')[x].get('artists')[0].get('name')
            album = r.get('albums').get('items')[x].get('name')
            print('%s by %s' %(album, artist))
    if choice==3:
        print("\n")
        for x in range(len(r.get('artists').get('items'))):
            artist = r.get('artists').get('items')[x].get('name')
            print('%s' %(artist))
    if choice==4:
        print("\nTracks\n----------------------------------------------------------------------------\n")
        for x in range(len(r1.get('tracks').get('items'))):
            artist = r1.get('tracks').get('items')[x].get('album').get('artists')[0].get('name')
            title = r1.get('tracks').get('items')[x].get('name')
            album = r1.get('tracks').get('items')[x].get('album').get('name')
            print('%s by %s from the album %s' %(title, artist, album))
        print("\nAlbums\n----------------------------------------------------------------------------\n")
        for x in range(len(r2.get('albums').get('items'))):
            artist = r2.get('albums').get('items')[x].get('artists')[0].get('name')
            album = r2.get('albums').get('items')[x].get('name')
            print('%s by %s' %(album, artist))
        print("\nArtists\n----------------------------------------------------------------------------\n")
        for x in range(len(r3.get('artists').get('items'))):
            artist = r3.get('artists').get('items')[x].get('name')
            print('%s' %(artist))

    # this choice by the user will either exit the program, or continue the loop
    restart = input("\n\nWould you like to search again? y/n?\n")
    if restart == "n" :
        break