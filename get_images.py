from Client import Client
from pprint import pprint #used for better console visualization
import os
from urllib.request import urlopen
from urllib.error import HTTPError
from clint.textui import puts, colored #addon for console display, to get it just 'pip install clint'

client = Client('011273049768982050681:xczrgn8dsdk', 'AIzaSyAxAVTUMn06VaIWIkVavtVtz0fOErt3whw')

options = {
    'page':"",
    'size':"large",
    'type':"",
    'dominantColor':"",
    'colorType':"",
    'safe':""
}

# Print the first element of the list
client.search('Steve Jobs', method='crawler')

#If you want to download the images to your computer just call this function
def downloadPhoto(folder, photo_url):
    try:
        u = urlopen(photo_url)
        if not os.path.exists(folder):
            os.makedirs(folder)

        photo = os.path.join(folder, photo_url.split('/')[-1])
        if not os.path.exists(photo):
            localFile = open(photo, "wb")
            localFile.write(u.read())
            localFile.close()
        u.close()
        return photo
    except HTTPError:
        puts(colored.red("HTTP ERROR: 404 - Not Found")) #This puts things is a addon for better console diplay


#Example:
# url = client.search('Steve Jobs', options)[0]['image']['contextLink']
# downloadPhoto("/Desktop",url) #will download this photo, to download all photos or more then one, just put in a url's loop

#If you wish to get all the links:
# search = client.search('Steve Jobs', options)
# links = []
# for index, link in enumerate(search):
#
#     links.append(link[index]['image']['contextLink']) #appending all links
#
#
# print(links)