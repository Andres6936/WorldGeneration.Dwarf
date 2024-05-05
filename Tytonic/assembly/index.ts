// The entry file of your WebAssembly module.

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
}

export function newHeightmap(width: i32, height: i32): Heightmap {
  return new Heightmap(width, height);
}

export function addHillToHeightmap(target: Heightmap, hx: f32, hy: f32, h_radius: f32, h_height: f32): void {
  target.addHill(hx, hy, h_radius, h_height);
}

export function getValuesOfHeightmap(target: Heightmap): Float32Array {
  return target.getValues();
}