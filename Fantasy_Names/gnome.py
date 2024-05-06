from Fantasy_Names.data import gnome_data
from Fantasy_Names.language import Language


class gnome(Language):
    transformations = gnome_data["transformations"]

    @classmethod
    def _name1_male(cls) -> str:
        cols = [gnome_data["name1_col1"], gnome_data["name1_male_suffixes"]]
        return cls._name_from_lists(cols)

    @classmethod
    def _name1_female(cls) -> str:
        cols = [gnome_data["name1_col1"], gnome_data["name1_female_suffixes"]]
        return cls._name_from_lists(cols)

    @classmethod
    def _name2(cls) -> str:
        cols = [gnome_data["name2_col1"], gnome_data["name2_col2"]]
        name = cls._name_from_lists(cols)
        return name


gnome = gnome.name
