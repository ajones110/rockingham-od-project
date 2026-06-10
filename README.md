# Rockingham County OD Matrix & Digital Twin Research

## Overview

This project develops a transportation and community connectivity framework for Rockingham County, North Carolina.

The workflow combines:

* Census Block Groups (CBGs)
* Census Place Boundaries
* ACS Demographic Data
* GIS Analysis
* Gravity-Based Origin-Destination Modeling

The long-term goal is to support rural transportation planning, digital twin development, and community technology readiness assessment.

---

## Study Area

Rockingham County, North Carolina

Primary municipalities include:

* Reidsville
* Eden
* Wentworth
* Madison
* Mayodan
* Stoneville

---

## Project Workflow

### 1. Census Geography Processing

Downloaded:

* TIGER/Line Block Groups
* TIGER/Line Place Boundaries

Generated:

* CBG centroids
* Municipality assignments

Output:

data/cbg_place_enriched.geojson

---

### 2. Municipality Assignment

Each Census Block Group was assigned to a municipality using:

1. Spatial join
2. Nearest-place fallback assignment

Final output:

outputs/rockingham_cbg_places.geojson

Result:

* 70 Rockingham County CBGs
* 100% municipality assignment coverage

---

### 3. ACS Demographic Integration

Variables:

* Total Population (B01003_001E)
* Median Household Income (B19013_001E)

Source:

American Community Survey 5-Year Estimates

Output:

outputs/rockingham_acs.csv

---

### 4. Gravity Model OD Matrix

Synthetic interaction model:

Trips ∝ (Population_i × Population_j) / Distance_ij²

Generated:

outputs/rockingham_od_population_weighted.csv

Characteristics:

* Population-weighted
* Distance-decay adjusted
* Internal and inter-community flows

---

### 5. Municipality Aggregation

CBG-level flows aggregated to municipality-to-municipality flows.

Output:

outputs/rockingham_place_od.csv

Example Results:

Reidsville → Reidsville

Eden → Eden

Reidsville ↔ Wentworth

Eden ↔ Reidsville

Eden ↔ Stoneville

---

### 6. Corridor Analysis

Top travel corridors identified by combining directional flows.

Output:

outputs/top_10_corridors.csv

Top Corridors:

1. Reidsville ↔ Wentworth
2. Eden ↔ Reidsville
3. Eden ↔ Stoneville
4. Eden ↔ Wentworth
5. Madison ↔ Mayodan

---

### 7. Flow Mapping

Municipality centroids were connected using weighted OD flows.

Output:

outputs/figures/place_flow_map.png

Visualization highlights:

* Reidsville as the primary county hub
* Eden as a secondary hub
* Strong Eden–Stoneville corridor
* Strong Reidsville–Wentworth corridor

---

## Current Research Applications

This workflow supports:

* Transportation Planning
* Regional Development Analysis
* Rural Accessibility Studies
* Digital Twin Development
* Community Technology Readiness Assessment

---

## Future Enhancements

Planned additions:

* LODES Employment Data
* OpenStreetMap Travel Times
* SUMO Network Simulation
* TAP-B Integration
* NeuralMOVES Demand Modeling

---

## Author

Akilah Jones

M.S. Civil Engineering 

North Carolina A&T State University

