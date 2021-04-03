import random

from funBlock.Request import Request


class Producer:

    def __init__(self, number: int, bottom: float, top: float, start_time=0.0):
        """top - upper value of the interval for the distribution function
        bottom - lower value of the interval for the distribution """
        self.__number = number
        self.__top = top
        self.__bottom = bottom
        self.__start_time = start_time
        self.__last_generated_req = None
        self.__generated_requests_count = 0

    def generate_requests(self) -> Request:
        delta = random.uniform(self.__bottom, self.__top)
        if self.__last_generated_req is None:
            self.__last_generated_req = Request(self.__number, self.__start_time + delta)
        else:
            self.__last_generated_req = Request(self.__number, self.__last_generated_req.get_time_of_creation() + delta)
            self.__generated_requests_count += 1
        return self.__last_generated_req

    def get_generated_requests_count(self):
        return self.__generated_requests_count

    def get_last_generated_req(self) -> Request:
        return self.__last_generated_req

    def get_number(self) -> int:
        return self.__number

    def comparator_key(self):
        return self.__last_generated_req.get_time_of_creation()
