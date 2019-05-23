import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

import resources

class StyleOverrides(qtw.QProxyStyle):

    def drawItemText(
        self, painter, rect,
        flags, palette, enabled,
        text, textRole
    ):
        """Force uppercase in all text"""
        text = text.upper()
        super().drawItemText(
            painter, rect, flags,
            palette, enabled, text,
            textRole
        )

    def drawPrimitive(
        self, element, option, painter, widget
    ):
        """Outline QLineEdits in Green"""
        self.green_pen = qtg.QPen(qtg.QColor('green'))
        self.green_pen.setWidth(4)
        if element == qtw.QStyle.PE_FrameLineEdit:
            painter.setPen(self.green_pen)
            painter.drawRoundedRect(widget.rect(), 10, 10)
        else:
            super().drawPrimitive(element, option, painter, widget)


class ColorButton(qtw.QPushButton):
    """Button with color and backgroundColor properties for animation"""

    def _color(self):
        return self.palette().color(qtg.QPalette.ButtonText)

    def _setColor(self, qcolor):
        palette = self.palette()
        palette.setColor(qtg.QPalette.ButtonText, qcolor)
        self.setPalette(palette)

    color = qtc.pyqtProperty(qtg.QColor, _color, _setColor)

    @qtc.pyqtProperty(qtg.QColor)
    def backgroundColor(self):
        return self.palette().color(qtg.QPalette.Button)

    @backgroundColor.setter
    def backgroundColor(self, qcolor):
        palette = self.palette()
        palette.setColor(qtg.QPalette.Button, qcolor)
        self.setPalette(palette)


