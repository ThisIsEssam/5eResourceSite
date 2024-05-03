from Backend.NPC_Class.NPC import NPC

class Hero(NPC):
    def __init__(self, fname, lname, race, class_name):
        super().__init__(fname, lname, race)

        self.class_name = class_name

    @classmethod
    def set_class(cls, class_name):
        cls.class_name = class_name








