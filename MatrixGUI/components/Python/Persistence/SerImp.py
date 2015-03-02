from Serializable import Serializable
from NonSer import NonSer

class SerImp(NonSer, Serializable):

    def __init__(self):
        super().__init__()
        print("Init of SerImp")

    def serialize(self):
        super().serialize()
        print("serialize of SerImp")
