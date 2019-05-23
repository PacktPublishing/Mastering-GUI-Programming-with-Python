from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
import sys

app = qtw.QApplication(sys.argv)

widget = qtw.QWidget()
palette = widget.palette()
tile_brush = qtg.QBrush(
    qtg.QColor('black'),
    qtg.QPixmap('tile.png')
)
palette.setBrush(qtg.QPalette.Window, tile_brush)
widget.setPalette(palette)

widget.show()
app.exec()
