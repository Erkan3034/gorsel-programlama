"""
Görüntü Yeniden Boyutlandırıcı ve Düzenleyici Uygulaması

Qt5 ve Pillow kullanarak görüntü düzenleme uygulaması.
Microsoft Fotoğraflar tarzı sürüklenebilir kırpma ve dinamik boyut gösterimi.
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox, QSlider,
    QMenuBar, QMenu, QAction, QToolBar, QSpinBox
)
from PyQt5.QtCore import Qt, QPoint, QRect, QSize
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QPen, QFont
from PIL import Image, ImageEnhance, ImageFilter


class ImageWidget(QLabel):
    """Görüntü gösterimi ve kırpma için özel widget"""
    def __init__(self):
        super().__init__()
        self.pil_image = None
        self.pixmap = None
        self.scale_factor = 1.0
        self.image_rect = QRect()
        
        # Kırpma için
        self.crop_mode = False
        self.crop_start = QPoint()
        self.crop_end = QPoint()
        self.crop_rect = QRect()
        self.dragging = False
        self.drag_handle = None  # 'nw', 'ne', 'sw', 'se', 'n', 's', 'e', 'w' veya None
        
        # Dinamik boyut gösterimi
        self.show_dimensions = True
        
        self.setMinimumSize(600, 400)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: #2b2b2b; border: 2px solid #404040;")
    
    def set_image(self, pil_image):
        """PIL Image'ı ayarla ve göster"""
        self.pil_image = pil_image
        self.update_display()
    
    def update_display(self):
        """Görüntüyü güncelle ve göster"""
        if not self.pil_image:
            return
        
        # PIL Image'ı QPixmap'a dönüştür
        q_image = self.pil_to_qimage(self.pil_image)
        self.pixmap = QPixmap.fromImage(q_image)
        
        # Widget boyutuna göre ölçeklendir
        widget_size = self.size()
        if widget_size.width() > 0 and widget_size.height() > 0:
            scaled = self.pixmap.scaled(
                widget_size.width() - 40,
                widget_size.height() - 40,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            # Ölçek faktörünü hesapla
            if self.pixmap.width() > 0:
                self.scale_factor = scaled.width() / self.pixmap.width()
            
            # Görüntünün widget içindeki konumunu hesapla
            x = (widget_size.width() - scaled.width()) // 2
            y = (widget_size.height() - scaled.height()) // 2
            self.image_rect = QRect(x, y, scaled.width(), scaled.height())
        
        self.update()
    
    def pil_to_qimage(self, pil_image):
        """PIL Image'ı QImage'a dönüştür"""
        if pil_image.mode == "RGB":
            r, g, b = pil_image.split()
            image = Image.merge("RGB", (b, g, r))
        elif pil_image.mode == "RGBA":
            r, g, b, a = pil_image.split()
            image = Image.merge("RGBA", (b, g, r, a))
        else:
            image = pil_image.convert("RGB")
            r, g, b = image.split()
            image = Image.merge("RGB", (b, g, r))
        
        img_byte_arr = image.tobytes("raw", image.mode[:3])
        return QImage(img_byte_arr, image.width, image.height, QImage.Format_RGB888)
    
    def get_crop_coords(self):
        """Kırpma koordinatlarını gerçek görüntü boyutuna göre döndür"""
        if not self.crop_rect.isValid() or not self.pil_image:
            return None
        
        # Widget koordinatlarını görüntü koordinatlarına dönüştür
        x1 = max(0, int((self.crop_rect.left() - self.image_rect.left()) / self.scale_factor))
        y1 = max(0, int((self.crop_rect.top() - self.image_rect.top()) / self.scale_factor))
        x2 = min(self.pil_image.width, int((self.crop_rect.right() - self.image_rect.left()) / self.scale_factor))
        y2 = min(self.pil_image.height, int((self.crop_rect.bottom() - self.image_rect.top()) / self.scale_factor))
        
        if x2 > x1 and y2 > y1:
            return (x1, y1, x2, y2)
        return None
    
    def paintEvent(self, event):
        """Widget'ı çiz"""
        painter = QPainter(self)
        
        # Arka plan
        painter.fillRect(self.rect(), QColor("#2b2b2b"))
        
        # Görüntüyü çiz
        if self.pixmap and not self.pixmap.isNull():
            painter.drawPixmap(self.image_rect, self.pixmap)
            
            # Boyut bilgisini göster
            if self.show_dimensions and self.pil_image:
                width, height = self.pil_image.size
                info_text = f"{width} × {height} px"
                painter.setPen(QPen(QColor(255, 255, 255, 200), 2))
                painter.setFont(QFont("Arial", 12, QFont.Bold))
                text_rect = painter.fontMetrics().boundingRect(info_text)
                text_x = self.image_rect.right() - text_rect.width() - 10
                text_y = self.image_rect.top() + text_rect.height() + 10
                painter.fillRect(text_x - 5, text_y - text_rect.height() - 5,
                               text_rect.width() + 10, text_rect.height() + 10,
                               QColor(0, 0, 0, 150))
                painter.drawText(text_x, text_y, info_text)
            
            # Kırpma dikdörtgenini çiz
            if self.crop_mode and self.crop_rect.isValid():
                # Karanlık overlay
                painter.fillRect(self.image_rect, QColor(0, 0, 0, 100))
                painter.fillRect(self.crop_rect, QColor(255, 255, 255, 0))
                
                # Kenar çizgileri
                pen = QPen(QColor(255, 255, 0), 2)
                painter.setPen(pen)
                painter.drawRect(self.crop_rect)
                
                # Köşe tutamaçları
                handle_size = 8
                handles = [
                    (self.crop_rect.left(), self.crop_rect.top()),  # NW
                    (self.crop_rect.right(), self.crop_rect.top()),  # NE
                    (self.crop_rect.left(), self.crop_rect.bottom()),  # SW
                    (self.crop_rect.right(), self.crop_rect.bottom()),  # SE
                    (self.crop_rect.center().x(), self.crop_rect.top()),  # N
                    (self.crop_rect.center().x(), self.crop_rect.bottom()),  # S
                    (self.crop_rect.left(), self.crop_rect.center().y()),  # W
                    (self.crop_rect.right(), self.crop_rect.center().y()),  # E
                ]
                
                for x, y in handles:
                    painter.fillRect(x - handle_size//2, y - handle_size//2,
                                   handle_size, handle_size, QColor(255, 255, 0))
    
    def mousePressEvent(self, event):
        """Fare basıldığında"""
        if not self.crop_mode or not self.pil_image:
            return
        
        pos = event.pos()
        
        # Tutamaç kontrolü
        if self.crop_rect.isValid():
            handle_size = 12
            handles = {
                'nw': (self.crop_rect.left(), self.crop_rect.top()),
                'ne': (self.crop_rect.right(), self.crop_rect.top()),
                'sw': (self.crop_rect.left(), self.crop_rect.bottom()),
                'se': (self.crop_rect.right(), self.crop_rect.bottom()),
                'n': (self.crop_rect.center().x(), self.crop_rect.top()),
                's': (self.crop_rect.center().x(), self.crop_rect.bottom()),
                'w': (self.crop_rect.left(), self.crop_rect.center().y()),
                'e': (self.crop_rect.right(), self.crop_rect.center().y()),
            }
            
            for handle_name, (hx, hy) in handles.items():
                if abs(pos.x() - hx) < handle_size and abs(pos.y() - hy) < handle_size:
                    self.drag_handle = handle_name
                    self.dragging = True
                    return
            
            # Dikdörtgen içinde ise taşı
            if self.crop_rect.contains(pos):
                self.dragging = True
                self.drag_offset = pos - self.crop_rect.topLeft()
                return
        
        # Yeni kırpma başlat
        self.crop_start = pos
        self.crop_end = pos
        self.crop_rect = QRect(self.crop_start, self.crop_end).normalized()
        self.crop_rect = self.crop_rect.intersected(self.image_rect)
        self.dragging = True
        self.update()
    
    def mouseMoveEvent(self, event):
        """Fare hareket ettiğinde"""
        if not self.crop_mode or not self.dragging:
            return
        
        pos = event.pos()
        
        if self.drag_handle:
            # Tutamaçtan sürükle
            rect = self.crop_rect
            if 'n' in self.drag_handle:
                rect.setTop(pos.y())
            if 's' in self.drag_handle:
                rect.setBottom(pos.y())
            if 'w' in self.drag_handle:
                rect.setLeft(pos.x())
            if 'e' in self.drag_handle:
                rect.setRight(pos.x())
            self.crop_rect = rect.normalized().intersected(self.image_rect)
        elif hasattr(self, 'drag_offset'):
            # Dikdörtgeni taşı
            new_top_left = pos - self.drag_offset
            if self.image_rect.contains(QRect(new_top_left, self.crop_rect.size())):
                self.crop_rect.moveTopLeft(new_top_left)
        else:
            # Yeni kırpma dikdörtgeni çiz
            self.crop_end = pos
            self.crop_rect = QRect(self.crop_start, self.crop_end).normalized()
            self.crop_rect = self.crop_rect.intersected(self.image_rect)
        
        self.update()
    
    def mouseReleaseEvent(self, event):
        """Fare bırakıldığında"""
        self.dragging = False
        self.drag_handle = None
    
    def resizeEvent(self, event):
        """Widget boyutu değiştiğinde"""
        super().resizeEvent(event)
        self.update_display()


class ImageResizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.original_image = None
        self.current_image = None
        
        self.init_ui()
    
    def init_ui(self):
        """Kullanıcı arayüzünü oluştur"""
        self.setWindowTitle("Görüntü Düzenleyici")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e1e; }
            QPushButton {
                background-color: #404040;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #505050; }
            QPushButton:pressed { background-color: #303030; }
            QPushButton:disabled { background-color: #2b2b2b; color: #666666; }
            QSlider::groove:horizontal {
                background-color: #404040;
                height: 6px;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background-color: #0078d4;
                width: 18px;
                height: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background-color: #005a9e;
            }
            QSpinBox {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #404040;
                padding: 4px;
                border-radius: 3px;
            }
            QLabel { color: white; }
            QMenuBar { background-color: #2b2b2b; color: white; }
            QMenu { background-color: #2b2b2b; color: white; }
            QMenu::item:selected { background-color: #0078d4; }
        """)
        
        # Merkez widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Menü bar
        self.create_menu_bar()
        
        # Toolbar
        self.create_toolbar()
        
        # Görüntü widget'ı
        self.image_widget = ImageWidget()
        layout.addWidget(self.image_widget)
        
        # Kontroller
        controls_layout = QHBoxLayout()
        
        # Boyut kontrolleri
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Genişlik:"))
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 10000)
        self.width_spin.valueChanged.connect(self.on_size_changed)
        size_layout.addWidget(self.width_spin)
        
        size_layout.addWidget(QLabel("Yükseklik:"))
        self.height_spin = QSpinBox()
        self.height_spin.setRange(1, 10000)
        self.height_spin.valueChanged.connect(self.on_size_changed)
        size_layout.addWidget(self.height_spin)
        
        controls_layout.addLayout(size_layout)
        controls_layout.addStretch()
        
        layout.addLayout(controls_layout)
        
        # Durum mesajları
        self.statusBar().showMessage("Hazır")
    
    def create_menu_bar(self):
        """Menü bar'ı oluştur"""
        menubar = self.menuBar()
        
        # Dosya menüsü
        file_menu = menubar.addMenu("Dosya")
        open_action = QAction("Görüntü Aç", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_image)
        file_menu.addAction(open_action)
        
        save_action = QAction("Kaydet", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_image)
        save_action.setEnabled(False)
        self.save_action = save_action
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        reset_action = QAction("Orijinal Haline Döndür", self)
        reset_action.triggered.connect(self.reset_image)
        reset_action.setEnabled(False)
        self.reset_action = reset_action
        file_menu.addAction(reset_action)
        
        # Döndürme menüsü
        rotate_menu = menubar.addMenu("Döndürme")
        
        rotate_left_action = QAction("90° Sola", self)
        rotate_left_action.triggered.connect(lambda: self.rotate_image(-90))
        rotate_left_action.setEnabled(False)
        self.rotate_left_action = rotate_left_action
        rotate_menu.addAction(rotate_left_action)
        
        rotate_right_action = QAction("90° Sağa", self)
        rotate_right_action.triggered.connect(lambda: self.rotate_image(90))
        rotate_right_action.setEnabled(False)
        self.rotate_right_action = rotate_right_action
        rotate_menu.addAction(rotate_right_action)
        
        rotate_menu.addSeparator()
        
        flip_h_action = QAction("Yatay Çevir", self)
        flip_h_action.triggered.connect(lambda: self.flip_image(True, False))
        flip_h_action.setEnabled(False)
        self.flip_h_action = flip_h_action
        rotate_menu.addAction(flip_h_action)
        
        flip_v_action = QAction("Dikey Çevir", self)
        flip_v_action.triggered.connect(lambda: self.flip_image(False, True))
        flip_v_action.setEnabled(False)
        self.flip_v_action = flip_v_action
        rotate_menu.addAction(flip_v_action)
        
        # Filtreler menüsü
        filter_menu = menubar.addMenu("Filtreler")
        
        brightness_action = QAction("Parlaklık", self)
        brightness_action.triggered.connect(self.show_brightness_dialog)
        brightness_action.setEnabled(False)
        self.brightness_action = brightness_action
        filter_menu.addAction(brightness_action)
        
        contrast_action = QAction("Kontrast", self)
        contrast_action.triggered.connect(self.show_contrast_dialog)
        contrast_action.setEnabled(False)
        self.contrast_action = contrast_action
        filter_menu.addAction(contrast_action)
        
        filter_menu.addSeparator()
        
        blur_action = QAction("Bulanıklaştır", self)
        blur_action.triggered.connect(lambda: self.apply_filter(ImageFilter.BLUR))
        blur_action.setEnabled(False)
        self.blur_action = blur_action
        filter_menu.addAction(blur_action)
        
        sharpen_action = QAction("Keskinleştir", self)
        sharpen_action.triggered.connect(lambda: self.apply_filter(ImageFilter.SHARPEN))
        sharpen_action.setEnabled(False)
        self.sharpen_action = sharpen_action
        filter_menu.addAction(sharpen_action)
        
        # Kırpma menüsü
        crop_menu = menubar.addMenu("Kırpma")
        
        crop_start_action = QAction("Kırpmayı Başlat", self)
        crop_start_action.triggered.connect(self.start_crop)
        crop_start_action.setEnabled(False)
        self.crop_start_action = crop_start_action
        crop_menu.addAction(crop_start_action)
        
        crop_apply_action = QAction("Kırpmayı Uygula", self)
        crop_apply_action.triggered.connect(self.apply_crop)
        crop_apply_action.setEnabled(False)
        self.crop_apply_action = crop_apply_action
        crop_menu.addAction(crop_apply_action)
        
        crop_cancel_action = QAction("Kırpmayı İptal Et", self)
        crop_cancel_action.triggered.connect(self.cancel_crop)
        crop_cancel_action.setEnabled(False)
        self.crop_cancel_action = crop_cancel_action
        crop_menu.addAction(crop_cancel_action)
    
    def create_toolbar(self):
        """Toolbar oluştur"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        btn_open = QPushButton("📂 Aç")
        btn_open.clicked.connect(self.open_image)
        toolbar.addWidget(btn_open)
        
        btn_save = QPushButton("💾 Kaydet")
        btn_save.clicked.connect(self.save_image)
        btn_save.setEnabled(False)
        self.btn_save = btn_save
        toolbar.addWidget(btn_save)
        
        toolbar.addSeparator()
        
        btn_crop = QPushButton("✂️ Kırp")
        btn_crop.clicked.connect(self.start_crop)
        btn_crop.setEnabled(False)
        self.btn_crop = btn_crop
        toolbar.addWidget(btn_crop)
    
    def open_image(self):
        """Görüntü aç"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Görüntü Seç", "",
            "Görüntü Dosyaları (*.png *.jpg *.jpeg *.bmp *.gif *.tiff);;Tüm Dosyalar (*.*)"
        )
        
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.current_image = self.original_image.copy()
                self.image_widget.set_image(self.current_image)
                
                width, height = self.original_image.size
                self.width_spin.blockSignals(True)
                self.height_spin.blockSignals(True)
                self.width_spin.setValue(width)
                self.height_spin.setValue(height)
                self.width_spin.blockSignals(False)
                self.height_spin.blockSignals(False)
                
                # Kontrolleri etkinleştir
                self.save_action.setEnabled(True)
                self.reset_action.setEnabled(True)
                self.btn_save.setEnabled(True)
                self.rotate_left_action.setEnabled(True)
                self.rotate_right_action.setEnabled(True)
                self.flip_h_action.setEnabled(True)
                self.flip_v_action.setEnabled(True)
                self.brightness_action.setEnabled(True)
                self.contrast_action.setEnabled(True)
                self.blur_action.setEnabled(True)
                self.sharpen_action.setEnabled(True)
                self.crop_start_action.setEnabled(True)
                self.btn_crop.setEnabled(True)
                
                self.statusBar().showMessage(f"Görüntü açıldı: {width}×{height} px")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Görüntü açılamadı: {str(e)}")
    
    def save_image(self):
        """Görüntü kaydet"""
        if not self.current_image:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Kaydet", "",
            "PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp);;TIFF (*.tiff)"
        )
        
        if file_path:
            try:
                self.current_image.save(file_path)
                QMessageBox.information(self, "Başarılı", "Görüntü kaydedildi!")
                self.statusBar().showMessage(f"Kaydedildi: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Kaydedilemedi: {str(e)}")
    
    def reset_image(self):
        """Orijinal haline döndür"""
        if not self.original_image:
            return
        
        self.current_image = self.original_image.copy()
        self.image_widget.set_image(self.current_image)
        self.image_widget.crop_mode = False
        self.image_widget.crop_rect = QRect()
        self.image_widget.update()
        
        width, height = self.original_image.size
        self.width_spin.blockSignals(True)
        self.height_spin.blockSignals(True)
        self.width_spin.setValue(width)
        self.height_spin.setValue(height)
        self.width_spin.blockSignals(False)
        self.height_spin.blockSignals(False)
        
        self.crop_start_action.setEnabled(True)
        self.crop_apply_action.setEnabled(False)
        self.crop_cancel_action.setEnabled(False)
        self.btn_crop.setText("✂️ Kırp")
        
        self.statusBar().showMessage("Orijinal haline döndürüldü")
    
    def on_size_changed(self):
        """Boyut değiştiğinde dinamik olarak uygula"""
        if not self.current_image:
            return
        
        width = self.width_spin.value()
        height = self.height_spin.value()
        
        # Orijinal boyutlardan başlayarak tüm değişiklikleri uygula
        self.current_image = self.original_image.copy()
        self.current_image = self.current_image.resize((width, height), Image.Resampling.LANCZOS)
        self.image_widget.set_image(self.current_image)
        self.statusBar().showMessage(f"Boyut: {width}×{height} px")
    
    def rotate_image(self, angle):
        """Görüntüyü döndür"""
        if not self.current_image:
            return
        
        self.current_image = self.current_image.rotate(angle, expand=True)
        self.image_widget.set_image(self.current_image)
        
        width, height = self.current_image.size
        self.width_spin.blockSignals(True)
        self.height_spin.blockSignals(True)
        self.width_spin.setValue(width)
        self.height_spin.setValue(height)
        self.width_spin.blockSignals(False)
        self.height_spin.blockSignals(False)
        
        self.statusBar().showMessage(f"{abs(angle)}° döndürüldü")
    
    def flip_image(self, horizontal, vertical):
        """Görüntüyü çevir"""
        if not self.current_image:
            return
        
        if horizontal:
            self.current_image = self.current_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        if vertical:
            self.current_image = self.current_image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        
        self.image_widget.set_image(self.current_image)
        self.statusBar().showMessage("Görüntü çevrildi")
    
    def show_brightness_dialog(self):
        """Parlaklık ayarlama dialogu"""
        from PyQt5.QtWidgets import QDialog, QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Parlaklık Ayarla")
        dialog.setStyleSheet(self.styleSheet())
        layout = QVBoxLayout(dialog)
        
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 200)
        slider.setValue(100)
        layout.addWidget(QLabel("Parlaklık (0-200):"))
        layout.addWidget(slider)
        
        value_label = QLabel("100")
        layout.addWidget(value_label)
        
        def on_value_changed(v):
            value_label.setText(str(v))
            if self.current_image:
                temp = self.original_image.copy()
                enhancer = ImageEnhance.Brightness(temp)
                temp = enhancer.enhance(v / 100.0)
                self.image_widget.set_image(temp)
        
        slider.valueChanged.connect(on_value_changed)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            enhancer = ImageEnhance.Brightness(self.current_image)
            self.current_image = enhancer.enhance(slider.value() / 100.0)
            self.image_widget.set_image(self.current_image)
            self.statusBar().showMessage("Parlaklık ayarlandı")
        else:
            # İptal edilirse geri yükle
            self.image_widget.set_image(self.current_image)
    
    def show_contrast_dialog(self):
        """Kontrast ayarlama dialogu"""
        from PyQt5.QtWidgets import QDialog, QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Kontrast Ayarla")
        dialog.setStyleSheet(self.styleSheet())
        layout = QVBoxLayout(dialog)
        
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 200)
        slider.setValue(100)
        layout.addWidget(QLabel("Kontrast (0-200):"))
        layout.addWidget(slider)
        
        value_label = QLabel("100")
        layout.addWidget(value_label)
        
        def on_value_changed(v):
            value_label.setText(str(v))
            if self.current_image:
                temp = self.original_image.copy()
                enhancer = ImageEnhance.Contrast(temp)
                temp = enhancer.enhance(v / 100.0)
                self.image_widget.set_image(temp)
        
        slider.valueChanged.connect(on_value_changed)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            enhancer = ImageEnhance.Contrast(self.current_image)
            self.current_image = enhancer.enhance(slider.value() / 100.0)
            self.image_widget.set_image(self.current_image)
            self.statusBar().showMessage("Kontrast ayarlandı")
        else:
            self.image_widget.set_image(self.current_image)
    
    def apply_filter(self, filter_type):
        """Filtre uygula"""
        if not self.current_image:
            return
        
        self.current_image = self.current_image.filter(filter_type)
        self.image_widget.set_image(self.current_image)
        self.statusBar().showMessage("Filtre uygulandı")
    
    def start_crop(self):
        """Kırpmayı başlat"""
        if not self.current_image:
            return
        
        self.image_widget.crop_mode = True
        self.crop_start_action.setEnabled(False)
        self.crop_apply_action.setEnabled(True)
        self.crop_cancel_action.setEnabled(True)
        self.btn_crop.setText("❌ İptal")
        self.statusBar().showMessage("Kırpma modu aktif - Kenarlardan sürükleyin")
    
    def apply_crop(self):
        """Kırpmayı uygula"""
        coords = self.image_widget.get_crop_coords()
        if not coords:
            QMessageBox.warning(self, "Uyarı", "Geçerli bir kırpma alanı seçin!")
            return
        
        x1, y1, x2, y2 = coords
        self.current_image = self.current_image.crop((x1, y1, x2, y2))
        self.image_widget.set_image(self.current_image)
        
        width, height = self.current_image.size
        self.width_spin.blockSignals(True)
        self.height_spin.blockSignals(True)
        self.width_spin.setValue(width)
        self.height_spin.setValue(height)
        self.width_spin.blockSignals(False)
        self.height_spin.blockSignals(False)
        
        self.cancel_crop()
        self.statusBar().showMessage(f"Kırpıldı: {width}×{height} px")
    
    def cancel_crop(self):
        """Kırpmayı iptal et"""
        self.image_widget.crop_mode = False
        self.image_widget.crop_rect = QRect()
        self.image_widget.update()
        self.crop_start_action.setEnabled(True)
        self.crop_apply_action.setEnabled(False)
        self.crop_cancel_action.setEnabled(False)
        self.btn_crop.setText("✂️ Kırp")
        self.statusBar().showMessage("Kırpma iptal edildi")


def main():
    app = QApplication(sys.argv)
    window = ImageResizer()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
