import React, { useEffect, useRef, useState } from 'react';
import maplibregl from 'maplibre-gl';
import { 
  GeoJSONFeature, GeoJSONFeatureCollection, LayerVisibilityState, 
  LayerOpacityState, TopologyIssue 
} from '../types/geoParcel';
import { LAYER_COLORS } from './layerStyles';

interface MapLibreCanvasProps {
  parcels: GeoJSONFeatureCollection;
  buildings: GeoJSONFeatureCollection;
  roads: GeoJSONFeatureCollection;
  groundTruth: GeoJSONFeatureCollection;
  issues: TopologyIssue[];
  visibility: LayerVisibilityState;
  opacity: LayerOpacityState;
  selectedFeature: GeoJSONFeature | null;
  onSelectFeature: (feature: GeoJSONFeature | null) => void;
  isEditing: boolean;
  onSaveGeometry: (featureId: string, updatedCoordinates: any) => void;
  focusTarget: { center: [number, number]; zoom?: number } | null;
}

export const MapLibreCanvas: React.FC<MapLibreCanvasProps> = ({
  parcels,
  buildings,
  roads,
  groundTruth,
  issues,
  visibility,
  opacity,
  selectedFeature,
  onSelectFeature,
  isEditing,
  onSaveGeometry,
  focusTarget
}) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);
  const [mapLoaded, setMapLoaded] = useState(false);
  const editMarkersRef = useRef<maplibregl.Marker[]>([]);
  const [editableCoords, setEditableCoords] = useState<number[][]>([]);

  // Initialize MapLibre GL Map
  useEffect(() => {
    if (!mapContainer.current || mapRef.current) return;

    // Blank vector style with dark GIS cartographic tone
    const map = new maplibregl.Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {},
        layers: [
          {
            id: 'background',
            type: 'background',
            paint: { 'background-color': '#090d16' }
          }
        ]
      },
      center: [77.5946, 12.9716],
      zoom: 16.5,
      pitch: 0,
      maxZoom: 22,
      minZoom: 12
    });

    map.addControl(new maplibregl.NavigationControl({ showCompass: true }), 'bottom-right');
    map.addControl(new maplibregl.ScaleControl({ unit: 'metric' }), 'bottom-left');

    map.on('load', () => {
      // 1. Add Drone Orthophoto Raster Source & Layer
      // Using /fixtures/imagery/sample_ortho.jpg served by FastAPI backend or direct path
      map.addSource('drone-ortho-source', {
        type: 'image',
        url: '/fixtures/imagery/sample_ortho.jpg',
        coordinates: [
          [77.5910, 12.9747], // Top-Left (NW)
          [77.5982, 12.9747], // Top-Right (NE)
          [77.5982, 12.9685], // Bottom-Right (SE)
          [77.5910, 12.9685]  // Bottom-Left (SW)
        ]
      });

      map.addLayer({
        id: 'drone-ortho-layer',
        type: 'raster',
        source: 'drone-ortho-source',
        paint: {
          'raster-opacity': 0.92,
          'raster-fade-duration': 0
        }
      });

      // 2. Add Vector Sources
      map.addSource('parcels-source', { type: 'geojson', data: parcels });
      map.addSource('buildings-source', { type: 'geojson', data: buildings });
      map.addSource('roads-source', { type: 'geojson', data: roads });
      map.addSource('ground-truth-source', { type: 'geojson', data: groundTruth });

      // Ground Truth Layers
      map.addLayer({
        id: 'ground-truth-fill',
        type: 'fill',
        source: 'ground-truth-source',
        paint: {
          'fill-color': LAYER_COLORS.groundTruth.fill,
          'fill-opacity': LAYER_COLORS.groundTruth.fillOpacity
        }
      });
      map.addLayer({
        id: 'ground-truth-line',
        type: 'line',
        source: 'ground-truth-source',
        paint: {
          'line-color': LAYER_COLORS.groundTruth.stroke,
          'line-width': LAYER_COLORS.groundTruth.strokeWidth,
          'line-dasharray': LAYER_COLORS.groundTruth.dasharray
        }
      });

      // Parcel Layers
      map.addLayer({
        id: 'parcels-fill',
        type: 'fill',
        source: 'parcels-source',
        paint: {
          'fill-color': LAYER_COLORS.parcel.fill,
          'fill-opacity': LAYER_COLORS.parcel.fillOpacity
        }
      });
      map.addLayer({
        id: 'parcels-line',
        type: 'line',
        source: 'parcels-source',
        paint: {
          'line-color': LAYER_COLORS.parcel.stroke,
          'line-width': LAYER_COLORS.parcel.strokeWidth
        }
      });

      // Building Layers
      map.addLayer({
        id: 'buildings-fill',
        type: 'fill',
        source: 'buildings-source',
        paint: {
          'fill-color': LAYER_COLORS.building.fill,
          'fill-opacity': LAYER_COLORS.building.fillOpacity
        }
      });
      map.addLayer({
        id: 'buildings-line',
        type: 'line',
        source: 'buildings-source',
        paint: {
          'line-color': LAYER_COLORS.building.stroke,
          'line-width': LAYER_COLORS.building.strokeWidth
        }
      });

      // Road Layers
      map.addLayer({
        id: 'roads-line',
        type: 'line',
        source: 'roads-source',
        paint: {
          'line-color': LAYER_COLORS.road.stroke,
          'line-width': LAYER_COLORS.road.strokeWidth,
          'line-dasharray': LAYER_COLORS.road.dasharray
        }
      });

      // Selection Highlight Layer
      map.addLayer({
        id: 'selection-highlight',
        type: 'line',
        source: 'parcels-source',
        filter: ['==', ['get', 'id'], ''],
        paint: {
          'line-color': '#38bdf8',
          'line-width': 4,
          'line-opacity': 0.9
        }
      });

      // Issue Overlay Source & Layer
      map.addSource('issues-source', {
        type: 'geojson',
        data: { type: 'FeatureCollection', features: [] }
      });
      map.addLayer({
        id: 'issues-line',
        type: 'line',
        source: 'issues-source',
        paint: {
          'line-color': LAYER_COLORS.issue.stroke,
          'line-width': LAYER_COLORS.issue.strokeWidth
        }
      });
      map.addLayer({
        id: 'issues-fill',
        type: 'fill',
        source: 'issues-source',
        paint: {
          'fill-color': LAYER_COLORS.issue.fill,
          'fill-opacity': LAYER_COLORS.issue.fillOpacity
        }
      });

      // Click Interaction for Feature Selection
      map.on('click', (e) => {
        const bbox: [maplibregl.PointLike, maplibregl.PointLike] = [
          [e.point.x - 4, e.point.y - 4],
          [e.point.x + 4, e.point.y + 4]
        ];
        const feats = map.queryRenderedFeatures(bbox, {
          layers: ['parcels-fill', 'buildings-fill', 'ground-truth-fill']
        });

        if (feats && feats.length > 0) {
          const clicked = feats[0];
          const featureId = clicked.properties?.id || clicked.id;
          
          // Match full feature from memory
          const fullFeature = 
            parcels.features.find(f => f.id === featureId) ||
            buildings.features.find(f => f.id === featureId) ||
            groundTruth.features.find(f => f.id === featureId);

          if (fullFeature) {
            onSelectFeature(fullFeature);
          }
        } else {
          onSelectFeature(null);
        }
      });

      // Hover cursor
      const pointerLayers = ['parcels-fill', 'buildings-fill', 'roads-line'];
      pointerLayers.forEach((layer) => {
        map.on('mouseenter', layer, () => {
          map.getCanvas().style.cursor = 'pointer';
        });
        map.on('mouseleave', layer, () => {
          map.getCanvas().style.cursor = '';
        });
      });

      mapRef.current = map;
      setMapLoaded(true);
    });

    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, []);

  // Update Vector Sources when data changes
  useEffect(() => {
    if (!mapRef.current || !mapLoaded) return;
    const map = mapRef.current;

    const updateSource = (id: string, data: any) => {
      const src = map.getSource(id) as maplibregl.GeoJSONSource;
      if (src && data) src.setData(data);
    };

    updateSource('parcels-source', parcels);
    updateSource('buildings-source', buildings);
    updateSource('roads-source', roads);
    updateSource('ground-truth-source', groundTruth);

    // Build conflict zone features for unresolved issues
    const issueFeatures = issues
      .filter(i => !i.resolved)
      .map(issue => {
        const target = parcels.features.find(f => f.id === issue.featureId);
        return target ? { ...target, id: `issue-feat-${issue.id}` } : null;
      })
      .filter(Boolean);

    updateSource('issues-source', {
      type: 'FeatureCollection',
      features: issueFeatures
    });
  }, [parcels, buildings, roads, groundTruth, issues, mapLoaded]);

  // Update Layer Visibilities
  useEffect(() => {
    if (!mapRef.current || !mapLoaded) return;
    const map = mapRef.current;

    const setVisibility = (layerId: string, isVisible: boolean) => {
      if (map.getLayer(layerId)) {
        map.setLayoutProperty(layerId, 'visibility', isVisible ? 'visible' : 'none');
      }
    };

    setVisibility('drone-ortho-layer', visibility.imagery);
    setVisibility('parcels-fill', visibility.parcels);
    setVisibility('parcels-line', visibility.parcels);
    setVisibility('buildings-fill', visibility.buildings);
    setVisibility('buildings-line', visibility.buildings);
    setVisibility('roads-line', visibility.roads);
    setVisibility('ground-truth-fill', visibility.groundTruth);
    setVisibility('ground-truth-line', visibility.groundTruth);
    setVisibility('issues-fill', visibility.issues);
    setVisibility('issues-line', visibility.issues);
  }, [visibility, mapLoaded]);

  // Update Opacities
  useEffect(() => {
    if (!mapRef.current || !mapLoaded) return;
    const map = mapRef.current;

    if (map.getLayer('drone-ortho-layer')) {
      map.setPaintProperty('drone-ortho-layer', 'raster-opacity', opacity.imagery);
    }
    if (map.getLayer('parcels-fill')) {
      map.setPaintProperty('parcels-fill', 'fill-opacity', opacity.parcels * LAYER_COLORS.parcel.fillOpacity);
    }
    if (map.getLayer('buildings-fill')) {
      map.setPaintProperty('buildings-fill', 'fill-opacity', opacity.buildings * LAYER_COLORS.building.fillOpacity);
    }
    if (map.getLayer('ground-truth-fill')) {
      map.setPaintProperty('ground-truth-fill', 'fill-opacity', opacity.groundTruth * LAYER_COLORS.groundTruth.fillOpacity);
    }
  }, [opacity, mapLoaded]);

  // Update Selection Highlight
  useEffect(() => {
    if (!mapRef.current || !mapLoaded) return;
    const map = mapRef.current;
    if (map.getLayer('selection-highlight')) {
      if (selectedFeature) {
        map.setFilter('selection-highlight', ['==', ['id'], selectedFeature.id]);
      } else {
        map.setFilter('selection-highlight', ['==', ['id'], '']);
      }
    }
  }, [selectedFeature, mapLoaded]);

  // Focus Camera transitions (e.g. on clicking an issue in the review queue)
  useEffect(() => {
    if (!mapRef.current || !focusTarget) return;
    mapRef.current.flyTo({
      center: focusTarget.center,
      zoom: focusTarget.zoom || 18,
      essential: true,
      duration: 1200
    });
  }, [focusTarget]);

  // Interactive Boundary Vertex Editing
  useEffect(() => {
    // Clear old edit markers
    editMarkersRef.current.forEach(m => m.remove());
    editMarkersRef.current = [];

    if (!mapRef.current || !isEditing || !selectedFeature) return;
    const map = mapRef.current;

    if (selectedFeature.geometry.type !== 'Polygon') return;
    const coords: number[][] = selectedFeature.geometry.coordinates[0];
    setEditableCoords([...coords]);

    // Create a draggable MapLibre marker for each vertex
    coords.forEach((pt, idx) => {
      // Avoid duplicate marker on closing vertex
      if (idx === coords.length - 1 && pt[0] === coords[0][0] && pt[1] === coords[0][1]) return;

      const el = document.createElement('div');
      el.className = 'gis-edit-vertex';
      el.style.width = '12px';
      el.style.height = '12px';
      el.style.backgroundColor = '#38bdf8';
      el.style.border = '2px solid #ffffff';
      el.style.borderRadius = '50%';
      el.style.cursor = 'grab';
      el.style.boxShadow = '0 0 8px rgba(56, 189, 248, 0.8)';

      const marker = new maplibregl.Marker({ element: el, draggable: true })
        .setLngLat([pt[0], pt[1]])
        .addTo(map);

      marker.on('dragend', () => {
        const lngLat = marker.getLngLat();
        const updated = [...coords];
        updated[idx] = [round(lngLat.lng, 6), round(lngLat.lat, 6)];
        // Keep polygon closed
        if (idx === 0) {
          updated[updated.length - 1] = updated[0];
        }
        setEditableCoords(updated);
        onSaveGeometry(selectedFeature.id, [updated]);
      });

      editMarkersRef.current.push(marker);
    });

    return () => {
      editMarkersRef.current.forEach(m => m.remove());
      editMarkersRef.current = [];
    };
  }, [isEditing, selectedFeature]);

  const round = (val: number, decimals: number) => {
    return Number(Math.round(Number(val + 'e' + decimals)) + 'e-' + decimals);
  };

  return (
    <div className="map-wrapper" style={{ width: '100%', height: '100%', position: 'relative' }}>
      <div ref={mapContainer} style={{ width: '100%', height: '100%' }} />

      {/* Editing Mode Banner */}
      {isEditing && (
        <div className="editor-banner">
          <span className="pulse-dot"></span>
          <span><strong>Vertex Edit Mode:</strong> Drag vertices to adjust parcel boundary. Edits recalculate topology automatically.</span>
        </div>
      )}
    </div>
  );
};
