import cv2
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.widget = QWidget(self)
        self.VBL = QVBoxLayout(self.widget)
        
        self.FeedLabel = QLabel()
        self.VBL.addWidget(self.FeedLabel)
        
        self.CancelBTN = QPushButton("Cancel")
        self.CancelBTN.clicked.connect(self.CancelFeed)
        self.VBL.addWidget(self.CancelBTN)
        
        self.setCentralWidget(self.widget)
        
        self.Worker1 = Worker1()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot, Qt.AutoConnection)
        self.Worker1.start()
        
                # Stop feed wwhen q hit
                # if key == ord('q') or key == 27:
                #     break
                # elif key == ord('a'):
                #     shift -= 1
                # elif key == ord('d'):
                #     shift += 1
                
        
    @pyqtSlot(QImage)
    def ImageUpdateSlot(self, roi):
        self.FeedLabel.setPixmap(QPixmap.fromImage(roi))
        
    def CancelFeed(self):
        self.Worker1.stop()
        
class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    
    def run(self):
        shift = 0
        v_margins = 200
        new_height = 960 - 2 * v_margins
    
        self.ThreadActive = True
        capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = capture.read()
            
            if ret:
                # Crop top and bottom of feed
                cropped_frame = frame[v_margins:960-v_margins, 0:1920]    
        
                #Specify ROI dimensions
                roi_x = 400
                roi_y = roi_x / 2 #Could change this if display isn't 2:1
        
                # Pad frame with extra ROI width
                half_frame = frame[:, 0:int(roi_x)]
                padded_frame = np.hstack((frame, half_frame))
        
                # Crop to ROI
                # Modulo to come back over!!!
                roi = padded_frame[0:new_height,(0+shift)%roi_x:roi_x+shift]
                
                ConvertToQtFormat = QImage(roi.data.tobytes(), roi.shape[1], roi.shape[0], QImage.Format.Format_BGR888)
                pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(pic)


        # End feed
        capture.release()
        
    def stop(self):
        self.ThreadActive = False
        self.quit()

if __name__ == "__main__":
    App = QApplication([])
    Root = MainWindow()
    Root.show()
    exitCode = App.exec()
    sys.exit(exitCode)
