// src/utils/angloName.js
import { orcData } from '../data/orcData';

function randomItem(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function maybe(probabilityPercent) {
  return Math.random() * 100 < probabilityPercent;
}

export function generateFirstName(gender) {
  const col1 = randomItem(orcData.name1_col1);

  if (gender === "male") {
    if (maybe(50)) {
      // name1_col1 + name1_col2
      return col1 + randomItem(orcData.name1_col2);
    } else {
      // name1_col1 + male suffix
      return col1 + randomItem(orcData.name1_male_suffixes);
    }
  }

  if (gender === "female") {
    if (maybe(50)) {
      // name1_col1 + female suffix
      return col1 + randomItem(orcData.name1_female_suffixes);
    } else {
      // name1_col1 + name1_col2 + female suffix
      const col2 = randomItem(orcData.name1_col2);
      const suffix = randomItem(orcData.name1_female_suffixes);
      return col1 + col2 + suffix;
    }
  }

  // fallback if gender is unspecified or invalid
  return col1;
}

export function generateLastName() {
  const col1 = randomItem(orcData.name2_col1);
  const col2 = randomItem(orcData.name2_col2);
  const base = col1 + col2;

  return maybe(50) ? `of ${base}` : base;
}

export function generateOrcName(gender = "male") {
  return {
    firstName: generateFirstName(gender),
    lastName: generateLastName(),
  };
}
