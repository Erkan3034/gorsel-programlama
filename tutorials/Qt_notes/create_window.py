import sys
from PyQt5  import QtWidgets

def window():
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QApplication 
    window= QtWidgets.QWidget() # Create an instance of QWidget
    window.setWindowTitle("My First GUI") # Set the title of the window
    window.setGeometry(100,100,500,300) # Set the position and size of the window (x_pos, y_pos, width, height)
    window.show() # Display the window
    sys.exit(app.exec_()) # Start the application's event loop

window()