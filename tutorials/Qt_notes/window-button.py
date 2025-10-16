"""
Pencere - Buton İlişkisini Anlatan Örnek

Bu dosya PyQt5 kullanarak pencereler ile butonların (ve diğer widget'ların)
nasıl ilişkilendirildiğini (signals/slots, enable/disable, toggle, custom
signals, veri iletimi, dialog açma vb.) gösterir.

Çalıştırmak için (PowerShell):
	pip install -r requirements.txt
	python window-button.py

Her bölümde kısa Türkçe açıklama ve örnek kod bulunur.
"""

import sys
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtWidgets import (
	QApplication,
	QWidget,
	QVBoxLayout,
	QPushButton,
	QLabel,
	QLineEdit,
	QMessageBox,
	QHBoxLayout,
)


class Communicator(QObject):
	"""
	Özel sinyaller (custom signals) oluşturmak için QObject'tan türeyen
	bir sınıf kullanıyoruz. Burada bir mesaj (string) gönderen sinyal tanımlanır.
	"""

	message = pyqtSignal(str)


class MainWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Pencere-Buton İlişkisi Örneği")
		self.resize(420, 220)

		# İletişim objesi: custom sinyal gönderip dinleyebiliriz
		self.comm = Communicator()
		self.comm.message.connect(self.on_custom_message)

		# --- Layout ve widget'lar ---
		self.label = QLabel("Durum: Hazır")
		self.label.setAlignment(Qt.AlignCenter)

		# Basit bir buton: tıklandığında label güncellenecek
		self.btn_click = QPushButton("Bana Tıkla")
		# clicked sinyali QPushButton'dan gelir; .connect ile slota bağlıyoruz
		self.btn_click.clicked.connect(self.on_btn_click)

		# Toggle (checkable) buton: durumuna göre farklı davranış
		self.btn_toggle = QPushButton("Toggle: Kapalı")
		self.btn_toggle.setCheckable(True)  # buton artık açık/kapalı davranır
		self.btn_toggle.toggled.connect(self.on_btn_toggled)

		# Bir buton diğerini devre dışı bırakacak (enable/disable örneği)
		self.btn_disable_other = QPushButton("Diğer Butonu Devre Dışı Bırak")
		self.btn_disable_other.clicked.connect(self.on_disable_other)

		# Girdi alanı: metin değiştirilince etiketi güncelleme (veri iletimi)
		self.input_line = QLineEdit()
		self.input_line.setPlaceholderText("Buraya yazın ve anında etiketi güncelleyin")
		self.input_line.textChanged.connect(self.on_text_changed)

		# Butonla dialog açma örneği
		self.btn_dialog = QPushButton("Dialog Aç")
		self.btn_dialog.clicked.connect(self.on_open_dialog)

		# Lambda ile parametre geçirmek: aynı slotu farklı argümanlarla kullanmak
		self.btn_send_custom = QPushButton("Özel Mesaj Gönder")
		self.btn_send_custom.clicked.connect(lambda: self.comm.message.emit("Merhaba from buton!"))

		# Layout düzeni
		h = QHBoxLayout()
		h.addWidget(self.btn_click)
		h.addWidget(self.btn_toggle)
		h.addWidget(self.btn_disable_other)

		h2 = QHBoxLayout()
		h2.addWidget(self.btn_dialog)
		h2.addWidget(self.btn_send_custom)

		layout = QVBoxLayout()
		layout.addWidget(self.label)
		layout.addLayout(h)
		layout.addWidget(self.input_line)
		layout.addLayout(h2)

		self.setLayout(layout)

		# Demonstrasyon: parent-child ilişkisi
		# btn_click parent'ı olarak MainWindow'ı alır (zaten eklenmiş).
		# Eğer btn_click'i silerseniz (deleteLater) parent onun yaşam döngüsünü
		# kontrol eder. Bu şekilde widget'lar hiyerarşik olarak yönetilir.

	# --- Slotlar (butonlardan gelen sinyalleri işleyen metodlar) ---
	def on_btn_click(self):
		"""Basit tıklama: label güncelle ve örnek olarak diğer butonu etkinleştir."""
		self.label.setText("Durum: " + "Bana Tıklandı")
		# Örnek: tıklayınca 'Diğer' butonun metnini değiştir
		self.btn_disable_other.setText("Diğer Buton (Hazır)")

	def on_btn_toggled(self, checked: bool):
		"""Toggle buton True/False gönderir. Bu örnekte metni ve pencere
		arka plan rengini değiştiriyoruz (küçük görsel etki için)."""
		if checked:
			self.btn_toggle.setText("Toggle: Açık")
			# disable click buton while toggled (örnek etkileşim)
			self.btn_click.setEnabled(False)
			self.label.setText("Durum: Toggle Açık — Click butonu devre dışı")
			# setStyleSheet örneği: pencere arka planını aç/kapa göre değiştir
			self.setStyleSheet("background-color: #f0fff0;")
		else:
			self.btn_toggle.setText("Toggle: Kapalı")
			self.btn_click.setEnabled(True)
			self.label.setText("Durum: Toggle Kapalı — Click butonu etkin")
			self.setStyleSheet("")

	def on_disable_other(self):
		"""Bir butonun başka bir butonu devre dışı bırakması (enable/disable).
		Bu, widget'lar arası etkileşimin temel örneklerinden biridir."""
		# btn_disable_other butonunun durumu göre hareket edelim
		currently_enabled = self.btn_click.isEnabled()
		self.btn_click.setEnabled(not currently_enabled)
		self.label.setText("Durum: btn_click {}".format("etkin" if not currently_enabled else "devre dışı"))

	def on_text_changed(self, text: str):
		"""QLineEdit'in textChanged sinyalini yakalayarak anlık veri aktarımı.
		Burada sadece label'a yansıtıyoruz."""
		if text:
			self.label.setText(f"Giriş: {text}")
		else:
			self.label.setText("Durum: Hazır")

	def on_open_dialog(self):
		reply = QMessageBox.question(
			self,
			"Soru",
			"Buton etkileşimini sıfırlamak istiyor musunuz?",
			QMessageBox.Yes | QMessageBox.No,
			QMessageBox.No,
		)
		if reply == QMessageBox.Yes:
			# Örnek: tüm widget'ları varsayılan duruma getir
			self.btn_toggle.setChecked(False)
			self.btn_click.setEnabled(True)
			self.input_line.clear()
			self.label.setText("Durum: Sıfırlandı")

	def on_custom_message(self, msg: str):

		# Kısa bir MessageBox ile gösterelim
		QMessageBox.information(self, "Özel Mesaj", f"Gelen mesaj: {msg}")


def main():
	app = QApplication(sys.argv)
	win = MainWindow()
	win.show()
	sys.exit(app.exec_())


if __name__ == "__main__":
	main()

