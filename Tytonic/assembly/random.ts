
/**
 * Get a random floating point number between `min` and `max`.
 *
 * @param {number} min - min number
 * @param {number} max - max number
 * @return {number} a random floating point number
 */
export function getRandomFloat(min: f32, max: f32): f32 {
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
export function getRandomInt(min: i32, max: i32): i32 {
    min = Math.ceil(min) as i32;
    max = Math.floor(max) as i32;
    return (Math.floor(Math.random() * (max - min + 1)) + min) as i32;
}
