from abc import ABCMeta, abstractmethod

class Serializable(metaclass=ABCMeta):

    @abstractmethod
    def serialize(self):
        return self.__dict__

    @staticmethod
    @abstractmethod
    def deserialize(serial):
        return
