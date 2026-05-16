# 🎲 5e NPC Generator

You have a tavern fully decked out in interesting lore, characters and backstories waiting for your crew of adventurers. That's when...they decide to head in the opposite direction towards a run-down shack with nothing on the inside. No problem, I've got you covered.

**5e NPC Generator** is a D&D 5th Edition tool that instantly creates fully-formed NPCs on the fly — complete with lineage, class, lineage-appropriate name, and spells (for the magic-users). Whether you need a grizzled Spartan fighter with a pet chicken and an obsession with spears or an Irish gnome time wizard who was once a university professor, I've got it all. 

Built for Dungeon Masters who like to improvise (or just forgot to prep).

> ⚠️ This project is actively in development. Expect new features, rough edges, and occasional dragons.

### Backend
- **Custom Python modules** (`Backend/`) with an object-oriented NPC model:
  - `Hero` class — for adventurer-type NPCs with a class, lineage, and optional spells
  - `Commoner` class — for civilian NPCs with a lineage and name
  - `APIHelper` — a wrapper around the [D&D 5e REST API](https://www.dnd5eapi.co/) for fetching live game data (classes, lineages, spells)
- **`python-dotenv`** — environment variable management via a `.env` file (API key stored as `KEY`)

### Frontend
- **PyQt** (`Frontend/PyQT/`) — a desktop GUI for interacting with the NPC generator locally
- **JavaScript** (`dnd-tool/`) — a separate web-based tool, alternative UI in React.js

### Data
- **`Fantasy_Names` module** — a custom local library that generates lore-appropriate names for all supported 5e lineages:
  - Dwarf, Elf, Gnome, Dragonborn, Orc, Halfling, Tiefling, Human (diverse), Half-Elf, Half-Orc
- **D&D 5e API** — live source of truth for class lists, racial lineages, and available spells
