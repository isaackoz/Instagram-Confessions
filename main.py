#!/usr/bin/env python3.5
# -#- coding: utf-8 -*-

import socket
import threading
from PIL import Image, ImageDraw, ImageFont
from textwrap3 import fill
import sqlite3
from InstagramAPI import InstagramAPI
import os

#---------config------------
dbName = "bruh.db"
myPort = 47225
IGUSER = "USERNAME-GOES-HERE"
IGPASS = "PASSWORD-GOES-HERE"
IGCAP = "Caption under image pos ted on Instagram"
fext = ".jpg"
#----------------------------

rootPath = os.path.dirname(__file__)

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        print("Server opened")

    def listen(self):
        self.sock.listen(10)
        while True:
            client, address = self.sock.accept()
            client.settimeout(5)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the recieved data
                    response = str(data.decode("utf-8"))
                    print("Confession received!")
                    self.storePeeInBalls(response)
                else:
                    client.close()
            except:
                client.close()
                return False
#okay maybe not the greatest function name...
    def storePeeInBalls(self, confession):
        print("++++ Attempting to store confession in db")
        confession = str(confession[:650] + (confession[650:] and '..'))
        #I split the username and confession into two using some random Thai character.
		#The web form adds it in automatically. Probably not the best way to do this, but it only requires one packet to be sent instead of two
	    splot = confession.split('ยง', 1) 
        print(splot[0])
        print(splot[1])
		#If the captcha fails all, then a blacklist can be used as a backup. Just put ip(s) in and separate by commas
        with open(str(rootPath) + "blacklist.txt", 'r') as black:
            for line in black:
                if splot[0] in line:
                    print("Blacklisted ip tried posting: " + splot[0])
                    break
                else:
					#in the db, store the ip, confession, and username in. nothings anonymous anymore lol
                    db = sqlite3.connect(dbName)
                    self.curs = db.cursor()
                    with db:
                        self.curs.execute('''INSERT INTO myTable (confession, ip) VALUES (?,?)''', (splot[1], splot[0],))
                        idnum = self.curs.lastrowid
                        print(idnum)
                    db.close()

                    print("++++ Successfully inserted confession into db: '" + splot[1] + "'")
                    createImg(splot[1], idnum)

#checks for db and if not exsist, create one
def tableCheck(dbName):
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    try:
        # create a table
        print("Checking if table exists and creating if not")
        cursor.execute("""CREATE TABLE IF NOT EXISTS myTable
                      (confession TEXT, ip TEXT)
                   """)
        conn.commit()
        conn.close()
    except:
        conn.commit()
        conn.close()

#creates image to be posted to instagram
def createImg(text, idnum):
    print("creating image")
    img = Image.open(str(rootPath) + "bg.jpg")
	#any square background with dimensions 1080x1080. if using other dim you have to adjust the wrap around below
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(str(rootPath) + "font.ttf", 30)
	#mess around with the numbers above and below to find perfect wrap around for text so it doesnt get cut off
    draw.text((40, 40), str(fill(text, 30)), (0, 0, 0), font)
    img.save(str(rootPath) + "images/" + str(idnum) + ".jpg")
    print("Image saved as " + str(idnum) + ".jpg")


#uploads photo created above and then deletes it off local storage.
def postIG():
    threading.Timer(65, postIG).start()
    filelist = [os.path.splitext(e.name)[0] for e in os.scandir(rootPath + "images/") if e.is_file()]
    print("Checking for pics to post...")
    if filelist:
        picToPost = str(min(filelist, key=float)) + ".jpg"
        print("Pic queue:\n   " + str(filelist) + "\nPosting picture:\n   " + picToPost)
        try:
            igapi.uploadPhoto(rootPath + "images/"+ picToPost, caption=IGCAP, upload_id=None)
            print("Succesfuly posted to Instagram!")
            os.remove(rootPath + "images/" + picToPost)
            print("Removed: " + picToPost)
        except Exception as e:
            print("Error posting to Instagram:\n    " + str(e))
			#if for some reason it can't login to instagram it tries again... make sure password and username are correct also
            igapi.login()

    else:
        print("No pictures to post!")



#---------------startup setup-------------
tableCheck(dbName)
igapi = InstagramAPI(IGUSER, IGPASS)
igapi.login()
postIG()
#------------------------------------------

if __name__ == "__main__":
    ThreadedServer('', myPort).listen()