class MainWindow(qtw.QMainWindow):

    def __init__(self):
        """MainWindow constructor.

        This widget will be our main window.
        We'll define all the UI components in here.
        """
        super().__init__()
        # Main UI code goes here

        # Basic Form Definition
        self.setWindowTitle('Fight Fighter Game Lobby')
        cx_form = qtw.QWidget()
        self.setCentralWidget(cx_form)
        cx_form.setLayout(qtw.QFormLayout())

        heading = qtw.QLabel("Fight Fighter!")
        cx_form.layout().addRow(heading)

        inputs = {
            'Server': qtw.QLineEdit(),
            'Name': qtw.QLineEdit(),
            'Password': qtw.QLineEdit(
                echoMode=qtw.QLineEdit.Password),
            'Team': qtw.QComboBox(),
            'Ready': qtw.QCheckBox('Check when ready')
        }
        teams = (
            'Crimson Sharks',
            'Shadow Hawks',
            'Night Terrors',
            'Blue Crew'
        )
        inputs['Team'].addItems(teams)

        for label, widget in inputs.items():
            cx_form.layout().addRow(label, widget)
        #self.submit = qtw.QPushButton(
        self.submit = ColorButton(
            'Connect',
            clicked=lambda: qtw.QMessageBox.information(
                None,
                'Connecting',
                'Prepare for Battle!'
            )
        )

        #self.cancel = qtw.QPushButton(
        self.cancel = ColorButton(
            'Cancel',
            clicked=self.close
        )
        cx_form.layout().addRow(self.submit, self.cancel)

        #self.show()
        #return
        #########
        # Fonts #
        #########

        # Configuring Fonts
        heading_font = qtg.QFont('Impact', 32, qtg.QFont.Bold)
        heading_font.setStretch(qtg.QFont.ExtraExpanded)
        heading.setFont(heading_font)

        # Explicit font configuration
        label_font = qtg.QFont()
        label_font.setFamily('Impact')
        label_font.setPointSize(14)
        label_font.setWeight(qtg.QFont.DemiBold)
        label_font.setStyle(qtg.QFont.StyleItalic)

        for inp in inputs.values():
            cx_form.layout().labelForField(inp).setFont(label_font)

        # Locating Alternative fonts

        button_font = qtg.QFont('Totally Nonexistant Font Family XYZ', 15.233)
        print(f'Font is {button_font.family()}')
        actual_font = qtg.QFontInfo(button_font).family()
        print(f'Actual font used is {actual_font}')

        # Set a style hint
        button_font.setStyleHint(qtg.QFont.Fantasy) # Use a "fantasy font"
        button_font.setStyleStrategy(
            qtg.QFont.PreferAntialias |
            qtg.QFont.PreferQuality
        )

        actual_font = qtg.QFontInfo(button_font)
        print(f'Actual font used is {actual_font.family()}'
              f' {actual_font.pointSize()}')

        self.submit.setFont(button_font)
        self.cancel.setFont(button_font)

        #self.show()
        #return
        ####################
        # Images and Icons #
        ####################

        # Display a simple raster image
        logo = qtg.QPixmap('logo.png')
        if logo.width() > 400:
            logo = logo.scaledToWidth(400, qtc.Qt.SmoothTransformation)
        heading.setPixmap(logo)

        # Create images

        go_pixmap = qtg.QPixmap(qtc.QSize(32, 32))
        stop_pixmap = qtg.QPixmap(qtc.QSize(32, 32))
        go_pixmap.fill(qtg.QColor('green'))
        stop_pixmap.fill(qtg.QColor('red'))

        # Creating icons

        connect_icon = qtg.QIcon()
        connect_icon.addPixmap(go_pixmap, qtg.QIcon.Active)
        connect_icon.addPixmap(stop_pixmap, qtg.QIcon.Disabled)
        self.submit.setIcon(connect_icon)
        self.submit.setDisabled(True)
        inputs['Server'].textChanged.connect(
            lambda x: self.submit.setDisabled(x == '')
        )

        # using resources
        # note import of "resources" at top
        inputs['Team'].setItemIcon(
            0, qtg.QIcon(':/teams/crimson_sharks.png'))
        inputs['Team'].setItemIcon(
            1, qtg.QIcon(':/teams/shadow_hawks.png'))
        inputs['Team'].setItemIcon(
            2, qtg.QIcon(':/teams/night_terrors.png'))
        inputs['Team'].setItemIcon(
            3, qtg.QIcon(':/teams/blue_crew.png'))

        # Loading a font from a resource file
        libsans_id = qtg.QFontDatabase.addApplicationFont(':/fonts/LiberationSans-Regular.ttf')
        family = qtg.QFontDatabase.applicationFontFamilies(libsans_id)[0]
        libsans = qtg.QFont(family)
        inputs['Team'].setFont(libsans)

        #self.show()
        #return

        ##########
        # Colors #
        ##########
        app = qtw.QApplication.instance()
        palette = app.palette()
        palette.setColor(
            qtg.QPalette.Button,
            qtg.QColor('#333')
        )
        palette.setColor(
            qtg.QPalette.ButtonText,
            qtg.QColor('#3F3')
        )
        palette.setColor(
            qtg.QPalette.Disabled,
            qtg.QPalette.ButtonText,
            qtg.QColor('#F88')
        )
        palette.setColor(
            qtg.QPalette.Disabled,
            qtg.QPalette.Button,
            qtg.QColor('#888')
        )
        self.submit.setPalette(palette)
        self.cancel.setPalette(palette)

        # Using Brushes
        dotted_brush = qtg.QBrush(qtg.QColor('white'), qtc.Qt.Dense2Pattern)

        gradient = qtg.QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, qtg.QColor('navy'))
        gradient.setColorAt(0.5, qtg.QColor('darkred'))
        gradient.setColorAt(1, qtg.QColor('orange'))
        gradient_brush = qtg.QBrush(gradient)

        window_palette = app.palette()
        window_palette.setBrush(
            qtg.QPalette.Window,
            gradient_brush
        )
        window_palette.setBrush(
            qtg.QPalette.Active,
            qtg.QPalette.WindowText,
            dotted_brush
        )
        self.setPalette(window_palette)

        #self.show()
        #return
        ##################
        # Qt StyleSheets #
        ##################

        stylesheet = """
        QMainWindow {
            background-color: black;
        }
        QWidget {
            background-color: transparent;
            color: #3F3;
        }
        QLineEdit, QComboBox, QCheckBox {
            font-size: 16pt;
        }"""
        #self.setStyleSheet(stylesheet)

        #self.show()
        #return
        # oops, we've lost our controls!
        stylesheet += """
         QPushButton {
             background-color: #333;
         }
         QCheckBox::indicator:unchecked {
             border: 1px solid silver;
             background-color: darkred;
         }
         QCheckBox::indicator:checked {
             border: 1px solid silver;
             background-color: #3F3;
         }
         """

        #self.setStyleSheet(stylesheet)

        # Using discrete classes
        stylesheet += """
        .QWidget {
           background: url(tile.png);
        }
        """

        # Using object names
        self.submit.setObjectName('SubmitButton')
        stylesheet += """
        #SubmitButton:disabled {
            background-color: #888;
            color: darkred;
        }
        """
        #self.setStyleSheet(stylesheet)
        for inp in ('Server', 'Name', 'Password'):
            inp_widget = inputs[inp]
            inp_widget.setStyleSheet('background-color: black')

        #self.show()
        #return
        #############
        # Qt Styles #
        #############

        # See main execution block for style setting call
        # app.setStyle(qtw.QStyleFactory.create('QtCurve'))


        #############
        # Animation #
        #############


        # Simple property animation
        self.heading_animation = qtc.QPropertyAnimation(
            heading, b'maximumSize')
        self.heading_animation.setStartValue(qtc.QSize(10, logo.height()))
        self.heading_animation.setEndValue(qtc.QSize(400, logo.height()))
        self.heading_animation.setDuration(2000)
        #self.heading_animation.start()

        # Parallel animations
        # See ColorButton class
        # you'll have to disable all stylesheets
        self.text_color_animation = qtc.QPropertyAnimation(
            self.submit, b'color')
        self.text_color_animation.setStartValue(qtg.QColor('#FFF'))
        self.text_color_animation.setEndValue(qtg.QColor('#888'))
        self.text_color_animation.setLoopCount(-1)
        self.text_color_animation.setEasingCurve(qtc.QEasingCurve.InOutQuad)
        self.text_color_animation.setDuration(2000)
        #self.text_color_animation.start()

        self.bg_color_animation = qtc.QPropertyAnimation(
            self.submit, b'backgroundColor')
        self.bg_color_animation.setStartValue(qtg.QColor('#000'))
        self.bg_color_animation.setKeyValueAt(0.5, qtg.QColor('darkred'))
        self.bg_color_animation.setEndValue(qtg.QColor('#000'))
        self.bg_color_animation.setLoopCount(-1)
        self.bg_color_animation.setDuration(1500)
        #self.bg_color_animation.start()

        self.button_animations = qtc.QParallelAnimationGroup()
        self.button_animations.addAnimation(self.text_color_animation)
        self.button_animations.addAnimation(self.bg_color_animation)
        #self.button_animations.start()

        self.all_animations = qtc.QSequentialAnimationGroup()
        self.all_animations.addAnimation(self.heading_animation)
        self.all_animations.addAnimation(self.button_animations)
        self.all_animations.start()


        # End main UI code
        self.show()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    windows_style = qtw.QStyleFactory.create('Windows')
    app.setStyle(windows_style)
    proxy_style = StyleOverrides()
    app.setStyle(proxy_style)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
