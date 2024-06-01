// The entry file of your WebAssembly module.

class ImmutableTuple<T> {
  constructor(public readonly first: T, public readonly second: T) {
  }
}

class Heightmap {
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

  private setValue(target: Float32Array) : void {
    this.values.set(target);
  }

  public getValues(): Float32Array {
    return this.values;
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
      for (let i = 0; i != this.width * this.height ; ++i) {
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
}

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