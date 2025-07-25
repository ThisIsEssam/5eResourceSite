export const elfData =  {
    "name1_col1": [
        "Ra",
        "Ga",
        "Ge",
        "Ei",
        "Ai",
        "Ie",
        "Gwe",
        "The",
        "A",
        "E",
        "Fa",
        "Ca",
    ],
    "name1_col2": ["Dral", "Than", "Val", "Rath", "Thar", "Ran", "Ral", "Nal"],
    "name1_female_suffixes": ["a", "ia", "ys", "yn"],
    "name1_male_suffixes": ["on", "ar", "ion", "as", "el", "or"], 
     "name2_col1": [ 
        "Al", "El", "Gal", "Mel", "Nel", "Rel", "Tal", "Val"
    ],
    "name2_col2": [
        "Nther",
        "Nion",
        "Nonus",
        "Niath",
        "Naire",
        "Nuth",
        "Neus",
        "Naine",
        "viel",
    ],
    "transformations": [
        {"input": "A", "outputs": ["a", "a", "e", "e", "ia", "ea", "y"]},
        {"input": "E", "outputs": ["a", "e"]},
        {"input": "N", "outputs": ["n", "m", "l", "r"]},
        {"input": "R", "outputs": ["l", "r"]},
        {"input": "M", "outputs": ["n", "m"]}
    ],
}