import { halflingData } from "../data/halflingData.js";

function randomItem(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function maybe(probabilityPercent) {
  return Math.random() * 100 < probabilityPercent;
}

// Transformation function
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
  const col1 = randomItem(halflingData.name1_col1);

  let name;
  if (gender === "male") {
    if (maybe(50)) {
      name = col1 + randomItem(halflingData.name1_col2);
    } else {
      name = col1 + randomItem(halflingData.name1_male_suffixes);
    }
  } else if (gender === "female") {
    if (maybe(50)) {
      name = col1 + randomItem(halflingData.name1_female_suffixes);
    } else {
      const col2 = randomItem(halflingData.name1_col2);
      const suffix = randomItem(halflingData.name1_female_suffixes);
      name = col1 + col2 + suffix;
    }
  } else {
    name = col1;
  }

  // Apply transformations
  return applyTransformation(name, halflingData.transformations);
}

function generateLastName() {
  const col1 = randomItem(halflingData.name2_col1);
  const col2 = randomItem(halflingData.name2_col2);
  const base = col1 + col2;

  // Apply transformations
  const transformedBase = applyTransformation(base, halflingData.transformations);

  return maybe(50) ? `of ${transformedBase}` : transformedBase;
}

export function generateHalflingName(gender = "male") {
  return {
    firstName: generateFirstName(gender),
    lastName: generateLastName(),
  };
}