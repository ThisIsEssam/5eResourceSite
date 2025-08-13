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

    const [chatLock, setChatLock] = useState(true)

    const [chatHistory, setChatHistory] = useState([]);


    

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

      let allBackgrounds = [];
      let nextUrl = "https://api.open5e.com/v2/backgrounds/";
      while (nextUrl) {
        const res = await fetch(nextUrl);
        const json = await res.json();
        allBackgrounds = allBackgrounds.concat(json.results);
        nextUrl = json.next; 
      }
      setBackgrounds(allBackgrounds);

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


  function generateNameByLineage(lineage, gender=gender, subtype=getRandomItem(["Anglo", "French"])) {
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

const sendToLLM = async(prompt, chatHistory) =>{
  setLoading(true);
  const res = await fetch("http://localhost:5000/api/llm", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ prompt, chat_history: chatHistory })
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.error || "Failed to fetch LLM response");
  }
  var chatBox = document.getElementById("chatResponse");
  var response = await res.json();
  chatBox.value = ''
  for (const item of response.chat_history) {
    if (item.content && item.content.includes("Role play in")) {
      continue;
    }
    if (item.role == "assistant"){
       chatBox.value += `🧙 ${firstName}: ${item.content}\n\n`;
    }
    else{
       chatBox.value += `🗣️ User: ${item.content}\n\n`;
    }
    
  }
  setChatHistory(response.chat_history);
  setLoading(false);
  return response;  // { response, chat_history }
}


  const generateNPC = async () => {
    var chatBox = document.getElementById("chatResponse");
    chatBox.value = ''
    setChatHistory([])
    setLoading(true);
     try {
    let backgroundData = background;
    const fullName = `${firstName} ${lastName}`.trim();
    var prompt = "Role play in the first person as a D&D "+ lineage +" non-playable character named "+fullName+". Have your own motivations and goals. Start off by introducing yourself, stay in first person."
  
    if (heroChecked && background?.name) {
      const bgResponse = await fetch(
        `http://localhost:5000/api/backgrounds?background=${encodeURIComponent(background.name)}`
      );

      if (!bgResponse.ok) throw new Error(`Failed to fetch background: ${bgResponse.statusText}`);
      backgroundData = await bgResponse.json();
      setBackground(backgroundData);
      prompt += " You are a level "+ level+" "+className+" with a "+backgroundData.name+" background. "+ backgroundData.desc+" Add verbal quirks based on your character's attributes. Keep your responses under 50 words." 
    }
    else{
      setBackground({name:"", desc: "No description available"})
      setClassName("")
    }
    await sendToLLM(prompt, []);

  } catch (error) {
    console.error("Error generating NPC:", error);
  }
  setChatLock(false)
  setLoading(false)
};

  const randomizeNPC = async () => {
    setLoading(true);
    setChatLock(true)
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
    
    <div >
      <div className='main-title'>
        <h1 className="title is-1" >D&D NPC Creator</h1>
      <h2 className="subtitle is-3">Bring your NPC's to life!</h2>
      </div>
      
      <div className='main-flex'>
        <div className='box generate-box'>
        <h1 className="subtitle is-4
         generate-heading" >Character Profile</h1>
      <div className="field">
        <label>
        Hero
        <input
          type="checkbox"
          checked={heroChecked}
          onChange={e => setHeroChecked(e.target.checked)}
        />
      </label>
      </div>
      <div className="field">
        <label> First Name </label><input
            type="checkbox"
            checked={firstNameLock}
            onChange={e => setFirstNameLock(e.target.checked)}
          /> Lock
          <div className='control'>
             <input
            className='input'
            type="text"
            value={firstName}
            disabled={firstNameLock}
            onChange={e => setFirstName(e.target.value)}
            placeholder='Enter First Name...'
              /> 
          </div>
      </div>
      <div className="field">
        <label>Last Name </label>
        <input
            type="checkbox"
            checked={lastNameLock}
            onChange={e => setLastNameLock(e.target.checked)}
          /> Lock
        <div>
          <input
          className='input'
          placeholder='Enter Last Name...'
            type="text"
            value={lastName}
            disabled={lastNameLock}
            onChange={e => setLastName(e.target.value)}
          />
        </div>
      </div>
      <div className="field">
        <label>Lineage</label>
        <div className='control'><div className='select'>
          <select
                value={lineage}
                disabled={lineageLock}
                onChange={e => setLineage(e.target.value)}>
                {lineages.map((l, idx) => (
                  <option key={idx} value={l}>
                    {l}
                  </option>
                ))}
              </select>
        </div><input
      type="checkbox"
      checked={lineageLock}
      onChange={e => setLineageLock(e.target.checked)}
    /> Lock</div>
      </div>
      <div className="field">
        <label>Class</label>
        <div className='control'>
          <div className='select'>
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
          </div><input
          type="checkbox"
          checked={classLock}
          onChange ={e => setClassLock(e.target.checked)}/>Lock
        </div>
        
      </div>
      <div className="field">
        <label>Background</label>
        <div className='control'>
          <div className='select'>
            <select
          value={background.name}
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
          </select></div><input
        type="checkbox"
        checked={backgroundLock}
        onChange={e => setBackgroundLock(e.target.checked)}/>
        Lock
        </div>
        
      </div>
      <div className='field'>
        <button className="button is-primary block" onClick={generateNPC}>Generate NPC</button>
      <button className="button is-primary" onClick={randomizeNPC}>Randomize NPC</button>
      </div>
      </div>
      
      <div className='chat-div'>
        <textarea
        className='textarea chat'
        readOnly
        rows="15"
        cols="60"
        id="chatResponse"
        disabled={chatLock}
        ></textarea>
        <div style={{ display: "flex", alignItems: "center", marginTop: "1em" }}>
          <input
        type="text"
        size={"55"}
        disabled={chatLock}
        id="promptText"
        className='chat-send input'
        />
        <button
        disabled={chatLock} 
        onClick={() => {
          sendToLLM(document.getElementById("promptText").value, chatHistory);
          document.getElementById("promptText").value = '';
        }}
        className="button is-small send-button">Send</button>
        </div>
      </div>
      </div>
      
      

      <div>
        
      </div>
      {loading && <div>Please wait...</div>}
    </div>
    
  );
}

export default NPCCreator;
