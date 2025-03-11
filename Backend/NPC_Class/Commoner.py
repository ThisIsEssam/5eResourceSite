from Backend.NPC_Class.NPC import NPC

class Commoner(NPC):
    def __init__(self, fname, lname, race):
        super().__init__(fname, lname, race)
        self.class_name = "Commoner"
