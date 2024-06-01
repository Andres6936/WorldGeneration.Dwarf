import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './app.tsx'
import './index.css'
import {getValuesOfHeightmap, addHillToHeightmap, newHeightmap} from "tytonic";
import {ReadonlyArray2D} from "./array2d.ts";

const WORLD_WIDTH = 80;
const WORLD_HEIGHT = 50;

/**
 * Returns a random integer between min (inclusive) and max (inclusive).
 * The value is no lower than min (or the next integer greater than min
 * if min isn't an integer) and no greater than max (or the next integer
 * lower than max if max isn't an integer).
 * Using Math.round() will give you a non-uniform distribution!
 *
 * Ref: https://stackoverflow.com/a/1527820
 */
function getRandomInt(min: number, max: number) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

const heightmap = newHeightmap(WORLD_WIDTH, WORLD_HEIGHT);

for (let i = 0; i < 250; i++) {
    addHillToHeightmap(heightmap,
        getRandomInt(WORLD_WIDTH / 10, WORLD_WIDTH - WORLD_WIDTH / 10),
        getRandomInt(WORLD_HEIGHT / 10, WORLD_HEIGHT - WORLD_HEIGHT / 10),
        getRandomInt(12, 16),
        getRandomInt(6, 10)
    );
}

const valuesOf = getValuesOfHeightmap(heightmap);
console.log(valuesOf)

const heightmapOf = new ReadonlyArray2D(valuesOf, WORLD_WIDTH, WORLD_HEIGHT);


ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
       <App valueOf={heightmapOf} width={1400} height={1000}/>
    </React.StrictMode>,
)