const NOISE_MAX_DIMENSIONS = 4;
const NOISE_MAX_OCTAVES = 128;

const enum NoiseType {
    NOISE_PERLIN = 1,
    NOISE_SIMPLEX = 2,
    NOISE_WAVELET = 4,
    NOISE_DEFAULT = 0
}

/**
 * Get a random floating point number between `min` and `max`.
 *
 * @param {number} min - min number
 * @param {number} max - max number
 * @return {number} a random floating point number
 */
function getRandomFloat(min: f32, max: f32): f32 {
    return (Math.random() * (max - min) + min) as f32;
}

/**
 * Returns a random integer between min (inclusive) and max (inclusive).
 * The value is no lower than min (or the next integer greater than min
 * if min isn't an integer) and no greater than max (or the next integer
 * lower than max if max isn't an integer).
 * Using Math.round() will give you a non-uniform distribution!
 *
 * Ref: https://stackoverflow.com/a/1527820
 */
function getRandomInt(min: i32, max: i32): i32 {
    min = Math.ceil(min) as i32;
    max = Math.floor(max) as i32;
    return (Math.floor(Math.random() * (max - min + 1)) + min) as i32;
}

class Noise {
    // fractal stuff
    private readonly H: f32;
    private readonly exponent: f32[];
    // Is a ref to f32
    private waveletTileData: f32 = 0;
    // Randomized map of indexes into buffer
    private readonly map: u8[];
    // Random 256 x ndim buffer
    private readonly buffer: f32[][];
    private readonly noiseType: NoiseType;

    constructor(private readonly ndim: i32, private readonly hurst: f32, private readonly lacunarity: f32) {
        this.map = new Array<u8>(256);
        this.exponent = new Array<f32>(NOISE_MAX_OCTAVES);
        this.buffer = new Array<Array<f32>>(256).fill(new Array<f32>(NOISE_MAX_DIMENSIONS))

        for (let i = 0; i < 256; ++i) {
            this.map[i] = i as u8;
            for (let j = 0; j < this.ndim; ++j) {
                this.buffer[i][j] = getRandomFloat(-0.5, 0.5);
            }
            Noise.normalize(ndim, this.buffer[i]);
        }

        for (let i = 255; i >= 0; --i) {
            const j: i32 = getRandomInt(0, 255);
            const swapVariable: u8 = this.map[i];
            this.map[i] = this.map[j];
            this.map[j] = swapVariable;
        }

        this.H = hurst;
        this.lacunarity = lacunarity;
        let f: f32 = 1 as f32;
        for (let i = 0; i < NOISE_MAX_OCTAVES; i++) {
            this.exponent[i] = 1.0 / f;
            f *= lacunarity;
        }
        this.noiseType = NoiseType.NOISE_DEFAULT;
    }

    public static normalize(ndim: i32, f: Array<f32>): void {
        let magnitude: f32 = 0;
        for (let i = 0; i < ndim; ++i) {
            magnitude += f[i] * f[i];
        }
        magnitude = ((1.0 as f32) / Math.sqrt(magnitude)) as f32;
        for (let i = 0; i < ndim; ++i) {
            f[i] *= magnitude;
        }
    }

    public getBuffer(): f32[][] {
        return this.buffer;
    }

    public getMap(): u8[] {
        return this.map;
    }
}

export function newNoise(ndim: i32, hurst: f32, lacunarity: f32): Noise {
    return new Noise(ndim, hurst, lacunarity);
}

export function getBufferNoise(target: Noise): f32[][] {
    return target.getBuffer();
}

export function getMapNoise(target: Noise): u8[] {
    return target.getMap();
}