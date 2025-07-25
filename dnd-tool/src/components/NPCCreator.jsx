import React, { useState, useEffect } from 'react';
import * as utils from '../utils/index'

function NPCCreator() {
    const [heroChecked, setHeroChecked] = useState(false);

    const [firstName, setFirstName] = useState("");
    const [firstNameLock, setFirstNameLock] = useState(false);

    const [lastName, setLastName] = useState("");
    const [lastNameLock, setLastNameLock] = useState(false);

    const [lineage, setLineage] = useState("");
    const [lineageLock, setLineageLock] = useState(true);

    const [className, setClassName] = useState("");
    const [classLock, setClassLock] = useState(true);

    const [level, setLevel] = useState("1");
    const [levelLock, setLevelLock] = useState(true);

    const [background, setBackground] = useState("");
    const [backgroundLock, setBackgroundLock] = useState(true);

    const [lineages, setLineages] = useState([]);
    const [classes, setClasses] = useState([]);
    const [backgrounds, setBackgrounds] = useState([]);

    const [loading, setLoading] = useState(false);

  useEffect(() => {
  async function fetchData() {
    try {
      const lineagesRes = await fetch("https://www.dnd5eapi.co/api/races");
      const lineagesJson = await lineagesRes.json();
      const lineageList = [...lineagesJson.results.map((r) => r.name), "Warforged"];
      setLineages(lineageList);

      const classesRes = await fetch("https://www.dnd5eapi.co/api/classes");
      const classesJson = await classesRes.json();
      setClasses(classesJson.results.map((c) => c.name));

      const backgroundsRes = await fetch("https://api.open5e.com/v2/backgrounds/");
      const backgroundsJson = await backgroundsRes.json();
      setBackgrounds(backgroundsJson.results.map((b) => b.name));
    } catch (error) {
      console.error("Failed to load dropdown data", error);
    }
  }
  fetchData();
}, []);
    useEffect(() => {
  if (heroChecked) {
    setClassLock(false);
    setLevelLock(false);
    setBackgroundLock(false);
  } else {
    setClassLock(true);
    setLevelLock(true);
    setBackgroundLock(true);
  }
}, [heroChecked]);




  function generateNameByLineage(lineage, gender, subtype="Anglo") {
  switch (lineage.toLowerCase()) {
    case 'human':
      return utils.generateHumanName(gender, subtype);
    case 'dragonborn':
      return utils.generateDragonbornName(gender);
    case 'dwarf':
      return utils.generateDwarfName(gender);
    case 'elf':
      return utils.generateElfName(gender)
    case 'gnome':
      return utils.generateGnomeName(gender)
    case 'orc':
      return utils.generateOrcName(gender)
    case'tiefling':
      return utils.generateTieflingName(gender)
    case 'warforged':
      return utils.generateWarforgedName(gender)
    case 'halfling':
      return utils.generateHalflingName(gender)
    case 'half-elf':
      return {
    firstName: (utils.generateElfName(gender).firstName),
    lastName: utils.generateHumanName(gender, subtype).lastName,
  }
    case 'half-orc':
      return {
    firstName: (utils.generateOrcName(gender).firstName),
    lastName: utils.generateHumanName(gender, subtype).lastName,
  }
    default:
      return { firstName: "Nameless", lastName: "One" };
  }
}
  const getRandomItem=(array) => {
    return array[Math.floor(Math.random() * array.length)];
  };


  const generateNPC = async () => {
    
  };

  const randomizeNPC = () => {
    if (!firstNameLock || !lastNameLock) {
      const gender = Math.random() < 0.5 ? "male" : "female";
      const chosenLineage = lineageLock && lineage ? lineage : getRandomItem(lineages);
      const { firstName, lastName } = generateNameByLineage(chosenLineage, gender);

      if (!firstNameLock) setFirstName(firstName);
      if (!lastNameLock) setLastName(lastName);
      if (!lineageLock) setLineage(chosenLineage);
    }
  };

  return (
    <div>
      <h2>D&D NPC Creator</h2>
      <label>
        Hero
        <input
          type="checkbox"
          checked={heroChecked}
          onChange={e => setHeroChecked(e.target.checked)}
        />
      </label>
      <div>
        <label>
          First Name
          <input
            type="text"
            value={firstName}
            disabled={firstNameLock}
            onChange={e => setFirstName(e.target.value)}
          />
          <input
            type="checkbox"
            checked={firstNameLock}
            onChange={e => setFirstNameLock(e.target.checked)}
          /> Lock
        </label>
      </div>
      <div>
        <label>
          Last Name
          <input
          type="text"
          value={lastName}
          disabled={lastNameLock}
          onChange={e => setLastNameLock(e.target.checked)}
           />
           <input
           type="checkbox"
           checked={lastNameLock}
           onChange={e =>setLastNameLock(e.target.checked)}>
           </input>
           Lock
        </label>

      </div>
      <div>
        <label/>Lineage
        <select
      value={lineage}
      disabled={lineageLock}
      onChange={e => setLineage(e.target.value)}
    >
      <option value="">-- Select a lineage --</option>
      {lineages.map((l, idx) => (
        <option key={idx} value={l}>
          {l}
        </option>
      ))}
    </select>
    <input
      type="checkbox"
      checked={lineageLock}
      onChange={e => setLineageLock(e.target.checked)}
    /> Lock
      </div>
      <button onClick={generateNPC}>Generate NPC</button>
      <button onClick={randomizeNPC}>Randomize NPC</button>

      {loading && <div>Loading spinner or animation here...</div>}
    </div>
  );
}

export default NPCCreator;
