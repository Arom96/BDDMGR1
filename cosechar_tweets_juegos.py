#pip install couchdb
#pip install tweepy

import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON

#mis credenciales en el tweeter

ckey = "jfEAkGmFG7iS7ujfxUJdRgm3E"
csecret = "QTDwwlzFJIUxO9o1H9AYjtDUfAUl3I5GyZLoCJn3S61ysOShG4"
atoken = "2907321089-j8GEtkCFrZz3ewJclnQ7LzGewNHnoIhKOFqJB3b"
asecret = "cKJnhdRzW4cypVNpeQjT4Si3ZJZrEtJqKqV5lmNyP0VWL"

class listener(StreamListener):
    
    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["_id"] = str(dictTweet['id'])
           
            doc = db.save(dictTweet) #Aqui se guarda el tweet en la base de couchDB
            print ("Guardado " + "=> " + dictTweet["_id"])
        except:
            print ("Documento ya existe")
            pass
        return True
    
    def on_error(self, status):
        print (status)
        
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

#Setear la URL del servidor de couchDB
server = couchdb.Server('http://admin:admin@localhost:5984/')
try:
    #Si no existe la Base de datos la crea
    db = server.create('juegos')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['juegos']
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
#twitterStream.filter(locations=[-118.4693,33.7115,-118.1389,34.3424]) #se usa con csv en boudingbox
twitterStream.filter(track = ["videojuegos","eeuu","games", "ubisoft", "epicgames"])