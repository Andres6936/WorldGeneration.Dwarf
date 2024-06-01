type ValueIterable = {
    valueOf: number,
    x: number,
    y: number,
}

export class ReadonlyArray2D {
    private readonly current: ValueIterable;
    private readonly last: ValueIterable;

    constructor(
        private readonly valueOf: Float32Array,
        private readonly width: number,
        private readonly height: number
    ) {
        if (valueOf.length === 0) throw new Error("The value of array must be a list with more of 1 element");

        this.current = {
            valueOf: valueOf[0],
            x: 0,
            y: 0,
        };
        this.last = {
            valueOf: valueOf[valueOf.length - 1],
            x: width - 1,
            y: height - 1,
        }
    }

    public getWidth(): number {
        return this.width;
    }

    public getHeight(): number {
        return this.height;
    }

    public at(x: number, y: number): number | undefined {
        return this.valueOf.at(x + y * this.width)
    }

    private next() {
        if (this.current.x === this.last.x && this.current.y === this.last.y) {
            return {done: true};
        }
        this.current.x++;
        if (this.current.x === this.width) {
            this.current.x = 0;
            this.current.y++;
        }
        this.current.valueOf = this.valueOf[this.current.x + this.current.y * this.width];
        return {
            done: false,
            value: {
                valueOf: this.current.valueOf,
                x: this.current.x,
                y: this.current.y,
            },
        };
    }

    public [Symbol.iterator]() {
        return {
            current: this.current,
            last: this.last,
            next: this.next.bind(this),
        }
    }

    public map(callback: (x: ValueIterable, indexOf?: number) => void) {
        for (let i = 0; i < this.valueOf.length; i++) {
            callback({
                valueOf: this.valueOf[i],
                x: i % this.width,
                y: Math.trunc(i / this.width),
            }, i)
        }
    }
}