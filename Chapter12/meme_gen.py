import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class ColorButton(qtw.QPushButton):

    changed = qtc.pyqtSignal()

    def __init__(self, default_color, changed=None):
        super().__init__()
        self.set_color(qtg.QColor(default_color))
        self.clicked.connect(self.on_click)
        if changed:
            self.changed.connect(changed)

    def set_color(self, color):
        self._color = color
        # update icon
        pixmap = qtg.QPixmap(32, 32)
        pixmap.fill(self._color)
        self.setIcon(qtg.QIcon(pixmap))

    def on_click(self):
        color = qtw.QColorDialog.getColor(self._color)
        if color:
            self.set_color(color)
            self.changed.emit()


class FontButton(qtw.QPushButton):

    changed = qtc.pyqtSignal()

    def __init__(self, default_family, default_size, changed=None):
        super().__init__()
        self.set_font(qtg.QFont(default_family, default_size))
        self.clicked.connect(self.on_click)
        if changed:
            self.changed.connect(changed)

    def set_font(self, font):
        self._font = font
        self.setFont(font)
        self.setText(f'{font.family()} {font.pointSize()}')

    def on_click(self):
        font, accepted = qtw.QFontDialog.getFont(self._font)
        if accepted:
            self.set_font(font)
            self.changed.emit()


class ImageFileButton(qtw.QPushButton):

    changed = qtc.pyqtSignal()

    def __init__(self, changed=None):
        super().__init__("Click to select…")
        self._filename = None
        self.clicked.connect(self.on_click)
        if changed:
            self.changed.connect(changed)

    def on_click(self):
        filename, _ = qtw.QFileDialog.getOpenFileName(
            None, "Select an image to use",
            qtc.QDir.homePath(), "Images (*.png *.xpm *.jpg)")
        if filename:
            self._filename = filename
            # set button text to filename without path
            self.setText(qtc.QFileInfo(filename).fileName())
            self.changed.emit()


class MemeEditForm(qtw.QWidget):

    changed = qtc.pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QFormLayout())

        # Image
        self.image_source = ImageFileButton(changed=self.on_change)
        self.layout().addRow('Image file', self.image_source)

        # Text entries
        self.top_text = qtw.QPlainTextEdit(textChanged=self.on_change)
        self.bottom_text = qtw.QPlainTextEdit(textChanged=self.on_change)
        self.layout().addRow("Top Text", self.top_text)
        self.layout().addRow("Bottom Text", self.bottom_text)

        # Text color and font
        self.text_color = ColorButton('white', changed=self.on_change)
        self.layout().addRow("Text Color", self.text_color)
        self.text_font = FontButton('Impact', 32, changed=self.on_change)
        self.layout().addRow("Text Font", self.text_font)

        # Background Boxes
        self.text_bg_color = ColorButton('black', changed=self.on_change)
        self.layout().addRow('Text Background', self.text_bg_color)
        self.top_bg_height = qtw.QSpinBox(
            minimum=0, maximum=32,
            valueChanged=self.on_change, suffix=' line(s)')
        self.layout().addRow('Top BG height', self.top_bg_height)
        self.bottom_bg_height = qtw.QSpinBox(
            minimum=0, maximum=32,
            valueChanged=self.on_change, suffix=' line(s)')
        self.layout().addRow('Bottom BG height', self.bottom_bg_height)
        self.bg_padding = qtw.QSpinBox(
            minimum=0, maximum=100, value=10,
            valueChanged=self.on_change, suffix=' px')
        self.layout().addRow('BG Padding', self.bg_padding)

    def on_change(self):
        data = {
            'image_source': self.image_source._filename,
            'top_text': self.top_text.toPlainText(),
            'bottom_text': self.bottom_text.toPlainText(),
            'text_color': self.text_color._color,
            'text_font': self.text_font._font,
            'bg_color': self.text_bg_color._color,
            'top_bg_height': self.top_bg_height.value(),
            'bottom_bg_height': self.bottom_bg_height.value(),
            'bg_padding': self.bg_padding.value()
        }
        self.changed.emit(data)


class MainWindow(qtw.QMainWindow):

    def __init__(self):
        """MainWindow constructor.

        This widget will be our main window.
        We'll define all the UI components in here.
        """
        super().__init__()
        # Main UI code goes here
        self.setWindowTitle('Qt Meme Generator')

        # define some constants
        self.max_size = qtc.QSize(800, 600)
        self.image = qtg.QImage(
            self.max_size, qtg.QImage.Format_ARGB32)
        self.image.fill(qtg.QColor('black'))

        # Container widget
        mainwidget = qtw.QWidget()
        self.setCentralWidget(mainwidget)
        mainwidget.setLayout(qtw.QHBoxLayout())

        # Image Previewer
        self.image_display = qtw.QLabel(pixmap=qtg.QPixmap(self.image))
        mainwidget.layout().addWidget(self.image_display)

        # The editing form
        self.form = MemeEditForm()
        mainwidget.layout().addWidget(self.form)
        self.form.changed.connect(self.build_image)

        # Create file saving
        toolbar = self.addToolBar('File')
        toolbar.addAction("Save Image", self.save_image)

        # End main UI code
        self.show()

    def save_image(self):
        save_file, _ = qtw.QFileDialog.getSaveFileName(
            None, "Save your image",
            qtc.QDir.homePath(), "PNG Images (*.png)")
        if save_file:
            self.image.save(save_file, "PNG")

    def build_image(self, data):
        # Create a QImage file
        if not data.get('image_source'):
            self.image.fill(qtg.QColor('black'))
        else:
            self.image.load(data.get('image_source'))
            # Scale down the image if it's over the max_size
            if not (self.max_size - self.image.size()).isValid():
                # isValid returns false if either dimension is negative
                self.image = self.image.scaled(
                    self.max_size, qtc.Qt.KeepAspectRatio)

        # create the painter
        painter = qtg.QPainter(self.image)

        # Paint the background blocks
        font_px = qtg.QFontInfo(data['text_font']).pixelSize()
        top_px = (data['top_bg_height'] * font_px) + data['bg_padding']
        top_block_rect = qtc.QRect(
            0, 0, self.image.width(), top_px)
        bottom_px = (
            self.image.height() - data['bg_padding']
            - (data['bottom_bg_height'] * font_px))
        bottom_block_rect = qtc.QRect(
            0, bottom_px, self.image.width(), self.image.height())

        painter.setBrush(qtg.QBrush(data['bg_color']))
        painter.drawRect(top_block_rect)
        painter.drawRect(bottom_block_rect)

        # Paint the text
        painter.setPen(data['text_color'])
        painter.setFont(data['text_font'])
        flags = qtc.Qt.AlignHCenter | qtc.Qt.TextWordWrap
        painter.drawText(
            self.image.rect(), flags | qtc.Qt.AlignTop, data['top_text'])
        painter.drawText(
            self.image.rect(), flags | qtc.Qt.AlignBottom,
            data['bottom_text'])

        # show the image
        self.image_display.setPixmap(qtg.QPixmap(self.image))


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
