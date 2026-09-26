---
doc_id: EGD-REQ-001
title: EmberGuard requirements
project: EmberGuard
doc_type: Requirements
version: "0.4"
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
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). R13 at $575; status from EGD-CAL-001 v0.2 for the gutter-corner pods, 2 K trigger, leeward-only rule and 10 Ah battery
---

# EmberGuard requirements

These requirements are proposals for review, not user-validated needs. Version 0.3 recorded Amish's decisions of 2026-09-25 (EGD-DDR-001): the budget in R13 went to $425 (D1), R8 covers the kit's own battery and makes grid-independent water an installation precondition (D6), and the arming defaults in R4 are decided (D7). Version 0.4 records his acceptance of the remaining recommendations on the same day (EGD-DDR-002): the budget is $575 (O2), the thermal sensors move to pods at the gutter corners (O3), only the leeward zone runs in wind (O4), and the trigger is 2 K with a 10 Ah battery (O5). The status column comes from EGD-CAL-001 v0.2 and `docs/04-calcs/results.csv`. Two requirements are **not met** (R6 and R13), three are **at risk** (R1, R2 and R10), one is not verifiable at TRL 3 (R11) and seven are met. The pods fix the gutter blind spot of the ridge-line head, but hanger straps still shadow deep debris, and the leeward eave stays short of water in the design wind.

Table 1. Requirements.

