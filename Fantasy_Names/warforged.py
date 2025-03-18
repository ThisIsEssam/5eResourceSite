from Fantasy_Names.data import warforged_data
from Fantasy_Names.language import Language


class warforged(Language):

    @classmethod
    def _name1_male(cls) -> str:
        cols = [warforged_data["name1_col1"], warforged_data["name1_male_suffixes"]]
        return cls._name_from_lists(cols)

    @classmethod
    def _name1_female(cls) -> str:
        cols = [warforged_data["name1_col1"], warforged_data["name1_female_suffixes"]]
        return cls._name_from_lists(cols)

    @classmethod
    def _name2(cls) -> str:
        cols = [warforged_data["name2_col1"], warforged_data["name2_col2"]]
        name = cls._name_from_lists(cols)
        return name


warforged = warforged.name