#pip install couchdb
#pip install tweepy

import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON

#mis credenciales en el tweeter

ckey = "moZvrMiNRc7XJaV778im5GYtY"
csecret = "V3S1T7SoR22WnjZCDxelEZYH1Hh4Oi5fFsLv9Kvii3OBprrXKH"
atoken = "1125594478981652485-fPgcVgnEseRBdC2HnRcadhbMFIxu6W"
asecret = "xd5qKgqJSWxm1fIbLY8j8VBLt69NpGV88IRjnZKpLDQAp"

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
    db = server.create('positivo')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['positivo']
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
#twitterStream.filter(locations=[-78.4924868833,-0.203871544,-78.4886712812,-0.2009682306]) #se usa con csv en boudingbox
twitterStream.filter(track = ["buenos","dias","maravilloso dia","suerte","mucha suerte","buen dia","good luck","good","happy"
    ,"feliz","love","amo","me gusta","sorte","agradecido","grato","bendecido","abençoado","gracias","thanks","obrigada","excelente"
    ,"increible","like"
    ,"España","EU","Miami","Argentina","buenos aires","Brazil","Rio de Janeiro","Ecuador","Quito"])