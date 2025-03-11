class NPC:
    def __init__(self, fname, lname, race):
        self.first_name = fname
        self.last_name = lname
        self.race = race

    def set_name(self, fname, lname):
        self.first_name = fname
        self.last_name = lname

    def set_race(self, race):
        self.race = race