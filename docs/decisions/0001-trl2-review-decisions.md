---
doc_id: EGD-DDR-001
title: EmberGuard TRL 2 review decisions
project: EmberGuard
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's decisions on the TRL 2 review items and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: O1 decided by Amish on 2026-10-02 (recommendation approved, EGD-DEC-001)
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted for items D1 to D9; items O2 to O5 accepted on 2026-09-25 (recorded in EGD-DDR-002); item O1 was decided on 2026-10-02 (EGD-DEC-001)

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed ten items as "Proposed, awaiting Amish", and the design precis EGD-PRC-001 v0.2 listed its key design choices as proposed. On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." Every item that carried a recommendation is therefore decided in favor of that recommendation. The item without a recommendation stays open, and the new questions raised by the TRL 3 calculations (EGD-CAL-001) are recorded as open.

The same instruction approved three portfolio-wide decisions: SwapCell interface v0.3 adds a wake method for hosts without CAN, a charge-while-discharging mode and a latch vibration rating for vehicles; shared SwapCell packs are priced once and excluded from each dependent kit budget; and community designs pick co-design partners per area later. EmberGuard does not use SwapCell in its baseline. The SwapCell items apply only to pump power option (c) under D6, which is studied, not adopted. The partner rule applies to O1.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in EGD-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Decided items.*

| # | Item | Decision |
| --- | --- | --- |
| D1 | Budget | Option (a): raise `budget_usd` from $300 to $425. `project.yaml` is updated. R13 now reads "$425 or less". Decided by Amish, 2026-09-25: go with recommendation. At TRL 3 the priced BOM totals $571 (EGD-CAL-001, G1), so R13 is still not met; see O2. |
| D2 | Sensing approach | Two MLX90640-class thermal arrays (32 x 24 pixels, 55 x 35 degree lens), not near-infrared flame sensors or a single wide-angle array. Decided by Amish, 2026-09-25: go with recommendation. |
| D3 | Mast position | Gable end at the ridge line, watching both roof planes. Decided by Amish, 2026-09-25: go with recommendation. EGD-CAL-001 (A4) shows that from this position the gutter interiors are hidden behind the eave; see O3. |
| D4 | Eave line material | Metal (copper or galvanized steel) on the eave runs and polyethylene only on the risers, if the budget allows. Decided by Amish, 2026-09-25: go with recommendation. At TRL 3 the budget does not allow it: the kit is already $146 over $425 and metal runs add $110. Polyethylene eave runs therefore stay in the baseline, and metal runs are carried as a priced option in `bom/bom.csv`. |
| D5 | Water source for the first design case | A tank with a pump on its own supply, not a mains connection, to protect hydrant pressure. Decided by Amish, 2026-09-25: go with recommendation. |
| D6 | Pump power in an outage | Option (a): pump power is out of the kit's scope; the homeowner provides a generator, a gravity feed or a battery pump. Options (b), a 12 V pump with its own battery, and (c), a 12 V pump on a SwapCell pack, were to be studied at TRL 3. Decided by Amish, 2026-09-25: go with recommendation. R8 is redefined so the kit battery covers sensing, logic and valves, and water supply independence from the grid is an installation precondition. The study is in EGD-CAL-001, section D. |
| D7 | Arming thresholds | Adjustable defaults of 30 km/h sustained or 50 km/h gusts with relative humidity at or below 20 % for 10 min, plus manual and remote arming; defaults to be reviewed with a local fire agency. Decided by Amish, 2026-09-25: go with recommendation. |
| D8 | Behaviour on sensor loss while armed | Fail to wet. Decided by Amish, 2026-09-25: go with recommendation. |
| D9 | Valve type | Normally closed valves that close on power loss, not latching valves. Decided by Amish, 2026-09-25: go with recommendation. |

*Table 2. Items left open by this record. O2 to O5 were decided later on 2026-09-25; see EGD-DDR-002 for what changed.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First partner for co-design and field input (a Firewise-style neighbourhood group, a county fire-safe council or a university WUI research group) | Decided by Amish, 2026-10-02 (recommendation approved): first partner to approach is a recognised Firewise USA neighbourhood group in a wildland-urban interface area whose houses have gable ends with timber verges; in Texas, through the Texas A&M Forest Service (EGD-DEC-001). |
| O2 | Cost against the $425 budget | Decided by Amish, 2026-09-25: go with recommendation (budget raised to $575; EGD-DDR-002). The priced BOM is $571, 34 % over. Options: (a) raise the budget to about $575; (b) drop to one thermal sensor and one zone watching one roof plane only, about $480, still over; (c) cost the spray lines, valves, transducer and earthing (about $121) as a separate zone kit, leaving a sense and control kit of about $450, still over. Recommendation: (a), because the misses in O3 and O4 need resolving before cutting parts. |
| O3 | Gutters hidden from the ridge-line head | Decided by Amish, 2026-09-25: go with recommendation (corner sensor pods; EGD-DDR-002). From 228 mm above the ridge, no point of either gutter interior is visible, and flat hot spots on the roof are seen at 1 to 3 degrees (EGD-CAL-001, A4 and A6). Options: (a) redefine R1 and R3 to the roof edge strip and accept unwatched gutters, relying on gutter guards and spraying; (b) move the two sensors to small pods at the gable-end gutter corners, looking along each gutter from outboard; (c) raise the head 1.0 to 1.5 m above the ridge, which improves grazing angles but still cannot see into the gutters (10.6 m would be needed). Recommendation: (b), studied at the next TRL 3 revision. |
| O4 | Net wetting in wind (R6) | Decided by Amish, 2026-09-25: go with recommendation (leeward zone only; EGD-DDR-002). A droplet screening model puts 0.8 to 2.6 mm/h on the leeward eave against 5 mm/h (EGD-CAL-001, C8). Options: (a) run the leeward zone only, chosen from the wind vane; (b) run both zones continuously at 8 L/min, which breaks R7; (c) redefine R6 for the windward eave and accept the leeward shortfall. Recommendation: (a), as it keeps 4 L/min. |
| O5 | Ember trigger threshold and battery margin | Decided by Amish, 2026-09-25: go with recommendation (2 K trigger and 10 Ah battery; EGD-DDR-002). A 2 K persistent-spot threshold (10 times the 4 Hz noise) would detect a 600 °C ember to 8.8 m and meet R2 for an ember centred in a pixel (EGD-CAL-001, B7), at an unknown false-trigger cost. A 12.8 V 10 Ah battery (about $13 more) would restore the R8 margin at 0 °C and end of life. Recommendation: adopt both. |

## Consequences

- `project.yaml`: `budget_usd` is 425. The pitch and problem lines are unchanged; no rewording was recommended.
- EGD-REQ-001 v0.3: R8 redefined (D6), R13 target $425 (D1), R4 defaults recorded as decided (D7); status of every requirement taken from EGD-CAL-001.
- EGD-PRC-001 v0.3: design choices D2, D3, D5, D7, D8 and D9 are no longer "proposed"; the eave runs stay polyethylene under D4; numbers match EGD-CAL-001.
- EGD-PRB-001 v0.3: budget constraint and the tank-first open question updated.
- `bom/bom.csv`: metal eave runs listed as a priced option outside the kit total.
- TRL 4 work stays on hold by Amish's instruction.
