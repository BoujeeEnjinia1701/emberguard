---
doc_id: EGD-DEC-001
title: EmberGuard design decisions register
project: EmberGuard
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-01'
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
---

# EmberGuard design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the changes made to make the design buildable | Accept all; accept with changes; reject some | Accept all | The whole build plan rests on them | EGD-DDR-003, Table 1 (P1 to P12) |
| 2 | Window in front of the sensor | None (as modelled); thin polyethylene; germanium | None for the prototype; decide after heated-target and ash trials | Pod west wall and lens hood | EGD-DDR-003, A2 |
| 3 | Pod mount on houses without a timber verge board | Verge cleat only, confirmed at the site; also draw a fascia-face bracket | Verge cleat now; fascia bracket once partner houses are known | Pod mount | EGD-DDR-003, A3 |
| 4 | Shade for the ground enclosure (battery reaches about 71 °C in sun at 60 °C ambient, R10) | A folded white sheet shade on the wall; mount the unit on a shaded wall; accept | A shade, designed at the next revision | Ground unit | EGD-CAL-001, F1; review note, 2026-09-25 |
| 5 | Leeward wetting in the design wind (R6 not met) | Larger, lower-angle droplets or a second row of heads, studied on paper; restate R6 at the 4.2 m/s lee wind; wait for a spray trial | Study on paper at the next revision | Spray heads and lines | EGD-DDR-002, N2 |
| 6 | Deep gutter debris hidden by hanger straps (R1 at risk) | Restate R1 for debris near the lip; raise the pods to about 1 m above the lip; gutter guards as an installation precondition | Study higher pods on paper; list gutter guards in the installation notes | Pod arm height | EGD-DDR-002, N3 |
| 7 | Pitch wording ("Roof-edge sensor mast" no longer matches the gutter-corner pods) | Keep; "Gutter-corner thermal sensors and a weather mast that detect ember showers and trigger a gutter and eave sprinkler zone." | The new wording | None | EGD-DDR-002, N4 |
| 8 | First co-design partner | A Firewise-style neighbourhood group; a county fire-safe council; a university WUI research group | None; picked per area later | Which houses the pod mount must suit | EGD-DDR-001, O1 |
| 9 | Product render layout | Accept the render-only layout (mast and ground unit drawn nearer the front corner) and say so in captions; redraw at installed spacing | Accept, with captions | None (renders only) | Review note, 2026-09-26, item 1 |
| 10 | Spray line colour in the concept media | Keep blue for legibility; draw black as bought | Keep blue | None (media only) | Review note, 2026-09-26, item 5 |
| 11 | A third sensor for vents, decks and the far gable | Add one; leave to a later version | Leave to a later version | None now | EGD-PRC-001, open questions |
| 12 | Share anonymised ember arrival data with wildfire researchers | Yes, opt-in; no | Opt-in, decided with the first partner | Firmware only | EGD-PRC-001, open questions |

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

## Value engineering

Value-engineering target: USD 605 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 689 (USD 84 over the target). Main cost drivers and savings worth trying:

- The USD 84 over the target is the parts added to make the kit buildable (EGD-DDR-003): flanges, crossover plates and U-bolts (+USD 32), pod mounts and lens hoods (+USD 18), the panel tilt bracket (+USD 6), longer cables (+USD 3), and the valve board, clips, glands and strap (+USD 25).
- The largest lines are the two thermal sensors (USD 96), the mast, standoffs and crossover plates (USD 80), the two sensor pods (USD 74) and the spray lines and heads (USD 52).
- Savings worth trying, about USD 35 in all: bolt the flanges straight to the wall without wall plates (about USD 10, but the anchor pull roughly doubles and must be rechecked), a plywood valve board (about USD 12), and unbranded thermal breakouts (about USD 10 to USD 15).
- Metal eave runs would add USD 110 and are a priced option outside the kit, not a saving.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D9: budget $425, two MLX90640 thermal arrays, gable-end mast, metal eave runs if the budget allows (it did not), tank with its own pump, pump power out of scope, adjustable arming defaults, fail to wet on sensor loss, normally closed valves | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | EGD-DDR-001 |
| 2026-09-25 | O2 to O5: budget $575, thermal sensors in gutter-corner pods, leeward zone only in wind, 2 K trigger and 10 Ah battery | Amish: "i accept all your recommendations, go with them across all repos." | EGD-DDR-002 |
| 2026-09-26 | Budget set to $605 to cover the priced BOM (N1) | Amish: "i approve all the budget items." | EGD-DDR-002 |
| 2026-09-26 | EmberGuard chosen for the first batch of product renders | Amish | Review note, 2026-09-26 |
