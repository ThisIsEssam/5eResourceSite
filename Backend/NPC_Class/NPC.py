class NPC:
    def __init__(self, fname, lname, race):
        self.first_name = fname
        self.last_name = lname
        self.race = race

    @classmethod
    def set_name(cls, fname, lname):
        cls.first_name = fname
        cls.last_name = lname


    @classmethod
    def set_race(cls, race):
        cls.race = race


