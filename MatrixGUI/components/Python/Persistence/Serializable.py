from abc import ABCMeta, abstractmethod

class Serializable(metaclass=ABCMeta):

    @abstractmethod
    def serialize(self):
        return self.__dict__

    @abstractmethod
    def deserialize(self, serial):
        for key in serial:
            setattr(self,key,serial[key])
