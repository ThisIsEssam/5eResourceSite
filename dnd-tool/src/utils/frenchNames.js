import { frenchData } from "../data/frenchData";

function randomItem(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function maybe(probabilityPercent) {
  return Math.random() * 100 < probabilityPercent;
}

// Add this function to apply transformations
function applyTransformation(str, transformations) {
  let result = str;
  transformations.forEach(({ input, outputs }) => {
    const regex = new RegExp(input, 'g');
    result = result.replace(regex, () => randomItem(outputs));
  });
  return result;
}

function generateFirstName(gender) {
  const col1 = randomItem(frenchData.name1_col1);

  let name;
  if (gender === "male") {
    if (maybe(50)) {
      name = col1 + randomItem(frenchData.name1_col2);
    } else {
      name = col1 + randomItem(frenchData.name1_male_suffixes);
    }
  } else if (gender === "female") {
    if (maybe(50)) {
      name = col1 + randomItem(frenchData.name1_female_suffixes);
    } else {
      const col2 = randomItem(frenchData.name1_col2);
      const suffix = randomItem(frenchData.name1_female_suffixes);
      name = col1 + col2 + suffix;
    }
  } else {
    name = col1;
  }

  // Apply transformations before returning
  return applyTransformation(name, frenchData.transformations);
}

function generateLastName() {
  const col1 = randomItem(frenchData.name2_col1);
  const col2 = randomItem(frenchData.name2_col2);
  const base = col1 + col2;

  // Optionally add a prefix
  let lastName = maybe(30) ? randomItem(frenchData.name2_prefixes) + base : base;

  // Apply transformations before returning
  return applyTransformation(lastName, frenchData.transformations);
}

export function generateFrenchName(gender = "male") {
  return {
    firstName: generateFirstName(gender),
    lastName: generateLastName(),
  };
}