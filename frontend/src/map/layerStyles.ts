/**
 * Professional GIS styling for MapLibre GL JS vector and raster layers.
 * High contrast, visible on top of drone imagery, distinct symbology.
 */

export const LAYER_COLORS = {
  parcel: {
    fill: '#0284c7',
    fillOpacity: 0.25,
    stroke: '#0369a1',
    strokeWidth: 2,
    selectedStroke: '#38bdf8',
    selectedFillOpacity: 0.45
  },
  building: {
    fill: '#f59e0b',
    fillOpacity: 0.40,
    stroke: '#b45309',
    strokeWidth: 1.8,
    selectedStroke: '#fbbf24'
  },
  road: {
    stroke: '#475569',
    strokeWidth: 3,
    dasharray: [4, 2]
  },
  groundTruth: {
    fill: '#10b981',
    fillOpacity: 0.15,
    stroke: '#059669',
    strokeWidth: 2.5,
    dasharray: [3, 2]
  },
  issue: {
    stroke: '#ef4444',
    strokeWidth: 3.5,
    fill: '#f87171',
    fillOpacity: 0.35
  }
};
