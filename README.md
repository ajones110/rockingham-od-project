# Rockingham County Mobility Analysis: Origin-Destination Matrix Development

## Overview

This project develops Origin-Destination (OD) matrices from Dewey Data Weekly Patterns mobility data for Rockingham County, North Carolina.

The workflow converts raw visitor home Census Block Group (CBG) data into planning-ready travel flows that can support:

* Transportation planning
* Regional mobility analysis
* Travel demand assessment
* Digital twin development
* Community technology readiness research
* Economic and regional development studies

This work is being conducted as part of graduate research investigating community readiness and mobility patterns in rural regions.

---

## Data Source

The analysis uses Dewey Data Weekly Patterns Plus mobility datasets.

Key fields include:

* VISITOR_HOME_CBGS
* POI_CBG
* LOCATION_NAME
* VISITOR_COUNTS
* VISIT_COUNTS

The Dewey dataset already contains normalized visit estimates, so no additional device-sample expansion factors are applied.

---

## Workflow

### 1. Load Weekly Patterns Data

Raw Weekly Patterns files are loaded from Dewey exports.

### 2. Parse Visitor Home CBGs

The VISITOR_HOME_CBGS field contains JSON-formatted home Census Block Group counts.

Example:

```json
{
  "370459510002": 290,
  "370459515032": 194
}
```

These records are expanded into individual origin-destination flows.

### 3. Build OD Matrix

Each home CBG is linked to a destination POI.

Output:

```text
Origin CBG → Destination → Trips
```

### 4. County Crosswalk

Origin CBGs are converted to county FIPS codes and county names.

Output:

```text
Origin County → Destination → Trips
```

### 5. Corridor Analysis

Travel corridors are aggregated to identify:

* Top origin counties
* Top destinations
* Major regional travel flows

### 6. Export Planning Outputs

Outputs are saved for visualization and further analysis.

---

## Repository Structure

```text
scripts/
│
├── full_pipeline.py
├── cbg_to_county.py
├── county_destination_flows.py
├── top_corridors_county.py
├── top_counties.py
├── top_destinations.py

outputs/
│
├── figures/
├── logs/
└── od_matrices/

data/
│
└── crosswalk/
```

---

## Key Outputs

### OD Matrix

```text
origin
destination_name
trips
```

### County Flow Matrix

```text
origin_county
destination_name
trips
```

### Top Destinations

Aggregated visitor volumes by destination.

### County-Destination Corridors

Largest travel flows connecting counties and destinations.

---

## Future Enhancements

* County flow maps
* CBG place-name enrichment
* Regional travel shed analysis
* Activity-center classification
* Digital twin integration
* Transportation accessibility analysis

---

## Author

Akilah Jones

M.S. Civil Engineering

North Carolina Agricultural & Technical State University
