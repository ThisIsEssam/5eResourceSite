import { dragonbornData as dragonBorn }  from "../data/dragonbornData" 

function randomItem(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function maybe(probabilityPercent) {
  return Math.random() * 100 < probabilityPercent;
}

function applyTransformation(str, transformations) {
  let result = str;
  transformations.forEach(trans => {
    const { input, outputs } = trans;
    const regex = new RegExp(input, 'g');
    result = result.replace(regex, () => {
      return outputs[Math.floor(Math.random() * outputs.length)];
    });
  });
  return result;
}

function generateFirstName(gender) {
  const col1 = randomItem(dragonBorn.name1_col1);

  let name;
  if (gender === "male") {
    if (maybe(50)) {
      // name1_col1 + name1_col2
      name = col1 + randomItem(dragonBorn.name1_col2);
    } else {
      // name1_col1 + male suffix
      name = col1 + randomItem(dragonBorn.name1_male_suffixes);
    }
  } else if (gender === "female") {
    if (maybe(50)) {
      // name1_col1 + female suffix
      name = col1 + randomItem(dragonBorn.name1_female_suffixes);
    } else {
      // name1_col1 + name1_col2 + female suffix
      const col2 = randomItem(dragonBorn.name1_col2);
      const suffix = randomItem(dragonBorn.name1_female_suffixes);
      name = col1 + col2 + suffix;
    }
  } else {
    // fallback if gender is unspecified or invalid
    name = col1;
  }

  // Apply transformations
  return applyTransformation(name, dragonBorn.transformations);
}

function generateLastName() {
  const col1 = randomItem(dragonBorn.name2_col1);
  const col2 = randomItem(dragonBorn.name2_col2);
  const base = col1 + col2;

  // Apply transformations
  const transformedBase = applyTransformation(base, dragonBorn.transformations);

  return maybe(50) ? `of ${transformedBase}` : transformedBase;
}

export function generateDragonbornName(gender = "male") {
  return {
    firstName: generateFirstName(gender),
    lastName: generateLastName(),
  };
}
