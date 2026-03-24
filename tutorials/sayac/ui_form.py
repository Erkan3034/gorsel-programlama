# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelSayac = QLabel(Widget)
        self.labelSayac.setObjectName(u"labelSayac")
        self.labelSayac.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(48)
        font.setBold(True)
        self.labelSayac.setFont(font)

        self.verticalLayout.addWidget(self.labelSayac)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.buttonArtir = QPushButton(Widget)
        self.buttonArtir.setObjectName(u"buttonArtir")

        self.horizontalLayout.addWidget(self.buttonArtir)

        self.butonAzalt = QPushButton(Widget)
        self.butonAzalt.setObjectName(u"butonAzalt")

        self.horizontalLayout.addWidget(self.butonAzalt)

        self.butonSifirla = QPushButton(Widget)
        self.butonSifirla.setObjectName(u"butonSifirla")

        self.horizontalLayout.addWidget(self.butonSifirla)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Saya\u00e7 Uygulamas\u0131", None))
        self.labelSayac.setText(QCoreApplication.translate("Widget", u"0", None))
        self.buttonArtir.setText(QCoreApplication.translate("Widget", u"Art\u0131r", None))
        self.butonAzalt.setText(QCoreApplication.translate("Widget", u"Azalt", None))
        self.butonSifirla.setText(QCoreApplication.translate("Widget", u"S\u0131f\u0131rla", None))
    # retranslateUi