| ID | Requirement | Target | Verification | Status at TRL 3 (EGD-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Detect a smouldering ignition on a watched gutter or roof edge | A 100 cm² (15.5 in²) hot spot at 300 °C or hotter, anywhere along the watched gutters from 1.5 m to 13 m from the mast, within 10 s | Radiometric calculation from sensor field of view and noise; later a heated-target trial | **At risk:** from the gutter-corner pods (decided, EGD-DDR-002, O3) a 100 x 50 mm hot debris face reaches the 2 K trigger to 41 m, and a flat spot on the debris reaches it to 12.1 m (1.6 K at 13 m). Hanger straps across the gutter top shadow debris 42 mm below the lip at 83 of 118 stations and everywhere beyond 7.8 m; debris within 10 mm of the lip is seen at 95 of 118 (EGD-CAL-001 v0.2, A4, B9 to B11) |
| R2 | Detect single landed embers | A 10 mm glowing ember at 600 °C or hotter within 8 m of the mast, within 10 s | Same as R1 | **At risk:** with the 2 K trigger (decided, O5) a 600 °C ember is detected to 8.8 m centred in a pixel but only 4.4 m on a pixel corner; the false-trigger rate at 2 K is unknown (B6) |
| R3 | Watch both roof planes | Both eave gutters of the reference house, each from 1.5 m from the gable end to the far end | Line-of-sight check on the parametric model | Met: each pod sees the inside of its gutter from 1.25 m to 12.95 m from the gutter end, for an open gutter (A3, A5); see R1 for hanger straps |
| R4 | Arm only in fire weather | Automatic arming when sustained wind is 30 km/h (19 mph) or more, or gusts 50 km/h (31 mph) or more, with relative humidity 20 % or less for 10 min; manual and remote arming; defaults adjustable and reviewed with a local fire agency (decided, D7) | Design review of the arming logic | Met by design |
| R5 | Start water quickly | Water at the farthest head within 60 s of a confirmed detection | Line fill calculation | Met: 55 s for the longer zone, filling the detection-side zone first (C3) |
| R6 | Wet the gutter and roof edge | Net water on a 1.2 m wide strip along each eave (gutter, fascia and first metre of roof) of 5 mm/h or more, averaged over each spray cycle, at the design wind of 30 km/h | Droplet drift screening model; later a spray trial in wind | **Not met:** with the leeward-only rule (decided, O4) the leeward eave gets 1.5 mm/h at 8.3 m/s and 5.1 mm/h at 4.2 m/s; the windward eave is sprayed only after a windward detection, then 7.4 mm/h (C10) |
| R7 | Use little water | Steady draw 4 L/min (1.1 US gal/min) or less; 1,000 L (264 US gal) or less for a 4 h ember event | Flow calculation from head ratings and duty cycle | Met: 4 L/min and 965 L, 3.5 % margin (C5) |
| R8 | Work through a grid outage (redefined, D6) | The kit battery alone runs sensing, logic and valves for 72 h armed plus 4 h of spraying, with no solar input. Water supply that does not depend on grid power (gravity feed, generator or battery pump) is an installation precondition provided by the homeowner and is outside the kit | Energy budget; installation check of the water supply | Met: 67.5 Wh needed; the 10 Ah battery (decided, O5) gives 115.2 Wh usable at 25 °C, 103.7 Wh at 0 °C and 92.2 Wh at end of life (D4) |
| R9 | Fail safely | Loss of sensor data while armed starts spraying (decided, D8); low battery, no water pressure or a faulty valve raises an alarm; power loss closes the normally closed valves (decided, D9) | Failure modes review | Met by design |
| R10 | Survive fire weather until the front arrives | Mast and sensor pods survive gusts of 120 km/h (75 mph); electronics operate from -10 to 60 °C ambient; sensors shaded from sun and radiant heat | Wind load and thermal calculations | **At risk:** mast 14 MPa (factor 16.6) and standoffs factor 4.7 met; the enclosure reaches about 71 °C in sun at 60 °C ambient, above the battery's limit; the pods sit 0.5 m above the gutters, where embers land; radiant heat not estimated (E3, E4, F1, F4) |
| R11 | Install without roof work or mains wiring | Mast, cable and spray lines fixed to walls, fascia and gutter lips with clamps; no roof penetrations; 12 V DC only; installable by two people with hand tools in 6 h or less | Design review; later a timed trial | Not verifiable at TRL 3: met by design except the install time |
| R12 | Tell people what it is doing | Local siren and status light; phone alert when armed, spraying, faulted or low on battery when a network is available; event log of detections, wind and valve actions | Design review | Met by design; phone alerts need a working network |
| R13 | Stay within the concept budget | Kit parts $575 or less (budget raised from $300 to $425, D1, and to $575, EGD-DDR-002, O2), excluding the water source and pump, and excluding priced options | Priced BOM | **Not met:** $605, 5 % over (G1) |

## Reference house and assumptions

- **House.** Single storey, 12 x 8 m (39 x 26 ft) footprint, 2.7 m walls, gable roof at 22 degrees with the ridge along the long side, 500 mm overhangs, gutters along both long eaves (13 m each, 26 m total). The weather mast stands off one gable end at the ridge line; the two thermal sensors sit in pods beyond the gable-end corners of the gutters (EGD-DDR-002, O3).
- **Water.** A 1,000 L tank with a pump on its own supply (decided, D5). The supply must hold about 2.3 bar at the valve manifold at 4 L/min (EGD-CAL-001, C4). EmberGuard does not include the tank or pump.
- **Ember event.** 4 h of active spraying within a 72 h armed period. This is a design assumption, not a measured duration; real ember exposure varies from minutes to many hours.
- **Heads.** Six micro-sprinklers per eave at 2.2 m spacing, about 40 L/h each at 2 bar (typical catalogue figure for small irrigation heads, to be confirmed with a named part).
- **Wind drift.** Estimated at TRL 3 with a droplet screening model (EGD-CAL-001, section C) in place of the TRL 2 guess of 50 %. The leeward eave is the worst case, which is why only the leeward zone runs in wind (O4). The model is uncertain and needs a spray trial.
- **Gutters.** Open half-round or box gutters with hanger straps across the top every 750 mm (assumed), debris surface 42 mm below the lip.
- **Ember targets.** Emissivity 0.9, sensor band 8 to 14 µm, background 300 K. See EGD-CAL-001, section B.

> **Safety:** EmberGuard does not replace evacuation. Requirements R4 to R9 describe behaviour while the house is empty. Nothing in these requirements permits anyone to stay behind to operate or watch the system.
