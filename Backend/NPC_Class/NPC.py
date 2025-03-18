class NPC:
    def __init__(self, fname, lname, lineage):
        self.first_name = fname
        self.last_name = lname
        self.lineage = lineage

    def set_name(self, fname, lname):
        self.first_name = fname
        self.last_name = lname

    def set_race(self, lineage):
        self.lineage = lineage