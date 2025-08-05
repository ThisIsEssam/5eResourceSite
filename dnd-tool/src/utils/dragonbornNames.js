import { dragonbornData as dragonBorn } from "../data/dragonbornData";

function randomItem(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function maybe(percent) {
  return Math.random() * 100 < percent;
}

function applyTransformation(str, transformations) {
  let result = str;
  transformations.forEach(({ input, outputs }) => {
    const regex = new RegExp(input, 'g');
    result = result.replace(regex, () => randomItem(outputs));
  });
  return result;
}

export function generateFirstName(gender) {
  const col1 = randomItem(dragonBorn.name1_col1);
  let name;

  if (gender === "male") {
    name = maybe(50)
      ? col1 + randomItem(dragonBorn.name1_col2)
      : col1 + randomItem(dragonBorn.name1_male_suffixes);
  } else if (gender === "female") {
    if (maybe(50)) {
      name = col1 + randomItem(dragonBorn.name1_female_suffixes);
    } else {
      const col2 = randomItem(dragonBorn.name1_col2);
      const suffix = randomItem(dragonBorn.name1_female_suffixes);
      name = col1 + col2 + suffix;
    }
  } else {
    name = col1;
  }

  return applyTransformation(name, dragonBorn.transformations);
}

export function generateLastName() {
  const col1 = randomItem(dragonBorn.name2_col1);
  const col2 = randomItem(dragonBorn.name2_col2);
  const base = col1 + col2;
  const transformedBase = applyTransformation(base, dragonBorn.transformations);
  return maybe(50) ? `of ${transformedBase}` : transformedBase;
}

export function generateDragonbornName(gender = "male") {
  return {
    firstName: generateFirstName(gender),
    lastName: generateLastName(),
  };
}