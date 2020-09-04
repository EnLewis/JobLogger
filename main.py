import sys
from csv import writer
from PyQt5.QtWidgets import (QWidget, QLabel, QToolTip, QPushButton, QApplication, QLineEdit, QInputDialog, QGridLayout, QMainWindow)
from PyQt5.QtGui import QFont
from PyQt5 import QtGui, QtCore

# def initiate_window():
#     app = QApplication([])
#     window = QWidget()
#     layout = QVBoxLayout()
#     button = QPushButton('Add Job Log')
#     button.clicked.connect(on_button_clicked)

#     layout.addWidget(button)
#     window.setLayout(layout)
#     window.show()
#     app.exec_()

# def on_button_clicked():
#     new_window = QWidget()
#     layout = QVBoxLayout()
#     layout.addWidget(QLineEdit('title'))
#     layout.addWidget(QLineEdit('date'))
#     layout.addWidget(QLineEdit('status'))
#     new_window.setLayout(layout)
#     new_window.show()

class LogDialog(QMainWindow):
    def __init__(self, parent=None):
        super(LogDialog, self).__init__(parent)
        self.setWindowTitle('Job Log')
        self.setGeometry(300,300,350,300)
        self.initUI()
        self.show()

    def initUI(self):
        wid = QWidget(self)
        self.setCentralWidget(wid)

        grid = QGridLayout()
        grid.setSpacing(5)
        wid.setLayout(grid)

        self.title = QLabel('Title')
        self.company = QLabel('Company')
        self.date = QLabel('Date Applied')
        self.status = QLabel('Status')
        self.url = QLabel('URL')

        self.title_edit = QLineEdit(self)
        self.company_edit = QLineEdit(self)
        self.date_edit = QLineEdit(self)
        self.status_edit = QLineEdit(self)
        self.url_edit = QLineEdit(self)

        grid.addWidget(self.title, 1, 0)
        grid.addWidget(self.title_edit, 1, 1)

        grid.addWidget(self.company, 2, 0)
        grid.addWidget(self.company_edit, 2, 1)

        grid.addWidget(self.date, 3, 0)
        grid.addWidget(self.date_edit, 3, 1)

        grid.addWidget(self.status, 4, 0)
        grid.addWidget(self.status_edit, 4, 1)

        grid.addWidget(self.url, 5, 0)
        grid.addWidget(self.url_edit, 5, 1)

        self.submit = QPushButton('Submit', self)
        self.submit.clicked.connect(self.on_submit_clicked)

        grid.addWidget(self.submit, 6, 1)

    def on_submit_clicked(self):
        self.log_csv_data()
        self.close()
    
    def log_csv_data(self):
        with open("job_logs.csv", mode='a+', newline='') as logscsv:
            entry = [self.title_edit.text(), \
                     self.company_edit.text(), \
                     self.date_edit.text(), \
                     self.status_edit.text(), \
                     self.url_edit.text()]
            csv_writer = writer(logscsv)
            csv_writer.writerow(entry)



class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Job Logger')
        self.setGeometry(300,200,300,200)
        self.initUI()

    
    def initUI(self):
        #set Font

        self.btn = QPushButton('Add Job Log', self)
        self.btn.clicked.connect(self.on_button_clicked)
        self.dialogs = []

        self.le = QLineEdit(self)
        self.le.move(20, 20)

        self.btn.setToolTip('Use this to add a job log')
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(100,100)

    
    def on_button_clicked(self):
        self.dialog = LogDialog(self)
        self.dialogs.append(self.dialog)
        self.dialog.show()
        
        

def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()