import sys

from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

from funBlock.Buffer import Buffer
from funBlock.Consumer import Consumer
from funBlock.Producer import Producer
from funBlock.StaticValues import StaticValues
from funBlock.funModule import process_queueing_system


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        # Параметры
        self.producers_count = 0
        self.consumers_count = 0
        self.buffer_size = 0
        self.requests_count = 0
        # Uniform distribution function values for Producers
        self.lower_distr_value = 0.0
        self.upper_distr_value = 0.0
        # Exponential distribution function value for Consumers
        self.lambd = 0.0

        self.iteration = 0

        # Элементы системы
        self.producers = []
        self.consumers = []
        self.events = []
        self.utilization_rate = []
        self.resultsTotal = []
        self.buffer = None
        #    Указатель на номер прибора, с которого должен начинать обход
        self.static_values = None
        #    Все обработанные заявки(для вывода во временнном порядке)
        self.processed_requests = []

        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)
        self.Form, self.Window = uic.loadUiType("tabs.ui")
        self.window = self.Window()
        self.form = self.Form()
        self.form.setupUi(self.window)
        self.window.setWindowTitle("Queuing System var 25")
        # Биндим кнопки
        # Для Parameters tab
        self.form.saveButton.clicked.connect(self.param_save_button_clicked)
        #       Проверка вводимых в qlineedit значений
        regex_int = QtCore.QRegExp("\d+")
        regex_float = QtCore.QRegExp("^[0-9]*[.]?[0-9]+$")
        validator_int = QtGui.QRegExpValidator(regex_int)
        validator_float = QtGui.QRegExpValidator(regex_float)
        self.form.numSourcesLineEd.setValidator(validator_int)
        self.form.numOfConsumersLineEd.setValidator(validator_int)
        self.form.sizeBufferLineEd.setValidator(validator_int)
        self.form.requestCountLineEd.setValidator(validator_int)
        self.form.alphaLineEd.setValidator(validator_float)
        self.form.betaLineEd.setValidator(validator_float)
        self.form.lambdaLineEd.setValidator(validator_float)
        # Сразу изменяем хранимые данные при изменении значений в строках
        # self.form.numSourcesLineEd.textChanged.connect(self.num_sources_line_changed)

        # Для Step mode tab
        self.form.resetButton.clicked.connect(self.initialize_steps_table)
        # self.form.resetButton2.clicked.connect(self.initialize_steps_table)
        self.form.nextStepButton.clicked.connect(self.step_m_next_step_clicked)
        self.form.allSteps_button.clicked.connect(self.all_steps_clicked)
        # self.form.allStepsTotalButton.clicked.connect(self.all_steps_clicked)
        # self.form.allStepsTotalButton.clicked.connect(self.initialize_steps_table)

    def num_sources_line_changed(self):
        line = self.producers_count = self.form.numSourcesLineEd.text()
        self.window.setWindowTitle(line)
        print("Text changed " + line)

    def param_save_button_clicked(self):
        self.producers_count = int(self.form.numSourcesLineEd.text())
        self.consumers_count = int(self.form.numOfConsumersLineEd.text())
        self.buffer_size = int(self.form.sizeBufferLineEd.text())
        self.requests_count = int(self.form.requestCountLineEd.text())
        self.lower_distr_value = float(self.form.alphaLineEd.text())
        self.upper_distr_value = float(self.form.betaLineEd.text())
        self.lambd = float(self.form.lambdaLineEd.text())

    def prepare_system(self):
        self.resultsTotal.clear()
        self.utilization_rate.clear()
        self.producers.clear()
        self.consumers.clear()
        self.processed_requests.clear()
        self.form.resultsTableWidget.clear()
        self.form.resultsTotalTableWidget1.clear()
        # self.form.resultsTotalTableWidget2.clear()
        self.form.resultsTotalTableWidget3.clear()
        self.producers = []
        for el in range(self.producers_count):
            self.resultsTotal.append([0, 0, 0, 0, 0, 0])
            self.producers.append(Producer(el, self.lower_distr_value, self.upper_distr_value))
        # print(self.resultsTotal)
        self.consumers = []
        for el in range(self.consumers_count):
            self.utilization_rate.append(0.0)
            self.consumers.append(Consumer(el, self.lambd))
        self.buffer = Buffer(self.buffer_size)
        self.static_values = StaticValues(self.requests_count)
        self.iteration = 0

    def step_m_next_step_clicked(self):
        if self.iteration == 0:
            self.initialize_steps_table()
        if self.static_values.current_step <= self.requests_count:
            process_queueing_system(self.static_values, self.iteration, self.producers, self.consumers, self.buffer,
                                    self.form.resultsTableWidget, self.form.resultsTotalTableWidget1,
                                    # self.form.resultsTotalTableWidget2,
                                    self.form.resultsTotalTableWidget3,
                                    self.processed_requests,
                                    self.events, False, self.utilization_rate, self.resultsTotal)
            self.iteration = self.iteration + 1

    def all_steps_clicked(self):
        if self.iteration == 0:
            self.initialize_steps_table()
        while self.static_values.current_step < self.requests_count - 1:
            self.step_m_next_step_clicked()
        process_queueing_system(self.static_values, self.iteration, self.producers, self.consumers, self.buffer,
                                self.form.resultsTableWidget, self.form.resultsTotalTableWidget1,
                                # self.form.resultsTotalTableWidget2,
                                self.form.resultsTotalTableWidget3,
                                self.processed_requests,
                                self.events, True, self.utilization_rate, self.resultsTotal)

    def initialize_steps_table(self):
        self.prepare_system()
        # Table1
        self.form.resultsTableWidget.setColumnCount(3 + self.buffer_size + self.consumers_count)
        self.form.resultsTableWidget.setRowCount(self.requests_count)
        self.form.resultsTableWidget.setItem(0, 0, QTableWidgetItem("Time"))
        self.form.resultsTableWidget.setItem(0, 1, QTableWidgetItem("Event"))
        self.form.resultsTableWidget.setItem(0, 2, QTableWidgetItem("Request"))
        for i in range(self.buffer_size):
            self.form.resultsTableWidget.setItem(0, 3 + i, QTableWidgetItem("Buf" + str(i)))
        for i in range(self.consumers_count):
            self.form.resultsTableWidget.setItem(0, 3 + self.buffer_size + i, QTableWidgetItem("Cons" + str(i)))
        # Table2
        self.form.resultsTotalTableWidget1.setColumnCount(5)
        self.form.resultsTotalTableWidget1.setRowCount(self.producers_count + 1)
        self.form.resultsTotalTableWidget1.setItem(0, 1, QTableWidgetItem("reqs_count"))
        self.form.resultsTotalTableWidget1.setItem(0, 2, QTableWidgetItem("time of waiting"))
        self.form.resultsTotalTableWidget1.setItem(0, 3, QTableWidgetItem("time of processing"))
        self.form.resultsTotalTableWidget1.setItem(0, 4, QTableWidgetItem("refusals probability"))
        # Table3
        # self.form.resultsTotalTableWidget2.setColumnCount(2)
        # self.form.resultsTotalTableWidget2.setRowCount(2)
        # Table3
        self.form.resultsTotalTableWidget3.setColumnCount(2)
        self.form.resultsTotalTableWidget3.setRowCount(self.consumers_count + 1)
        self.form.resultsTotalTableWidget3.setItem(0, 1, QTableWidgetItem("utilization rate"))


if __name__ == "__main__":
    app = QApplication([])
    m_window = MainWindow()
    m_window.window.show()
    sys.exit(app.exec_())
