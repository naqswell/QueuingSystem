import copy

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

from funBlock.Producer import Producer
from funBlock.Request import Request

from funBlock.StaticValues import StaticValues


def print_system_state(event_time, producer_number, processed_req, string, static_values: StaticValues,
                       resultsTableWidget: QtWidgets.QTableWidget, consumers,
                       buffer):
    """Вывод информации о состоянии системы"""
    row_offset = 1  # для сдвига таблицы сверху
    t_col_index = 0
    t_row_index = static_values.table_row + row_offset

    # Вывод события (1-ый столбец)
    str_event_time = str(round(event_time, 4))
    resultsTableWidget.setItem(t_row_index, t_col_index, QTableWidgetItem(str_event_time))
    t_col_index += 1

    str_event_prod_number = "p" + str(producer_number) + "; " + string
    resultsTableWidget.setItem(t_row_index, t_col_index, QTableWidgetItem(str_event_prod_number))
    t_col_index += 1

    if processed_req is not None:
        str_prod_number = str(processed_req.get_producer_number())
        str_cons_number = str(processed_req.get_consumer_number())
        str_time_creation = str(round(processed_req.get_time_of_creation(), 4))
        string = " p" + str_prod_number + "; " + "c" + str_cons_number + "; " + str_time_creation
        resultsTableWidget.setItem(t_row_index, t_col_index, QTableWidgetItem(string))

    if buffer is not None:
        # Вывод состояния буфера
        t_col_index += 1
        bf = buffer.get_requests()
        counter = 0
        for i in bf:
            if i is not None:
                str_prod_number = str(i.get_producer_number())
                str_time_creation = str(round(i.get_time_of_creation(), 4))
                string = "p" + str_prod_number + "; " + str_time_creation
                resultsTableWidget.setItem(t_row_index, t_col_index + counter, QTableWidgetItem(string))
            counter += 1

    if consumers is not None:
        # Вывод состояния приборов
        counter = 0
        for i in consumers:
            if i.get_last_processed_request() is not None:
                str_prod_number = str(i.get_last_processed_request().get_producer_number())
                str_time_creation = str(round(i.get_last_processed_request().get_time_of_creation(), 4))
                str_time_when_was_processed = str(
                    round(i.get_last_processed_request().get_time_when_was_processed(), 4))
                string = "p" + str_prod_number + "; " + str_time_creation + "; " + str_time_when_was_processed
                resultsTableWidget.setItem(t_row_index, t_col_index + buffer.get_size() + counter,
                                           QTableWidgetItem(string))
            else:
                string = ""
                resultsTableWidget.setItem(t_row_index, t_col_index + buffer.get_size() + counter,
                                           QTableWidgetItem(string))
            counter += 1

    static_values.table_row += 1
    resultsTableWidget.resizeColumnsToContents()


def process_queueing_system(static_values: StaticValues, iteration, producers, consumers, buffer,
                            resultsTableWidget: QtWidgets.QTableWidget,
                            total_table1: QtWidgets.QTableWidget,
                            # total_table2: QtWidgets.QTableWidget,
                            total_table3: QtWidgets.QTableWidget,
                            processed_requests, events, isFinal, utilization_rate, resultsTotal):
    resultsTableWidget.setRowCount(static_values.table_rows + iteration)

    if iteration == 0:
        # Генерируем заявки во всех источниках только при первой итерации
        for producer in producers:
            producer.generate_requests()
    else:
        # На всех итерациях, кроме 1-ой генерируем заявку только в первом источнике,т.к список источников отсортирован
        producers[0].generate_requests()

    producers.sort(key=Producer.comparator_key)
    fastest_req: Request = copy.deepcopy(producers[0].get_last_generated_req())

    past_events = []
    for el in events:
        if el.get_time_when_was_processed() < fastest_req.get_time_of_creation():
            past_events.append(el)
            events.remove(el)
    past_events.sort(key=Request.get_time_when_was_processed)

    # Сначала выводим заявки, которые были обработаны в интервалы между моментами генерации заявок
    # Контрольные точки - моменты генерации заявок

    string = "Processed"
    for el in past_events:
        for i in consumers:
            if i.get_last_processed_request() is not None:
                if i.get_last_processed_request().get_time_of_creation() == el.get_time_of_creation():
                    i.reset_last_processed_req()
        # static_values.current_step += 1
        print_system_state(el.get_time_when_was_processed(), el.get_producer_number(), el, string, static_values,
                           resultsTableWidget, consumers, buffer)

    # Сохраняем состояние указателя, чтобы вернуть его, если не найдется свободного прибора

    # Начинаем обход приборов в поисках свободного
    counter = 0
    for consumer in consumers:
        counter += 1

        if consumer.get_req_proc_end_time() < fastest_req.get_time_of_creation():
            # Если прибор освободился

            if not buffer.is_empty():
                # Если в буфере есть запросы
                req_from_buffer: Request = buffer.pop_request()

                consumer.process_request(req_from_buffer, processed_requests, fastest_req.get_time_of_creation(),
                                         utilization_rate, resultsTotal, static_values)

                events.append(consumer.get_last_processed_request())
                break

            else:
                consumer.process_request(fastest_req, processed_requests, fastest_req.get_time_of_creation(),
                                         utilization_rate, resultsTotal, static_values)

                events.append(consumer.get_last_processed_request())
                static_values.increase_by_one(len(consumers) - 1)
                break

        if counter == len(consumers):
            # Если прибор занят, кладем заявку в буфер
            buffer.put(fastest_req, resultsTotal)

    string = "Generated"
    print_system_state(fastest_req.get_time_of_creation(), fastest_req.get_producer_number(), None, string,
                       static_values,
                       resultsTableWidget, consumers, buffer)

    if isFinal:
            # reqs_count 0
            # tow 1`
            # top 2

            # por
            # tis

        for i in range(len(producers)):
            row = i + 1
            string = "Producer" + str(i)
            total_table1.setItem(row, 0, QTableWidgetItem(string))
            string = str(resultsTotal[i][0])
            total_table1.setItem(row, 1, QTableWidgetItem(string))

            string = str(resultsTotal[i][1] / resultsTotal[i][0])
            total_table1.setItem(row, 2, QTableWidgetItem(string))
            string = str(resultsTotal[i][2] / resultsTotal[i][0])
            total_table1.setItem(row, 3, QTableWidgetItem(string))
            string = str(resultsTotal[i][3] / resultsTotal[i][0])
            total_table1.setItem(row, 4, QTableWidgetItem(string))


        for i in range(len(consumers)):
            row = i + 1
            string = "Consumer" + str(i)
            total_table3.setItem(row, 0, QTableWidgetItem(string))
            string = str(utilization_rate[i] / fastest_req.get_time_of_creation())
            total_table3.setItem(row, 1, QTableWidgetItem(string))

        total_table1.resizeColumnsToContents()
        # total_table2.resizeColumnsToContents()
        total_table3.resizeColumnsToContents()
