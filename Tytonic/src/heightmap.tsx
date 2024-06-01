import type {ReadonlyArray2D} from "./array2d.ts";
import {useMemo} from "react";
import * as d3 from "d3"


const MARGIN = {top: 20, right: 50, bottom: 20, left: 50};

export type HeatmapProps = {
    width: number;
    height: number;
    valueOf: ReadonlyArray2D;
};

export default function Heightmap({
                                width,
                                height,
                                valueOf,
                            }: HeatmapProps) {

    // The bounds (=area inside the axis) is calculated by substracting the margins
    const boundsWidth = width - MARGIN.right - MARGIN.left;
    const boundsHeight = height - MARGIN.top - MARGIN.bottom;

    const allYGroups = useMemo(() => [...new Set(valueOf.map((d) => d.y.toString()))], [valueOf]);
    const allXGroups = useMemo(() => [...new Set(valueOf.map((d) => d.x.toString()))], [valueOf]);

    const [min = 0, max = 0] = d3.extent(valueOf.map((d) => d.valueOf)); // extent can return [undefined, undefined], default to [0,0] to fix types

    const xScale = useMemo(() => {
        return d3
            .scaleBand()
            .range([0, boundsWidth])
            .domain(allXGroups)
            .padding(0.01);
    }, [valueOf, width]);

    const yScale = useMemo(() => {
        return d3
            .scaleBand()
            .range([boundsHeight, 0])
            .domain(allYGroups)
            .padding(0.01);
    }, [valueOf, height]);

    const colorScale = d3
        .scaleSequential()
        .interpolator(d3.interpolateInferno)
        .domain([min, max]);

    // Build the rectangles
    const allShapes = valueOf.map((d, i) => {
        const x = xScale(d.x.toString());
        const y = yScale(d.y.toString());

        if (d.valueOf === null || !x || !y) {
            return;
        }

        return (
            <rect
                key={i}
                x={xScale(d.x.toString())}
                y={yScale(d.y.toString())}
                width={xScale.bandwidth()}
                height={yScale.bandwidth()}
                opacity={1}
                fill={colorScale(d.valueOf)}
                stroke="white"
            />
        );
    });

    const xLabels = allXGroups.map((name, i) => {
        const x = xScale(name);

        if (!x) {
            return null;
        }

        return (
            <text
                key={i}
                x={x + xScale.bandwidth() / 2}
                y={boundsHeight + 10}
                textAnchor="middle"
                dominantBaseline="middle"
                fontSize={10}
            >
                {name}
            </text>
        );
    });

    const yLabels = allYGroups.map((name, i) => {
        const y = yScale(name);

        if (!y) {
            return null;
        }

        return (
            <text
                key={i}
                x={-5}
                y={y + yScale.bandwidth() / 2}
                textAnchor="end"
                dominantBaseline="middle"
                fontSize={10}
            >
                {name}
            </text>
        );
    });

    return (
        <svg width={width} height={height}>
            <g
                width={boundsWidth}
                height={boundsHeight}
                transform={`translate(${[MARGIN.left, MARGIN.top].join(",")})`}
            >
                {allShapes}
                {xLabels}
                {yLabels}
            </g>
        </svg>
    )
}