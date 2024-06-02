import React, {useState} from 'react'
import ReactDOM from 'react-dom/client'
import Heightmap, {type InteractionData} from './heightmap.tsx'
import './index.css'
import {useMeasure} from "@uidotdev/usehooks";
import {
    addHillToHeightmap,
    addFbmHeightmap,
    getValuesOfHeightmap,
    newHeightmap,
    newNoise,
    normalizeHeightmap
} from "tytonic";
import {ReadonlyArray2D} from "./array2d.ts";
import {Tooltip} from "./tooltip.tsx";

const WORLD_WIDTH = 80;
const WORLD_HEIGHT = 50;
const NOISE_DEFAULT_HURST = 0.5;
const NOISE_DEFAULT_LACUNARITY = 2.0;

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

console.log('* World Gen START *')

const hm = newHeightmap(WORLD_WIDTH, WORLD_HEIGHT);

for (let i = 0; i < 250; i++) {
    addHillToHeightmap(hm,
        getRandomInt(WORLD_WIDTH / 10, WORLD_WIDTH - WORLD_WIDTH / 10),
        getRandomInt(WORLD_HEIGHT / 10, WORLD_HEIGHT - WORLD_HEIGHT / 10),
        getRandomInt(12, 16),
        getRandomInt(6, 10)
    );
}

console.log('- Main Hills -')

for (let i = 0; i < 1000; i++) {
    addHillToHeightmap(hm,
        getRandomInt(WORLD_WIDTH / 10, WORLD_WIDTH - WORLD_WIDTH / 10),
        getRandomInt(WORLD_HEIGHT / 10, WORLD_HEIGHT - WORLD_HEIGHT / 10),
        getRandomInt(2, 4),
        getRandomInt(6, 10)
    );
}

console.log('- Small Hills -')

normalizeHeightmap(hm, 0.0, 1.0)
const valuesOfHm = getValuesOfHeightmap(hm);
const hmOf = new ReadonlyArray2D(valuesOfHm, WORLD_WIDTH, WORLD_HEIGHT);

const noiseHm = newHeightmap(WORLD_WIDTH, WORLD_HEIGHT);
const noise2D = newNoise(2, NOISE_DEFAULT_HURST, NOISE_DEFAULT_LACUNARITY);
addFbmHeightmap(noiseHm, noise2D, 6, 6, 0, 0, 32, 1, 1);
normalizeHeightmap(noiseHm, 0.0, 1.0)
const valueOfNoiseHm = getValuesOfHeightmap(noiseHm);
const noiseHmOf = new ReadonlyArray2D(valueOfNoiseHm, WORLD_WIDTH, WORLD_HEIGHT);

function App() {
    const [hoveredCell, setHoveredCell] = useState<InteractionData | null>(null);
    const [ref, {width, height}] = useMeasure();

    return (
        <main style={{position: "relative", height: "100%"}} ref={ref}>
            <Heightmap valueOf={hmOf} width={width!} height={height!} setHoveredCell={setHoveredCell}/>
            <Heightmap valueOf={noiseHmOf} width={width!} height={height!} setHoveredCell={setHoveredCell}/>
            <Tooltip interactionData={hoveredCell} width={width!} height={height!}/>
        </main>
    )
}

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <App/>
    </React.StrictMode>,
)