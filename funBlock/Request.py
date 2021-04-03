class Request:

    def __init__(self, producer_number: int, time_of_creation: float, time_when_was_processed=None):
        self.__producer_number = producer_number
        self.__time_of_creation = time_of_creation
        self.__time_with_waiting = time_of_creation
        self.__time_when_was_processed = time_when_was_processed
        self.__consumer_number = None

    def get_producer_number(self):
        return self.__producer_number

    def get_time_of_creation(self):
        return self.__time_of_creation

    def get_time_with_waiting_in_buf(self):
        return self.__time_with_waiting

    def set_time_when_was_processed(self, time: float):
        self.__time_when_was_processed = time

    def set_time_with_waiting_in_buf(self, time: float):
        self.__time_with_waiting = time

    def set_consumer_number(self, number: int):
        self.__consumer_number = number

    def get_consumer_number(self):
        return self.__consumer_number

    def get_time_when_was_processed(self):
        return self.__time_when_was_processed
