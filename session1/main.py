# -*- coding: utf-8 -*-

"""La interfaz gráfica para la aplicación"""

# Imports típicos
import os,sys

# Importamos los módulos Qt
from PyQt4 import QtCore,QtGui

# Importamos el módulo generado por pyuic (podríamos cargar 
# directamente el XML)
from windowUi import Ui_MainWindow

# Creamos una clase para nuestra ventana principal
class Main(QtGui.QMainWindow):
    def __init__(self):
        # Si, ya sé que tendría que usar super()
        QtGui.QMainWindow.__init__(self)
        
        # Esto es siempre EXACTAMENTE igual
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

def main():
    # De nuevo, esto es "boilerplate", es igual en todas las aplicaciones
    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.show()
    # Es exec_ porque exec es reservada en python
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()