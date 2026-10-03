---
doc_id: EGD-DEC-001
title: EmberGuard design decisions register
project: EmberGuard
doc_type: Design decisions register
version: "0.4"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the open decisions from the review note, the decision records and the build plan work
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Budget treated as a value-engineering target
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: Amish approved the recommendations for open decisions 1 to 12 (EGD-DDR-003 accepted; pitch reworded); moved to decisions made
  - version: "0.4"
    date: '2026-10-02'
    author: Amish Chadha
    change: Approved follow-ups carried out; value engineering section updated to USD 707 with the sun shade and the 45 °C charge controller priced
---

# EmberGuard design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The thermal sensor breakout is no larger than 25 x 25 mm, with the sensor can centred and four corner holes | It mounts on the inside of the pod's west wall with its can in a 9.5 mm window | EGD-DDR-003, P6 |
| 2 | The die-cast pod box has walls of 4 mm or more and its lid screws into corner bosses | The sensor and lens hood screw into tapped holes in the wall; the hood spacers into the lid | EGD-DDR-003, P6, P7 |
| 3 | The slip-on base flange fits 33.7 mm pipe, its four holes lie on an 80 mm circle and it has set screws | The wall plate's flange holes and the standoff fit depend on it | EGD-DDR-003, P1 |
| 4 | The U-bolts' leg spacing for 40 mm tube and for 33.7 mm pipe | They set the eight holes in each crossover plate | EGD-DDR-003, P1 |
| 5 | The steel enclosure comes with a gear plate on studs and a four-lug wall kit | The battery strap, board standoffs and wall fixing use them | EGD-DDR-003, P9 |
| 6 | The solar panel frame accepts the pole-mount tilt bracket | The panel's only fixing | EGD-DDR-003, P3 |
| 7 | The zone valves have inlet and outlet in line, top and bottom, with the coil to one side | The valves hang from the manifold tees | EGD-DDR-003, P10 |
| 8 | The gutter-lip clips fit the gutter's lip profile | They carry the eave line | EGD-DDR-003, P11 |
| 9 | At the house: a sound timber verge board at each gutter end, a fascia lower edge for the riser clip, and a gable wall that takes the wall anchors (about 535 N pull each) | The pods, risers and mast fix to them | EGD-DDR-003, P1, P5, P11; EGD-CAL-001, E4 |
| 10 | The charge controller takes a battery temperature probe and stops charging above 45 °C | The enclosure reaches about 63 °C in sun at 60 °C ambient, above the pack's charge limit | BOM line 9; EGD-CAL-001, F6 |
| 11 | The gable wall takes two M6 plugs for the sun shade (about 320 N pull each at 120 km/h) | The shade's only fixing | BOM line 18; EGD-CAL-001, E7 |

## Value engineering

Value-engineering target: USD 605. Estimated cost of the constructable design: USD 707 (USD 102 over the target). The target is a hypothetical control target, not a limit. Main cost drivers and savings worth trying:

