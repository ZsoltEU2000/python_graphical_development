from PyQt5.QtCore import (QCoreApplication, QRect, QMetaObject, Qt)
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
import backend
import sys
from exeptions import *
from os import remove
from glob import glob


class HistogramWindow(QWidget):

    def __init__(self, picture, parent=None):
        super(HistogramWindow, self).__init__(parent)
        self.setWindowTitle('Histogram')
        self.setWindowIcon(QIcon('statistics.png'))
        label = QLabel(self)
        picture = QPixmap(picture)
        label.setPixmap(picture)
        self.resize(picture.width(), picture.height())

    def close_event(self, event):
        event.ignore()


class MainWindow(object):

    def __init__(self, main_window):

        if main_window.objectName():
            main_window.setObjectName('main_window')
        main_window.resize(400, 625)

        main_window.setWindowIcon(QIcon('statistics.png'))

        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName('central_widget')
        main_window.setCentralWidget(self.central_widget)

        self.menu_bar = QMenuBar(main_window)
        self.menu_bar.setObjectName('menu_bar')
        main_window.setMenuBar(self.menu_bar)

        self.status_bar = QStatusBar(main_window)
        self.status_bar.setObjectName('status_bar')
        main_window.setStatusBar(self.status_bar)

        self.container = QWidget(self.central_widget)
        self.container.setObjectName('grid_layout')
        self.container.setGeometry(QRect(20, 30, 360, 390))

        self.average = QPushButton(self.container)
        self.average.setObjectName('average')
        self.average.setGeometry(QRect(0, 200, 170, 25))

        self.upper_quartile = QPushButton(self.container)
        self.upper_quartile.setObjectName('upper_quartile')
        self.upper_quartile.setGeometry(QRect(0, 235, 170, 25))

        self.lower_quartile = QPushButton(self.container)
        self.lower_quartile.setObjectName('lower_quartile')
        self.lower_quartile.setGeometry(QRect(0, 305, 170, 25))

        self.dispersion = QPushButton(self.container)
        self.dispersion.setObjectName('dispersion')
        self.dispersion.setGeometry(QRect(0, 340, 170, 25))

        self.kurtosis = QPushButton(self.container)
        self.kurtosis.setObjectName('kurtosis')
        self.kurtosis.setGeometry(QRect(190, 200, 170, 25))

        self.skewness = QPushButton(self.container)
        self.skewness.setObjectName('skewness')
        self.skewness.setGeometry(QRect(190, 235, 170, 25))

        self.median_quartile = QPushButton(self.container)
        self.median_quartile.setObjectName('median_quartile')
        self.median_quartile.setGeometry(QRect(0, 270, 140, 25))

        self.show_histogram_button = QPushButton(self.container)
        self.show_histogram_button.setObjectName('show_histogram_button')
        self.show_histogram_button.setGeometry(QRect(150, 265, 60, 35))

        self.max = QPushButton(self.container)
        self.max.setObjectName('max')
        self.max.setGeometry(QRect(220, 270, 140, 25))

        self.min = QPushButton(self.container)
        self.min.setObjectName('min')
        self.min.setGeometry(QRect(190, 305, 170, 25))

        self.extent = QPushButton(self.container)
        self.extent.setObjectName('extent')
        self.extent.setGeometry(QRect(190, 340, 170, 25))

        self.upload_button = QPushButton(self.central_widget)
        self.upload_button.setObjectName('upload_button')
        self.upload_button.setGeometry(QRect(20, 405, 360, 35))

        self.input = QLineEdit(self.central_widget)
        self.input.setObjectName('input')
        self.input.setGeometry(20, 450, 200, 23)
        self.input.setPlaceholderText('1.0;2.0;3.0;4.0;....;n.0;')

        self.add_list_button = QPushButton(self.central_widget)
        self.add_list_button.setObjectName('add_list_button')
        self.add_list_button.setGeometry(235, 450, 70, 25)

        self.clear_list_button = QPushButton(self.central_widget)
        self.clear_list_button.setObjectName('clear_list_button')
        self.clear_list_button.setGeometry(308, 450, 70, 25)

        self.last_calculations = QListWidget(self.central_widget)
        self.last_calculations.setObjectName('calculate_button')
        self.last_calculations.setGeometry(QRect(20, 485, 360, 80))

        self.clear_database_button = QPushButton(self.central_widget)
        self.clear_database_button.setObjectName('clear_list_button')
        self.clear_database_button.setGeometry(20, 570, 170, 25)

        self.remove_ls_button = QPushButton(self.central_widget)
        self.remove_ls_button.setObjectName('remove_ls_button')
        self.remove_ls_button.setGeometry(210, 570, 170, 25)

        self.result = QLineEdit(self.container)
        self.result.setGeometry(0, 0, 360, 160)
        self.result.setReadOnly(True)
        self.result.setStyleSheet('font-size: 18pt; line-break: break-word;')

        self.clear_result_button = QPushButton(self.container)
        self.clear_result_button.setObjectName('clear_result_button')
        self.clear_result_button.setGeometry(0, 165, 360, 25)

        self.actual_ls = []

        self.last_calculations_list = []

        self.reload_data()

        self.retranslate(main_window)

        QMetaObject.connectSlotsByName(main_window)

        self.last_calculations.itemClicked.connect(self.item_click)
        self.upload_button.clicked.connect(self.upload)
        self.add_list_button.clicked.connect(self.add_list)
        self.clear_list_button.clicked.connect(self.clear_list)
        self.average.clicked.connect(self.calculate_average)
        self.upper_quartile.clicked.connect(self.calculate_upper_quartile)
        self.median_quartile.clicked.connect(self.calculate_median_quartile)
        self.lower_quartile.clicked.connect(self.calculate_lower_quartile)
        self.dispersion.clicked.connect(self.calculate_dispersion)
        self.kurtosis.clicked.connect(self.calculate_kurtosis)
        self.skewness.clicked.connect(self.calculate_skewness)
        self.max.clicked.connect(self.calculate_max)
        self.min.clicked.connect(self.calculate_min)
        self.extent.clicked.connect(self.calculate_extent)
        self.clear_result_button.clicked.connect(self.clear_result)
        self.clear_database_button.clicked.connect(self.clear_database)
        self.remove_ls_button.clicked.connect(self.remove_ls_from_database)
        self.show_histogram_button.clicked.connect(self.show_histogram)

    def retranslate(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate('main_window', 'Statistics'))
        self.upload_button.setText(QCoreApplication.translate('main_window', 'Upload..'))
        self.add_list_button.setText(QCoreApplication.translate('main_window', 'Add'))
        self.clear_list_button.setText(QCoreApplication.translate('main_window', 'Clear'))
        self.average.setText(QCoreApplication.translate('main_window', 'Average'))
        self.upper_quartile.setText(QCoreApplication.translate('main_window', 'Upper quartile'))
        self.median_quartile.setText(QCoreApplication.translate('main_window', 'Median quartile'))
        self.lower_quartile.setText(QCoreApplication.translate('main_window', 'Lower quartile'))
        self.dispersion.setText(QCoreApplication.translate('main_window', 'Dispersion'))
        self.kurtosis.setText(QCoreApplication.translate('main_window', 'Kurtosis'))
        self.skewness.setText(QCoreApplication.translate('main_window', 'Skewness'))
        self.max.setText(QCoreApplication.translate('main_window', 'Max'))
        self.min.setText(QCoreApplication.translate('main_window', 'Min'))
        self.extent.setText(QCoreApplication.translate('main_window', 'Extent'))
        self.clear_database_button.setText(QCoreApplication.translate('main_window', 'Clear database'))
        self.remove_ls_button.setText(QCoreApplication.translate('main_window', 'Remove item'))
        self.clear_result_button.setText(QCoreApplication.translate('main_window', 'Clear'))
        self.show_histogram_button.setText(QCoreApplication.translate('main_window', 'Histogram'))

    def upload(self):
        url = str(QFileDialog.getOpenFileName())
        uploaded_file = url.split("'")[1]
        filename_test = str(uploaded_file).split('.')[-1]
        ls = []
        if uploaded_file != '':
            file = open(uploaded_file, 'r')
            try:
                if filename_test == 'txt':
                    for line in file:
                        tmp = line.split(';')
                        for element in tmp:
                            test_element = StringToFloat(element)
                            if not test_element.is_float():
                                unusable_element = element
                                raise ElementIsNotUsable
                            else:
                                ls.append(float(element))
                else:
                    raise FileIsNotTxt
                if len(ls) != 0:
                    new_item = backend.List(ls)
                    is_in_list = False
                    for element in self.last_calculations_list:
                        if new_item.__str__() == element.__str__():
                            is_in_list = True
                    if not is_in_list:
                        new_item.create_histogram()
                        self.last_calculations_list.append(new_item)
                        self.save_to_file()
                        self.reload_data()
                    else:
                        self.already_exists_error()
                else:
                    raise EmptyListError
            except FileIsNotTxt:
                message = QMessageBox()
                message.setWindowTitle('File is not .txt!')
                message.setText("The actual file is not a .txt, please try to upload a .txt file!")
                message.setIcon(QMessageBox.Warning)
                message.exec()
            except ElementIsNotUsable:
                message = QMessageBox()
                message.setWindowTitle('Unusable item!')
                message.setText("One of the inserted items ({}) can't be "
                                "used so it must to be removed!".format(unusable_element))
                message.setIcon(QMessageBox.Warning)
                message.exec()
            except EmptyListError:
                message = QMessageBox()
                message.setWindowTitle('No usable data found!')
                message.setText("There weren't usable elements in the .txt file!")
                message.setIcon(QMessageBox.Warning)
                message.exec()

    def add_list(self):
        input_list = self.input.text()[:-1]
        ls = []
        try:
            if input_list != '':
                input_list = input_list.split(';')
                for element in input_list:
                    if element != '':
                        test_element = StringToFloat(element)
                        if not test_element.is_float():
                            unusable_element = element
                            raise ElementIsNotUsable
                        else:
                            ls.append(float(element))
                if len(ls) != 0:
                    new_item = backend.List(ls)
                    is_in_list = False
                    for element in self.last_calculations_list:
                        if new_item.__str__() == element.__str__():
                            is_in_list = True
                    if not is_in_list:
                        new_item.create_histogram()
                        self.last_calculations_list.append(new_item)
                        self.save_to_file()
                        self.reload_data()
                    else:
                        self.already_exists_error()
                else:
                    raise EmptyListError
            else:
                raise EmptyListError
        except ElementIsNotUsable:
            message = QMessageBox()
            message.setWindowTitle('Unusable item!')
            message.setText("One of the inserted items ({}) can't be "
                            "used so it must to be removed!".format(unusable_element))
            message.setIcon(QMessageBox.Warning)
            message.exec()
        except EmptyListError:
            message = QMessageBox()
            message.setWindowTitle('No usable data found!')
            message.setText("There weren't usable elements in the input!")
            message.setIcon(QMessageBox.Warning)
            message.exec()

    def clear_list(self):
        self.input.clear()
        self.input.setReadOnly(False)
        self.add_list_button.setCheckable(True)

    def clear_result(self):
        self.result.clear()

    def clear_database(self):
        file = open('database.txt', 'w')
        file.write('')
        file.close()
        images = glob('plots/*')
        for image in images:
            remove(image)
        self.reload_data()

    def show_histogram(self):
        if not self.actual_ls == []:
            picture = 'plots/' + self.actual_ls.__str__() + '.jpg'
            self.ui = HistogramWindow(picture)
            self.ui.show()
        else:
            return self.no_item_selected_error()

    def close_event(self, event):
        widget_list = QApplication.topLevelWidgets()
        num_windows = len(widget_list)
        if num_windows > 1:
            event.accept()
        else:
            event.ignore()

    def calculate_average(self):
        try:
            data = self.actual_ls
            if not isinstance(data, backend.List):
                raise UnselectedItemError
        except UnselectedItemError:
            return self.no_item_selected_error()
        else:
            self.result.setText(str(data.get_avg()))

    def calculate_upper_quartile(self):
        try:
            data = self.actual_ls
            if not isinstance(data, backend.List):
                raise UnselectedItemError
        except UnselectedItemError:
            self.no_item_selected_error()
        else:
            quartiles = data.get_quartiles()
            for index in range(len(quartiles)):
                if index == 2:
                    self.result.setText(str(quartiles[index]))

    def calculate_median_quartile(self):
        try:
            data = self.actual_ls
            if not isinstance(data, backend.List):
                raise UnselectedItemError
        except UnselectedItemError:
            self.no_item_selected_error()
        else:
            quartiles = data.get_quartiles()
            for index in range(len(quartiles)):
                if index == 1:
                    self.result.setText(str(quartiles[index]))

    def calculate_lower_quartile(self):
        try:
            data = self.actual_ls
            if not isinstance(data, backend.List):
                raise UnselectedItemError
        except UnselectedItemError:
            self.no_item_selected_error()
        else:
            quartiles = data.get_quartiles()
            for index in range(len(quartiles)):
                if index == 0:
                    self.result.setText(str(quartiles[index]))

    def calculate_dispersion(self):
        try:
            data = self.actual_ls
            if not isinstance(data, backend.List):
                raise UnselectedItemError
        except UnselectedItemError:
            self.no_item_selected_error()
        else:
            self.result.setText(str(data.get_dispersion()))

    def calculate_kurtosis(self):
        try:
            data = self.actual_ls
            if not isinstance(data, backend.List):
                raise UnselectedItemError
        except UnselectedItemError:
            self.no_item_selected_error()
        else:
            self.result.setText(str(data.get_kurtosis()))

    def calculate_skewness(self):
        try:
            data = self.actual_ls
            if not isinstance(data, backend.List):
                raise UnselectedItemError
        except UnselectedItemError:
            self.no_item_selected_error()
        else:
            self.result.setText(str(data.get_skewness()))

    def calculate_max(self):
        try:
            data = self.actual_ls
            if not isinstance(data, backend.List):
                raise UnselectedItemError
        except UnselectedItemError:
            self.no_item_selected_error()
        else:
            self.result.setText(str(data.get_max()))

    def calculate_min(self):
        try:
            data = self.actual_ls
            if not isinstance(data, backend.List):
                raise UnselectedItemError
        except UnselectedItemError:
            self.no_item_selected_error()
        else:
            self.result.setText(str(data.get_min()))

    def calculate_extent(self):
        try:
            data = self.actual_ls
            if not isinstance(data, backend.List):
                raise UnselectedItemError
        except UnselectedItemError:
            self.no_item_selected_error()
        else:
            self.result.setText(str(data.get_extent()))

    def save_to_file(self):
        file = open('database.txt', 'w')
        last_calculations = self.last_calculations_list
        for calculation in last_calculations:
            file.write(calculation.__str__())
            file.write('\n')
        file.close()

    def reload_data(self):
        file = open('database.txt', 'r')
        self.last_calculations_list.clear()
        self.last_calculations.clear()
        for line in file:
            ls = []
            data = line.split(';')[:-1]
            for element in data:
                if element != '':
                    ls.append(float(element))
            if len(ls) != 0:
                list_element = backend.List(ls)
                self.last_calculations_list.append(list_element)
        for element in self.last_calculations_list:
            self.last_calculations.addItem(QListWidgetItem(element.__str__()))

    def item_click(self, item):
        tmp = item.text()
        for element in self.last_calculations_list:
            if tmp == element.__str__():
                self.actual_ls = element
                self.input.setText(element.__str__())

    def remove_ls_from_database(self):
        try:
            if not isinstance(self.actual_ls, backend.List):
                raise UnselectedItemError
        except UnselectedItemError:
            self.no_item_selected_error()
        else:
            for element in self.last_calculations_list:
                if element.__str__() == self.actual_ls.__str__():
                    self.last_calculations_list.remove(self.actual_ls)
                    remove('plots/' + element.__str__() + '.jpg')
            self.save_to_file()
            self.reload_data()
            self.actual_ls = []

    @staticmethod
    def no_item_selected_error():
        message = QMessageBox()
        message.setWindowTitle('Select a list!')
        message.setText("No list have been chosen by you! Please select one!")
        message.setIcon(QMessageBox.Warning)
        message.exec()

    @staticmethod
    def already_exists_error():
        message = QMessageBox()
        message.setWindowTitle('List already exists!')
        message.setText("This list already have been added to your database.\n"
                        "There are few things you can do:\n"
                        "   - your can recall it by clicking on it\n"
                        "   - you can clear this input and try to add a new one.")
        message.setIcon(QMessageBox.Warning)
        message.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = MainWindow(window)
    window.show()
    sys.exit(app.exec_())
