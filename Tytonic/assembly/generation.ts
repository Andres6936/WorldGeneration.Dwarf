import {Heightmap} from "./heightmap";
import {getRandomInt} from "./random";

export function poleGen(heightmap: Heightmap, north: boolean, south: boolean): void {
    if (north) {
        let rng = getRandomInt(2, 5);
        for (let i = 0; i < heightmap.getWidth(); i++) {
            for (let j = 0; j < rng; j++) {
                heightmap.setAt(i, heightmap.getHeight() - 1 - j, 0.31)
            }
            rng += getRandomInt(1, 3) - 2
            if (rng > 6) {
                rng = 5;
            }
            if (rng < 2) {
                rng = 2;
            }
        }
    }

    if (south) {
        let rng = getRandomInt(2, 5);
        for (let i = 0; i < heightmap.getWidth(); i++) {
            for (let j = 0; j < rng; j++) {
                heightmap.setAt(i, j, 0.31)
            }
            rng += getRandomInt(1, 3) - 2;
            if (rng > 6) {
                rng = 5;
            }
            if (rng < 2) {
                rng = 2;
            }
        }
    }
}