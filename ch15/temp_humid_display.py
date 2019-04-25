import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import Adafruit_DHT
from RPi import GPIO

SENSOR_MODEL = 11
GPIO.setmode(GPIO.BCM)


class HWButton(qtc.QObject):

    button_press = qtc.pyqtSignal()

    def __init__(self, pin):
        super().__init__()
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.pin = pin
        self.pressed = GPIO.input(self.pin) == GPIO.LOW
        # Using a timer to Poll
        #self.timer = qtc.QTimer(interval=50, timeout=self.check)
        #self.timer.start()

        # Using a threaded event handler
        GPIO.add_event_detect(
            self.pin,
            GPIO.RISING,
            callback=self.on_event_detect)

    def on_event_detect(self, *args):
        self.button_press.emit()

    def check(self):
        pressed = GPIO.input(self.pin) == GPIO.LOW
        if pressed != self.pressed:
            if pressed:
                self.button_press.emit()
            self.pressed = pressed


class SensorInterface(qtc.QObject):

    temperature = qtc.pyqtSignal(float)
    humidity = qtc.pyqtSignal(float)
    read_time = qtc.pyqtSignal(qtc.QTime)

    def __init__(self, pin, sensor_model, fahrenheit=False):
        super().__init__()
        self.pin = pin
        self.model = sensor_model
        self.fahrenheit = fahrenheit

    @qtc.pyqtSlot()
    def take_reading(self):
        h, t = Adafruit_DHT.read_retry(self.model, self.pin)
        if self.fahrenheit:
            t = ((9/5) * t) + 32
        self.temperature.emit(t)
        self.humidity.emit(h)
        self.read_time.emit(qtc.QTime.currentTime())


class MainWindow(qtw.QMainWindow):

    def __init__(self):
        super().__init__()

        # Create widget and style it
        widget = qtw.QWidget()
        widget.setLayout(qtw.QFormLayout())
        self.setCentralWidget(widget)
        p = widget.palette()
        p.setColor(qtg.QPalette.WindowText, qtg.QColor('cyan'))
        p.setColor(qtg.QPalette.Window, qtg.QColor('navy'))
        p.setColor(qtg.QPalette.Button, qtg.QColor('#335'))
        p.setColor(qtg.QPalette.ButtonText, qtg.QColor('cyan'))
        self.setPalette(p)

        # Create readouts for temperature and humidity
        tempview = qtw.QLCDNumber()
        humview = qtw.QLCDNumber()
        tempview.setSegmentStyle(qtw.QLCDNumber.Flat)
        humview.setSegmentStyle(qtw.QLCDNumber.Flat)
        widget.layout().addRow('Temperature', tempview)
        widget.layout().addRow('Humidity', humview)

        # Create sensor in its own thread
        self.sensor = SensorInterface(4, SENSOR_MODEL, True)
        self.sensor_thread = qtc.QThread()
        self.sensor.moveToThread(self.sensor_thread)
        self.sensor_thread.start()

        # Connect sensor output
        self.sensor.temperature.connect(tempview.display)
        self.sensor.humidity.connect(humview.display)
        self.sensor.read_time.connect(self.show_time)

        # Connect sensor controls
        self.timer = qtc.QTimer(interval=(60000))
        self.timer.timeout.connect(self.sensor.take_reading)
        self.timer.start()

        # Add a Qt button for reading the values
        readbutton = qtw.QPushButton('Read Now')
        widget.layout().addRow(readbutton)
        readbutton.clicked.connect(self.sensor.take_reading)

        # Add hardware button
        self.hwbutton = HWButton(18)
        self.hwbutton.button_press.connect(self.sensor.take_reading)

        self.show()

    def show_time(self, qtime):
        self.statusBar().showMessage(
            f'Read at {qtime.toString("HH:mm:ss")}'
            )


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    app.exec()
