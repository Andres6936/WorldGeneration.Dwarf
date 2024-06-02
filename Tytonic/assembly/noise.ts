const NOISE_MAX_DIMENSIONS = 4;
const NOISE_MAX_OCTAVES = 128;
const DELTA = 1e-6;
const SIMPLEX_SCALE = 0.5;

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


/**
 * Computes the largest integer less than or equal to a given number.
 *
 * @param {number} a - The number to apply the floor operation to.
 *
 * @returns {number} The largest integer less than or equal to `a`.
 */
function floor(a: f32): i32 {
    return a > 0 ? a as i32 : (a as i32) - 1;
}

/**
 * Calculates the absolute modulo of two integers.
 *
 * @param {number} x - The dividend.
 * @param {number} n - The divisor.
 * @returns {number} The absolute modulo of x and n.
 */
function absmod(x: i32, n: i32): i32 {
    const m = x % n;
    return m < 0 ? m + n : m;
}

export class Noise {
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

    private simplex(f: Array<f32>): f32 {
        switch (this.ndim) {
            case 2: {
                const F2 = 0.366025403;  // 0.5 * (sqrtf(3.0) - 1.0);
                const G2 = 0.211324865;  // (3.0 - sqrtf(3.0)) / 6.0;
                const s = (f[0] + f[1]) * F2 * SIMPLEX_SCALE;
                const xs = f[0] * SIMPLEX_SCALE + s;
                const ys = f[1] * SIMPLEX_SCALE + s;
                const i = floor(xs);
                const j = floor(ys);
                const t = (i + j) * G2;
                const xo = i - t;
                const yo = j - t;
                const x0 = f[0] * SIMPLEX_SCALE - xo;
                const y0 = f[1] * SIMPLEX_SCALE - yo;
                const ii = absmod(i, 256);
                const jj = absmod(j, 256);
                let i1: i32;
                let j1: i32;
                if (x0 > y0) {
                    i1 = 1;
                    j1 = 0;
                } else {
                    i1 = 0;
                    j1 = 1;
                }
                const x1 = x0 - i1 + G2;
                const y1 = y0 - j1 + G2;
                const x2 = x0 - 1.0 + 2.0 * G2;
                const y2 = y0 - 1.0 + 2.0 * G2;
                let t0 = 0.5 - x0 * x0 - y0 * y0;
                let n0 = 0.0;
                if (t0 >= 0.0) {
                    let idx = (ii + this.map[jj]) & 0xFF;
                    t0 *= t0;
                    idx = this.map[idx];

                    // NOISE_SIMPLEX_GRADIENT_2D (4 params)
                    let u: f32;
                    let v: f32;
                    idx &= 0x7;
                    if (idx < 4) {
                        u = x0;
                        v = 2.0 * y0;
                    } else {
                        u = y0;
                        v = 2.0 * x0;
                    }
                    n0 = ((idx & 1) ? -u : u) + ((idx & 2) ? -v : v);

                    n0 *= t0 * t0;
                }

                let t1 = 0.5 - x1 * x1 - y1 * y1;
                let n1 = 0.0;
                if (t1 >= 0.0) {
                    let idx = (ii + i1 + this.map[(jj + j1) & 0xFF]) & 0xFF;
                    t1 *= t1;
                    idx = this.map[idx];

                    // NOISE_SIMPLEX_GRADIENT_2D (4 params)
                    let u: f32;
                    let v: f32;
                    idx &= 0x7;
                    if (idx < 4) {
                        u = x1;
                        v = 2.0 * y1;
                    } else {
                        u = y1;
                        v = 2.0 * x1;
                    }
                    n1 = ((idx & 1) ? -u : u) + ((idx & 2) ? -v : v);

                    n1 *= t1 * t1;
                }

                let t2 = 0.5 - x2 * x2 - y2 * y2;
                let n2 = 0.0
                if (t2 >= 0.0) {
                    let idx = (ii + 1 + this.map[(jj + 1) & 0xFF]) & 0xFF
                    t2 *= t2;
                    idx = this.map[idx];

                    // NOISE_SIMPLEX_GRADIENT_2D (4 params)
                    let u: f32;
                    let v: f32;
                    idx &= 0x7;
                    if (idx < 4) {
                        u = x2;
                        v = 2.0 * y2;
                    } else {
                        u = y2;
                        v = 2.0 * x2;
                    }
                    n2 = ((idx & 1) ? -u : u) + ((idx & 2) ? -v : v);

                    n2 *= t2 * t2;
                }

                return this.clampSignedF(40.0 * (n0 + n1 + n2));
            }
            default:
                return 1.0;
        }
    }

    public getBuffer(): f32[][] {
        return this.buffer;
    }

    public getMap(): u8[] {
        return this.map;
    }

    public getFbm(f: Array<f32>, octaves: f32): f32 {
        switch (this.noiseType) {
            case NoiseType.NOISE_DEFAULT:
            case NoiseType.NOISE_SIMPLEX:
                return this.getFbmSimplex(f, octaves);
            case NoiseType.NOISE_PERLIN:
            case NoiseType.NOISE_WAVELET:
                return 1.0;
        }
    }

    private getFbmSimplex(f: Array<f32>, octaves: f32): f32 {
        return this.getFbmInt(f, octaves, this.simplex.bind(this));
    }

    private getFbmInt(f: Array<f32>, octaves: f32, callback: (f: Array<f32>) => f32): f32 {
        const tf: Array<f32> = new Array<f32>(NOISE_MAX_DIMENSIONS).fill(0);
        // Initialize locals
        for (let i = 0; i < this.ndim; ++i) {
            tf[i] = f[i];
        }

        // Inner loop of spectral construction, where the fractal is built
        let value: f32 = 0;
        let i: i32;
        for (i = 0; i < octaves; ++i) {
            value += callback(tf) * this.exponent[i];
            for (let j = 0; j < this.ndim; ++j) {
                tf[j] *= this.lacunarity;
            }
        }

        // Take care of remainder in octaves
        octaves -= octaves as i32;
        if (octaves > DELTA) {
            value += octaves * callback(tf) * this.exponent[i];
        }
        return this.clampSignedF(value);
    }

    private clampSignedF(value: f32): f32 {
        const LOW = -1.0 + f32.EPSILON;
        const HIGH = 1.0 - f32.EPSILON;
        if (value < LOW) {
            return LOW;
        }
        if (value > HIGH) {
            return HIGH;
        }
        return value;
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