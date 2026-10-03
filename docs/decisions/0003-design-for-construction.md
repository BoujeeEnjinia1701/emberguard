---
doc_id: EGD-DDR-003
title: EmberGuard design for construction
project: EmberGuard
doc_type: Design decision record
version: "0.4"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: Accepted by Amish, including the recommendations for A2 and A3
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: Product render note updated; appearance model brought to the constructable design
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** accepted. Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This covers every change in Tables 1 and 2 and the recommendations for A2 and A3 in Table 3, now decided as recommended and recorded in the design decisions register (EGD-DEC-001); A1 is a value-engineering note carried in the register. The changes were made under Amish's 2026-09-30 instruction to make the design physically buildable.

## Context

On 2026-09-30 Amish asked for every repo to get an illustrated prototype build plan and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The concept model of EGD-DDR-002 showed what EmberGuard does but was a massing model: many parts overlapped, floated or had no fixing. Checking the model with build123d (intersection volumes and gaps between every pair of parts and against the reference house) found the problems in Table 1.

The changes keep what EmberGuard does: the mast's position, height and sensors, the pods' position 200 mm beyond each gutter end and 500 mm above the lip, the sensors' aim (10 degrees toward the house, 5 degrees down) and 55 x 35 degree view, the two spray zones with six heads each at 4 L/min, the ground unit's contents and the 12 V, no-mains, no-roof-penetration approach. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now runs 103 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, parts that must not touch are apart by at least the stated clearance, and nothing stands in either thermal sensor's view. All 103 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The two standoff pipes ran straight into the mast's centre line, through the tube, joined by solid collars; at the wall each pipe butted onto a 12 mm plate, which would need welding to galvanized pipe. | Each standoff now passes 6 mm beside the mast, its centre 43 mm to the side, and a 100 x 100 x 6 mm aluminium crossover plate sits between them: two M8 U-bolts round the mast and two round the pipe. At the wall the pipe sits in a bought slip-on base flange (set-screw grip), bolted with four countersunk M8 screws to a 140 x 140 x 8 mm aluminium wall plate held by four M10 anchors. | The crossover clamp is the standard way to join two tubes at right angles without welding or drilling either. The flange needs no threads on the pipe. The wall plate keeps the 100 mm anchor spacing that EGD-CAL-001 used, so the 535 N anchor pull still stands [E4]. |
| P2 | The mast cable ran up the outside of the mast and through both standoff collars and the humidity sensor's arm. | The mast cable runs inside the 36 mm bore of the mast, leaves through a grommet in a plastic end cap at the mast foot, runs under the lower standoff to the wall and down it. The humidity and panel leads enter the tube through two grommeted 12 mm holes. | The tube protects the cable from embers and sun; nothing else needs a hole through it. |
| P3 | The solar panel floated 42 mm from the end of its arm, and it faced away from the equator side (+Y in the model) instead of toward it (-Y), as the precis gives. | The panel faces south (the equator side, -Y in the model) at 45 degrees on a bought pole-mount tilt bracket: a clamp on the mast, a short arm and a rail bolted to the panel frame. | Corrects the model to the stated design and gives the panel a fixing. The wind area and height are unchanged, so the mast check stands [E2], [E3]. |
| P4 | The humidity shield's plates floated on an arm that passed through one of them, and the arm only touched the mast. The anemometer's adapter was a solid block sitting on the open mast top. | The shield's five plates sit on a centre rod with an arm above them and a clamp on the mast. The anemometer and vane crossarm stand on a sleeve that slides 40 mm over the mast top with two set screws. | These are how the bought weather-station spares fit; the parts now have something to hold them. |
| P5 | The pod bracket ended in a solid clamp block sitting inside the end of the gutter (96,000 mm³ of overlap), with a 20 mm rod post and arm and no real fixing to the house. | A verge cleat (80 x 80 x 6 mm aluminium angle, 140 mm long) is screwed by two 8 mm coach screws to the end of the roof overhang (the verge or barge board), 30 to 170 mm in from the eave edge. A 40 x 6 mm flat bar arm, bent twice, is bolted flat on the cleat and carries a 6 mm pod plate on its top tab. The plate turns on an M8 pivot bolt and an M6 bolt in a curved slot locks the 10 degree aim; two spacers of different height under the pod give the 5 degree downward tilt. | A gutter is too thin to carry a pod 500 mm above it; the verge board is the strongest timber at the eave corner and is not part of the roof covering, so R11's "no roof penetrations" still holds. The arm stays clear of the roof, fascia and gutter by 8 mm and the pod by 18 mm. At 120 km/h the arm sees about 8 MPa (factor 19 on 6063-T6) and each coach screw about 70 N of pull [E5]. |
| P6 | The sensor looked down a 32 mm tube reaching 70 mm out of the pod, through a wall with no opening. A tube of 29 mm bore that long would cut the sensor's 55 x 35 degree view to about 23 degrees across. | The sensor's 9.2 mm can sits in a 9.5 mm window in the pod's west wall, its board screwed to the inside of the wall on four M2.5 screws over 1 mm washers. Outside, a short lens hood bent from 1 mm stainless (28 x 18 mm inside, 20 mm deep) shades the window. A new check builds the sensor's 55 x 35 degree view as a solid and confirms it clears the lens hood, the pod hood and the mount. | Keeps the full field of view, on which the gutter coverage of EGD-CAL-001 section A depends, while still shading the lens from above and the sides. |
| P7 | The hood was a 6 mm slab floating 2 mm above the pod with no fixing. | The hood is 1 mm stainless with 10 mm drip flanges, on four 15 mm M4 spacers screwed into the lid, overhanging the lens end by 40 mm. | Gives it a fixing and an air gap that keeps sun and radiant heat off the box. This adopts the spaced hood of the product appearance model (review note, 2026-09-26, item 3). |
| P8 | Inside the pod the node board was not modelled, and the sensor board filled the inside height exactly. | The node board stands on four 12 mm standoffs on the pod floor, clear of the two M6 bolts that come down from inside the pod to the pod plate. The pod cable enters through an M16 gland in the east wall. | Everything inside is fixed and reachable with the lid off. |
| P9 | The ground enclosure floated 5 mm off the wall with no fixing; the cables entered through its top; the controller, relay and battery floated inside (the battery 32 mm above the floor). | Four wall lugs at the back corners hold the box 2 mm off the wall on M8 screws into wall plugs. Inside, the box's gear plate sits on four studs; the controller and relay stand on standoffs on it; the battery stands on the floor against it, held by a strap. The cables enter through four M20 glands in the bottom, near the door, clear of the battery. The siren sits on the top on its gasket; the key switch goes through the door. | A sealed box is entered from below so water runs off the glands. |
| P10 | The valves and manifold floated 250 mm off the wall, held only by the spray lines, and the valves sat in line on the manifold, so a closed valve A would have shut off the water to valve B. | A 3 mm aluminium valve board on the wall carries the manifold in two stand-off pipe clips, 520 mm above the ground. Each valve hangs from its own tee on the manifold, so the zones are fed side by side; a third tee carries the pressure transducer. | The zones can now run independently, which the leeward-only rule (EGD-DDR-002, O4) needs. |
| P11 | Each riser stood free 250 mm from the gable wall for 2.2 m and passed up through the gutter's outer lip; the eave line floated 22 mm above the lip with no clips. | Each riser runs along the base of the gable wall and up its corner on saddle clips, turns out under the gutter at 2.3 m (one stand-off clip screwed into the fascia's lower edge), rises 8 mm in front of the gutter and turns along it. The eave line sits 20 mm in front of the lip and 30 mm above it in 24 gutter-lip clips (already in the BOM, now modelled); the heads sit on tees. | Every metre of line is now supported and nothing passes through the gutter. The zone lines are 17.5 m and 21.1 m (were 17.7 m and 21.3 m), so water reaches the farthest head in 54 s (was 55 s) [C2], [C3]; the supply still needs about 2.3 bar [C4]. |
| P12 | The pod cables ran through the air beyond the house corner; the mast earthing (item 17) was not modelled. | Each pod cable runs along its arm, round the verge, under the soffit and down the gable wall corner to the enclosure's bottom glands. A bonding clamp on the mast foot, a 16 mm² conductor held 40 mm off the wall (clear of the spray line along the wall base) and a 1.2 m earth rod 400 mm out from the wall are now in the model. | Every cable and conductor has a supported route that the build plan can show. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Cost | BOM lines 1, 2, 7, 9, 13, 14 and 16 respecified, lines 1, 2, 9, 13 and 16 repriced: kit $689.00 against the $605 value-engineering target, USD 84 or 14 % over [G1]. R13 moves from met to over the target. `budget_usd` is unchanged (Table 3, A1). | Parts added for construction: flanges, crossover plates and U-bolts (+$32), pod mounts and lens hoods (+$18), panel tilt bracket (+$6), longer cables (+$3), valve board, clips, glands and strap (+$25). |
| Calculations | EGD-CAL-001 v0.4: line lengths, fill times and supply pressure from the new routes [C2] to [C4]; a new wind check on the pod arm and cleat [E5]; cost [G1]. | Follows the model. |
| Drawing | EGD-DWG-001 Rev P4; making sketches EGD-DWG-101 to 113 added. | Follows the model. |
| Documents | EGD-REQ-001 v0.6 (R5, R10, R11, R13), EGD-PRC-001 v0.6 (components, numbers, cost). | Follows the model. |
| Product renders | The appearance model `cad/src/product_model.py` was brought to the constructable design on 2026-10-02 (pod mount and lens hood, riser, panel facing the equator, valve board, sun shade) and the render scenes exported. The photoreal renders, `media/card.png` and `media/social-preview.png` are made on Amish's Mac next. | Blender is on Amish's Mac. |

