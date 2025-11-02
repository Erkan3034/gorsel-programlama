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
        
        # Şekil çizme modu
        self.draw_mode = None  # None, 'rectangle', 'circle', 'line', 'free'
        self.shapes = []  # Çizilen şekiller
        self.draw_start = QPoint()
        self.draw_current = QPoint()
        self.draw_pen = QPen(QColor(255, 0, 0), 3)  # Kırmızı, kalınlık 3
        self.is_drawing = False
        
        # Dinamik boyut gösterimi
        self.show_dimensions = True
        
        self.setMinimumSize(600, 400)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: #2b2b2b; border: 2px solid #404040;")
        self.setMouseTracking(True)
    
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
            
            # Şekilleri çiz
            for shape in self.shapes:
                shape_type, points, pen = shape
                painter.setPen(pen)
                
                if shape_type == 'rectangle' and len(points) == 2:
                    rect = QRect(points[0], points[1]).normalized()
                    painter.drawRect(rect)
                elif shape_type == 'circle' and len(points) == 2:
                    rect = QRect(points[0], points[1]).normalized()
                    painter.drawEllipse(rect)
                elif shape_type == 'line' and len(points) == 2:
                    painter.drawLine(points[0], points[1])
                elif shape_type == 'free' and len(points) > 1:
                    for i in range(len(points) - 1):
                        painter.drawLine(points[i], points[i + 1])
            
            # Şu an çizilen şekli göster
            if self.is_drawing and self.draw_mode:
                painter.setPen(self.draw_pen)
                if self.draw_mode == 'rectangle':
                    rect = QRect(self.draw_start, self.draw_current).normalized()
                    painter.drawRect(rect)
                elif self.draw_mode == 'circle':
                    rect = QRect(self.draw_start, self.draw_current).normalized()
                    painter.drawEllipse(rect)
                elif self.draw_mode == 'line':
                    painter.drawLine(self.draw_start, self.draw_current)
            
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
        if not self.pil_image:
            return
        
        pos = event.pos()
        
        # Şekil çizme modu
        if self.draw_mode and self.image_rect.contains(pos):
            self.draw_start = pos
            self.draw_current = pos
            self.is_drawing = True
            if self.draw_mode == 'free':
                self.shapes.append(('free', [pos], QPen(self.draw_pen.color(), self.draw_pen.width())))
            self.update()
            return
        
        # Kırpma modu
        if not self.crop_mode:
            return
        
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
        pos = event.pos()
        
        # Şekil çizme modu
        if self.is_drawing and self.draw_mode:
            self.draw_current = pos
            if self.draw_mode == 'free' and self.shapes:
                # Serbest çizime nokta ekle
                self.shapes[-1][1].append(pos)
            self.update()
            return
        
        # Kırpma modu
        if not self.crop_mode or not self.dragging:
            return
        
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
        # Şekil çizme modu
        if self.is_drawing and self.draw_mode:
            if self.draw_mode in ['rectangle', 'circle', 'line']:
                # Şekli kaydet
                if self.image_rect.contains(self.draw_start) and self.image_rect.contains(self.draw_current):
                    self.shapes.append((self.draw_mode, [self.draw_start, self.draw_current], 
                                      QPen(self.draw_pen.color(), self.draw_pen.width())))
                    # Görüntüyü güncelle
                    self.update_image_with_shapes()
            self.is_drawing = False
            self.update()
            return
        
        self.dragging = False
        self.drag_handle = None
    
    def update_image_with_shapes(self):
        """Şekilleri görüntüye çiz"""
        if not self.pil_image or not self.shapes:
            return
        
        # PIL Image'ı QImage'a dönüştür
        from PyQt5.QtGui import QImage
        q_image = self.pil_to_qimage(self.pil_image)
        painter = QPainter(q_image)
        
        # Şekilleri çiz
        for shape in self.shapes:
            shape_type, points, pen = shape
            painter.setPen(pen)
            
            if shape_type == 'rectangle' and len(points) == 2:
                rect = QRect(points[0], points[1]).normalized()
                # Widget koordinatlarını görüntü koordinatlarına dönüştür
                x1 = int((rect.left() - self.image_rect.left()) / self.scale_factor)
                y1 = int((rect.top() - self.image_rect.top()) / self.scale_factor)
                x2 = int((rect.right() - self.image_rect.left()) / self.scale_factor)
                y2 = int((rect.bottom() - self.image_rect.top()) / self.scale_factor)
                painter.drawRect(QRect(x1, y1, x2 - x1, y2 - y1))
            elif shape_type == 'circle' and len(points) == 2:
                rect = QRect(points[0], points[1]).normalized()
                x1 = int((rect.left() - self.image_rect.left()) / self.scale_factor)
                y1 = int((rect.top() - self.image_rect.top()) / self.scale_factor)
                x2 = int((rect.right() - self.image_rect.left()) / self.scale_factor)
                y2 = int((rect.bottom() - self.image_rect.top()) / self.scale_factor)
                painter.drawEllipse(QRect(x1, y1, x2 - x1, y2 - y1))
            elif shape_type == 'line' and len(points) == 2:
                x1 = int((points[0].x() - self.image_rect.left()) / self.scale_factor)
                y1 = int((points[0].y() - self.image_rect.top()) / self.scale_factor)
                x2 = int((points[1].x() - self.image_rect.left()) / self.scale_factor)
                y2 = int((points[1].y() - self.image_rect.top()) / self.scale_factor)
                painter.drawLine(x1, y1, x2, y2)
            elif shape_type == 'free' and len(points) > 1:
                for i in range(len(points) - 1):
                    x1 = int((points[i].x() - self.image_rect.left()) / self.scale_factor)
                    y1 = int((points[i].y() - self.image_rect.top()) / self.scale_factor)
                    x2 = int((points[i + 1].x() - self.image_rect.left()) / self.scale_factor)
                    y2 = int((points[i + 1].y() - self.image_rect.top()) / self.scale_factor)
                    painter.drawLine(x1, y1, x2, y2)
        
        painter.end()
        
        # QImage'ı PIL Image'a dönüştür
        buffer = q_image.bits().asstring(q_image.byteCount())
        self.pil_image = Image.frombytes("RGB", (q_image.width(), q_image.height()), buffer)
        self.update_display()
        
        # Parent'a şekil eklendiğini bildir
        parent = self.parent()
        while parent and not hasattr(parent, 'on_shape_added'):
            parent = parent.parent()
        if parent:
            parent.on_shape_added(self.pil_image)
    
    def resizeEvent(self, event):
        """Widget boyutu değiştiğinde"""
        super().resizeEvent(event)
        self.update_display()


class ImageResizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.original_image = None
        self.current_image = None
        
        # Undo/Redo için geçmiş
        self.history = []  # Geçmiş görüntüler
        self.history_index = -1  # Mevcut pozisyon
        self.max_history = 20  # Maksimum geçmiş sayısı
        
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
        
        undo_action = QAction("Geri Al", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.undo)
        undo_action.setEnabled(False)
        self.undo_action = undo_action
        file_menu.addAction(undo_action)
        
        redo_action = QAction("İleri Al", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.redo)
        redo_action.setEnabled(False)
        self.redo_action = redo_action
        file_menu.addAction(redo_action)
        
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
        
        # Şekil Çizme menüsü
        draw_menu = menubar.addMenu("Şekil Çizme")
        
        rect_action = QAction("Dikdörtgen", self)
        rect_action.triggered.connect(lambda: self.set_draw_mode('rectangle'))
        rect_action.setEnabled(False)
        self.rect_menu_action = rect_action
        draw_menu.addAction(rect_action)
        
        circle_action = QAction("Daire", self)
        circle_action.triggered.connect(lambda: self.set_draw_mode('circle'))
        circle_action.setEnabled(False)
        self.circle_menu_action = circle_action
        draw_menu.addAction(circle_action)
        
        line_action = QAction("Çizgi", self)
        line_action.triggered.connect(lambda: self.set_draw_mode('line'))
        line_action.setEnabled(False)
        self.line_menu_action = line_action
        draw_menu.addAction(line_action)
        
        free_action = QAction("Serbest Çizim", self)
        free_action.triggered.connect(lambda: self.set_draw_mode('free'))
        free_action.setEnabled(False)
        self.free_menu_action = free_action
        draw_menu.addAction(free_action)
        
        draw_menu.addSeparator()
        
        clear_shapes_action = QAction("Tüm Şekilleri Sil", self)
        clear_shapes_action.triggered.connect(self.clear_shapes)
        clear_shapes_action.setEnabled(False)
        self.clear_shapes_action = clear_shapes_action
        draw_menu.addAction(clear_shapes_action)
        
        draw_off_action = QAction("Çizimi Kapat", self)
        draw_off_action.triggered.connect(lambda: self.set_draw_mode(None))
        draw_off_action.setEnabled(False)
        self.draw_off_action = draw_off_action
        draw_menu.addAction(draw_off_action)
    
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
        
        # Geri alma / İleri alma butonları (küçük)
        self.btn_undo = QPushButton("◀")
        self.btn_undo.setMaximumWidth(30)
        self.btn_undo.setToolTip("Geri Al (Ctrl+Z)")
        self.btn_undo.clicked.connect(self.undo)
        self.btn_undo.setEnabled(False)
        toolbar.addWidget(self.btn_undo)
        
        self.btn_redo = QPushButton("▶")
        self.btn_redo.setMaximumWidth(30)
        self.btn_redo.setToolTip("İleri Al (Ctrl+Y)")
        self.btn_redo.clicked.connect(self.redo)
        self.btn_redo.setEnabled(False)
        toolbar.addWidget(self.btn_redo)
        
        toolbar.addSeparator()
        
        btn_crop = QPushButton("✂️ Kırp")
        btn_crop.clicked.connect(self.start_crop)
        btn_crop.setEnabled(False)
        self.btn_crop = btn_crop
        toolbar.addWidget(btn_crop)
        
        # Şekil çizme butonları
        toolbar.addSeparator()
        toolbar.addWidget(QLabel("Şekil:"))
        
        btn_rect = QPushButton("▭")
        btn_rect.setMaximumWidth(30)
        btn_rect.setToolTip("Dikdörtgen")
        btn_rect.clicked.connect(lambda: self.set_draw_mode('rectangle'))
        btn_rect.setEnabled(False)
        self.btn_rect = btn_rect
        toolbar.addWidget(btn_rect)
        
        btn_circle = QPushButton("○")
        btn_circle.setMaximumWidth(30)
        btn_circle.setToolTip("Daire")
        btn_circle.clicked.connect(lambda: self.set_draw_mode('circle'))
        btn_circle.setEnabled(False)
        self.btn_circle = btn_circle
        toolbar.addWidget(btn_circle)
        
        btn_line = QPushButton("╱")
        btn_line.setMaximumWidth(30)
        btn_line.setToolTip("Çizgi")
        btn_line.clicked.connect(lambda: self.set_draw_mode('line'))
        btn_line.setEnabled(False)
        self.btn_line = btn_line
        toolbar.addWidget(btn_line)
        
        btn_free = QPushButton("✎")
        btn_free.setMaximumWidth(30)
        btn_free.setToolTip("Serbest Çizim")
        btn_free.clicked.connect(lambda: self.set_draw_mode('free'))
        btn_free.setEnabled(False)
        self.btn_free = btn_free
        toolbar.addWidget(btn_free)
        
        btn_clear_shapes = QPushButton("🗑 Şekilleri Sil")
        btn_clear_shapes.clicked.connect(self.clear_shapes)
        btn_clear_shapes.setEnabled(False)
        self.btn_clear_shapes = btn_clear_shapes
        toolbar.addWidget(btn_clear_shapes)
        
        btn_draw_off = QPushButton("✖ Çizimi Kapat")
        btn_draw_off.clicked.connect(lambda: self.set_draw_mode(None))
        btn_draw_off.setEnabled(False)
        self.btn_draw_off = btn_draw_off
        toolbar.addWidget(btn_draw_off)
    
    def add_to_history(self, image):
        """Geçmişe ekle"""
        # Mevcut pozisyondan sonrasını sil (yeni bir yol açıldığında)
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        
        # Görüntüyü kopyala ve ekle
        self.history.append(image.copy())
        self.history_index += 1
        
        # Maksimum geçmiş sayısını kontrol et
        if len(self.history) > self.max_history:
            self.history.pop(0)
            self.history_index -= 1
        
        # Buton durumlarını güncelle
        self.btn_undo.setEnabled(self.history_index > 0)
        self.btn_redo.setEnabled(self.history_index < len(self.history) - 1)
        self.undo_action.setEnabled(self.history_index > 0)
        self.redo_action.setEnabled(self.history_index < len(self.history) - 1)
    
    def undo(self):
        """Geri al"""
        if self.history_index > 0:
            self.history_index -= 1
            self.current_image = self.history[self.history_index].copy()
            self.image_widget.set_image(self.current_image)
            
            width, height = self.current_image.size
            self.width_spin.blockSignals(True)
            self.height_spin.blockSignals(True)
            self.width_spin.setValue(width)
            self.height_spin.setValue(height)
            self.width_spin.blockSignals(False)
            self.height_spin.blockSignals(False)
            
            self.btn_undo.setEnabled(self.history_index > 0)
            self.btn_redo.setEnabled(True)
            self.undo_action.setEnabled(self.history_index > 0)
            self.redo_action.setEnabled(True)
            self.statusBar().showMessage("Geri alındı")
    
    def redo(self):
        """İleri al"""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.current_image = self.history[self.history_index].copy()
            self.image_widget.set_image(self.current_image)
            
            width, height = self.current_image.size
            self.width_spin.blockSignals(True)
            self.height_spin.blockSignals(True)
            self.width_spin.setValue(width)
            self.height_spin.setValue(height)
            self.width_spin.blockSignals(False)
            self.height_spin.blockSignals(False)
            
            self.btn_undo.setEnabled(True)
            self.btn_redo.setEnabled(self.history_index < len(self.history) - 1)
            self.undo_action.setEnabled(True)
            self.redo_action.setEnabled(self.history_index < len(self.history) - 1)
            self.statusBar().showMessage("İleri alındı")
    
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
                
                # Geçmişi sıfırla
                self.history = [self.current_image.copy()]
                self.history_index = 0
                
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
                self.btn_rect.setEnabled(True)
                self.btn_circle.setEnabled(True)
                self.btn_line.setEnabled(True)
                self.btn_free.setEnabled(True)
                self.btn_clear_shapes.setEnabled(True)
                self.btn_draw_off.setEnabled(True)
                self.rect_menu_action.setEnabled(True)
                self.circle_menu_action.setEnabled(True)
                self.line_menu_action.setEnabled(True)
                self.free_menu_action.setEnabled(True)
                self.clear_shapes_action.setEnabled(True)
                self.draw_off_action.setEnabled(True)
                
                # Şekilleri temizle
                self.image_widget.shapes = []
                
                self.statusBar().showMessage(f"Görüntü açıldı: {width}×{height} px")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Görüntü açılamadı: {str(e)}")
    
    def on_shape_added(self, image):
        """Şekil eklendiğinde çağrılır"""
        self.current_image = image
        self.add_to_history(image)
    
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
        self.add_to_history(self.current_image)
        self.image_widget.set_image(self.current_image)
        self.statusBar().showMessage(f"Boyut: {width}×{height} px")
    
    def rotate_image(self, angle):
        """Görüntüyü döndür"""
        if not self.current_image:
            return
        
        self.current_image = self.current_image.rotate(angle, expand=True)
        self.add_to_history(self.current_image)
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
        
        self.add_to_history(self.current_image)
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
            self.add_to_history(self.current_image)
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
            self.add_to_history(self.current_image)
            self.image_widget.set_image(self.current_image)
            self.statusBar().showMessage("Kontrast ayarlandı")
        else:
            self.image_widget.set_image(self.current_image)
    
    def apply_filter(self, filter_type):
        """Filtre uygula"""
        if not self.current_image:
            return
        
        self.current_image = self.current_image.filter(filter_type)
        self.add_to_history(self.current_image)
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
        self.add_to_history(self.current_image)
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
    
    def set_draw_mode(self, mode):
        """Şekil çizme modunu ayarla"""
        self.image_widget.draw_mode = mode
        self.image_widget.crop_mode = False
        
        # Buton durumlarını güncelle
        if mode:
            self.btn_rect.setStyleSheet("")
            self.btn_circle.setStyleSheet("")
            self.btn_line.setStyleSheet("")
            self.btn_free.setStyleSheet("")
            if mode == 'rectangle':
                self.btn_rect.setStyleSheet("background-color: #0078d4;")
            elif mode == 'circle':
                self.btn_circle.setStyleSheet("background-color: #0078d4;")
            elif mode == 'line':
                self.btn_line.setStyleSheet("background-color: #0078d4;")
            elif mode == 'free':
                self.btn_free.setStyleSheet("background-color: #0078d4;")
            self.statusBar().showMessage(f"Çizim modu: {mode}")
        else:
            self.btn_rect.setStyleSheet("")
            self.btn_circle.setStyleSheet("")
            self.btn_line.setStyleSheet("")
            self.btn_free.setStyleSheet("")
            self.statusBar().showMessage("Çizim modu kapatıldı")
    
    def clear_shapes(self):
        """Tüm şekilleri sil"""
        if self.image_widget.shapes:
            reply = QMessageBox.question(
                self, "Onay",
                "Tüm şekilleri silmek istediğinize emin misiniz?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.image_widget.shapes = []
                self.image_widget.update()
                self.statusBar().showMessage("Şekiller silindi")
    
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
