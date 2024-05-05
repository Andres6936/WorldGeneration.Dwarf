import assert from "assert";
import { newHeightmap, addHillToHeightmap, getValuesOfHeightmap } from "../build/debug.js";
// assert.strictEqual(get(10, 10).length, 100);

const heightmap = newHeightmap(80, 50);
addHillToHeightmap(heightmap, 40, 25, 12, 6);
const valuesOf = getValuesOfHeightmap(heightmap);

console.log(valuesOf)
