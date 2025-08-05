import React, { useState, useEffect } from 'react';
import * as utils from '../utils/index'

function NPCCreator() {
    const [heroChecked, setHeroChecked] = useState(false);

    const [firstName, setFirstName] = useState("");
    const [firstNameLock, setFirstNameLock] = useState(false);

    const [lastName, setLastName] = useState("");
    const [lastNameLock, setLastNameLock] = useState(false);

    const [lineage, setLineage] = useState("");
    const [lineageLock, setLineageLock] = useState(false);

    const [className, setClassName] = useState("");
    const [classLock, setClassLock] = useState(true);

    const [level, setLevel] = useState("1");
    const [levelLock, setLevelLock] = useState(true);

    const [background, setBackground] = useState({});
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

      const backgroundsRes = await fetch("https://api.open5e.com/v2/backgrounds");
      const backgroundsJson = await backgroundsRes.json();
      setBackgrounds(backgroundsJson.results || []);

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
    setClassName("");
    setLevel("1");
    setBackground({ name: "", desc: "" });
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
     try {
    let backgroundData = background;

    if (heroChecked && background?.name) {
      const bgResponse = await fetch(
        `http://localhost:5000/api/backgrounds?background=${encodeURIComponent(background.name)}`
      );

      if (!bgResponse.ok) throw new Error(`Failed to fetch background: ${bgResponse.statusText}`);
      backgroundData = await bgResponse.json();
      setBackground(backgroundData); 
    }
    else{
      setBackground({name:"", desc: "No description available"})
      setClassName("")
    }

    const fullName = `${firstName} ${lastName}`.trim();

    const npc = {
      name: fullName,
      race: lineage,
      class: className,
      level: level,
      background: backgroundData.name,
      description: backgroundData.desc,
      isHero: heroChecked,
    };

    console.log("Generated NPC:", npc);
  } catch (error) {
    console.error("Error generating NPC:", error);
  }
};

  const randomizeNPC = async () => {
    setLoading(true);
    try {
      const chosenLineage = lineageLock && lineage ? lineage : getRandomItem(lineages);
      if (!lineageLock) setLineage(chosenLineage);

      if (!classLock) setClassName(getRandomItem(classes));

      if (!firstNameLock || !lastNameLock) {
        const gender = Math.random() < 0.5 ? "male" : "female";
        const { firstName, lastName } = generateNameByLineage(chosenLineage, gender);
        if (!firstNameLock) setFirstName(firstName);
        if (!lastNameLock) setLastName(lastName);
      }

      if (!backgroundLock && backgrounds.length > 0) {
        const randomBackground = getRandomItem(backgrounds);
        const bgResponse = await fetch(`http://localhost:5000/api/backgrounds?background=${encodeURIComponent(randomBackground.name)}`);
        if (!bgResponse.ok) throw new Error(`Failed fetching background details: ${bgResponse.statusText}`);
        const bgDetail = await bgResponse.json();
        setBackground(bgDetail);
      }

      
    } catch (error) {
      console.error("Error during NPC randomization:", error);
    } finally {
      setLoading(false);
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
            onChange={e => setLastName(e.target.value)}
          />
          <input
            type="checkbox"
            checked={lastNameLock}
            onChange={e => setLastNameLock(e.target.checked)}
          /> Lock
        </label>

      </div>
      <div>
        <label/>Lineage
        <select
      value={lineage}
      disabled={lineageLock}
      onChange={e => setLineage(e.target.value)}
    >
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
      <div>
        <label>Class
          <select
          value={className}
          disabled={!heroChecked || classLock}
          onChange={e => setClassName(e.target.value)}>
      {classes.map((l, idx) => (
        <option key={idx} value={l}>
          {l}
        </option>
      ))}
          </select>
          <input
          type="checkbox"
          checked={classLock}
          onChange ={e => setClassLock(e.target.checked)}/>Lock
        </label>
      </div>
      <div>
        <label>
          Background
          <select
          value={background.name || ""}
          disabled={!heroChecked || backgroundLock}
           onChange={e => {
      const selected = backgrounds.find(b => b.name === e.target.value);
      setBackground(selected);
    }}>
              {backgrounds.map((b, idx) => (
      <option key={idx} value={b.name}>
        {b.name}
      </option>
          ))}
          </select>
        </label>
        <input
        type="checkbox"
        checked={backgroundLock}
        onChange={e => setBackgroundLock(e.target.checked)}/>
        Lock
      </div>
      <button onClick={generateNPC}>Generate NPC</button>
      <button onClick={randomizeNPC}>Randomize NPC</button>
      <div>
        <textarea
      rows="5"
      cols="40">

      </textarea>

      </div>
      {loading && <div>Randomizing NPC...</div>}
    </div>
    
  );
}

export default NPCCreator;
