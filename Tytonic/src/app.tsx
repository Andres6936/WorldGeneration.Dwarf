import React from 'react';
import {Group} from '@visx/group';
import genBins, {type Bin, type Bins} from '@visx/mock-data/lib/generators/genBins';
import {scaleLinear} from '@visx/scale';
import {HeatmapRect} from '@visx/heatmap';
import {getSeededRandom} from '@visx/mock-data';
// import {newHeightmap, addHillToHeightmap, getValuesOfHeightmap} from "tytonic";

const cool1 = 'red';
const cool2 = 'yellow';
export const background = '#28272c';

const seededRandom = getSeededRandom(0.41);

const binData = genBins(
  /* length = */ 80,
  /* height = */ 50,
  /** binFunc */ (idx) => 150 * idx,
  /** countFunc */ (i, number) => 25 * (number - i) * seededRandom(),
);

function max<Datum>(data: Datum[], value: (d: Datum) => number): number {
  return Math.max(...data.map(value));
}

// accessors
const bins = (d: Bins) => d.bins;
const count = (d: Bin) => d.count;

const colorMax = max(binData, (d) => max(bins(d), count));
const bucketSizeMax = max(binData, (d) => bins(d).length);

// scales
const xScale = scaleLinear<number>({
  domain: [0, binData.length],
});
const yScale = scaleLinear<number>({
  domain: [0, bucketSizeMax],
});
const rectColorScale = scaleLinear<string>({
  range: [cool1, cool2],
  domain: [0, colorMax],
});

export type HeatmapProps = {
  width: number;
  height: number;
  margin?: { top: number; right: number; bottom: number; left: number };
  separation?: number;
  events?: boolean;
};

const defaultMargin = { top: 20, left: 20, right: 20, bottom: 110 };

// const WORLD_WIDTH = 80;
// const WORLD_HEIGHT = 50
//
// /**
//  * Returns a random integer between min (inclusive) and max (inclusive).
//  * The value is no lower than min (or the next integer greater than min
//  * if min isn't an integer) and no greater than max (or the next integer
//  * lower than max if max isn't an integer).
//  * Using Math.round() will give you a non-uniform distribution!
//  *
//  * Ref: https://stackoverflow.com/a/1527820
//  */
// function getRandomInt(min: number, max: number) {
//     min = Math.ceil(min);
//     max = Math.floor(max);
//     return Math.floor(Math.random() * (max - min + 1)) + min;
// }
//
// const heightmap = newHeightmap(WORLD_WIDTH, WORLD_HEIGHT);
//
// for (let i = 0; i < 250; i++) {
//     addHillToHeightmap(heightmap,
//         getRandomInt(WORLD_WIDTH / 10, WORLD_WIDTH - WORLD_WIDTH / 10),
//         getRandomInt(WORLD_HEIGHT / 10, WORLD_HEIGHT - WORLD_HEIGHT / 10),
//         getRandomInt(12, 16),
//         getRandomInt(6, 10)
//     );
// }
//
// const valuesOf = getValuesOfHeightmap(heightmap);
//
// console.log(valuesOf)

export default function App({
  width,
  height,
  margin = defaultMargin,
}: HeatmapProps) {
  // bounds
  const size =
    width > margin.left + margin.right ? width - margin.left - margin.right : width;
  const xMax = size / 1.5;
  const yMax = height - margin.bottom - margin.top;

  const binWidth = xMax / binData.length;

  xScale.range([0, xMax]);
  yScale.range([yMax, 0]);

  return (
    <svg width={width} height={height}>
      <rect x={0} y={0} width={width} height={height} fill={background} />
      <Group top={margin.top} left={margin.left}>
        <HeatmapRect
          data={binData}
          xScale={(d) => xScale(d) ?? 0}
          yScale={(d) => yScale(d) ?? 0}
          colorScale={rectColorScale}
          binWidth={binWidth}
          binHeight={binWidth}
        >
          {(heatmap) =>
            heatmap.map((heatmapBins) =>
              heatmapBins.map((bin) => (
                <rect
                  key={`heatmap-rect-${bin.row}-${bin.column}`}
                  className="visx-heatmap-rect"
                  width={bin.width}
                  height={bin.height}
                  x={bin.x}
                  y={bin.y}
                  fill={bin.color}
                />
              )),
            )
          }
        </HeatmapRect>
      </Group>
    </svg>
  );
}