- Of the USD 102 over the target, USD 84 is the parts added to make the kit buildable (EGD-DDR-003): flanges, crossover plates and U-bolts (+USD 32), pod mounts and lens hoods (+USD 18), the panel tilt bracket (+USD 6), longer cables (+USD 3), and the valve board, clips, glands and strap (+USD 25).
- The largest lines are the two thermal sensors (USD 96), the mast, standoffs and crossover plates (USD 80), the two sensor pods (USD 74) and the spray lines and heads (USD 52).
- Decided on 2026-10-02 and now priced: the folded white shade for the ground enclosure (line 18, USD 14: sheet USD 5, flat bar USD 3, paint USD 2, screws, plugs and rivets USD 4) and a charge controller with a battery temperature probe that stops charging above 45 °C (line 9, USD 4 more).
- Savings worth trying, about USD 35 in all: bolt the flanges straight to the wall without wall plates (about USD 10, but the anchor pull roughly doubles and must be rechecked), a plywood valve board (about USD 12), and unbranded thermal breakouts (about USD 10 to USD 15).
- Metal eave runs would add USD 110 and are a priced option outside the kit, not a saving.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D9: budget $425, two MLX90640 thermal arrays, gable-end mast, metal eave runs if the budget allows (it did not), tank with its own pump, pump power out of scope, adjustable arming defaults, fail to wet on sensor loss, normally closed valves | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | EGD-DDR-001 |
| 2026-09-25 | O2 to O5: budget $575, thermal sensors in gutter-corner pods, leeward zone only in wind, 2 K trigger and 10 Ah battery | Amish: "i accept all your recommendations, go with them across all repos." | EGD-DDR-002 |
| 2026-09-26 | Budget set to $605 to cover the priced BOM (N1) | Amish: "i approve all the budget items." | EGD-DDR-002 |
| 2026-09-26 | EmberGuard chosen for the first batch of product renders | Amish | Review note, 2026-09-26 |
| 2026-10-02 | Design for construction accepted: the changes P1 to P12, as made, including P10, which feeds the two zone valves side by side | Amish: "i approve your recommendations for all 555 open decisions." | EGD-DDR-003, Table 1 (P1 to P12) |
| 2026-10-02 | No window in front of the sensor for the prototype; an ash-fouled lens case is included in the TRL 4 heated-target and ash trials, and the window is decided from that result | Amish: "i approve your recommendations for all 555 open decisions." | EGD-DDR-003, A2 |
| 2026-10-02 | Pod mount: the verge cleat now, with a sound timber verge confirmed at each site; a fascia-face bracket is drawn once the partner's houses are known | Amish: "i approve your recommendations for all 555 open decisions." | EGD-DDR-003, A3 |
| 2026-10-02 | Ground enclosure: a light finish and the shadiest available wall now; the folded white shade is designed at the next revision; the charge controller must stop charging above 45 °C | Amish: "i approve your recommendations for all 555 open decisions." | EGD-CAL-001, F1; review note, 2026-09-25 |
| 2026-10-02 | Leeward wetting: larger, lower-angle droplets and a second leeward row are studied on paper at the next revision; R6 stays at the 30 km/h design wind | Amish: "i approve your recommendations for all 555 open decisions." | EGD-DDR-002, N2 |
| 2026-10-02 | Deep gutter debris: raising the pods to about 1 m above the gutter lip is studied on paper (including the arm's wind load and ember exposure); gutter guards are listed in the installation notes now | Amish: "i approve your recommendations for all 555 open decisions." | EGD-DDR-002, N3 |
| 2026-10-02 | Pitch adopted: "Gutter-corner thermal sensors and a weather mast that detect ember showers and trigger gutter and eave sprinkler zones." | Amish: "i approve your recommendations for all 555 open decisions." | EGD-DDR-002, N4 |
| 2026-10-02 | First co-design partner to approach: a recognised Firewise USA neighbourhood group in a wildland-urban interface area whose houses have gable ends with timber verges; in Texas, through the Texas A&M Forest Service, which supports such groups | Amish: "i approve your recommendations for all 555 open decisions." | EGD-DDR-001, O1 |
| 2026-10-02 | Product render layout accepted as render-only, with captions saying the mast and ground unit are drawn closer than installed | Amish: "i approve your recommendations for all 555 open decisions." | Review note, 2026-09-26, item 1 |
| 2026-10-02 | Spray lines stay blue in the concept media; the BOM still specifies black line | Amish: "i approve your recommendations for all 555 open decisions." | Review note, 2026-09-26, item 5 |
| 2026-10-02 | A third sensor for vents, decks and the far gable is left to a later version | Amish: "i approve your recommendations for all 555 open decisions." | EGD-PRC-001, open questions |
| 2026-10-02 | Ember arrival data sharing is opt-in, with the first partner agreeing what is shared and with whom | Amish: "i approve your recommendations for all 555 open decisions." | EGD-PRC-001, open questions |
