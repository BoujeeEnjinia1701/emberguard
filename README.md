# EmberGuard

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Situational Field Hardware · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $300 USD · **Difficulty:** 3 of 5

Roof-edge sensor mast that detects ember showers with IR and wind data and triggers a gutter and eave sprinkler zone.

![EmberGuard concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Problem

Wildfire embers ignite homes well ahead of the fire front, most often in gutters, on roof edges and in debris near the eaves, while the house is empty and the power may be off. Commercial exterior sprinkler systems exist but are costly and closed, and timer-based sprinklers waste water that fire crews need.

## Concept

Roof-edge sensor mast that detects ember showers with IR and wind data and triggers a gutter and eave sprinkler zone.

A slim mast at one gable end carries two small thermal array cameras just above the ridge, watching both roof planes and gutters, plus an anemometer, wind vane and humidity sensor. The system arms itself in fire weather, and when it sees a hot spot or a burst of hot specks it runs two alternating spray zones along the gutter lips at a steady 4 L/min. It runs for three days armed on a small LiFePO4 battery with solar top-up. First-order estimates, not yet verified: about 960 L per 4 h ember event; kit parts about $420 against a $300 concept budget (under review).

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Gable-end mast with sensor head and heat hood
- Two thermal array sensors (32 x 24 pixels)
- Anemometer, wind vane, temperature and humidity sensor
- Controller with 12.8 V LiFePO4 battery and 10 W solar panel
- Two 12 V normally closed zone valves and a pressure transducer
- Pump-start dry contact for an existing pump
- Micro-sprinkler lines on both gutter lips

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Not a substitute for evacuation orders, home hardening or professional fire protection. Leave when told to leave. Installation involves work at height. The kit is 12 V DC only; a mains pump keeps its own certified controls. The LiFePO4 battery must be fused and enclosed, and the mast must be earthed against lightning. See the safety section of the precis.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (EGD-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `EGD-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
