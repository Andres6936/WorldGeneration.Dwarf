// The entry file of your WebAssembly module.
import {Heightmap} from "./heightmap";

export function newHeightmap(width: i32, height: i32): Heightmap {
  return new Heightmap(width, height);
}

export function addHillToHeightmap(target: Heightmap, hx: f32, hy: f32, h_radius: f32, h_height: f32): void {
  target.addHill(hx, hy, h_radius, h_height);
}

export function normalizeHeightmap(target: Heightmap, min: f32, max: f32): void {
  target.normalize(min, max);
}

export function getValuesOfHeightmap(target: Heightmap): Float32Array {
  return target.getValues();
}