from PyQt6.QtWidgets import (QButtonGroup, QCheckBox, QComboBox, QHBoxLayout, QLabel, QMainWindow, QApplication, QRadioButton, QSpinBox, QTextEdit, QWidget, 
                             QVBoxLayout, QLineEdit, QPushButton,
                             QMessageBox)
import sys

class KayitFormu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kullanıcı Kayıt Formu")
        self.setGeometry(100, 100, 500, 600)
        self.initUI()
        
    def initUI(self):
        # merkezi widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # ana layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)


        # ---------- alanlar -----------
        ad_label = QLabel("Ad: ")
        self.ad_input = QLineEdit()

        soyad_label  = QLabel('Soyad: ')
        self.soyad_input = QLineEdit()

        mail_label= QLabel('Mail: ')
        self.mail_input = QLineEdit()

        yas_label = QLabel("Yaş: ")
        self.yas_input = QSpinBox()
        self.yas_input.setRange(1,100)
        self.yas_input.setValue(18)

        cinsiyet_label = QLabel('Cinsiyet: ')
        self.cinsiyet_erkek = QRadioButton('Erkek')
        self.cinsiyet_kadin = QRadioButton('Kadın')
        self.cinsiyet_diger = QRadioButton('Diğer')

        #radio butonları grupla
        self.cinsiyet_grup = QButtonGroup()
        self.cinsiyet_grup.addButton(self.cinsiyet_erkek)
        self.cinsiyet_grup.addButton(self.cinsiyet_kadin)
        self.cinsiyet_grup.addButton(self.cinsiyet_diger)

        #horizontal layouta ile yan yana hizalandırma
        cinsiyet_layout = QHBoxLayout()
        cinsiyet_layout.addWidget(self.cinsiyet_erkek)
        cinsiyet_layout.addWidget(self.cinsiyet_kadin)
        cinsiyet_layout.addWidget(self.cinsiyet_diger)


        ilgi_label = QLabel("İlgi Alanları: ")
        self.ilgi_muzik = QCheckBox("Müzik")
        self.ilgi_spor = QCheckBox("Spor")
        self.ilgi_kitap = QCheckBox("Kitap")
        self.ilgi_sinema = QCheckBox("Sinema")

        ilgi_layout = QHBoxLayout()
        ilgi_layout.addWidget(self.ilgi_muzik)
        ilgi_layout.addWidget(self.ilgi_spor)
        ilgi_layout.addWidget(self.ilgi_kitap)
        ilgi_layout.addWidget(self.ilgi_sinema)

        ulke_label = QLabel("Ülke: ")
        self.ulke_combo = QComboBox()
        self.ulke_combo.addItems(["Türkiye", "Almanya", "Fransa", "İngiltere", "ABD"])

        aciklama_label = QLabel("Açıklama: ")
        self.aciklama_text = QTextEdit()
        self.aciklama_text.setMaximumHeight(100)


        sifre_label = QLabel('Şifre: ')
        self.sifre_input = QLineEdit()
        self.sifre_input.setEchoMode(QLineEdit.EchoMode.Password)

        sifre_tekrar_label = QLabel('Şifre Tekrar: ')
        self.sifre_tekrar_input = QLineEdit()
        self.sifre_tekrar_input.setEchoMode(QLineEdit.EchoMode.Password)


        self.kaydet_btn = QPushButton("Kaydet")
        self.kaydet_btn.clicked.connect(self.kaydet)



        # layouta ekle
        main_layout.addWidget(ad_label)
        main_layout.addWidget(self.ad_input)

        main_layout.addWidget(soyad_label)
        main_layout.addWidget(self.soyad_input)

        main_layout.addWidget(mail_label)
        main_layout.addWidget(self.mail_input)

        main_layout.addWidget(yas_label)
        main_layout.addWidget(self.yas_input)

        main_layout.addWidget(ilgi_label)
        main_layout.addLayout(ilgi_layout)

        main_layout.addWidget(ulke_label)
        main_layout.addWidget(self.ulke_combo)

        main_layout.addWidget(cinsiyet_label)
        main_layout.addLayout(cinsiyet_layout)  

        main_layout.addWidget(aciklama_label)
        main_layout.addWidget(self.aciklama_text)




        main_layout.addWidget(sifre_label)
        main_layout.addWidget(self.sifre_input)

        main_layout.addWidget(sifre_tekrar_label)
        main_layout.addWidget(self.sifre_tekrar_input)


        main_layout.addWidget(self.kaydet_btn)

    def kaydet(self):
        hatalar = []
        
        if not self.ad_input.text().strip():
            hatalar.append("Ad boş olamaz")
        
        if not self.soyad_input.text().strip():
            hatalar.append("Soyad boş olamaz")
        
        email = self.mail_input.text()
        if not email or "@" not in email:
            hatalar.append("geçerli bir e-posta adresi giriniz ( @ içermeli )")

        sifre = self.sifre_input.text()
        if len(sifre) < 6:
            hatalar.append("Şifre en az 6 karakter olmalıdır")
        
        
        if sifre != self.sifre_tekrar_input.text():
            hatalar.append("Şifreler eşleşmiyor")
        
        if self.ilgi_muzik.isChecked() == False and self.ilgi_spor.isChecked() == False and self.ilgi_kitap.isChecked() == False and self.ilgi_sinema.isChecked() == False:
            hatalar.append("En az bir ilgi alanı seçmelisiniz")

        if self.cinsiyet_erkek.isChecked() == False and self.cinsiyet_kadin.isChecked() == False and self.cinsiyet_diger.isChecked() == False:
            hatalar.append("Cinsiyet seçmelisiniz")

        
        if hatalar:
            QMessageBox.warning(self, "Validasyon Hatası", "\n".join(hatalar))
        else:
            QMessageBox.information(self, "Başarılı", "Kayıt başarıyla tamamlandı.")


        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = KayitFormu()
    widget.show()
    sys.exit(app.exec())