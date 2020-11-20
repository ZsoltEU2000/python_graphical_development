from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                           QIcon, QLinearGradient, QPalette, QPainter, QPixmap)
from PySide2.QtWidgets import *
import backend
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(500, 350)
        icon = QIcon()
        icon.addFile(u"graph-bar.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet('background-color: #353a42;')

        style_label = 'color: white; font-weight: 600; font-family: Arial;'
        style_button = 'background-color: black; color: white; font-weight: 800; font-family: Arial; cursor: pointer; border-radius: 5%;'
        style_list = 'border: none; color: white; font-size: 10pt;'

        self.btnCalculate = QPushButton(self.centralwidget)
        self.btnCalculate.setObjectName(u"btnCalculate")
        self.btnCalculate.setGeometry(QRect(40, 280, 200, 30))
        font = QFont()
        font.setFamily(u"MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.btnCalculate.setFont(font)
        self.btnCalculate.setAutoFillBackground(False)
        self.btnCalculate.setStyleSheet(style_button)

        self.last_results = QListWidget(self.centralwidget)
        self.last_results.setObjectName(u"last_results")
        self.last_results.setGeometry(QRect(260, 25, 211, 201))
        self.last_results.setStyleSheet(style_list)

        self.avg = QLabel(self.centralwidget)
        self.avg.setObjectName(u"avg")
        self.avg.setGeometry(QRect(40, 25, 200, 15))
        self.avg.setStyleSheet(style_label)

        self.quartiles = QLabel(self.centralwidget)
        self.quartiles.setObjectName(u"quartiles")
        self.quartiles.setGeometry(QRect(40, 45, 200, 100))
        self.quartiles.setStyleSheet(style_label)

        self.dispersion = QLabel(self.centralwidget)
        self.dispersion.setObjectName(u"dispersion")
        self.dispersion.setGeometry(QRect(40, 125, 200, 15))
        self.dispersion.setStyleSheet(style_label)

        self.kurtosis = QLabel(self.centralwidget)
        self.kurtosis.setObjectName(u"kurtosis")
        self.kurtosis.setGeometry(QRect(40, 150, 200, 15))
        self.kurtosis.setStyleSheet(style_label)

        self.skewness = QLabel(self.centralwidget)
        self.skewness.setObjectName(u"skewness")
        self.skewness.setGeometry(QRect(40, 175, 200, 15))
        self.skewness.setStyleSheet(style_label)

        self.max = QLabel(self.centralwidget)
        self.max.setObjectName(u"max")
        self.max.setGeometry(QRect(40, 200, 200, 15))
        self.max.setStyleSheet(style_label)

        self.min = QLabel(self.centralwidget)
        self.min.setObjectName(u"min")
        self.min.setGeometry(QRect(40, 225, 200, 15))
        self.min.setStyleSheet(style_label)

        self.extent = QLabel(self.centralwidget)
        self.extent.setObjectName(u"extent")
        self.extent.setGeometry(QRect(40, 250, 200, 15))
        self.extent.setStyleSheet(style_label)

        self.btnUpload = QPushButton(self.centralwidget)
        self.btnUpload.setObjectName(u"btnUpload")
        self.btnUpload.setGeometry(QRect(280, 280, 170, 30))
        font1 = QFont()
        font1.setPointSize(10)
        self.btnUpload.setFont(font1)
        self.btnUpload.setStyleSheet(style_button)

        self.upload = QLabel(self.centralwidget)
        self.upload.setObjectName(u"upload")
        self.upload.setGeometry(QRect(40, 340, 460, 30))

        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setWindowIcon(QIcon('statistics.png'))

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 500, 21))
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.filename = ''

        self.memory = []

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
        self.btnCalculate.clicked.connect(self.Calculate)
        self.btnUpload.clicked.connect(self.Upload)
        self.last_results.itemClicked.connect(self.item_click)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Statistics", None))
        self.btnCalculate.setText(QCoreApplication.translate("MainWindow", u"Calculate", None))
        self.avg.setText(QCoreApplication.translate("MainWindow", u"Átlag: ", None))
        self.quartiles.setText(QCoreApplication.translate("MainWindow", u"Alsó kvartilis:\nKözépső kvartilis/Medián:\nFelső kvartilis:", None))
        self.dispersion.setText(QCoreApplication.translate("MainWindow", u"Szórás: ", None))
        self.kurtosis.setText(QCoreApplication.translate("MainWindow", u"Csúcsosság: ", None))
        self.skewness.setText(QCoreApplication.translate("MainWindow", u"Ferdeség: ", None))
        self.max.setText(QCoreApplication.translate("MainWindow", u"Max: ", None))
        self.min.setText(QCoreApplication.translate("MainWindow", u"Min: ", None))
        self.extent.setText(QCoreApplication.translate("MainWindow", u"Terjedelem: ", None))
        self.btnUpload.setText(QCoreApplication.translate("MainWindow", u"Upload", None))
        self.upload.setText("")
        self.reload_data()

    def Calculate(self):
        ls = []
        if self.filename != '':
            filename_test = str(self.filename).split('.')[-1]
            file = open(self.filename, 'r')
            try:
                if filename_test == 'txt':
                    for string in file:
                        tmp = string.split(';')
                        for element in tmp:
                            ls.append(float(element))
                    list = backend.List(ls)
                    self.avg.setText('Átlag: '+str(list.get_avg()))
                    self.quartiles.setText(str(list.get_quartiles()))
                    self.dispersion.setText('Szórás: '+str(list.get_dispersion()))
                    self.kurtosis.setText('Csúcsosság: '+str(list.get_kurtosis()))
                    self.skewness.setText('Ferdeség: '+str(list.get_skewness()))
                    self.max.setText('Max: '+str(list.get_max()))
                    self.min.setText('Min: '+str(list.get_min()))
                    self.extent.setText('Terjedelem: '+str(list.get_extent()))
                    tmp = ''
                    for element in ls:
                        tmp += str(element) + ';'
                    tmp += '|'
                    tmp += '\n'
                    r_database = open('database.txt', 'r')
                    if tmp not in r_database:
                        r_database.close()
                        w_database = open('database.txt', 'a')
                        w_database.write(tmp)
                        w_database.close()
                    r_database.close()
                else:
                    raise TypeError
            except ValueError:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Your data must to look like: 1;2;3;4\n and must to contain integers or floats!')
                msg.setWindowTitle("Error")
                msg.exec_()
            except TypeError:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Your file extension must to be .txt!')
                msg.setWindowTitle("Error")
                msg.exec_()

    def Upload(self):
        filename = str(QFileDialog.getOpenFileName())
        tmp = filename.split("'")
        url = tmp[1]
        self.upload.setText(str(url))
        self.filename = url

    def reload_data(self):
        file = open("database.txt","r")
        for str in file:
            list = []
            div = str.split('|')
            tmp = div[0].split(';')
            tmp.remove('')
            for element in tmp:
                list.append(element)
            self.memory.append(backend.List(list))
        file.close()
        for element in self.memory:
            self.last_results.addItem(element.__str__())

    def item_click(self, item):
        tmp = item.text()
        for element in self.memory:
            if str(tmp) == str(element):
                self.avg.setText('Átlag: ' + str(element.get_avg()))
                self.quartiles.setText(str(element.get_quartiles()))
                self.dispersion.setText('Szórás: ' + str(element.get_dispersion()))
                self.kurtosis.setText('Csúcsosság: ' + str(element.get_kurtosis()))
                self.skewness.setText('Ferdeség: ' + str(element.get_skewness()))
                self.max.setText('Max: ' + str(element.get_max()))
                self.min.setText('Min: ' + str(element.get_min()))
                self.extent.setText('Terjedelem: ' + str(element.get_extent()))


app = QApplication()
MainWindow = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
