from vidstream import StreamingServer
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

class VideoStreamServerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Stream Server")
        
        self.host = StreamingServer('192.168.1.111', 4424)
        
        self.start_button = QPushButton("Start Server", self)
        self.start_button.setGeometry(50, 50, 150, 50)
        self.start_button.clicked.connect(self.start_server)
        
        self.stop_button = QPushButton("Stop Server", self)
        self.stop_button.setGeometry(50, 120, 150, 50)
        self.stop_button.clicked.connect(self.stop_server)
        self.stop_button.setEnabled(False)
        
        self.server_thread = None

    def start_server(self):
        self.server_thread = threading.Thread(target=self.host.start_server)
        self.server_thread.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_server(self):
        self.host.stop_server()
        self.server_thread.join()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

if __name__ == "__main__":
    app = QApplication([])
    window = VideoStreamServerApp()
    window.show()
    app.exec_()
