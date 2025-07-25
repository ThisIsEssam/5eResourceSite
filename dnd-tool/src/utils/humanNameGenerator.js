import { generateAngloName } from './angloNames';
import { generateFrenchName } from './frenchNames';

/**
 * Generates a human name based on subtype.
 * @param {string} subtype - "Anglo" or "French"
 * @returns {{ firstName: string, lastName: string }}
 */
export function generateHumanName(subtype = "Anglo") {
  switch (subtype) {
    case "French":
      return generateFrenchName();
    case "Anglo":
    default:
      return generateAngloName();
  }
}
