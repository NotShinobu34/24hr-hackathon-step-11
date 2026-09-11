# Environment & Configuration Specification

## Purpose

This document specifies all runtime environments, software prerequisites, and configuration variables required to run GeoParcel AI locally and in production.

---

## 1. Runtime Requirements

### Backend
- **Python**: 3.10 or 3.11 (Avoid Python 3.13 due to C-extension wheel availability).
- **Package Manager**: `pip` or `uv`.
- **System Libraries**: Standard C runtime (pre-compiled binary wheels used for `shapely`, `geopandas`, and `opencv-python-headless`).

### Frontend
- **Node.js**: LTS 18.x or 20.x.
- **Package Manager**: `npm` (bundled with Node).
- **Browser Compatibility**: Modern Evergreen browsers with WebGL 2.0 support (Chrome 100+, Edge 100+, Firefox 100+, Safari 16+).

---

## 2. Environment Variables

### Backend Configuration (`backend/.env`)

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `PORT` | `8000` | Port for the FastAPI ASGI server. |
| `HOST` | `0.0.0.0` | Network binding interface. |
| `ENV` | `development` | Environment mode (`development`, `production`, `test`). |
| `CORS_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173` | Comma-separated allowed frontend origins. |
| `DATA_DIR` | `./data` | Directory for file storage (assets, uploads, job records). |
| `FIXTURES_DIR` | `../fixtures` | Directory containing verified demo imagery and GeoJSON. |
| `DEFAULT_METRIC_CRS` | `EPSG:3857` | Default projected CRS used for metric calculations when source lacks projection. |
| `TOLERANCE_OVERLAP_M2` | `0.05` | Prototype threshold (in $m^2$) above which parcel intersection is flagged as overlap. |
| `TOLERANCE_SLIVER_M2` | `2.0` | Prototype threshold (in $m^2$) below which parcel polygon is flagged as suspicious sliver. |
| `MAX_UPLOAD_SIZE_MB` | `50` | Maximum allowable upload file size for prototype. |

### Frontend Configuration (`frontend/.env`)

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `VITE_API_BASE_URL` | `http://localhost:8000/api` | Base URL for FastAPI backend endpoints. |
| `VITE_USE_MOCK_FALLBACK` | `true` | When `true`, frontend gracefully falls back to local fixtures if backend is unreachable. |
| `VITE_DEFAULT_MAP_CENTER` | `[77.5946, 12.9716]` | Default map center longitude/latitude `[lon, lat]`. |
| `VITE_DEFAULT_MAP_ZOOM` | `17` | Default zoom level focusing on urban parcels. |

---

## 3. Configuration Loading Pattern

- **Backend**: Uses Pydantic `BaseSettings` or `pydantic-settings` to parse environment variables with type casting, validation, and sensible defaults.
- **Frontend**: Vite automatically injects variables prefixed with `VITE_` via `import.meta.env`.
