import sys
from PyQt5.QtWidgets import QApplication
from ui import EmailSenderWidget

def start_gui():
    app = QApplication(sys.argv)
    sender_widget = EmailSenderWidget()
    sender_widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    start_gui()
