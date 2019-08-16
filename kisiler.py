from ui_pages.ui_kisiler import *
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QTableWidget
from PyQt5.QtGui import QPixmap
import kayit, veritabani, os


class KisilerMainWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.ui = Ui_Form1()
		self.ui.setupUi(self)
		self.ui.btnAktar.clicked.connect(self.aktar)
		self.ui.btnGuncelle.clicked.connect(self.guncelle)

		self.show()

	def sirketiGonder(self, sirket):
		self.sirket = sirket
		self.sirket.kisileri_goster(self.ui)

	"""def kayitWindow(self):
		self.kaydet=kayit.KayitMainWindow(self.sirket)"""

	def aktar(self):
		self.a = self.ui.tableWidget.currentRow()
		self.sirket.baglanti_olustur()
		sorgu = "select * from kisiler"
		self.sirket.cursor.execute(sorgu, )
		veri = self.sirket.cursor.fetchall()
		k_id = str(veri[self.a][2])
		self.ui.adLineEdit.setText(veri[self.a][0])
		self.ui.soyadLineEdit.setText(veri[self.a][1])
		self.ui.idLineEdit.setText(veri[self.a][2])
		self.ui.kimlikLineEdit.setText(veri[self.a][5])
		self.ui.kurumComboBox.setItemText(0, veri[self.a][4])
		self.ui.durumComboBox.setItemText(0, veri[self.a][3])
		self.genel = veri[self.a][6]
		yol = os.getcwd()+"/dataset/"+k_id+"/"+k_id+"_0.jpg"
		self.ui.label.setPixmap(QPixmap(yol))

		self.sirket.baglantiyi_kes()

	def guncelle(self):
		isim = self.ui.adLineEdit.text()
		soyisim = self.ui.soyadLineEdit.text()
		idx = self.ui.idLineEdit.text()
		kurum = self.ui.kurumComboBox.currentText()
		durum = self.ui.durumComboBox.currentText()
		kimlik = self.ui.kimlikLineEdit.text()

		vesikalik = self.genel
		# print(isim,soyisim,kurum,durum)
		yeni = veritabani.Kisi(isim, soyisim, durum, kurum, idx)
		# print(yeni)
		self.sirket.updatex(isim, soyisim, durum, kurum, idx)
		self.sirket.kisiTemizle(self.ui)
		self.sirket.kisileri_goster(self.ui)
