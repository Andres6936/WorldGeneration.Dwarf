// import { newHeightmap, addHillToHeightmap, getValuesOfHeightmap } from "../build/debug.js";
// import {ReadonlyArray2D} from "../src/array2d.ts";

import {getBufferNoise, newHeightmap, getMapNoise, newNoise, addFbmHeightmap, getValuesOfHeightmap} from "../build/debug";

const MAP_WIDTH = 80;
const MAP_HEIGHT = 50;
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

const noiseHm = newHeightmap(MAP_WIDTH, MAP_HEIGHT)
const noise2D = newNoise(2, 0.5, 2.0);

// const buffer = getBufferNoise(noise2D)
// console.log(buffer)
// const map = getMapNoise(noise);
// console.log(map)

addFbmHeightmap(noiseHm, noise2D, 6, 6, 0, 0, 32, 1, 1);
const valueOfNoiseHm = getValuesOfHeightmap(noiseHm);
console.log(valueOfNoiseHm);