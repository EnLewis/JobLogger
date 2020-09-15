import sys
from datetime import date
from dataclasses import dataclass
from csv import reader, writer
from PyQt5.QtWidgets import (QWidget, QLabel, QToolTip, QPushButton, QApplication, QLineEdit, QInputDialog, QGridLayout, QMainWindow, QComboBox, QListWidget, QListWidgetItem, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QFont
from PyQt5 import QtGui, QtCore

def status_switch(x):
    return {
        'No Response' : 0,
        'Rejected': 1,
        'Interviewed': 2,
        'Accepted': 3
    }[x]

@dataclass
class job_log:
    title: str
    company: str
    status: str
    url: str
    date_applied: str
    date_rejected: str = "n/a"
    date_interviewed: str = "n/a"
    date_accepted: str = "n/a"

    def update_status(self, status):
        status_i = status_switch(status)
        new_date = date.today().strftime("%d/%m/%Y")
        if status_i == 0:
            self.date_applied = new_date
        elif status_i == 1:
            self.date_rejected = new_date
        elif status_i == 2:
            self.date_interviewed = new_date
        elif status_i == 3:
            self.date_accepted = new_date
    
    def list_fields(self):
        return [self.title, self.company, self.status, self.url, self.date_applied, self.date_rejected, self.date_interviewed, self.date_accepted]

class QCustomQWidget(QWidget):
    def __init__(self, parent = None):
        super(QCustomQWidget, self).__init__(parent)
        # Define all layout parts
        self.left_sub_layout = QVBoxLayout()
        self.right_btn_layout = QHBoxLayout()
        self.right_sub_layout = QVBoxLayout()
        self.full_layout = QHBoxLayout()

        #Define left sub layout
        self.upperQLabel = QLabel()
        self.lowerQLabel = QLabel()
        self.left_sub_layout.addWidget(self.upperQLabel)
        self.left_sub_layout.addWidget(self.lowerQLabel)
        self.upperQLabel.setStyleSheet('''
            color: rgb(35,35,35)
            ''')
        self.lowerQLabel.setStyleSheet('''
            color: rgb(100,100,100)
            ''')
        self.upperQLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.lowerQLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)

        #Define right btn layout
        self.update = QPushButton("Update")
        self.update.clicked.connect(self.on_update_clicked)
        self.status_edit = QComboBox() # self?
        #self.update.setStyleSheet("background-color: red")
        self.status_edit.addItems(["No Response", "Rejected", "Interviewed", "Accepted"])
        self.right_btn_layout.addWidget(self.status_edit, 0)
        self.right_btn_layout.addWidget(self.update, 1)

        #Define right sub layout
        self.dateQLabel = QLabel()
        self.right_sub_layout.addLayout(self.right_btn_layout, 0)
        self.right_sub_layout.addWidget(self.dateQLabel, 1)
        self.dateQLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)

        #Define overall layout 
        self.full_layout.addLayout(self.left_sub_layout, 0)
        # hspacer = QSpacerItem(20,40, QtGui.QSize)
        # self.full_layout.addWidget()
        self.full_layout.addStretch(1)
        self.full_layout.addLayout(self.right_sub_layout, 2)
        self.right_sub_layout.setAlignment(QtCore.Qt.AlignRight)

        self.setLayout(self.full_layout)        
    
    def set_upper_text(self,text,style_sheet=None):
        self.upperQLabel.setText(text)
        if style_sheet != None:
            self.upperQLabel.setStyleSheet(style_sheet)
    
    def set_lower_text(self,text,style_sheet=None):
        self.lowerQLabel.setText(text)
        if style_sheet != None:
            self.upperQLabel.setStyleSheet(style_sheet)
    
    def set_date_text(self,text,style_sheet=None):
        self.dateQLabel.setText(text)
        if style_sheet != None:
            self.dateQLabel.setStyleSheet(style_sheet)
    
    def on_update_clicked(self):
        pass


    def set_status(self,status):
        self.status_edit.setCurrentIndex(status_switch(status))


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
        self.date_edit = QLineEdit(self, date.today().strftime("%d/%m/%Y"))
        self.status_edit = QComboBox(self)
        self.status_edit.addItems(["No Response", "Rejected", "Interviewed", "Accepted"])
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
            log = job_log(self.title_edit.text(), \
                          self.company_edit.text(), \
                          self.status_edit.currentText(), \
                          self.url_edit.text(), \
                          self.date_edit.text())
            csv_writer = writer(logscsv)
            csv_writer.writerow(log.list_fields())

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Job Logger')
        self.setGeometry(300,200,300,200)
        self.initUI()

    
    def initUI(self):
        #set Font
        layout = QVBoxLayout(self)

        btn = QPushButton('Add Job Log', self)
        btn.clicked.connect(self.on_button_clicked)
        self.dialogs = []

        jobs_list = QListWidget()
        jobs_list.setAlternatingRowColors(True)
        self.populate_list(jobs_list)

        btn.setToolTip('Use this to add a job log')
        btn.resize(btn.sizeHint())

        layout.addWidget(btn)
        layout.addWidget(jobs_list)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def on_button_clicked(self):
        dialog = LogDialog(self)
        self.dialogs.append(dialog)
        dialog.show()
    
    def populate_list(self, jobs_list):
        # TODO: Add "Show rejected and old" button
        with open("job_logs.csv", mode='r', newline='') as logscsv:
            csv_reader = reader(logscsv, delimiter=',')          
            jobs = [row for row in csv_reader]
            jobs.pop(0) # get rid of labels line
            for job in jobs:
                list_item = QCustomQWidget()
                list_item.set_upper_text(job[0])
                list_item.set_lower_text(job[1])
                list_item.set_date_text("Date Applied: " + job[2])
                list_item.set_status(job[3])

                widget_item = QListWidgetItem(jobs_list)
                widget_item.setSizeHint(list_item.sizeHint())
                jobs_list.addItem(widget_item)
                jobs_list.setItemWidget(widget_item, list_item)
                print(job[0])       
        

def main():
    app = QApplication(sys.argv)
    mainw = MainWindow()
    mainw.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()