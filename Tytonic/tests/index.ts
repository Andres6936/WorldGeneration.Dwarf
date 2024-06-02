// import { newHeightmap, addHillToHeightmap, getValuesOfHeightmap } from "../build/debug.js";
// import {ReadonlyArray2D} from "../src/array2d.ts";

import {getBufferNoise, getMapNoise, newNoise} from "../build/debug.js";

// const MAP_WIDTH = 3;
// const MAP_HEIGHT = 3;
//
// const heightmap = newHeightmap(MAP_WIDTH, MAP_HEIGHT);
// // addHillToHeightmap(heightmap, 40, 25, 12, 6);
// const valuesOf = getValuesOfHeightmap(heightmap);
//
// const heightmapOf = new ReadonlyArray2D(valuesOf, MAP_WIDTH, MAP_HEIGHT);
// // for (let heightmapOfElement of heightmapOf) {
// //     console.log(heightmapOfElement)
// // }
// //
// // console.log("Using @{map} method of ReadonlyArray2D")
//
// heightmapOf.map((valueOf) => {
//     console.log(valueOf);
// })

const noise = newNoise(2, 0.5, 2.0);
// const buffer = getBufferNoise(noise)
// console.log(buffer)
const map = getMapNoise(noise);
console.log(map)