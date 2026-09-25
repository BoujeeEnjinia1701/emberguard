---
doc_id: EGD-REQ-001
title: EmberGuard requirements
project: EmberGuard
doc_type: Requirements
version: "0.3"
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
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3. Record Amish's decisions (EGD-DDR-001); R8 redefined (pump power out of kit scope), R13 at $425, R4 defaults decided; status of every requirement from EGD-CAL-001
---

# EmberGuard requirements

These requirements are proposals for review, not user-validated needs. Version 0.3 records Amish's decisions of 2026-09-25 (EGD-DDR-001): the budget in R13 is $425 (D1), R8 now covers the kit's own battery and makes grid-independent water an installation precondition (D6), and the arming defaults in R4 are decided (D7). The status column comes from the TRL 3 calculations in EGD-CAL-001 v0.1 and `docs/04-calcs/results.csv`. Five requirements are **not met** (R1, R2, R3, R6 and R13), two are **at risk** (R8 and R10), one is not verifiable at TRL 3 (R11) and five are met. The misses in R1 and R3 come from the viewing geometry: the gutter interiors cannot be seen from the ridge-line head.

Table 1. Requirements.

| ID | Requirement | Target | Verification | Status at TRL 3 (EGD-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Detect a smouldering ignition on a watched gutter or roof edge | A 100 cm² (15.5 in²) hot spot at 300 °C or hotter, anywhere along the watched gutters from 1.5 m to 13 m from the mast, within 10 s | Radiometric calculation from sensor field of view and noise; later a heated-target trial | **Not met:** gutter interiors are hidden behind the eave; a flat spot on the roof edge gives 2.8 K at 8.2 m, below the 5 K trigger; a hot debris face of 100 x 50 mm is seen to 26 m (EGD-CAL-001, A4, B9 to B11) |
| R2 | Detect single landed embers | A 10 mm glowing ember at 600 °C or hotter within 8 m of the mast, within 10 s | Same as R1 | **Not met:** 2.4 K at 8 m centred in a pixel; reaches the 5 K trigger within 5.5 m (B4, B6) |
| R3 | Watch both roof planes | Both eave gutters of the reference house, each from 1.5 m from the gable end to the far end | Line-of-sight check on the parametric model | **Not met:** roof edges in view from 1.25 m to 13.15 m; gutter interiors not visible (A3, A4) |
| R4 | Arm only in fire weather | Automatic arming when sustained wind is 30 km/h (19 mph) or more, or gusts 50 km/h (31 mph) or more, with relative humidity 20 % or less for 10 min; manual and remote arming; defaults adjustable and reviewed with a local fire agency (decided, D7) | Design review of the arming logic | Met by design |
| R5 | Start water quickly | Water at the farthest head within 60 s of a confirmed detection | Line fill calculation | Met: 55 s for the longer zone, filling the detection-side zone first (C3) |
| R6 | Wet the gutter and roof edge | Net water on a 1.2 m wide strip along each eave (gutter, fascia and first metre of roof) of 5 mm/h or more, averaged over each spray cycle, at the design wind of 30 km/h | Droplet drift screening model; later a spray trial in wind | **Not met:** leeward eave 0.8 mm/h at 8.3 m/s and 2.6 mm/h at 4.2 m/s; windward eave 7.4 mm/h (C8) |
| R7 | Use little water | Steady draw 4 L/min (1.1 US gal/min) or less; 1,000 L (264 US gal) or less for a 4 h ember event | Flow calculation from head ratings and duty cycle | Met: 4 L/min and 965 L, 3.5 % margin (C5) |
| R8 | Work through a grid outage (redefined, D6) | The kit battery alone runs sensing, logic and valves for 72 h armed plus 4 h of spraying, with no solar input. Water supply that does not depend on grid power (gravity feed, generator or battery pump) is an installation precondition provided by the homeowner and is outside the kit | Energy budget; installation check of the water supply | **At risk:** 61.0 Wh needed; 69.1 Wh usable at 25 °C (met), but 62.2 Wh at 0 °C and 55.3 Wh at end of life leave little or no margin (D4) |
| R9 | Fail safely | Loss of sensor data while armed starts spraying (decided, D8); low battery, no water pressure or a faulty valve raises an alarm; power loss closes the normally closed valves (decided, D9) | Failure modes review | Met by design |
| R10 | Survive fire weather until the front arrives | Mast and head survive gusts of 120 km/h (75 mph); electronics operate from -10 to 60 °C ambient; head shaded from sun and radiant heat | Wind load and thermal calculations | **At risk:** mast 27 MPa (factor 8.9) and standoffs factor 3.5 met; the enclosure reaches about 71 °C in sun at 60 °C ambient, above the battery's limit; radiant heat not estimated (E3, E4, F1) |
| R11 | Install without roof work or mains wiring | Mast, cable and spray lines fixed to walls, fascia and gutter lips with clamps; no roof penetrations; 12 V DC only; installable by two people with hand tools in 6 h or less | Design review; later a timed trial | Not verifiable at TRL 3: met by design except the install time |
| R12 | Tell people what it is doing | Local siren and status light; phone alert when armed, spraying, faulted or low on battery when a network is available; event log of detections, wind and valve actions | Design review | Met by design; phone alerts need a working network |
| R13 | Stay within the concept budget | Kit parts $425 or less (budget raised from $300, D1), excluding the water source and pump, and excluding priced options | Priced BOM | **Not met:** $571 (G1) |

## Reference house and assumptions

- **House.** Single storey, 12 x 8 m (39 x 26 ft) footprint, 2.7 m walls, gable roof at 22 degrees with the ridge along the long side, 500 mm overhangs, gutters along both long eaves (13 m each, 26 m total). The sensor mast stands off one gable end at the ridge line.
- **Water.** A 1,000 L tank with a pump on its own supply (decided, D5). The supply must hold about 2.3 bar at the valve manifold at 4 L/min (EGD-CAL-001, C4). EmberGuard does not include the tank or pump.
- **Ember event.** 4 h of active spraying within a 72 h armed period. This is a design assumption, not a measured duration; real ember exposure varies from minutes to many hours.
- **Heads.** Six micro-sprinklers per eave at 2.2 m spacing, about 40 L/h each at 2 bar (typical catalogue figure for small irrigation heads, to be confirmed with a named part).
- **Wind drift.** Estimated at TRL 3 with a droplet screening model (EGD-CAL-001, section C) in place of the TRL 2 guess of 50 %. The leeward eave is the worst case. The model is uncertain and needs a spray trial.
- **Ember targets.** Emissivity 0.9, sensor band 8 to 14 µm, background 300 K. See EGD-CAL-001, section B.

> **Safety:** EmberGuard does not replace evacuation. Requirements R4 to R9 describe behaviour while the house is empty. Nothing in these requirements permits anyone to stay behind to operate or watch the system.
