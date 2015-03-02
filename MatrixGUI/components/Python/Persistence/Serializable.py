from abc import ABCMeta, abstractmethod

class Serializable(metaclass=ABCMeta):

    @abstractmethod
    def serialize(self):
        print("serialize of Serializable")
