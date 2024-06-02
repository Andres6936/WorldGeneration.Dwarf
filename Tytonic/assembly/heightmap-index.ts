import {Noise} from "./noise";
import {Heightmap} from "./heightmap";

export function newHeightmap(width: i32, height: i32): Heightmap {
    return new Heightmap(width, height);
}

export function addFbmHeightmap(target: Heightmap, noise: Noise, mul_x: f32, mul_y: f32, add_x: f32, add_y: f32, octaves: f32, delta: f32, scale: f32): void {
    target.addFbm(noise, mul_x, mul_y, add_x, add_y, octaves, delta, scale);
}

export function addHillToHeightmap(target: Heightmap, hx: f32, hy: f32, h_radius: f32, h_height: f32): void {
    target.addHill(hx, hy, h_radius, h_height);
}

export function normalizeHeightmap(target: Heightmap, min: f32, max: f32): void {
    target.normalize(min, max);
}

export function multiplyHeightmap(target: Heightmap, origin: Heightmap): void {
    target.multiply(origin);
}

export function getValuesOfHeightmap(target: Heightmap): Float32Array {
    return target.getValues();
}