from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
import sys


class MainWindow(qtw.QMainWindow):

    def __init__(self):
        super().__init__()

        # Your code goes here
        self.resize(800, 600)
        main = qtw.QWidget()
        self.setCentralWidget(main)
        main.setLayout(qtw.QVBoxLayout())
        oglw = GlWidget()
        main.layout().addWidget(oglw)

        # Animation controls
        btn_layout = qtw.QHBoxLayout()
        main.layout().addLayout(btn_layout)
        for direction in ('none', 'left', 'right', 'up', 'down'):
            button = qtw.QPushButton(
                direction,
                autoExclusive=True,
                checkable=True,
                clicked=getattr(oglw, f'spin_{direction}')
                )
            btn_layout.addWidget(button)
        zoom_layout = qtw.QHBoxLayout()
        main.layout().addLayout(zoom_layout)
        zoom_in = qtw.QPushButton('zoom in', clicked=oglw.zoom_in)
        zoom_layout.addWidget(zoom_in)
        zoom_out = qtw.QPushButton('zoom out', clicked=oglw.zoom_out)
        zoom_layout.addWidget(zoom_out)
        self.show()


class GlWidget(qtw.QOpenGLWidget):
    """A widget to display our OpenGL drawing"""

    def initializeGL(self):
        super().initializeGL()

        # Fetch version-specific functions
        gl_context = self.context()
        version = qtg.QOpenGLVersionProfile()
        version.setVersion(2, 1)
        self.gl = gl_context.versionFunctions(version)

        # Configure
        self.gl.glEnable(self.gl.GL_DEPTH_TEST)
        self.gl.glDepthFunc(self.gl.GL_LESS)
        self.gl.glEnable(self.gl.GL_CULL_FACE)

        # Create the program
        self.program = qtg.QOpenGLShaderProgram()
        self.program.addShaderFromSourceFile(
            qtg.QOpenGLShader.Vertex, 'vertex_shader.glsl')
        self.program.addShaderFromSourceFile(
            qtg.QOpenGLShader.Fragment, 'fragment_shader.glsl')
        self.program.link()

        # Get variable locations
        self.vertex_location = self.program.attributeLocation('vertex')
        self.matrix_location = self.program.uniformLocation('matrix')
        self.color_location = self.program.attributeLocation('color_attr')

        # Create transformation matrix
        self.view_matrix = qtg.QMatrix4x4()
        self.view_matrix.perspective(
            45,  # Angle
            self.width() / self.height(),  # Aspect Ratio
            0.1,  # Near clipping plane
            100.0  # Far clipping plane
        )
        self.view_matrix.translate(0, 0, -5)
        self.rotation = [0, 0, 0, 0]

    def paintGL(self):
        # Fill the window with dark violet
        self.gl.glClearColor(0.1, 0, 0.2, 1)
        self.gl.glClear(
            self.gl.GL_COLOR_BUFFER_BIT | self.gl.GL_DEPTH_BUFFER_BIT)
        self.program.bind()

        # Drawing
        front_vertices = [
            qtg.QVector3D(0.0, 1.0, 0.0),  # Peak
            qtg.QVector3D(-1.0, 0.0, 0.0),  # Bottom left
            qtg.QVector3D(1.0, 0.0, 0.0)  # Bottom right
            ]

        face_colors = (
            qtg.QColor('red'),
            qtg.QColor('orange'),
            qtg.QColor('yellow'),
        )
        gl_colors = [
            self.qcolor_to_glvec(color)
            for color in face_colors
        ]
        self.program.setUniformValue(
            self.matrix_location, self.view_matrix)
        self.program.enableAttributeArray(self.vertex_location)
        self.program.setAttributeArray(self.vertex_location, front_vertices)
        self.program.enableAttributeArray(self.color_location)
        self.program.setAttributeArray(self.color_location, gl_colors)

        # Draw the front
        self.gl.glDrawArrays(self.gl.GL_TRIANGLES, 0, 3)
        # Draw the back
        back_vertices = [
            qtg.QVector3D(x.toVector2D(), -0.5)
            for x in front_vertices]
        self.program.setAttributeArray(
            self.vertex_location, reversed(back_vertices))
            # If you try the line below instead, the back side
            # will not show unless you disable face culling
            #self.vertex_location, back_vertices)
        self.gl.glDrawArrays(self.gl.GL_TRIANGLES, 0, 3)

        # draw the sides
        sides = [(0, 1), (1, 2), (2, 0)]
        side_vertices = list()
        for index1, index2 in sides:
            side_vertices += [
                front_vertices[index1],
                back_vertices[index1],
                back_vertices[index2],
                front_vertices[index2]
            ]
        side_colors = [
            qtg.QColor('blue'),
            qtg.QColor('purple'),
            qtg.QColor('cyan'),
            qtg.QColor('magenta'),
        ]
        gl_colors = [
            self.qcolor_to_glvec(color)
            for color in side_colors
        ] * 3

        self.program.setAttributeArray(self.color_location, gl_colors)
        self.program.setAttributeArray(self.vertex_location, side_vertices)
        self.gl.glDrawArrays(self.gl.GL_QUADS, 0, len(side_vertices))
        self.program.disableAttributeArray(self.vertex_location)
        self.program.disableAttributeArray(self.color_location)
        self.program.release()

        # Animation
        # rotate
        self.view_matrix.rotate(*self.rotation)
        self.update()

    def qcolor_to_glvec(self, qcolor):
        return qtg.QVector3D(
            qcolor.red() / 255,
            qcolor.green() / 255,
            qcolor.blue() / 255
        )

    def spin_none(self):
        self.rotation = [0, 0, 0, 0]

    def spin_left(self):
        self.rotation = [-1, 0, 1, 0]

    def spin_right(self):
        self.rotation = [1, 0, 1, 0]

    def spin_up(self):
        self.rotation = [1, 1, 0, 0]

    def spin_down(self):
        self.rotation = [-1, 1, 0, 0]

    def zoom_in(self):
        self.view_matrix.scale(1.1, 1.1, 1.1)

    def zoom_out(self):
        self.view_matrix.scale(.9, .9, .9)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    app.exec_()
