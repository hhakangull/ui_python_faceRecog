import threading
import time
import os
import cv2,glob

path_images="images/"

cnt=0

import threading
import time
import os

path_images="images/"

cnt=0


def printit():
	images_list=[os.path.splitext(image)[0] for image in sorted(os.listdir(path_images))]
	threading.Timer(0.033,printit).start()
	global cnt
	curr_time=time.time()
	
	if curr_time - float(images_list[len(images_list) - 1]) < 0.033:
		#print(curr_time - float(images_list[len(images_list)-1]))
		list_of_files=glob.glob('images/*')  # * means all if need specific format then *.csv
		
		last_file=max(list_of_files,key=os.path.getctime)
		print(last_file)
		cnt+=1
		a =cv2.imread(last_file)

		# cv2.imshow('frame',gray)
		print(cnt)
printit()
cv2.waitKey(0)
cv2.destroyAllWindows()

