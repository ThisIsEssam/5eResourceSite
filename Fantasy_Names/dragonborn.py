from Fantasy_Names.data import dragonborn_data
from Fantasy_Names.language import Language


class dragonborn(Language):
    transformations = dragonborn_data["transformations"]

    @classmethod
    def _name1_male(cls) -> str:
        cols = [dragonborn_data["name1_col1"], dragonborn_data["name1_male_suffixes"]]
        return cls._name_from_lists(cols)

    @classmethod
    def _name1_female(cls) -> str:
        cols = [dragonborn_data["name1_col1"], dragonborn_data["name1_female_suffixes"]]
        return cls._name_from_lists(cols)

    @classmethod
    def _name2(cls) -> str:
        cols = [dragonborn_data["name2_col1"], dragonborn_data["name2_col2"]]
        name = cls._name_from_lists(cols)
        return name


dragonborn = dragonborn.name