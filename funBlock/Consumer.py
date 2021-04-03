import copy
import random

from funBlock.Request import Request


class Consumer:

    def __init__(self, number: int, lambd: float, downtime=0.0, req_proc_end_time=0.0):
        self.__number = number
        self.__downtime = downtime
        self.__req_arrival_time = float('-inf')
        self.__req_proc_end_time = req_proc_end_time
        self.__lambd = lambd
        self.__last_processed_req = None
        self.__processed_requests = []

    def process_request(self, req: Request, processed_requests, current_time_is_sys, utilization_rate, resultsTotal,
                        static_values):
        # Считаем время простоя относительно времени, когда была обработана последняя заявка
        static_values.current_step += 1
        self.__downtime += current_time_is_sys - self.__req_proc_end_time
        # Устанавливаем время, когда будет обработана новая зааявка
        delta = random.expovariate(self.__lambd)
        self.__req_proc_end_time = current_time_is_sys + delta
        utilization_rate[self.__number] += delta
        # utilization_rate[self.__number] += delta
        # utilization_rate[self.__number] = current_time_is_sys
        req.set_time_when_was_processed(self.__req_proc_end_time)
        req.set_time_with_waiting_in_buf(current_time_is_sys)
        # Сохраняем время прибытия новой заявки и саму заявку
        self.__req_arrival_time = current_time_is_sys
        processed_requests.append(req)
        self.__last_processed_req = copy.deepcopy(req)

        resultsTotal[req.get_producer_number()][0] += 1
        resultsTotal[req.get_producer_number()][1] += req.get_time_when_was_processed() - req.get_time_of_creation()
        resultsTotal[req.get_producer_number()][
            2] += req.get_time_when_was_processed() - req.get_time_with_waiting_in_buf()

    def get_last_processed_request(self) -> Request:
        if self.__last_processed_req is not None:
            self.__last_processed_req.set_consumer_number(self.__number)
        return self.__last_processed_req

    def reset_last_processed_req(self):
        self.__last_processed_req = None

    def get_req_arrival_time(self) -> float:
        return self.__req_arrival_time

    def get_req_proc_end_time(self) -> float:
        return self.__req_proc_end_time

    def get_number(self):
        return self.__number
