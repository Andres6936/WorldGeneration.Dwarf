import assert from "assert";
import { get } from "../build/debug.js";
assert.strictEqual(get(10, 10).length, 100);
console.log("ok");
console.log(get(10, 10))
