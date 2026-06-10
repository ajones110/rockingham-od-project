# Rockingham County OD Matrix & Mobility Patterns

## Overview

This project looks at how people move within Rockingham County, North Carolina using Census Block Groups (CBGs), place boundaries, and mobility data.

The goal is to understand real movement patterns between towns like Eden, Reidsville, Wentworth, Madison, and Mayodan, and use that to support transportation planning and regional development work.

Instead of relying only on synthetic models, this project builds both:
- a gravity-based OD model
- an observed mobility-based OD matrix

to compare how predicted movement differs from real behavior.

---

## Study Area

Rockingham County, North Carolina

Key municipalities:
- Eden  
- Reidsville  
- Wentworth  
- Madison  
- Mayodan  
- Stoneville  

---

## Data Used

- Census Block Groups (TIGER/Line)
- Census Place Boundaries
- American Community Survey (5-year estimates)
- Dewey mobility dataset (weekly aggregated patterns)
- GIS spatial joins and centroid calculations

---

## Workflow

### 1. Building the spatial foundation
CBG geometries were processed and matched to municipalities using spatial joins and nearest-neighbor assignment where needed.

Output:
- `data/cbg_place_enriched.geojson`

---

### 2. Demographic integration
ACS data was added at the CBG level, including:
- population
- median household income

Output:
- `outputs/rockingham_acs.csv`

---

### 3. Gravity model (baseline comparison)
A simple gravity model was used to estimate expected flows:

Trips increase with population and decrease with distance.

Output:
- `outputs/rockingham_od_population_weighted.csv`

---

### 4. Observed OD construction
Mobility data was processed at the CBG level and expanded into home-to-POI flows.

These were then aggregated into municipality-level flows.

Output:
- `rockingham_place_od.csv`

---

### 5. Corridor analysis
Major movement corridors were identified by ranking OD flows between municipalities.

Output:
- `outputs/top_10_corridors.csv`

---

### 6. Flow mapping
Municipality centroids were connected using weighted flows to visualize dominant travel patterns across the county.

Output:
- `outputs/figures/place_flow_map.png`

---

## Key Patterns

- Eden and Reidsville act as the primary mobility hubs in the county  
- Strong two-way flow between Eden and Reidsville  
- Wentworth behaves as a feeder zone into Reidsville  
- Movement is highly localized, with strong internal town flows dominating overall mobility  

---

## Applications

This work supports:
- transportation planning
- rural mobility analysis
- regional accessibility studies
- digital twin development
- community planning and infrastructure decisions

---

## Future Work

- LODES employment integration  
- OpenStreetMap travel times  
- SUMO traffic simulation  
- TAP-B modeling  
- Neural MOVES demand modeling  

---

## Author

Akilah Jones  
M.S. Civil Engineering  
North Carolina A&T State University  
