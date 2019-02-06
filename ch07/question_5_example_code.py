from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtMultimedia as qtmm
from PyQt5 import QtMultimediaWidgets as qtmmw


class MainWindow(qtw.QWidget):

    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())

        # camera
        self.camera = qtmm.QCamera()

        # viewfinder
        cvf = qtmmw.QCameraViewfinder()
        self.camera.setViewfinder(cvf)
        self.layout().addWidget(cvf)

        # Form
        form = qtw.QFormLayout()
        self.layout().addLayout(form)

        # zoom
        zoomslider = qtw.QSlider(
            minimum=1,
            maximum=10,
            sliderMoved=self.on_slider_moved,
            orientation=qtc.Qt.Horizontal
        )
        form.addRow('Zoom', zoomslider)

        self.camera.start()
        self.show()

    def on_slider_moved(self, value):

        focus = self.camera.focus()
        focus.zoomTo(1, value)


if __name__ == '__main__':
    app = qtw.QApplication([])
    mw = MainWindow()
    app.exec()
