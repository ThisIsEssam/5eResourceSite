from Backend.NPC_Class.NPC import NPC

class Hero(NPC):
    def __init__(self, fname, lname, race, class_name):
        super().__init__(fname, lname, race)
        self.class_name = class_name

    def set_class(self, class_name):
        self.class_name = class_name