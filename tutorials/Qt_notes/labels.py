"""
PyQt5 QLabel (Etiket/Label) Kullanımı Örneği

QLabel, PyQt5'te metin veya görsel göstermek için kullanılan temel widget'lardan biridir.
Aşağıdaki örnek, farklı QLabel özelliklerini ve temel kullanım şeklini gösterir.

Genel Notlar:
- QLabel ile metin veya resim gösterebiliriz
- Text hizalama, font, stil vs. kolaylıkla ayarlanabilir.
- QLabel genellikle bilgi göstermek veya kullanıcıya durum bildirmek için kullanılır.
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class LabelDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QLabel Kullanımı / Label Örneği")
        self.resize(400, 220)
        
        # Basit bir metin etiketi
        label1 = QLabel("Bu bir <b>QLabel</b> örneğidir.")
        label1.setAlignment(Qt.AlignCenter)  # Ortala
        
        # Çok satırlı/hizalı metin
        label2 = QLabel("Birden fazla satır içerebilir.\nAyrıca hizalama değiştirilebilir.")
        label2.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # Sola hizalı, dikey ortala
        
        # HTML desteği ile formatlanmış metin
        label3 = QLabel('<span style="color:blue;">Renkli</span> <i>ve</i> <u>Biçimli</u> <b>Label</b>')
        label3.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        
        # Resim göstermek için QLabel kullanılabilir
        # label4 = QLabel()
        # label4.setPixmap(QPixmap("birresim.png"))
        
        # LABEL'i DISABLE ETMEK (kullanıcı etkileşimi olmasın)
        label2.setDisabled(True)

        # Layout ile etiketleri yerleştir
        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(label3)
        # layout.addWidget(label4)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LabelDemo()
    win.show()
    sys.exit(app.exec_())