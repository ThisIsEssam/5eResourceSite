import { orcData } from '../data/orcData';

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

export function generateFirstName(gender) {
  const col1 = randomItem(orcData.name1_col1);
  let name;

  if (gender === "male") {
    if (maybe(50)) {
      name = col1 + randomItem(orcData.name1_col2);
    } else {
      name = col1 + randomItem(orcData.name1_male_suffixes);
    }
  } else if (gender === "female") {
    if (maybe(50)) {
      name = col1 + randomItem(orcData.name1_female_suffixes);
    } else {
      const col2 = randomItem(orcData.name1_col2);
      const suffix = randomItem(orcData.name1_female_suffixes);
      name = col1 + col2 + suffix;
    }
  } else {
    name = col1;
  }

  return applyTransformation(name, orcData.transformations);
}

export function generateLastName() {
  const col1 = randomItem(orcData.name2_col1);
  const col2 = randomItem(orcData.name2_col2);
  const base = col1 + col2;

  const transformedBase = applyTransformation(base, orcData.transformations);

  return maybe(50) ? `of ${transformedBase}` : transformedBase;
}

export function generateOrcName(gender = "male") {
  return {
    firstName: generateFirstName(gender),
    lastName: generateLastName(),
  };
}