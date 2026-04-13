import math

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

# This function loads a series of sprite images stored in a folder with a
# consistent naming pattern: sprite_# or sprite_##. It returns a list of the images.
def load_sprite(sprite_folder_name, number_of_frames):
    frames = []
    padding = math.ceil(math.log(number_of_frames - 1, 10))
    for frame in range(number_of_frames):
        folder_and_file_name = sprite_folder_name + "/sprite_" + str(frame).rjust(padding, '0') + ".png"
        frames.append(QPixmap(folder_and_file_name))

    return frames

class SpritePreview(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sprite Animation Preview")
        # This loads the provided sprite and would need to be changed for your own.
        self.num_frames = 21
        self.frames = load_sprite('spriteImages',self.num_frames)

        # Add any other instance variables needed to track information as the program
        # runs here

        self.current_frame = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateAnimation)
        self.animating = False
        self.fps = 1


        # Make the GUI in the setupUI method
        self.setupUI()


    def setupUI(self):
        # An application needs a central widget - often a QFrame
        frame = QFrame()
        self.setCenterWidget(frame)

        # Add a lot of code here to make layouts, more QFrame or QWidgets, and
        # the other components of the program.
        # Create needed connections between the UI components and slot methods
        # you define in this class.

        self.mainLayout = QVBoxLayout(frame)
        topSection = QHBoxLayout()
        self.imageLable = QLabel()

        if self.frames:
            self.imageLable.setPixmap(self.frames[0])

        self.fpsSlider = QSlider(Qt.Orientation.Horizontal)
        self.fpsSlider.setMinimum(1)
        self.fpsSlider.setMaximum(100)
        self.fpsSlider.setValue(self.fps)
        self.fpsSlider.setTickPosition(QSlider.TickPosition.TicksLeft)
        self.fpsSlider.setTickInterval(25)

        #--------------------------------

        topSection.addWidget(self.imageLable)
        topSection.addWidget(self.fpsSlider)

        #--------------------------------

        self.mainLayout.addLayout(topSection)
        self.startStop = QPushButton("Start")
        self.mainLayout.addWidget(self.startStop)

        fpsSection = QHBoxLayout()
        self.fpsLable = QLabel("FPS")
        self.fpsVal = QLabel(str(self.fps))

        fpsSection.addWidget(self.fpsLable)
        fpsSection.addWidget(self.fpsVal)

        self.mainLayout.addLayout(fpsSection)

        #-----------------------------

        menu = self.menuBar()
        menu.setNativeMenuBar(False)
        fileMenu = menu.addMenu("File")

        pause = QAction("Pause")
        pause.triggered.connect(self.stopPlay)

        exit = QAction("Exit")
        exit.triggered.connect(self.close)

        fileMenu.addAction(pause)
        fileMenu.addAction(exit)

        self.startStop.clicked.conect(self.togglePlay)
        self.fpsSlider.valueChanged.connect(self.handleSlider)

    # You will need methods in the class to act as slots to connect to signals

    def handle_slider(self):
        self.fps = self.fpsSlider.value()
        self.fpsVal.setText((str(self.fps)))
        if self.animating:
            self.timer.start(int(1000 / self.fps))

    def startPlay(self):
        self.animating = True
        self.startStop.setText("Stop")
        self.timer.start(int(1000 / self.fps))

    def stopPlay(self):
        self.animating = False
        self.startStop.setText("Start")
        self.timer.stop()

    def togglePlay(self):
        if self.animating:
            self.stopPlay()
        else:
            self.startPlay()

    def updateAnimation(self):
        self.current_frame = (self.current_frame + 1) % self.num_frames
        if self.frames:
            self.imageLable.setPixmap(self.frames[self.current_frame])



def main():
    app = QApplication([])
    # Create our custom application
    window = SpritePreview()
    # And show it
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
