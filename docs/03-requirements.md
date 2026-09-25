---
doc_id: EGD-REQ-001
title: EmberGuard requirements
project: EmberGuard
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, reference house and status against the concept
---

# EmberGuard requirements

These are first-pass requirements for the concept. Targets are proposals for review, not user-validated needs. The status column gives the position of the concept in EGD-PRC-001 v0.2, based on first-order estimates that will be checked by calculation at TRL 3. Two requirements are **not met** (R6 on net wetting, R13 on cost), one is **partly met** (R2 on single embers) and one is **not met by the kit alone** (R8 on pump power).

Table 1. Requirements.

| ID | Requirement | Target | Verification (TRL 3 or later) | Concept status |
| --- | --- | --- | --- | --- |
| R1 | Detect a smouldering ignition on a watched gutter or roof edge | A 100 cm² (15.5 in²) hot spot at 300 °C or hotter, anywhere along the watched gutters from 1.5 m to 13 m from the mast, within 10 s | Radiometric calculation from sensor field of view and noise; later a heated-target trial | Met on paper, large margin (estimate) |
| R2 | Detect single landed embers | A 10 mm glowing ember at 600 °C or hotter within 8 m of the mast, within 10 s | Same as R1 | **Partly met:** a 600 °C ember gives about 3 K of pixel rise at 8 m, below the proposed 5 K trigger threshold; it reaches the threshold only within about 5 m. An 800 °C ember is at the threshold at 8 m (estimate) |
| R3 | Watch both roof planes | Both eave gutters of the reference house, each from 1.5 m from the gable end to the far end | Geometry of fields of view on the massing model | Met except the first 1.3 m of each gutter nearest the mast |
| R4 | Arm only in fire weather | Automatic arming when sustained wind is 30 km/h (19 mph) or more, or gusts 50 km/h (31 mph) or more, with relative humidity 20 % or less for 10 min; manual and remote arming; defaults adjustable | Design review of the arming logic | Met by design |
| R5 | Start water quickly | Water at the farthest head within 60 s of a confirmed detection | Line fill calculation | Met, about 55 s with empty lines (estimate) |
| R6 | Wet the gutter and roof edge | Net water on a 1.2 m wide strip along each eave (gutter, fascia and first metre of roof) of 5 mm/h or more, averaged over each spray cycle, at the design wind of 30 km/h | Application-rate calculation with a drift allowance; later a spray trial in wind | **Not met:** about 7.7 mm/h gross but about 3.8 mm/h net at an assumed 50 % wind drift (estimate) |
| R7 | Use little water | Steady draw 4 L/min (1.1 US gal/min) or less; 1,000 L (264 US gal) or less for a 4 h ember event | Flow calculation from head ratings and duty cycle | Met, 4 L/min and about 960 L; no margin |
| R8 | Work through a grid outage | Sensing, logic and valves: 72 h armed plus 4 h of spraying on the battery alone, with no solar input. Water supply must not depend on grid power | Energy budget | Kit part met, about 64 Wh needed against about 69 Wh usable. **Not met by the kit alone** where the pump runs on grid power |
| R9 | Fail safely | Loss of sensor data while armed starts spraying; low battery, no water pressure or a faulty valve raises an alarm; power loss closes the valves | Failure modes review | Met by design |
| R10 | Survive fire weather until the front arrives | Mast and head survive gusts of 120 km/h (75 mph); electronics operate from -10 to 60 °C ambient; head shaded from sun and radiant heat | Wind load and thermal calculations | Wind met on first-order check (about 25 MPa bending stress in the mast, estimate); thermal unverified |
| R11 | Install without roof work or mains wiring | Mast, cable and spray lines fixed to walls, fascia and gutter lips with clamps; no roof penetrations; 12 V DC only; installable by two people with hand tools in 6 h or less | Design review; later a timed trial | Met by design; install time unverified |
| R12 | Tell people what it is doing | Local siren and status light; phone alert when armed, spraying, faulted or low on battery when a network is available; event log of detections, wind and valve actions | Design review | Met by design; phone alerts need a working network |
| R13 | Stay within the concept budget | Kit parts $300 or less, excluding the water source and pump | Priced BOM | **Not met:** about $420 (indicative) |

## Reference house and assumptions

- **House.** Single storey, 12 x 8 m (39 x 26 ft) footprint, 2.7 m walls, gable roof at 22 degrees with the ridge along the long side, 500 mm overhangs, gutters along both long eaves (13 m each, 26 m total). The sensor mast stands off one gable end at the ridge line.
- **Water.** A 1,000 L tank with a pump on its own supply, or a mains connection that holds at least 2 bar at 4 L/min. EmberGuard does not include the tank or pump.
- **Ember event.** 4 h of active spraying within a 72 h armed period. This is a design assumption, not a measured duration; real ember exposure varies from minutes to many hours.
- **Heads.** Six micro-sprinklers per eave at about 2.2 m spacing, about 40 L/h each at 2 bar (typical catalogue figure for small irrigation heads, to be confirmed with a named part).
- **Wind drift.** 50 % of the sprayed water misses the target strip at the design wind. This is an assumption with high uncertainty and is the main reason R6 is not met.
- **Ember targets.** Emissivity 0.9, sensor band 8 to 14 µm, background 300 K. See EGD-PRC-001 for the radiometric estimate.

> **Safety:** EmberGuard does not replace evacuation. Requirements R4 to R9 describe behaviour while the house is empty. Nothing in these requirements permits anyone to stay behind to operate or watch the system.
