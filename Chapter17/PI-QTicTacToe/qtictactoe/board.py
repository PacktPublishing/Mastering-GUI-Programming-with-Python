from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from os import path
import sys


class TTTBoard(qtw.QGraphicsScene):

    square_rects = (
        qtc.QRectF(5, 5, 190, 190),
        qtc.QRectF(205, 5, 190, 190),
        qtc.QRectF(405, 5, 190, 190),
        qtc.QRectF(5, 205, 190, 190),
        qtc.QRectF(205, 205, 190, 190),
        qtc.QRectF(405, 205, 190, 190),
        qtc.QRectF(5, 405, 190, 190),
        qtc.QRectF(205, 405, 190, 190),
        qtc.QRectF(405, 405, 190, 190)
    )

    square_clicked = qtc.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setSceneRect(0, 0, 600, 600)
        self.setBackgroundBrush(qtg.QBrush(qtc.Qt.cyan))
        for square in self.square_rects:
            self.addRect(square, brush=qtg.QBrush(qtc.Qt.white))

        if getattr(sys, 'frozen', False):
            directory = sys._MEIPASS
        else:  # Not frozen
            directory = path.dirname(__file__)
        self.mark_pngs = {
            'X': qtg.QPixmap(path.join(directory, 'images', 'X.png')),
            'O': qtg.QPixmap(path.join(directory, 'images', 'O.png'))
        }
        self.marks = []

    def set_board(self, marks):
        for i, square in enumerate(marks):
            if square in self.mark_pngs:
                mark = self.addPixmap(self.mark_pngs[square])
                mark.setPos(self.square_rects[i].topLeft())
                self.marks.append(mark)

    def clear_board(self):
        for mark in self.marks:
            self.removeItem(mark)

    def mousePressEvent(self, mouse_event):
        """Handle mouse clicks on the board"""
        position = mouse_event.buttonDownScenePos(qtc.Qt.LeftButton)
        for square, qrect in enumerate(self.square_rects):
            if qrect.contains(position):
                self.square_clicked.emit(square)
                break
