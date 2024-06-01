class Array2D<T> {
    constructor(private valueOf: Array<T>, private width: number, private height: number) { }

    public getWidth(): number {
        return this.width;
    }

    public getHeight(): number {
        return this.height;
    }

    public at(x: number, y: number): T | undefined {
        return this.valueOf.at(x + y * this.width)
    }
}