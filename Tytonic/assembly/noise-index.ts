import {Noise} from "./noise";

export function newNoise(ndim: i32, hurst: f32, lacunarity: f32): Noise {
    return new Noise(ndim, hurst, lacunarity);
}

export function getBufferNoise(target: Noise): f32[][] {
    return target.getBuffer();
}

export function getMapNoise(target: Noise): u8[] {
    return target.getMap();
}