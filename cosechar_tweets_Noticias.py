#pip install couchdb
#pip install tweepy

import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON


ckey = "qAdBXwt3wMH89XAGXNoIZVHGt"
csecret = "9Emc1qT8ni4kAfN9dAPSh6KnOReCjHCf2xd7u5ZeWILCm5Malq"
atoken = "294370588-SXCJtBycjTOBwmsEiXzITBdhJHPAyRy2fjZi1HsK"
asecret = "jzRYkdgrqwOCO25yYu4UVwWpsDSsY5lLAB98YENeQFdgT"

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
server = couchdb.Server('http://localhost:5984/')
try:
    #Si no existe la Base de datos la crea
    db = server.create('noticias')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['noticias']
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
#twitterStream.filter(locations=[-78.519583,-0.228567,-78.480944,-0.19247])
twitterStream.filter(track = ["noticias","news","noticias_internacionales","international_News","international News"])