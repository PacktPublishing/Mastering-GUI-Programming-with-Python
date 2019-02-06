import sys
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtMultimedia as qtmm
from PyQt5 import QtMultimediaWidgets as qtmmw


class MainWindow(qtw.QMainWindow):

    def __init__(self):
        """MainWindow constructor.

        Code in this method should define window properties,
        create backend resources, etc.
        """
        super().__init__()
        # Main framework
        self.resize(qtc.QSize(800, 600))
        base_widget = qtw.QWidget()
        base_widget.setLayout(qtw.QHBoxLayout())
        notebook = qtw.QTabWidget()
        base_widget.layout().addWidget(notebook)
        self.file_list = qtw.QListWidget()
        base_widget.layout().addWidget(self.file_list)

        self.setCentralWidget(base_widget)

        # transport controls
        toolbar = self.addToolBar("Transport")
        record_act = toolbar.addAction('Rec')
        stop_act = toolbar.addAction('Stop')
        play_act = toolbar.addAction('Play')
        pause_act = toolbar.addAction('Pause')

        # define the video directory
        self.video_dir = qtc.QDir.home()
        if not self.video_dir.cd('captains_log'):
            qtc.QDir.home().mkdir('captains_log')
            self.video_dir.cd('captains_log')

        # Read the files in the directory
        self.refresh_video_list()

        ############
        # Playback #
        ############

        # setup the player and video widget
        self.player = qtmm.QMediaPlayer()
        self.video_widget = qtmmw.QVideoWidget()
        self.player.setVideoOutput(self.video_widget)
        notebook.addTab(self.video_widget, "Play")

        # connect the transport
        play_act.triggered.connect(self.player.play)
        pause_act.triggered.connect(self.player.pause)
        stop_act.triggered.connect(self.player.stop)
        play_act.triggered.connect(
            lambda: notebook.setCurrentWidget(self.video_widget))

        # connect file list
        self.file_list.itemDoubleClicked.connect(
            self.on_file_selected)
        self.file_list.itemDoubleClicked.connect(
            lambda: notebook.setCurrentWidget(self.video_widget))



        #############
        # Recording #
        #############

        # set up camera
        self.camera = self.camera_check()
        if not self.camera:
            self.show()
            return
        self.camera.setCaptureMode(qtmm.QCamera.CaptureVideo)

        # Create the viewfinder widget for recording
        self.cvf = qtmmw.QCameraViewfinder()
        self.camera.setViewfinder(self.cvf)
        notebook.addTab(self.cvf, 'Record')

        # start the camera
        self.camera.start()

        # Configure recorder
        #self.recorder = qtmm.QMediaRecorder(self.camera)
        #settings = self.recorder.videoSettings()
        #settings.setResolution(640, 480)
        #settings.setFrameRate(24.0)
        #settings.setQuality(qtmm.QMultimedia.VeryHighQuality)
        #self.recorder.setVideoSettings(settings)

        # connect the transport
        record_act.triggered.connect(self.record)
        record_act.triggered.connect(
            lambda: notebook.setCurrentWidget(self.cvf)
        )
        pause_act.triggered.connect(self.recorder.pause)
        stop_act.triggered.connect(self.recorder.stop)

        # refresh the files when the recording is made
        stop_act.triggered.connect(self.refresh_video_list)


        self.show()

    ######################
    # Playback callbacks #
    ######################

    def refresh_video_list(self):
        self.file_list.clear()
        video_files = self.video_dir.entryList(
            ["*.ogg", "*.avi", "*.mov", "*.mp4", "*.mkv"],
            qtc.QDir.Files | qtc.QDir.Readable
        )
        for fn in sorted(video_files):
            self.file_list.addItem(fn)

    def on_file_selected(self, item):
        fn = item.text()
        url = qtc.QUrl.fromLocalFile(self.video_dir.filePath(fn))
        content = qtmm.QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()

    #######################
    # Recording callbacks #
    #######################

    def camera_check(self):
        cameras = qtmm.QCameraInfo.availableCameras()
        print(cameras)
        if not cameras:
            qtw.QMessageBox.critical(
                self,
                'No cameras',
                'No cameras were found, recording disabled.'
            )
        else:
            return qtmm.QCamera(cameras[0])

    def record(self):
        # create a filename
        datestamp = qtc.QDateTime.currentDateTime().toString()
        self.mediafile = qtc.QUrl.fromLocalFile(
            self.video_dir.filePath('log - ' + datestamp)
        )
        self.recorder.setOutputLocation(self.mediafile)
        # start recording
        self.recorder.record()

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
