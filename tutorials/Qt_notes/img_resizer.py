"""
Görüntü Yeniden Boyutlandırıcı ve Düzenleyici Uygulaması

Qt5 ve Pillow kullanarak görüntü açma, yeniden boyutlandırma ve düzenleme özellikleri
içeren bir GUI uygulaması.

Özellikler:
- Görüntü açma ve görüntüleme
- Görüntü yeniden boyutlandırma (resize)
- Görüntü düzenleme (parlaklık, kontrast, döndürme, filtreler)
- Görüntü kaydetme
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox,
    QSlider, QSpinBox, QGroupBox, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image, ImageEnhance, ImageFilter


class ImageResizer(QWidget):
    def __init__(self):
        super().__init__()
        self.original_image = None
        self.current_image = None
        self.image_path = None
        
        self.init_ui()
    
    def init_ui(self):
        """Kullanıcı arayüzünü oluştur"""
        self.setWindowTitle("Görüntü Düzenleyici ve Yeniden Boyutlandırıcı")
        self.setGeometry(100, 100, 1000, 700)
        
        # Ana layout
        main_layout = QVBoxLayout()
        
        # Üst bölüm: Dosya işlemleri
        file_group = QGroupBox("Dosya İşlemleri")
        file_layout = QHBoxLayout()
        
        self.btn_open = QPushButton("Görüntü Aç")
        self.btn_open.clicked.connect(self.open_image)
        self.btn_save = QPushButton("Görüntü Kaydet")
        self.btn_save.clicked.connect(self.save_image)
        self.btn_save.setEnabled(False)
        self.btn_reset = QPushButton("Orijinal Haline Döndür")
        self.btn_reset.clicked.connect(self.reset_image)
        self.btn_reset.setEnabled(False)
        
        file_layout.addWidget(self.btn_open)
        file_layout.addWidget(self.btn_save)
        file_layout.addWidget(self.btn_reset)
        file_group.setLayout(file_layout)
        
        # Orta bölüm: Görüntü görüntüleme
        image_group = QGroupBox("Görüntü Önizleme")
        image_layout = QVBoxLayout()
        
        self.image_label = QLabel("Görüntü açmak için 'Görüntü Aç' butonuna tıklayın")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumHeight(400)
        self.image_label.setStyleSheet("border: 1px solid gray; background-color: #f0f0f0;")
        
        scroll = QScrollArea()
        scroll.setWidget(self.image_label)
        scroll.setWidgetResizable(True)
        
        image_layout.addWidget(scroll)
        image_group.setLayout(image_layout)
        
        # Alt bölüm: Düzenleme kontrolleri
        controls_group = QGroupBox("Görüntü Düzenleme Kontrolleri")
        controls_layout = QVBoxLayout()
        
        # Yeniden boyutlandırma
        resize_layout = QHBoxLayout()
        resize_layout.addWidget(QLabel("Genişlik:"))
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 10000)
        self.width_spin.setValue(800)
        self.width_spin.valueChanged.connect(self.on_resize_changed)
        resize_layout.addWidget(self.width_spin)
        
        resize_layout.addWidget(QLabel("Yükseklik:"))
        self.height_spin = QSpinBox()
        self.height_spin.setRange(1, 10000)
        self.height_spin.setValue(600)
        self.height_spin.valueChanged.connect(self.on_resize_changed)
        resize_layout.addWidget(self.height_spin)
        
        self.btn_apply_resize = QPushButton("Boyutlandırmayı Uygula")
        self.btn_apply_resize.clicked.connect(self.apply_resize)
        self.btn_apply_resize.setEnabled(False)
        resize_layout.addWidget(self.btn_apply_resize)
        
        controls_layout.addLayout(resize_layout)
        
        # Parlaklık kontrolü
        brightness_layout = QHBoxLayout()
        brightness_layout.addWidget(QLabel("Parlaklık:"))
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(0, 200)
        self.brightness_slider.setValue(100)
        self.brightness_slider.valueChanged.connect(self.on_brightness_changed)
        brightness_layout.addWidget(self.brightness_slider)
        self.brightness_value = QLabel("100")
        brightness_layout.addWidget(self.brightness_value)
        controls_layout.addLayout(brightness_layout)
        
        # Kontrast kontrolü
        contrast_layout = QHBoxLayout()
        contrast_layout.addWidget(QLabel("Kontrast:"))
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(0, 200)
        self.contrast_slider.setValue(100)
        self.contrast_slider.valueChanged.connect(self.on_contrast_changed)
        contrast_layout.addWidget(self.contrast_slider)
        self.contrast_value = QLabel("100")
        contrast_layout.addWidget(self.contrast_value)
        controls_layout.addLayout(contrast_layout)
        
        # Döndürme butonları
        rotate_layout = QHBoxLayout()
        self.btn_rotate_left = QPushButton("↺ 90° Sola")
        self.btn_rotate_left.clicked.connect(lambda: self.rotate_image(-90))
        self.btn_rotate_right = QPushButton("↻ 90° Sağa")
        self.btn_rotate_right.clicked.connect(lambda: self.rotate_image(90))
        self.btn_flip_h = QPushButton("↔ Yatay Çevir")
        self.btn_flip_h.clicked.connect(lambda: self.flip_image(horizontal=True))
        self.btn_flip_v = QPushButton("↕ Dikey Çevir")
        self.btn_flip_v.clicked.connect(lambda: self.flip_image(vertical=True))
        
        rotate_layout.addWidget(self.btn_rotate_left)
        rotate_layout.addWidget(self.btn_rotate_right)
        rotate_layout.addWidget(self.btn_flip_h)
        rotate_layout.addWidget(self.btn_flip_v)
        controls_layout.addLayout(rotate_layout)
        
        controls_group.setLayout(controls_layout)
        
        # Ana layout'a ekle
        main_layout.addWidget(file_group)
        main_layout.addWidget(image_group)
        main_layout.addWidget(controls_group)
        
        self.setLayout(main_layout)
        
        # Kontrolleri başlangıçta devre dışı bırak
        self.set_controls_enabled(False)
    
    def set_controls_enabled(self, enabled):
        """Tüm düzenleme kontrollerini etkin/devre dışı yap"""
        self.brightness_slider.setEnabled(enabled)
        self.contrast_slider.setEnabled(enabled)
        self.width_spin.setEnabled(enabled)
        self.height_spin.setEnabled(enabled)
        self.btn_apply_resize.setEnabled(enabled)
        self.btn_rotate_left.setEnabled(enabled)
        self.btn_rotate_right.setEnabled(enabled)
        self.btn_flip_h.setEnabled(enabled)
        self.btn_flip_v.setEnabled(enabled)
    
    def open_image(self):
        """Görüntü dosyası aç"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Görüntü Seç",
            "",
            "Görüntü Dosyaları (*.png *.jpg *.jpeg *.bmp *.gif *.tiff);;Tüm Dosyalar (*.*)"
        )
        
        if file_path:
            try:
                self.image_path = file_path
                self.original_image = Image.open(file_path)
                self.current_image = self.original_image.copy()
                self.display_image(self.current_image)
                
                # Orijinal boyutları spin box'lara ayarla
                width, height = self.original_image.size
                self.width_spin.blockSignals(True)
                self.height_spin.blockSignals(True)
                self.width_spin.setValue(width)
                self.height_spin.setValue(height)
                self.width_spin.blockSignals(False)
                self.height_spin.blockSignals(False)
                
                # Kontrolleri etkinleştir
                self.set_controls_enabled(True)
                self.btn_save.setEnabled(True)
                self.btn_reset.setEnabled(True)
                
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Görüntü açılamadı: {str(e)}")
    
    def display_image(self, image):
        """Görüntüyü QLabel'da göster"""
        # PIL Image'ı QImage'a dönüştür
        if image.mode == "RGB":
            r, g, b = image.split()
            image = Image.merge("RGB", (b, g, r))
        elif image.mode == "RGBA":
            r, g, b, a = image.split()
            image = Image.merge("RGBA", (b, g, r, a))
        elif image.mode == "L":
            image = image.convert("RGB")
            r, g, b = image.split()
            image = Image.merge("RGB", (b, g, r))
        
        img_byte_arr = image.tobytes("raw", "RGB")
        q_image = QImage(img_byte_arr, image.width, image.height, QImage.Format_RGB888)
        
        pixmap = QPixmap.fromImage(q_image)
        
        # Görüntüyü label boyutuna göre ölçeklendir (orantılı olarak)
        label_size = self.image_label.size()
        scaled_pixmap = pixmap.scaled(
            label_size.width() - 20,
            label_size.height() - 20,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        
        self.image_label.setPixmap(scaled_pixmap)
    
    def apply_resize(self):
        """Yeniden boyutlandırmayı uygula"""
        if not self.current_image:
            return
        
        width = self.width_spin.value()
        height = self.height_spin.value()
        
        self.current_image = self.current_image.resize((width, height), Image.Resampling.LANCZOS)
        self.display_image(self.current_image)
    
    def on_resize_changed(self):
        """Boyut değiştiğinde uyar (otomatik uygulama yok)"""
        pass
    
    def on_brightness_changed(self, value):
        """Parlaklık değiştiğinde görüntüyü güncelle"""
        if not self.original_image:
            return
        
        self.brightness_value.setText(str(value))
        self.update_image_enhancements()
    
    def on_contrast_changed(self, value):
        """Kontrast değiştiğinde görüntüyü güncelle"""
        if not self.original_image:
            return
        
        self.contrast_value.setText(str(value))
        self.update_image_enhancements()
    
    def update_image_enhancements(self):
        """Parlaklık ve kontrast değişikliklerini uygula"""
        if not self.original_image:
            return
        
        # Orijinal görüntüden başla
        self.current_image = self.original_image.copy()
        
        # Orijinal boyutları koru (resize uygulanmadıysa)
        current_size = self.current_image.size
        width = self.width_spin.value()
        height = self.height_spin.value()
        
        if current_size != (width, height):
            self.current_image = self.current_image.resize((width, height), Image.Resampling.LANCZOS)
        
        # Parlaklık uygula
        brightness_factor = self.brightness_slider.value() / 100.0
        enhancer = ImageEnhance.Brightness(self.current_image)
        self.current_image = enhancer.enhance(brightness_factor)
        
        # Kontrast uygula
        contrast_factor = self.contrast_slider.value() / 100.0
        enhancer = ImageEnhance.Contrast(self.current_image)
        self.current_image = enhancer.enhance(contrast_factor)
        
        self.display_image(self.current_image)
    
    def rotate_image(self, angle):
        """Görüntüyü döndür"""
        if not self.current_image:
            return
        
        self.current_image = self.current_image.rotate(angle, expand=True)
        
        # Boyutları güncelle
        width, height = self.current_image.size
        self.width_spin.blockSignals(True)
        self.height_spin.blockSignals(True)
        self.width_spin.setValue(width)
        self.height_spin.setValue(height)
        self.width_spin.blockSignals(False)
        self.height_spin.blockSignals(False)
        
        self.display_image(self.current_image)
    
    def flip_image(self, horizontal=False, vertical=False):
        """Görüntüyü çevir (yatay veya dikey)"""
        if not self.current_image:
            return
        
        if horizontal:
            self.current_image = self.current_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        if vertical:
            self.current_image = self.current_image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        
        self.display_image(self.current_image)
    
    def reset_image(self):
        """Görüntüyü orijinal haline döndür"""
        if not self.original_image:
            return
        
        self.current_image = self.original_image.copy()
        
        # Orijinal boyutları ayarla
        width, height = self.original_image.size
        self.width_spin.blockSignals(True)
        self.height_spin.blockSignals(True)
        self.width_spin.setValue(width)
        self.height_spin.setValue(height)
        self.width_spin.blockSignals(False)
        self.height_spin.blockSignals(False)
        
        # Slider'ları sıfırla
        self.brightness_slider.setValue(100)
        self.contrast_slider.setValue(100)
        
        self.display_image(self.current_image)
    
    def save_image(self):
        """Görüntüyü kaydet"""
        if not self.current_image:
            QMessageBox.warning(self, "Uyarı", "Kaydedilecek görüntü yok!")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Görüntüyü Kaydet",
            "",
            "PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp);;TIFF (*.tiff);;Tüm Dosyalar (*.*)"
        )
        
        if file_path:
            try:
                self.current_image.save(file_path)
                QMessageBox.information(self, "Başarılı", f"Görüntü kaydedildi: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Görüntü kaydedilemedi: {str(e)}")


def main():
    app = QApplication(sys.argv)
    window = ImageResizer()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

