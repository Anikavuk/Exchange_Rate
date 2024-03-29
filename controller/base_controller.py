from abc import ABC, abstractmethod


class BaseController(ABC):

    @abstractmethod
    def do_GET(self):
        pass

    def do_POST(self):
        pass

    def do_PATCH(self):
        pass


