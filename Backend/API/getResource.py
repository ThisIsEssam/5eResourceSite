import json
from pprint import pprint
from functools import lru_cache
import json
import os
from APIHelper import ApiHelper 

@lru_cache(maxsize=128)
def get_spells(spell=""):
    response = ApiHelper.request("GET", payload="",
                                 headers="", url="https://www.dnd5eapi.co/api/spells/" + spell,
                                 expected_status_code=200)
    return ApiHelper.return_json(response)

@lru_cache(maxsize=128)
def get_lineage(index=""):

    response = ApiHelper.request("GET", payload="",
                                 headers="", url="https://www.dnd5eapi.co/api/races/" + index,
                                 expected_status_code=200)
    return ApiHelper.return_json(response)

@lru_cache(maxsize=128)
def get_class(class_name=""):
    response = ApiHelper.request("GET", payload="",
                                 headers="", url="https://www.dnd5eapi.co/api/classes/" + class_name,
                                 expected_status_code=200)
    return ApiHelper.return_json(response)




file_path = os.path.join(os.path.dirname(__file__), "backgrounds.json")
with open(file_path, "r") as f:
    BACKGROUND_DESCRIPTIONS = json.load(f)

def get_background_description(background):
    print("GETTING BACKGROUND")
    return BACKGROUND_DESCRIPTIONS.get(background, "No description available.")

BACKGROUND_PREFIXES = {
    "a5e-ag": ["acolyte", "artisan", "charlatan", "criminal","cultist", "entertainer", "exile", "farmer", "folk-hero", "gambler",
               "guard", "guildmember", "hermit", "marauder", "noble", "outlander", "sage", "sailor", "soldier", "trader",
               "urchin"],
    "a5e-ddg": ["deep-hunter", "dungeon-robber", "escapee-from-below", "imposter"],
    "a5e-gpg": ["cursed", "haunted"],
    "tdcs": ["crime-syndicate-member", "elemental-warden", "fate-touched", "lyceum-student", "recovered-cultist"],
    "toh": ["desert-runner", "court-servant", "destined", "diplomat", "forest-dweller", "former-adventurer", "freebooter",
            "gamekeeper", "innkeeper", "mercenary-company-scion", "mercenary-recruit", "monstrous-adoptee",
            "mysterious-origins", "northern-minstrel", "occultist", "parfumier", "sentry", "trophy-hunter"],
    "open5e":["scoundrel", "con-artist"]
}
def get_backgrounds(background=""):
    background = background.lower().replace(" ", "-")
    background_plus = background
    for prefix, backgrounds in BACKGROUND_PREFIXES.items():         
        if background in backgrounds:
            background_plus = f"{prefix}_{background}"
            break
    response = ApiHelper.request("GET", payload="",
                                 headers="", url="https://api.open5e.com/v2/backgrounds/" + background_plus,
                                 expected_status_code=200)
    if background == "":
        return ApiHelper.return_json(response)

    response_json = response.json()
    description = response_json["desc"]
    if "[No description provided]" in description:
        print("GETTING DESCRIPTION")
        response_json["desc"] = get_background_description(background)
    return response_json

