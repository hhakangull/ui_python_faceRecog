"""import sqlite3
import veritabani

class taban():
	def __init__(self):
		self.baglan()
	
	def baglan(self):
		self.baglanti=sqlite3.connect("sirket.db")
		self.cursor=self.baglanti.cursor()
	
	def kes(self):
		self.baglanti.close()
	
	def getir(self):
		#id=isim
		sorgu="select id from kisiler "
		self.cursor.execute(sorgu,)
		a=self.cursor.fetchall()
		sayac = 0
		b = list()
		exsayac=list()
		if len(a) == 0:
			print("Kişi Bulunamadı")
		else:
			for i in a:
				for j in i:
					exsayac.append(j)
					if exsayac in "47":
						print("ssada")
					
					
				sayac+=1
				#print(i)
		print(exsayac.index("16"))
		self.kes()
	
	def ekle(self,id):
		self.baglan()
		kontrol="select * from kisiler where id =(?)"
		ex=self.cursor.execute(kontrol,(id,))
		x=self.cursor.fetchall()
		print(x[0][2])
		
		self.kes()


k=veritabani.Kisi("Hakan","gül","123","durum","kurum","kimlik","vesika")

a=taban()

a.getir()"""

import cv2

"""
post = {"user_id":209, "message":"D5 E5 C5 C4 G4","language":"English","datetime":"20230215T124231Z","location":(44.590533, -104.715556)}


post2 = dict(message="SS Cotopaxi", language="English")
#print(post2)
post2["user_id"] = 209
post2["datetime"] = "193458823459823"""

"""
if 'location' in post2:
	print(post2['location'])
else:
	print("Location Bulunmuyor")
	
	
try:
	print(post2['location'])
except KeyError:
	print("The post doesn't have a location")
	
	"""
"""
for key in post.keys():
	value = post[key]
	print(key, "=",value)
	"""

#print(dictx.get('id2'))
import os

sayac=-1
"""for (root,dirs,files) in os.walk('./kisiler/',topdown=True):
	print (dirs)
	sayac+=1
	print ('--------------------------------')
print(sayac)"""

path="./kisiler"
s=-1
idlist=list()
for root,dirs,files in os.walk(path):
	s+=1
	idlist.append(dirs)

temizIdList=idlist[0]
#print(temizIdList)
dix=dict()
u=len(temizIdList)
#print(dix.items())
for i in range(0,u):
	dix[temizIdList[i]]="value{}".format(i)

print(dix)

#----------------
x=list()
y=list()
for i in range(17):
	x.append(cv2.imread("images/adam{}.jpg".format(i)))

dictx=dict()
print("-------------")
dictx["id1"]=x
dictx["id2"]=y

print(dictx.keys())

print("-------------")

import veritabani

import glob
import numpy as np
from PIL import Image

fileList=glob.glob('images/*.jpg')
x=np.array([np.array(Image.open(fname)) for fname in fileList])

from timeloop import Timeloop
from datetime import timedelta

count=0
import sqlite3,csv

baglan=sqlite3.connect("sirket.db")
cursor=baglan.cursor()

sorgu="select * from kisiler"
cursor.execute(sorgu,)
data=cursor.execute("SELECT * FROM kisiler")
dosya=open("dosya.csv","w")

dosya.write(",İsim,Soyisim,id,durum,kurum,kimlik,vesikalik \n")
for rwData in enumerate(data):
	veri=str(rwData)
	veri=veri.strip()
	veri=veri.replace("(","")
	veri=veri.replace(")","")
	veri = veri.replace(" ","")
	veri = veri.replace("'","")
	print(veri)
	dosya.write(str(veri))
	dosya.write("\n")

dosya.close()
