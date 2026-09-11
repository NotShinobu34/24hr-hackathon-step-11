# Deployment & Production Readiness Specification

## Purpose

This document outlines the deployment strategy for GeoParcel AI, ensuring that the prototype can be hosted reliably for remote judge evaluation or staged locally with identical behavior.

---

## 1. Target Deployment Topologies

### Topology A: Decoupled Cloud Hosting (Recommended)
- **Frontend**: Static SPA built via `npm run build`, hosted on Vercel, Netlify, or Cloudflare Pages with global CDN edge caching.
- **Backend**: Containerized FastAPI ASGI app hosted on Render, Fly.io, or Railway running via `uvicorn main:app --host 0.0.0.0 --port $PORT`.

### Topology B: Single-Container Unified Deployment
- FastAPI serves the compiled Vite static assets from `frontend/dist/` under `/` while serving API routes under `/api`.
- Ideal for offline judge evaluation or unified Docker execution with zero CORS concerns.

---

## 2. Production Build Commands

### Frontend Build
```bash
cd frontend
npm ci
npm run build
# Outputs optimized static bundle to frontend/dist/
```

### Backend Startup
```bash
cd backend
python -m pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2
```

---

## 3. Production Readiness Checklist

1. **CORS Security**:
   - In production, replace wildcard `*` with the exact deployed frontend origin (e.g. `https://geoparcel-ai.vercel.app`).
2. **Security Headers**:
   - `X-Content-Type-Options: nosniff`
   - `X-Frame-Options: DENY`
   - `Referrer-Policy: strict-origin-when-cross-origin`
3. **Asset Compression & Caching**:
   - Map tiles and GeoJSON fixtures served with `gzip`/`brotli` compression.
   - Cache-Control headers applied appropriately (immutable hashing for Vite JS/CSS bundles).
4. **Clean Error Boundaries**:
   - FastAPI exception handlers return structured JSON (`{"error": {"code": "...", "message": "..."}}`).
   - Debug stack traces disabled in production (`ENV=production`).
5. **SEO & Discovery**:
   - `robots.txt` and `sitemap.xml` accessible at domain root.
