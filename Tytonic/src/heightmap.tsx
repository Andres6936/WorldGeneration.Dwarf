import type {ReadonlyArray2D} from "./array2d.ts";
import {useMemo} from "react";
import * as d3 from "d3"


const MARGIN = {top: 30, right: 30, bottom: 30, left: 30};

export type InteractionData = {
    xLabel: string;
    yLabel: string;
    xPos: number;
    yPos: number;
    value: number;
};

export type HeatmapProps = {
    width: number;
    height: number;
    valueOf: ReadonlyArray2D;
    setHoveredCell: (hoveredCell: InteractionData | null) => void;
};

export default function Heightmap({
                                      width,
                                      height,
                                      valueOf,
                                      setHoveredCell,
                                  }: HeatmapProps) {

    // The bounds (=area inside the axis) is calculated by substracting the margins
    const boundsWidth = width - MARGIN.right - MARGIN.left;
    const boundsHeight = height - MARGIN.top - MARGIN.bottom;

    const allYGroups = useMemo(() =>
        [...new Set(valueOf.map(x => x.y.toString()))], [valueOf]
    );

    const allXGroups = useMemo(() =>
        [...new Set(valueOf.map(x => x.x.toString()))], [valueOf]
    );

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
            .range([0, boundsHeight])
            .domain(allYGroups)
            .padding(0.01);
    }, [valueOf, height]);

    const colorScale = d3
        .scaleSequential()
        .interpolator(d3.interpolateInferno)
        .domain([min, max]);

    // Build the rectangles
    const allShapes = valueOf.map((item, indexOf) => {
        const x = xScale(item.x.toString());
        const y = yScale(item.y.toString());

        if (item.valueOf === null || !x || !y) {
            return;
        }

        return (
            <rect
                key={indexOf}
                x={xScale(item.x.toString())}
                y={yScale(item.y.toString())}
                width={xScale.bandwidth()}
                height={yScale.bandwidth()}
                opacity={1}
                onMouseEnter={(e) => {
                    setHoveredCell({
                        xLabel: item.x.toString(),
                        yLabel: item.y.toString(),
                        xPos: x + xScale.bandwidth() + MARGIN.left,
                        yPos: y + xScale.bandwidth() / 2 + MARGIN.top,
                        value: Math.round(item.valueOf * 100) / 100,
                    });
                }}
                onMouseLeave={() => setHoveredCell(null)}
                fill={colorScale(item.valueOf)}
                stroke="white"
            />
        );
    });

    const xLabels = allXGroups.map((name, indexOf) => {
        const x = xScale(name);

        if (!x) {
            return null;
        }

        return (
            <text
                key={indexOf}
                x={x + xScale.bandwidth() / 2}
                y={-5}
                textAnchor="middle"
                dominantBaseline="middle"
                fontSize={10}
            >
                {name}
            </text>
        );
    });

    const yLabels = allYGroups.map((name, indexOf) => {
        const y = yScale(name);

        if (!y) {
            return null;
        }

        return (
            <text
                key={indexOf}
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