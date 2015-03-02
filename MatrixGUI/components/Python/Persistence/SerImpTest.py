from Serializable import Serializable

class SerImpTest(Serializable):

    def __init__(self, att_str="A string", att_int=7, att_list=None,\
            att_dict=None, att_obj=None):
        print("Init of SerImpTest")
        self.att_str = att_str
        self.att_int = att_int
        self.att_list = [1, "deux"] if att_list==None else att_list
        self.att_dict = {'one': 1, 'two':"2"}if att_dict==None else att_dict
        self.att_obj = object() if att_obj==None else att_obj

    def serialize(self):
        return super().serialize()

    @staticmethod
    def deserialize(serial):
        return SerImpTest(\
                att_str = serial['att_str'],\
                att_int = serial['att_int'],\
                att_list = serial['att_list'],\
                att_dict = serial['att_dict'],\
                att_obj = object())