*Table 3. Proposed for Amish; A2 and A3 accepted as recommended on 2026-10-02.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | The kit now prices at $689 against the $605 value-engineering target (`budget_usd`, a hypothetical control target), USD 84 over. | No decision needed. The target stays $605. Savings worth trying, about $35: bolt the flanges straight to the wall without wall plates (about $10, but the anchor pull roughly doubles and must be rechecked), a plywood valve board (about $12), unbranded thermal breakouts (about $10 to $15); quotations at TRL 4 may also move the estimate. | Carry in the value engineering section of EGD-DEC-001. The added parts are what makes the kit buildable; the savings trade strength and quality for small sums. |
| A2 | The sensor can now sits open in the pod's west wall, sealed by an O-ring but with nothing in front of the lens. | (a) no window, as modelled; (b) a thin polyethylene window across the lens hood's mouth (passes long-wave infrared, cheap, melts in ember attack); (c) a germanium window (about $30 to $60 each). | (a) for the prototype; decide after the heated-target and ash trials at TRL 4. Accepted by Amish, 2026-10-02, with an ash-fouled lens case included in those trials. |
| A3 | The pod mount needs a sound timber verge (barge) board at each gutter end. Many houses have one; some have a metal verge or none. | (a) the verge cleat as modelled, confirmed at the site; (b) also draw a fascia-face bracket for houses without a timber verge, at the next revision. | (a) now, (b) when a co-design partner's houses are known (O1). Accepted by Amish, 2026-10-02. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan EGD-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`); decisions are indexed in the design decisions register EGD-DEC-001.
- With A2 accepted, the prototype has no window in front of the sensor and the TRL 4 trials include an ash-fouled lens case. With A3 accepted, the verge cleat is used and a sound timber verge is confirmed at each site.
- Requirement status: one not met (R6), one over its value-engineering target (R13), three at risk (R1, R2, R10), one not verifiable at TRL 3 (R11), seven met (EGD-CAL-001 v0.4). R13 is the only change.
- The product renders and storefront images need updating on Amish's Mac.
- The enclosure, thermal breakout, pod box, flange and U-bolts are chosen at TRL 4; their hole patterns must be checked then (register, items to confirm).
