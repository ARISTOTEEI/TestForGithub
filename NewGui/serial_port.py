import sys
import glob
import serial

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction,QContextMenuEvent
from PySide6.QtWidgets import *
from ui_mainwindow import Ui_MainWindow

speeds = ['1200','2400', '4800', '9600', '19200', '38400', '57600', '115200']

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    print(sys.platform)
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            print(s.is_open)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    print(1)
    print(result)
    return result

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.realport = ...
        self.ui.setupUi(self)
        self.ui.Port.addItems(serial_ports())
        self.ui.Speed.addItems(speeds)
        self.ui.start.clicked.connect(self.connect)
        self.ui.send.clicked.connect(self.send)

    def connect(self):
        try:
            self.realport = serial.Serial(self.ui.Port.currentText(),int(self.ui.Speed.currentText()))
            self.ui.status.setText("Статус: Подключено")
        except Exception as e:
            print(e)

    def send(self):
        if self.realport:
            message = self.ui.message.text()
            self.realport.write(message) if message.isalpha() else None 

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())