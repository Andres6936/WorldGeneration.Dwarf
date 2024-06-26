import {ImmutableTuple} from "./immutable-tuple";
import {Noise} from "./noise";

export class Heightmap {
    private readonly width: i32;
    private readonly height: i32;
    private readonly values: Float32Array;

    constructor(width: i32, height: i32) {
        this.values = new Float32Array(width * height);
        this.width = width;
        this.height = height;
    }

    public static from(target: Float32Array, width: i32, height: i32): Heightmap {
        const heightmap = new Heightmap(width, height);
        heightmap.setValue(target);
        return heightmap;
    }

    public getWidth(): i32 {
        return this.width;
    }

    public getHeight(): i32 {
        return this.height;
    }

    private setValue(target: Float32Array): void {
        this.values.set(target);
    }

    public getValues(): Float32Array {
        return this.values;
    }

    public setAt(x: i32, y: i32, valueOf: f32): void {
        this.values[x + y * this.width] = valueOf;
    }

    public addHill(hx: f32, hy: f32, h_radius: f32, h_height: f32): void {
        const h_radius2: f32 = h_radius * h_radius;
        const coef: f32 = h_height / h_radius2;
        const minx: i32 = Math.max((hx - h_radius), 0) as i32;
        const miny: i32 = Math.max((hy - h_radius), 0) as i32;
        const maxx: i32 = Math.min(Math.ceil(hx + h_radius), this.width) as i32;
        const maxy: i32 = Math.min(Math.ceil(hy + h_radius), this.height) as i32;
        for (let y: i32 = miny; y < maxy; y++) {
            const y_dist: f32 = (y as f32 - hy) * (y as f32 - hy);
            for (let x: i32 = minx; x < maxx; x++) {
                const x_dist: f32 = (x as f32 - hx) * (x as f32 - hx);
                const z: f32 = h_radius2 - x_dist - y_dist;
                if (z > 0) {
                    this.values[x + y * this.width] += z * coef;
                }
            }
        }
    }

    public normalize(min: f32, max: f32): void {
        const currentValuesOf = this.getMinMax();
        const currentMin = currentValuesOf.first;
        const currentMax = currentValuesOf.second;

        if (currentMax - currentMin < f32.EPSILON) {
            for (let i = 0; i != this.width * this.height; ++i) {
                this.values[i] = min;
            }
        } else {
            const normalizeScale: f32 = (max - min) / (currentMax - currentMin);
            for (let i = 0; i != this.width * this.height; ++i) {
                this.values[i] = min + (this.values.at(i) - currentMin) * normalizeScale;
            }
        }
    }

    public getMinMax(): ImmutableTuple<f32> {
        if (!this.inBounds(0, 0)) {
            return new ImmutableTuple<f32>(0, 0);
        }

        let min: f32 = this.values.at(0);
        let max: f32 = this.values.at(0);

        for (let i = 0; i != this.width * this.height; i++) {
            const value = this.values.at(i);
            min = Math.min(min, value) as f32;
            max = Math.max(max, value) as f32;
        }

        return new ImmutableTuple<f32>(min, max);
    }

    public inBounds(x: i32, y: i32): boolean {
        if (x < 0 || x >= this.width) return false;
        if (y < 0 || y >= this.height) return false;
        return true;
    }

    public addFbm(noise: Noise, mul_x: f32, mul_y: f32, add_x: f32, add_y: f32, octaves: f32, delta: f32, scale: f32): void {
        const x_coefficient = mul_x / (this.width as f32);
        const y_coefficient = mul_y / (this.height as f32);
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                let f = new Array<f32>(2);
                f[0] = ((x as f32) + add_x) * x_coefficient;
                f[1] = ((y as f32) + add_y) * y_coefficient;
                this.values[x + y * this.width] += delta + noise.getFbm(f, octaves) * scale;
            }
        }
    }

    private static isSameSize(origin: Heightmap, destine: Heightmap): boolean {
        return origin.width == destine.width && origin.height == destine.height;
    }

    public multiply(heightmap: Heightmap): void {
        if (!Heightmap.isSameSize(this, heightmap)) {
            return;
        }

        for (let i = 0; i < this.width * this.height; i++) {
            this.values[i] *= heightmap.values[i];
        }
    }
}