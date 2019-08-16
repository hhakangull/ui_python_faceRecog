# -*- coding: utf-8 -*-
# import  PyQt5 modüller
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget
from ui_pages.ui_main import *
from veritabani import Sirket
from kisiler import *
from data import *
import cv2
import datetime
import kayit

import glob, os

# Kaynak Dosya Yollarını Belirlemek için Bunlar 0 - 1 -2 -3 -4 diye gidebilir kameralara bağlı olarak
source1 = 0  # "videolar/video1.mp4"  # 0
source2 = "videolar/video1.mp4"
source3 = "videolar/video1.mp4"  # 6
source4 = "videolar/video1.mp4"
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


class MainWindow(QWidget):
	# class constructor
	def __init__(self):
		# QWidget Yani Pencereyi oluşturduğumuz kısım
		super().__init__()
		self.ui = Ui_Form()
		self.ui.setupUi(self)
		# Data Yüklemesi
		self.sirket = Sirket()
		self.sirket.kayitlariGoster(self.ui)
		# create a timer kamerayı açmak için lazım olan timer fonksiyonları
		self.timer = QTimer()
		self.timer2 = QTimer()
		self.timer3 = QTimer()
		self.timer4 = QTimer()
		# set timer timeout callback function
		self.camKontrol = False
		self.timer.timeout.connect(self.viewCam)
		self.timer2.timeout.connect(self.viewCam2)
		self.timer3.timeout.connect(self.viewCam3)
		self.timer4.timeout.connect(self.viewCam4)
		# butonlara basıldığında yapması gereken işlemlerin olduğu kısım
		self.ui.control_bt.clicked.connect(self.controlTimer)
		self.ui.pushButton.clicked.connect(self.getir)
		# self.ui.control_bt_2.clicked.connect(self.duzelt)
		self.ui.btnKisiler.clicked.connect(self.kisilerWindow)
		self.ui.btnKayit.clicked.connect(self.dataWindow)
		self.ui.btnKisiEkle.clicked.connect(self.kayitWindow)
		self.gonder = None
		self.ui.image_label.setText("Kamera 1")
		self.ui.image_label_2.setText("Kamera 2")
		self.ui.image_label_3.setText("Kamera 3")
		self.ui.image_label_4.setText("Kamera 4")
		self.last_img_fname = "0"
		self.ui.control_bt_2.clicked.connect(self.dosyaOlustur)
		self.kontrolList = list()

	def viewCam(self):
		# # read image in BGR format
		# ret,image=self.cap.read()
		# # convert image to RGB format
		# image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
		# # image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
		# # get image infos
		# height,width,channel=image.shape
		# step=channel*width
		# # create QImage from image
		# qImg=QImage(image.data,width,height,step,QImage.Format_RGB888)
		# # show image in img_label
		# self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))
		# self.ui.image_label.setScaledContents(True)
		global id
		imreaddir = "kisiler/"

		imdirs = sorted(glob.glob(imreaddir + "/" + '*.jpg'))

		updated_img_fname = imdirs[-1].split(os.path.sep)[-1][:-4]

		if updated_img_fname != self.last_img_fname:
			image = cv2.imread(imdirs[-1])
			got_image = False
		if updated_img_fname != self.last_img_fname:
			got_image = False
			while not got_image:
				try:
					image = cv2.imread(imdirs[-1])
					image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
					got_image = True
				except:
					got_image = False

			height, width, channel = image.shape
			step = channel * width
			qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
			self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))
			self.ui.image_label.setScaledContents(True)
			imnamedata = updated_img_fname.split("_")
			if len(imnamedata) > 1:
				id = imnamedata[1]
			# TODO: add entered guy id to list
			# print(str(id))
			self.last_img_fname = updated_img_fname
		# print(self.last_img_fname)
		self.kisi1BilgiGetir(kisiID=id)

	def dosyaOlustur(self):
		with open("dataset/__train__", "w") as f:
			f.write("")

	def getir(self):
		try:
			veri = self.gonder.ui.kontrol.text()
			self.renkDegis(veri)
		except AttributeError:
			# TO DO veri
			pass

	# Kisiler Penceresi
	def kisi1BilgiGetir(self, kisiID):
		self.tarih = datetime.datetime.now()
		self.saat = datetime.datetime.now()
		print(self.saat)
		isim = kisiID
		kisi = self.sirket.kisi_sorgula(isim)
		adSoyad = kisi.isim + " " + kisi.soyisim
		self.ui.lbl_AdSoyad.setText(adSoyad)
		self.ui.lblCikis.hide()
		tarih = str(datetime.datetime.strftime(self.tarih, '%x'))
		saat = str(datetime.datetime.strftime(self.saat, '%X'))
		if (kisi.durum == "izinli"):
			self.ui.lbl_izinsiz.hide()
		else:
			self.ui.lbl_izinli.hide()
		self.ui.lbl_ID.setText(kisi.id)
		giris = "Giriş"
		if isim not in self.kontrolList:
			self.sirket.kayitEkle(kisi.id, kisi.durum, giris, kisi.isim, kisi.soyisim, tarih, saat)
			self.sirket.tableClear(self.ui)
			self.sirket.kayitlariGoster(self.ui)
			self.kontrolList.append(isim)
		else:

			yol = "kisiler/"
			x = self.last_img_fname
			x += ".jpg"
			# print(yol+x)
			fotograf = cv2.imread(yol + x, 1)
			faces = face_cascade.detectMultiScale(cv2.cvtColor(fotograf, cv2.COLOR_BGR2GRAY), 1.3, 5)
			for (x, y, w, h) in faces:
				roi_gray = faces[y:y + h, x:x + w]
				roi_color = fotograf[y:y + h, x:x + w]
			fotograf = cv2.cvtColor(roi_color, cv2.COLOR_BGR2RGB)
			h, w, c = fotograf.shape
			step = c * w
			fotografx = QImage(fotograf.data, w, h, step, QImage.Format_RGB888)
			self.ui.lblProfilFoto.setPixmap(QPixmap.fromImage(fotografx))
			self.ui.lblProfilFoto.setScaledContents(True)

	def kisilerWindow(self):
		self.kisiler = KisilerMainWindow()
		self.kisiler.sirketiGonder(self.sirket)

	def kayitWindow(self):
		self.gonder = kayit.KayitMainWindow(self.sirket)
		if self.camKontrol:
			self.timer.stop()
			self.cap.release()

	def dataWindow(self):
		self.dataPy = DataMainWindow()

	# view camera 1

	# view camera 2
	def viewCam2(self):
		# read image in BGR format
		ret, image = self.cap2.read()
		# convert image to RGB format
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		# get image infos
		height, width, channel = image.shape
		step = channel * width
		# create QImage from image
		qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
		# show image in img_label
		self.ui.image_label_2.setPixmap(QPixmap.fromImage(qImg))
		self.ui.image_label_2.setScaledContents(True)

	# view camera 3
	def viewCam3(self):
		# read image in BGR format
		ret, image = self.cap3.read()
		# convert image to RGB format
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		# image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
		# get image infos
		height, width, channel = image.shape
		step = channel * width
		# create QImage from image
		qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
		# show image in img_label
		self.ui.image_label_3.setPixmap(QPixmap.fromImage(qImg))
		self.ui.image_label_3.setScaledContents(True)

	# view camera 4
	def viewCam4(self):
		# read image in BGR format
		ret, image = self.cap4.read()
		# convert image to RGB format
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		# image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
		# get image infos
		height, width, channel = image.shape
		step = channel * width
		# create QImage from image
		qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
		# show image in img_label
		self.ui.image_label_4.setPixmap(QPixmap.fromImage(qImg))
		self.ui.image_label_4.setScaledContents(True)

	# start/stop timer
	def controlTimer(self):

		# if timer is stopped
		if not (self.timer.isActive() or self.timer2.isActive() or self.timer3.isActive()):
			# create video capture
			self.cap = cv2.VideoCapture(source1)
			# self.cap2=cv2.VideoCapture(source2)
			# self.cap3=cv2.VideoCapture(source3)
			# self.cap4=cv2.VideoCapture(source4)
			# start timer
			self.timer.start()
			# self.timer2.start()
			# self.timer3.start()
			# self.timer4.start()
			self.camKontrol = True
			# update control_bt text
			self.ui.control_bt.setText("Stop")
			self.getir()
		# if timer is started
		else:
			# stop timer
			self.timer.stop()
			# self.timer2.stop()
			# self.timer3.stop()
			# self.timer4.stop()
			# release video capture
			self.cap.release()
			# self.cap2.release()
			# self.cap3.release()
			# self.cap4.release()
			# update control_bt text
			self.ui.control_bt.setText("Start")

	def renkDegis(self, kontrol):
		durumx = kontrol
		self.durum = durumx
		if self.durum == "True":
			self.ui.control_bt_2.setStyleSheet("background-color: rgb(52, 101, 164);")
			durumx = "False"

	def duzelt(self):
		self.ui.control_bt_2.setStyleSheet("")

	def x(self):
		x = self.ui.tableWidget.cellClicked()
		print(x)

	def resimOku(self):
		pass


if __name__ == '__main__':
	import sys

	app = QApplication(sys.argv)
	# create and show mainWindow
	mainWindow = MainWindow()
	mainWindow.show()
	sys.exit(app.exec_())
