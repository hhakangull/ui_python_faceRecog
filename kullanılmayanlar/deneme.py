import time
from datetime import datetime
import threading,glob
import timestamps
import cv2

"""
class d:
	
	def __init__(self):
		self.x=0
		self.dosya=0
		self.b=None
		self.a=None
	
	def yaz(self):
		self.a=(str(int(datetime.timestamp(datetime.now()))))
		self.dosya+=1
		print(self.dosya)
		
		if self.a != self.b:
			print("değişiklik var")
			self.x+=1
			print(self.x)
		threading.Timer(0.1,self.yaz).start()
		self.b=self.a
"""

import time
import threading,glob
from numpy import random
import imageio

import glob
import os
import numpy as np



#random_numpy_image = random.random((250,250))   # Test data
random_numpy_image = np.random.randint(255, size=(900,800,3),dtype=np.uint8)


class d:
	def __init__(self):
		self.sayac=0
	def yaz(self):
		timestamp=time.time()
		filename=str(timestamp) + ".jpg"
		imageio.imwrite('images/' + filename,random_numpy_image)
		self.sayac+=1
		threading.Timer(0.2,self.yaz).start()
		
		if len(os.listdir('images/')) > 100:
			list_of_files=glob.glob('images/*')  # * means all if need specific format then *.csv
			
			oldest_file=min(list_of_files,key=os.path.getctime)
			os.remove(oldest_file)

d().yaz()