---
doc_id: EGD-DDR-002
title: EmberGuard recommendations accepted
project: EmberGuard
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); record the decisions on O2 to O5 of EGD-DDR-001 and what changed in the repo
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted for items O2 to O5 of EGD-DDR-001; item O1 remains proposed

## Context

After the TRL 3 session, EGD-DDR-001 left five items open (O1 to O5) and `docs/REVIEW.md` listed them under "Still awaiting Amish". Four of them carried a recommendation. On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every open item with a recommendation is therefore decided in favor of that recommendation. Where a recommendation offered several options, the recommended option is the decision. The item without a recommendation (O1, the first co-design partner) stays open. TRL 4 remains on hold by Amish's instruction, and the project stays at `trl: 3`, `trl_target: 3`.

## Options considered

The options for each item are those in EGD-DDR-001, Table 2, and in `docs/REVIEW.md` (session 2026-09-25, TRL 3).

## Decision

*Table 1. Items decided on 2026-09-25 and what changed in the repo.*

| # | Item | Decision | What changed |
| --- | --- | --- | --- |
| O2 | Cost against the budget | Decided by Amish, 2026-09-25: go with recommendation. Option (a): raise `budget_usd` from $425 to $575 while O3 and O4 are resolved. | `project.yaml` `budget_usd` 425 to 575; R13 target $575 in EGD-REQ-001 v0.4. The revised kit (O3 and O5 below) prices at $605, so R13 is still not met, by 5 % (EGD-CAL-001 v0.2, G1). |
| O3 | Gutters hidden from the ridge-line head | Decided by Amish, 2026-09-25: go with recommendation. Option (b): move the two thermal sensors into small pods at the gable-end gutter corners, each looking along its gutter from outboard. | The ridge-line sensor head is removed. BOM item 2 is now two sensor pods (die-cast box, stainless hood, pod node board, bracket clamped to the gutter end and fascia corner), $28 each; item 13 adds two pod cables ($20 to $30). The mast keeps the wind, humidity and solar parts. `cad/src/model.py` places each pod 200 mm beyond the gutter end and 500 mm above the lip, aimed along the gutter, 10 degrees toward the house and 5 degrees down; STEP and STL re-exported (`sensor-head` replaced by `sensor-pod`). EGD-CAL-001 v0.2: open gutter in view from 1.25 to 12.95 m (was none); R3 now met. Hanger straps across the gutter top shadow debris 42 mm below the lip at 83 of 118 stations and everywhere beyond 7.8 m, so R1 is at risk rather than met. Drawing EGD-DWG-001 to Rev P2. |
| O4 | Net wetting in wind (R6) | Decided by Amish, 2026-09-25: go with recommendation. Option (a): run only the leeward zone, chosen from the wind vane. | Firmware rule added to EGD-PRC-001 v0.4: above 2 m/s of cross-eave wind only the leeward zone runs, continuously at 4 L/min; a detection on the windward side returns to alternating zones. Leeward eave 0.8 to 1.5 mm/h at 8.3 m/s and 2.6 to 5.1 mm/h at 4.2 m/s (EGD-CAL-001 v0.2, C10). R6 is still not met at the 30 km/h design wind, and the windward eave is dry until a windward detection. Flow diagram redrawn for the leeward-only case. |
| O5 | Ember trigger threshold and battery margin | Decided by Amish, 2026-09-25: go with recommendation. Adopt both: a 2 K persistent-spot trigger and a 12.8 V 10 Ah battery. | Trigger 5 K to 2 K in EGD-PRC-001 and EGD-CAL-001. A 600 °C ember now reaches the trigger to 8.8 m centred in a pixel (was 5.5 m), 4.4 m on a pixel corner; R2 moves from not met to at risk, as the false-trigger rate at 2 K is unknown. BOM item 8 is a 10 Ah pack ($32 to $45); usable energy 69.1 to 115.2 Wh at 25 °C, 55.3 to 92.2 Wh at end of life against a 67.5 Wh need (was 61.0 Wh; two pod nodes replace one head node). R8 moves from at risk to met. |

*Table 2. Items still open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First partner for co-design and field input (a Firewise-style neighbourhood group, a county fire-safe council or a university WUI research group) | Proposed, awaiting Amish. No partner was recommended; co-design partners are to be picked per area later. |
| N1 | Cost of the revised kit: $605 against the new $575 budget | Proposed, awaiting Amish. New at this revision, raised by the O3 and O5 changes. Options: (a) raise the budget to about $610; (b) find about $30 of savings, for example a lighter mast now that it carries no sensor head, or unbranded thermal breakouts; (c) accept R13 as not met until a TRL 4 costing with quotes. Recommendation: (b), with (a) as the fallback. |
| N2 | Leeward wetting at the design wind | Proposed, awaiting Amish. New at this revision. The leeward-only rule does not meet R6 at 8.3 m/s. Options: (a) larger, lower-angle droplets or a second row of heads on the leeward side, studied on paper; (b) restate R6 at the 4.2 m/s local wind the eave sees in the lee of the ridge, where the rule gives 5.1 mm/h; (c) wait for a spray trial in wind (TRL 4, on hold). Recommendation: (a) at the next TRL 3 revision. |
| N3 | Gutter hanger shadow | Proposed, awaiting Amish. New at this revision. Options: (a) restate R1 for debris that reaches within about 10 mm of the lip, which the pods see at 95 of 118 stations; (b) raise the pods to about 1 m above the lip; (c) recommend gutter guards as an installation precondition. Recommendation: (b) studied on paper, with (c) in the installation notes. |
| N4 | Pitch wording | Proposed, awaiting Amish. New at this revision. The pitch in `project.yaml` and `README.md` still says "Roof-edge sensor mast that detects ember showers", but the thermal sensors now sit in gutter-corner pods. Recommendation: "Gutter-corner thermal sensors and a weather mast that detect ember showers and trigger a gutter and eave sprinkler zone." The pitch is unchanged until Amish decides. |

## Consequences

- `project.yaml`: `budget_usd` 575 (was 425). Pitch and problem lines unchanged; no rewording was recommended before this record, and a new wording is proposed as N4.
- EGD-REQ-001 v0.4: R13 target $575; status of every requirement from EGD-CAL-001 v0.2. Two not met (R6, R13), three at risk (R1, R2, R10), one not verifiable at TRL 3 (R11) and seven met. Before this record: five not met, two at risk.
- EGD-PRC-001 v0.4: gutter-corner pods, 2 K trigger, leeward-only rule and 10 Ah battery; numbers from EGD-CAL-001 v0.2.
- EGD-CAL-001 v0.2: section A rewritten for the pods, radiometry at 2 K, leeward-only wetting, pod-node energy, mast without a head, cost.
- EGD-PRB-001 v0.4: budget constraint updated.
- EGD-DDR-001 v0.2: O2 to O5 marked as decided.
- `bom/bom.csv`: items 2, 3, 8 and 13 revised; kit total $571 to $605.
- `cad/src/model.py`, `cad/step/`, `cad/stl/`, `cad/drawings/EGD-DWG-001` (Rev P2), `media/`: regenerated from the revised model.
- Cross-repo actions: none. EmberGuard's pump option (c) still only studies a SwapCell pack and is not adopted.
- TRL 4 work (heated-target and ember trials, recorded thermal video for false triggers at 2 K, spray trial in wind, battery and enclosure heat tests, firmware beyond a sketch) stays on hold by Amish's instruction.
