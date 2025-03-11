import sys
sys.path.append('/c:/Users/essam/5eResourceSite/Backend/API')
import pytest

import getResource


@pytest.mark.parametrize("spell",
                         ["prestidigitation", "wish", "acid-arrow", "", "hellish-rebuke"])
def test_get_spells(spell):
    spell = getResource.get_spells(spell)
    print(spell)

@pytest.mark.parametrize("spell",
                         ["tiefling", "dwarf", "human", "", "half-orc", "half-elf", "elf",
                          "halfling", "dragonborn"])
def test_get_spells(spell):
    spell = getResource.get_lineage(spell)
    print(spell)


@pytest.mark.parametrize("class_name",
                         ["", "barbarian", "bard", "cleric", "monk", "fighter", "paladin",
                          "ranger", "rogue", "sorcerer", "warlock", "wizard"])
def test_get_spells(class_name):
    class_info = getResource.get_class(class_name)
    print(class_info)