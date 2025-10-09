import sys
from PyQt5  import QtWidgets
"""
def window():
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QApplication 
    window= QtWidgets.QWidget() # Create an instance of QWidget
    window.setWindowTitle("My First GUI") # Set the title of the window
    window.setGeometry(100,100,500,300) # Set the position and size of the window (x_pos, y_pos, width, height)
    window.show() # Display the window
    sys.exit(app.exec_()) # Start the application's event loop

window()

"""

def create_a_window():
    app =QtWidgets.QApplication(sys.argv) #uygulama ornegi olustur
    window= QtWidgets.QWidget() #pencere ornegi olustur
    window.setWindowTitle("İlk GUI projem") #pencere basligini ayarla
    window.setGeometry(250,250,400,400) #pencerenin konumunu ve boyutunu ayarla (x_pos, y_pos, width, height)
    window.show() #pencereyi goster
    sys.exit(app.exec_()) #uygulamanin olay dongusunu baslat

   
create_a_window()
