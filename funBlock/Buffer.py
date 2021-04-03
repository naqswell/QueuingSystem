import copy

from funBlock.Request import Request


class Buffer:

    def __init__(self, size: int):
        self.__ptr = []
        self.__capacity = int(size)
        self.__requests = []

    def get_str_requests_time(self):
        string = ""
        for i in self.__requests:
            if i is not None:
                string += str(i.get_time_of_creation())
        return string

    def get_size(self):
        return self.__capacity

    def put(self, request: Request, resultsTotal):
        if len(self.__requests) < self.__capacity:
            self.__requests.append(request)
            return
        if len(self.__requests) > 0:
            rev_sorted_list = copy.deepcopy(self.__requests)
            rev_sorted_list.sort(key=Request.get_time_of_creation, reverse=True)
            removed_req = rev_sorted_list.pop()

            for i in range(len(self.__requests)):
                if removed_req.get_time_of_creation() == self.__requests[i].get_time_of_creation():
                    req = self.__requests.pop(i)
                    resultsTotal[req.get_producer_number()][3] += 1
                    break

            self.__requests.append(request)

    def pop_request(self):
        return self.__requests.pop()

    def is_empty(self):
        return len(self.__requests) == 0

    def get_requests(self):
        return self.__requests
