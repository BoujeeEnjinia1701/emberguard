---
doc_id: EGD-BLD-001
title: EmberGuard prototype build plan
project: EmberGuard
doc_type: Build plan
version: "0.2"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: First build plan; design made constructable (EGD-DDR-003)
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Budget treated as a value-engineering target
---

# EmberGuard prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order, in three groups each drawn at its own scale. One of the two sensor pods is shown.*

The prototype is one EmberGuard kit fitted to the east gable end of a single-storey house like the 12 x 8 m reference house: a 2.45 m aluminium mast held 700 mm off the gable wall by two steel standoffs, carrying the wind sensors, a humidity sensor and a 10 W solar panel; two small sensor pods, each on an arm screwed to the end of the roof overhang beyond a gutter, looking along that gutter with a thermal camera; a steel ground enclosure on the gable wall holding the battery, controller and relay; a valve board below it with two zone valves; and a spray line clipped along each gutter lip with six micro-sprinklers. Figure 1 shows the 26 components in the order you make or fit them. Thirteen are made or drilled in a small workshop: the wall plates, standoff pipes, crossover plates, mast tube, pod boxes, lens hoods, pod hoods, pod plates, pod arms, verge cleats, enclosure, battery strap and valve board. Everything else is bought and fitted: the sensors, panel, battery, electronic modules, valves, flanges, U-bolts, line, heads and clips. The work is sawing, drilling, tapping, bending flat bar, folding thin stainless sheet, wiring bought modules with screw terminals, and fixing to a house wall from a ladder. The parts cost about $689 from the bill of materials, against a value-engineering target of $605.

> **Safety:** Fitting the kit means working at height at the roof edge. Use a stable ladder with a second person footing it, never stand on the roof covering, and do not work in wind, rain or on a wet or mossy surface. The kit holds a 12.8 V lithium iron phosphate battery of about 128 Wh: keep its fuse out until section 6 says otherwise. It runs on 12 V DC only; the pump keeps its own mains supply and certified controls, and EmberGuard touches it only through a dry contact. The mast is the highest point on the house and must be earthed before it is left standing. EmberGuard never replaces evacuation: nobody stays behind to watch or operate it during a fire.

## 2. What changed to make it buildable

The concept showed what EmberGuard does; many of its parts could not be made or fixed as drawn. Each change below keeps what the kit does, and all of them are recorded in decision record EGD-DDR-003, open for Amish's review.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Mast standoffs | Pipes running into the middle of the mast through solid collars; pipes butted onto 12 mm wall plates | Pipes passing beside the mast, joined by a crossover plate and four U-bolts; slip-on flanges bolted to aluminium wall plates (Figures 3 and 6) | No welding and no holes in the mast or pipe |
| Mast cable | Up the outside of the mast, through the standoff collars and the humidity sensor's arm | Inside the mast tube, out through the end cap, under the lower standoff (Figure 8) | Protected from embers; nothing in its way |
| Solar panel | Floating 42 mm off its arm, facing away from the sun | Facing south at 45 degrees on a clamp, arm and tilt rail (Figure 9) | A real fixing, facing the right way |
| Weather sensors | Shield plates and the wind sensor head floating on the mast | Shield on a centre rod and mast clamp; wind sensors on a sleeve over the mast top | How the bought spares fit |
| Pod mount | A clamp block buried in the gutter end and a thin rod post | A cleat screwed to the end of the roof overhang, a bent flat bar arm and a pod plate that sets the aim (Figures 15 and 18) | A gutter cannot carry a pod 500 mm above it; the verge board can |
| Thermal sensor | Looking down a 70 mm tube through a wall with no hole; the tube would have cut its view to less than half | Sensor in a small window in the pod wall with a short lens hood that clears the full 55 x 35 degree view (Figure 11) | Keeps the view the gutter coverage depends on |
| Pod hood | A slab floating above the pod | Folded stainless sheet on four spacers, with an air gap (Figure 13) | A fixing, and shade for the box |
| Ground enclosure | Floating off the wall; cables in through the top; battery and boards floating inside | Wall lugs; glands in the bottom; battery strapped on the floor; boards on the gear plate (Figures 20 and 21) | Fixed, sealed and entered from below |
| Valves | Floating 250 mm off the wall, in line on the manifold so one would block the other | On their own tees under a manifold on a wall-mounted valve board (Figure 25) | Each zone runs on its own |
| Spray lines | Risers standing free and passing up through the gutter; the eave line floating above the lip | Risers on wall clips up the gable corner, out under the gutter and up in front of it; eave line in lip clips (Figures 26 and 27) | Supported all the way; nothing through the gutter |
| Cables and earthing | Pod cables in the air beyond the house; no earthing in the model | Cables along the arms, under the verge and down the wall; earth clamp, conductor and rod (Figure 8) | Every run supported and shown |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "East" is away from the gable wall, "front" is the eave nearer the street (zone A), "back" the other eave (zone B). Workshop tolerance is 0.5 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4.

### 3.1 Wall plates (make 2)

![Figure 2. Making sketch of the wall plate](../cad/drawings/EGD-DWG-101.png)

*Figure 2. Wall plate making sketch (EGD-DWG-101).*

**What it is and what it is made from.** The square plate that carries each standoff on the gable wall. Aluminium plate 8 mm thick, 6082 or 5083 class, 140 x 140 mm.

**How to make it.**

1. Cut two blanks 140 x 140 mm. File the edges square and round the corners to about 3 mm.
2. Mark the centre. Anchor holes: four 11 mm holes on a 100 mm square, 20 mm in from each edge.
3. Flange holes: four 9 mm holes on an 80 mm circle, on the diagonals. Check this circle against the flange you bought first.
4. Countersink the four flange holes on the wall side so the M8 countersunk screw heads sit flush.
5. Deburr both faces.

**How it fits the parts next to it.**

![Figure 3. Joint 1: wall plate, flange and standoff](05-build-plan/joint-01.png)

*Figure 3. The plate lies flat on the wall; the flange is bolted to its outer face; the standoff pipe goes into the flange hub to its stop.*

The plate's back lies flat on the gable wall, held by four M10 anchors, its centre 43 mm to the side of the mast's line (toward the back eave) and 2.45 m or 3.90 m above the ground. The flange sits flat on its outer face on four M8 countersunk screws with nyloc nuts on the flange side.

**Check before moving on.** With the flange bolted on, the plate's back is flat: no screw head stands proud.

### 3.2 Standoff pipes (make 2)

![Figure 4. Making sketch of the standoff pipe](../cad/drawings/EGD-DWG-102.png)

*Figure 4. Standoff pipe making sketch (EGD-DWG-102).*

**What it is and what it is made from.** The arm that holds the mast 700 mm out from the wall. Galvanized steel pipe DN25, 33.7 mm outside, 3.2 mm wall.

**How to make it.**

1. Cut two 739 mm lengths with a pipe cutter or hacksaw. Square the ends with a file and deburr inside and out.
2. Paint the cut ends with zinc-rich paint and let it dry.
3. Push a plastic end cap onto one end of each.

**How it fits the parts next to it.** The plain end goes 45 mm into the flange hub, to its stop, and the flange's set screws grip it. The pipe runs straight out from the wall, passes 6 mm beside the mast and ends 50 mm beyond it; the crossover plate lies between the two (Figure 6).

**Check before moving on.** Length 739 mm within 2 mm; both ends square.

### 3.3 Crossover plates (make 2)

![Figure 5. Making sketch of the crossover plate](../cad/drawings/EGD-DWG-103.png)

*Figure 5. Crossover plate making sketch (EGD-DWG-103).*

**What it is and what it is made from.** The plate that joins the mast to each standoff at right angles. Aluminium plate 6 mm, 6082 or 5083 class, 100 x 100 mm.

**How to make it.**

1. Cut two 100 x 100 mm blanks; deburr.
2. Mark a centre cross. Mast U-bolt holes: four 9 mm holes, 24 mm each side of the vertical centre line, 30 mm above and below the horizontal one.
3. Standoff U-bolt holes: four 9 mm holes, 35 mm each side of the vertical centre line, 20.9 mm above and below the horizontal one. Check both patterns against the U-bolts you bought first.
4. Drill the two plates clamped together so they match.

**How it fits the parts next to it.**

![Figure 6. Joint 2: crossover plate](05-build-plan/joint-02.png)

*Figure 6. The mast touches one face, the standoff the other; two M8 U-bolts wrap each, with nyloc nuts on the opposite face.*

The plate stands upright, its faces parallel to the standoff. The mast lies against the face toward the front eave, the standoff against the face toward the back eave. The mast's U-bolts go round the mast and through the plate to nuts on the standoff side, above and below the pipe; the standoff's U-bolts go round the pipe and through to nuts on the mast side, either side of the mast.

**Check before moving on.** All eight U-bolt legs drop through their holes by hand.

### 3.4 Mast tube and what it carries

![Figure 7. Making sketch of the mast tube](../cad/drawings/EGD-DWG-104.png)

*Figure 7. Mast tube making sketch (EGD-DWG-104).*

**What it is and what it is made from.** The upright that carries the wind sensors at its top, the humidity shield and the solar panel. Aluminium tube 40 x 2 mm, 6061-T6, 2,450 mm long.

**How to make it.**

1. Cut 2,450 mm of tube; square and deburr both ends, inside as well, so nothing can cut the cable.
2. Measuring from the bottom end, drill one 12 mm hole through one wall at 1,220 mm on the side that will face east, and one at 1,250 mm on the side that will face south. Fit a rubber grommet in each.
3. Pull the mast cable through the tube from the top, leaving 1 m out at the top for the wind sensors and enough at the bottom to reach the enclosure. Feed the humidity and panel leads in through their grommets.
4. Push the plastic end cap, with the cable through its grommet, into the bottom end.

**How it fits the parts next to it.**

![Figure 8. Joint 12: mast foot](05-build-plan/joint-12.png)

*Figure 8. The cable leaves through the end cap and runs under the lower standoff to the wall; the earth clamp sits 25 mm up from the foot.*

The mast stands upright 700 mm off the gable wall, on the ridge line, its foot 2.25 m above the ground and its top 4.70 m. The two crossover plates hold it at 2.45 m and 3.90 m. The wind sensors' sleeve slides 40 mm over the top and is locked by two set screws. The humidity shield's clamp goes round the tube with its arm just above the shield, the clamp's centre 1,175 mm up the tube; the panel clamp's centre is 1,310 mm up.

![Figure 9. Joint 3: solar panel mount](05-build-plan/joint-03.png)

*Figure 9. The panel clamp on the mast, the arm out to the hinge and the tilt rail bolted to the panel's frame at 45 degrees.*

**Check before moving on.** The cable slides freely in the tube; the grommets are seated; the end cap is tight.

### 3.5 Pod boxes, drilled (make 2)

![Figure 10. Drilling sketch of the pod box](../cad/drawings/EGD-DWG-105.png)

*Figure 10. Pod box drilling sketch (EGD-DWG-105).*

**What it is and what it is made from.** A bought die-cast aluminium box about 100 x 80 x 70 mm with 4 mm walls and a screwed lid, holding the thermal sensor and the pod node board. Five kinds of hole are drilled in it.

**How to make it.**

1. Hold the box in soft vice jaws. The west wall is one of the two short ends; it will face along the gutter.
2. West wall: one 9.5 mm window in the middle, 35 mm up from the box's underside. Around it, four holes drilled 2.05 mm and tapped M2.5, 10 mm each side and 10 mm above and below the window. Above and below the window, 15 mm from it, two holes drilled 2.5 mm and tapped M3.
3. East wall: one 16.2 mm hole in the middle, 20 mm up, for the M16 cable gland.
4. Floor: two 6.5 mm holes on the long centre line, 30 mm each side of the middle.
5. Lid: four holes drilled 3.3 mm and tapped M4, 35 mm each side of the middle along the box and 28 mm across it.
6. Deburr every hole inside and out and blow out the chips.

**How it fits the parts next to it.**

![Figure 11. Joint 4: thermal sensor and lens hood](05-build-plan/joint-04.png)

*Figure 11. The sensor board sits on the inside of the west wall on four M2.5 screws over 1 mm washers, its can in the window and sealed by an O-ring; the lens hood is on the outside.*

The thermal sensor's 9.2 mm can sits in the window with its face flush with the outside of the wall; a 9.5 mm O-ring round the can, squeezed between the board and the wall, seals it. The node board stands on four 12 mm standoffs on the floor toward the east end, clear of the two bolt heads inside the floor. The pod cable comes in through the M16 gland in the east wall.

**Check before moving on.** The can passes the window without touching it; the board sits flat on its washers.

### 3.6 Lens hoods (make 2)

![Figure 12. Making sketch of the lens hood](../cad/drawings/EGD-DWG-106.png)

*Figure 12. Lens hood making sketch (EGD-DWG-106).*

**What it is and what it is made from.** A short rectangular tube that shades the sensor window from above and the sides without entering its view. Stainless steel sheet 1 mm, 304 class.

**How to make it.**

1. Cut a cross-shaped blank: a 30 x 20 mm centre opening edged by four 19 mm sides, two 30 mm wide and two 20 mm wide, with an 11 mm flange on the outer end of each wide side.
2. Fold the four sides through 90 degrees to make a tube 28 mm wide and 18 mm tall inside, 20 mm deep. Fold the two flanges 90 degrees outward.
3. Drill a 3.4 mm hole in the middle of each flange.

**How it fits the parts next to it.** The flanges lie flat on the west wall, the opening centred on the window with its long side level, held by two M3 stainless screws (Figure 11). From the window, the inside edges are 31 degrees off the axis sideways and 19 degrees up and down, outside the sensor's 27.5 and 17.5 degrees.

**Check before moving on.** Looking in through the hood from 1 m away along the axis, you can see the whole window with no edge of the hood across it.

### 3.7 Pod hoods (make 2)

![Figure 13. Making sketch of the pod hood](../cad/drawings/EGD-DWG-107.png)

*Figure 13. Pod hood making sketch (EGD-DWG-107).*

**What it is and what it is made from.** The roof over the pod that keeps sun and radiant heat off it. Stainless steel sheet 1 mm, 304 class.

**How to make it.**

1. Cut a 170 x 150 mm blank: a 150 x 130 mm top with a 10 mm flange on every edge. Drill a 3 mm relief hole at each corner where the fold lines cross.
2. Fold all four flanges 90 degrees down.
3. Drill four 4.4 mm holes, 35 mm each side and 28 mm in front of and behind a point 15 mm east of the middle of the top, so the hood hangs 40 mm further over the lens end.

**How it fits the parts next to it.** Four 15 mm M4 aluminium spacers screw into the lid's tapped holes; the hood sits on them and four M4 screws hold it. The air gap is 15 mm, and the drip flanges stand 5 mm clear of the lid.

**Check before moving on.** The hood sits level on all four spacers.

### 3.8 Pod plates (make 2: a front and a back)

![Figure 14. Making sketch of the pod plate](../cad/drawings/EGD-DWG-108.png)

*Figure 14. Pod plate making sketch (EGD-DWG-108).*

**What it is and what it is made from.** The plate the pod stands on; it turns on the arm to aim the pod. Aluminium plate 6 mm, 6082 class, 120 x 70 mm.

**How to make it.**

1. Cut two 120 x 70 mm blanks; deburr. Mark the long centre line: it is the pod's axis.
2. One 8.5 mm pivot hole at the centre.
3. Two holes on the long centre line, 30 mm each side of the centre, drilled 5 mm and tapped M6.
4. A curved slot 6.5 mm wide on a 35 mm radius about the centre, from 25 to 49 degrees off the long centre line, on the side away from the house and toward the pod's east end. Chain drill along the arc and file smooth. The front and back plates are mirror images.

**How it fits the parts next to it.**

![Figure 15. Joint 5: pod on its plate and the arm's tab](05-build-plan/joint-05.png)

*Figure 15. The pod stands on two spacers of different height, which tip it 5 degrees nose down; the plate turns on the pivot bolt and the slot bolt locks the aim.*

The pod stands on two aluminium spacers, about 12.5 mm under the lens end and 17.7 mm under the other end, with a domed washer on each. Two M6 bolts go down from inside the pod, through the spacers, into the tapped holes. The plate lies flat on the arm's top tab, on an M8 pivot bolt with a nyloc nut, and an M6 bolt through the slot and the tab locks it.

**Check before moving on.** With the pod bolted on, an angle finder on the pod's lid reads 5 degrees nose down, give or take 1 degree.

### 3.9 Pod arms (make 2)

![Figure 16. Making sketch of the pod arm](../cad/drawings/EGD-DWG-109.png)

*Figure 16. Pod arm making sketch (EGD-DWG-109), drawn laid square.*

**What it is and what it is made from.** The bracket that carries a pod out from the verge cleat and up to its height. Aluminium flat bar 40 x 6 mm, 6060 or 6063-T6.

**How to make it.**

1. Cut 540 mm of bar for each arm.
2. Bend 1: up through 90 degrees, its outside face 236 mm from the start end. Bend cold in a vice round a 12 mm former.
3. Bend 2: forward through 90 degrees, so that the top of the tab is 212 mm above the underside of the run.
4. Trim the tab to 80 mm beyond the rise's outside face.
5. On the run, two 6.5 mm holes on the centre line, 20 and 60 mm from the start end. On the tab, an 8.5 mm pivot hole 25 mm, and a 6.5 mm hole 60 mm, beyond the rise's outside face. Mark the holes after bending.

**How it fits the parts next to it.** The run lies flat on the cleat's level leg, held by two M6 bolts with nyloc nuts; it points out at 47 degrees from the gable line, away from the house, to put the pod over the gutter's centre line 200 mm beyond its end (Figure 18). The pod plate lies on the tab (Figure 15). At 120 km/h the arm sees about 8 MPa, a nineteenth of its strength.

**Check before moving on.** With the run on a flat bench, the tab is level within 1 degree.

### 3.10 Verge cleats (make 2: a front and a back)

![Figure 17. Making sketch of the verge cleat](../cad/drawings/EGD-DWG-110.png)

*Figure 17. Verge cleat making sketch (EGD-DWG-110).*

**What it is and what it is made from.** The angle that fixes each pod arm to the end of the roof overhang. Aluminium equal angle 80 x 80 x 6 mm, 140 mm long.

**How to make it.**

1. Cut two 140 mm lengths; square and deburr.
2. Upright leg: two 9 mm holes 45 mm down from the top face, 40 mm each side of the middle, for 8 mm coach screws.
3. Level leg: two 6.5 mm holes on the arm's line, 37 and 64 mm out from the face on the verge, 7 and 37 mm toward the gutter from the middle. It is easiest to clamp the arm in place and drill through it.

**How it fits the parts next to it.**

![Figure 18. Joint 6: cleat and arm at the front gutter corner](05-build-plan/joint-06.png)

*Figure 18. The cleat screwed to the verge; the arm's run bolted flat on its level leg, clear of the roof, fascia and gutter.*

The upright leg lies flat on the end face of the roof overhang (the verge or barge board), between 30 and 170 mm in from the eave edge, its top 232 mm above the gutter lip, held by two 8 mm x 80 mm coach screws into solid timber. The level leg sticks out east. Nothing touches the fascia or the gutter.

**Check before moving on.** The level leg is level; each coach screw pulls tight into timber, not into the roof covering.

### 3.11 Ground enclosure, drilled

![Figure 19. Drilling sketch of the ground enclosure](../cad/drawings/EGD-DWG-111.png)

*Figure 19. Ground enclosure drilling sketch (EGD-DWG-111).*

**What it is and what it is made from.** A bought steel IP65 wall box, 400 tall, 320 wide and 160 deep, light-coloured, with a gasketed door on the front, a gear plate on four studs inside the back and four wall lugs.

**How to make it.**

1. Take out the gear plate. Mark holes from the box's vertical centre line, left and right as seen facing the door.
2. Bottom: four 20.5 mm holes for M20 glands, 25 mm behind the door face, at 100 and 40 mm left and 40 and 100 mm right of centre: front pod, valves, mast and back pod cables.
3. Top: one 16 mm hole for the siren's lead, 80 mm left of centre and 110 mm out from the back.
4. Door: one 22 mm hole for the key switch, 90 mm right of centre and 120 mm above the middle.
5. Pilot drill 4 mm, open out with a step drill, deburr and touch up the paint on every edge.

**How it fits the parts next to it.**

![Figure 20. Joint 7: inside the enclosure](05-build-plan/joint-07.png)

*Figure 20. The battery stands on the floor against the gear plate, held by the strap; the controller and relay stand on standoffs on the gear plate above it.*

![Figure 21. Joint 8: enclosure bottom, lugs and glands](05-build-plan/joint-08.png)

*Figure 21. Four glands near the door side of the floor; the lugs hold the box 2 mm off the wall.*

The four lugs bolt to the back corners and stand 25 mm above and below the box; each takes an M8 screw into a wall plug. The gear plate goes back on its studs with the controller board (on four 10 mm standoffs) and the relay (on two) fitted to it. The battery stands on the floor against the gear plate, held by the strap 50 mm above the floor. The siren sits on the top on its own gasket; the key switch goes through the door.

**Check before moving on.** No swarf inside; the door closes evenly on its gasket; the battery cannot move when pushed.

#### 3.11.1 Wiring

![Figure 22. Block-level wiring](05-build-plan/wiring.png)

*Figure 22. Block-level wiring with wire sizes. No circuit board is laid out at this stage; bought modules on a protoboard stand in for the controller.*

The controller is a protoboard carrying bought modules, which is enough for this prototype; a laid-out board is TRL 4 work. Wire it like this, with stranded copper and a ferrule on every screw terminal:

1. Panel lead (in the mast cable) to the charge controller's panel input: 1.0 mm².
2. Charge controller to the battery, and battery to the controller board, through the 10 A fuse at the battery terminal: 1.5 mm².
3. Wind, vane and humidity signals (in the mast cable) to the controller: 0.25 mm².
4. Each pod cable to the controller: the RS-485 pair as 0.25 mm² twisted pair, and 12 V and ground at 0.5 mm² through a 5 A fuse for both pods.
5. Valve drivers to the two valve coils through the valve cable: 1.0 mm², with a flyback diode across each coil.
6. Transducer to the controller: 0.25 mm², shielded, 5 V supply.
7. Controller to the relay coil, siren, status light and key switch: 0.5 mm².
8. Relay contacts to the pump's own control input: dry contact only, in a separate cable.

**Check before moving on.** Every wire continues end to end; with the battery fuse out, every rail reads open to ground; every wire is labelled.

### 3.12 Battery strap

![Figure 23. Making sketch of the battery strap](../cad/drawings/EGD-DWG-112.png)

*Figure 23. Battery strap making sketch (EGD-DWG-112).*

**What it is and what it is made from.** The band that holds the battery against the gear plate. Aluminium strip 25 x 1.5 mm.

**How to make it.**

1. Cut about 395 mm of strip.
2. Mark the battery's front width (151 mm) in the middle, its depth (98 mm) each side of that, and a 20 mm foot on each end.
3. Fold 90 degrees at each mark so the strap fits round the front and sides and the feet turn outward.
4. Drill a 4.5 mm hole in the middle of each foot and line the inside with 2 mm closed-cell foam tape.

**How it fits the parts next to it.** The feet lie flat on the gear plate, 50 mm above the box floor, on two M4 screws with nyloc nuts (Figure 20).

**Check before moving on.** The strap holds the battery snug without denting its case.

### 3.13 Valve board

![Figure 24. Making sketch of the valve board](../cad/drawings/EGD-DWG-113.png)

*Figure 24. Valve board making sketch (EGD-DWG-113).*

**What it is and what it is made from.** The plate on the gable wall that carries the manifold, valves and transducer. Aluminium sheet 3 mm, 5052 class, 1,100 x 270 mm.

**How to make it.**

1. Cut the blank, round the corners and deburr.
2. Wall holes: six 7 mm holes, 105 mm above and below the middle, at the middle and 500 mm each side of it.
3. Pipe clip holes: two pairs of 5.5 mm holes, 500 mm each side of the middle, 55 mm above the middle, 24 mm apart up and down.

**How it fits the parts next to it.**

![Figure 25. Joint 9: valve board, manifold and valves](05-build-plan/joint-09.png)

*Figure 25. The manifold sits in two stand-off pipe clips; each valve hangs from its own tee, coil facing out; the transducer stands on the middle tee.*

The board's middle is 465 mm above the ground, directly below the enclosure. The manifold's centre is 45 mm off the board and 520 mm above the ground, in two stand-off pipe clips. Valve A (front zone) hangs from the tee 300 mm toward the front eave of the enclosure's centre line, valve B 300 mm toward the back; water flows down through each. The supply hose connects to the manifold's end toward the back eave.

**Check before moving on.** The board is level and flat on the wall; every threaded joint has sealant.

### 3.14 Spray lines (cut from the roll)

**What it is and what it is made from.** 16 mm UV-stable polyethylene line, cut to length on site: 17.5 m for the front zone and 21.1 m for the back, each with an end plug, two elbows at the eave corner and six tees for the heads.

**How it fits the parts next to it.**

![Figure 26. Joint 10: spray line on a gutter-lip clip](05-build-plan/joint-10.png)

*Figure 26. The clip hooks over the gutter lip and holds the line 20 mm in front of it and 30 mm above it.*

![Figure 27. Joint 11: riser round the eave corner](05-build-plan/joint-11.png)

*Figure 27. Up the gable wall, out under the gutter on a stand-off clip at the fascia, up in front of the gutter and along the lip.*

From its valve each riser bends back to the wall, runs along the base of the gable wall 250 mm above the ground in saddle clips every 600 mm, and turns up the wall 25 mm in from the corner, with a clip every 500 mm. At 2.30 m it turns out under the eave, passes 30 mm under the fascia (one stand-off clip screwed into the fascia's lower edge holds it) and 8 mm in front of the gutter, rises to 30 mm above the lip and turns along the gutter. The eave run sits in 12 gutter-lip clips per eave, one 450 mm each side of every head. The heads push onto tees at 2.2 m spacing, 1.1 m, 3.3 m and 5.5 m each side of the house's middle, pointing up.

**Check before moving on.** The line is supported at every clip and does not touch the gutter anywhere.

### 3.15 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Mast tube, pipe, flanges and U-bolts (line 1).** 40 x 2 mm 6061-T6 tube; DN25 galvanized pipe; two slip-on base flanges for 33.7 mm tube with set screws and four holes on an 80 mm circle; four M8 U-bolts for 40 mm tube and four for 33.7 mm pipe, stainless, with nyloc nuts; eight M10 wall anchors suited to the wall.
- **Pod parts (line 2).** Die-cast aluminium box about 100 x 80 x 70 mm, 4 mm walls; pod node board (small microcontroller and RS-485 transceiver); M16 cable gland; four 15 mm M4 aluminium spacers; two 8 mm x 80 mm coach screws, M6 and M8 stainless bolts.
- **Thermal sensors (line 3).** MLX90640 BAB (55 x 35 degree lens) on a breakout of 25 x 25 mm or less with the can centred and corner holes, with a 9.5 mm O-ring.
- **Wind and humidity sensors (lines 4 and 5).** Weather-station cup anemometer and vane with a crossarm and mast-top sleeve; SHT4x-class probe in a five-plate shield with a mast clamp.
- **Enclosure (line 7).** Steel IP65 wall box about 400 x 320 x 160 mm, light-coloured, with a gear plate on studs and four wall lugs.
- **Controller, battery, panel and relay (lines 6, 8, 9 and 12).** ESP32-class module, MOSFET valve drivers, RS-485 transceiver, 12 to 3.3 V buck and fuses on a protoboard; 12.8 V 10 Ah LiFePO4 with built-in BMS and low-temperature charge cut-off; 10 W 12 V panel with a pole-mount tilt bracket and a PWM charge controller with a LiFePO4 profile; isolated 10 A dry-contact relay module.
- **Valves and transducer (lines 10 and 11).** Two 12 V DC normally closed DN20 solenoid valves of zero-minimum-pressure type, inlet and outlet in line; a 0 to 10 bar, 0.5 to 4.5 V transducer.
- **Cables (line 13).** 10 m of shielded 4-pair outdoor cable for the mast, 6 m and 10 m for the pods, 2 m twin for the valves, 1 m silicone heat sleeve at each pod.
- **Spray line (line 14).** 50 m of 16 mm UV-stable polyethylene, 12 micro-sprinklers of about 40 L/h at 2 bar, 24 gutter-lip clips, elbows, tees and end plugs.
- **Siren (line 15).** 12 V piezo siren about 100 dB with status light, keyed arm switch.
- **Fittings (line 16).** Manifold pipe with three tees and a hose connector, two stand-off pipe clips, saddle clips, two stand-off clips for the fascia, four M20 glands, wall plugs and screws, cable ties, fuse holders and fuses.
- **Earthing (line 17).** 1.2 m copper-clad earth rod with clamp, 6 m of 16 mm² green-yellow conductor, mast bonding clamp.

## 4. Putting it together

In each picture the parts already fitted are grey and the parts being fitted are in colour, with an arrow showing the way they go in. Steps 1 to 10 are bench work; steps 11 to 17 are on the house.

### Step 1: flange onto each wall plate

![Step 1](05-build-plan/step-01.png)

Four M8 countersunk screws from the back of the plate, nyloc nuts on the flange, tight. Make two.

### Step 2: end cap and wind sensors on the mast

![Step 2](05-build-plan/step-02.png)

With the mast cable already pulled through (section 3.4), push the end cap into the foot. Slide the wind sensors' sleeve 40 mm over the top and tighten its two set screws; connect the wind sensors to the cable.

### Step 3: humidity shield and solar panel onto the mast

![Step 3](05-build-plan/step-03.png)

Humidity shield clamp centred 1,175 mm up the tube, arm pointing east; panel clamp centred 1,310 mm up, arm pointing south. Set the panel to 45 degrees with an angle finder and tighten. Feed both leads into their grommets.

### Step 4: sensor, node board and lens hood into the pod

![Step 4](05-build-plan/step-04.png)

Sensor board inside the west wall on four M2.5 screws over 1 mm nylon washers, O-ring round the can, can in the window. Node board on its four standoffs. Lens hood outside on two M3 screws. Connect the sensor to the node board.

### Step 5: cable gland, lid and hood on the pod

![Step 5](05-build-plan/step-05.png)

Pod cable in through the M16 gland and onto the node board's terminals; tighten the gland. Lid on, screws tightened evenly. Spacers into the lid, hood on them with four M4 screws.

### Step 6: pod plate under the pod

![Step 6](05-build-plan/step-06.png)

Two M6 bolts from inside the pod, through the floor (sealing washers), through the short spacer under the lens end and the tall one under the other end, into the plate's tapped holes. **Hold point:** the pod reads 5 degrees nose down on the lid.

### Step 7: arm onto the cleat

![Step 7](05-build-plan/step-07.png)

The run lies flat on the cleat's level leg; two M6 bolts with nyloc nuts. Make a front pair and a back pair; they are mirror images.

### Step 8: lugs, glands, siren and key switch on the enclosure

![Step 8](05-build-plan/step-08.png)

Lugs on the four back corners as the box maker describes. Glands from below, nuts inside. Siren on the top on its gasket. Key switch through the door from the front, nut inside.

### Step 9: gear plate, controller, relay and battery into the enclosure

![Step 9](05-build-plan/step-09.png)

Gear plate on its four studs with the controller and relay already on it. Battery on the floor against the plate, strap round it on two M4 screws. Wire as section 3.11.1. **Hold point:** battery fuse out (section 6, S3).

### Step 10: clips, manifold, valves and transducer on the valve board

![Step 10](05-build-plan/step-10.png)

Two stand-off pipe clips on the board. Manifold into the clips with its three tees pointing down, down and up. Valves onto the down tees, flow arrows pointing down, coils facing out. Transducer onto the up tee. Thread sealant on every threaded joint.

### Step 11: wall plates and standoffs on the gable wall

![Step 11](05-build-plan/step-11.png)

Mark the mast's line (the ridge line) on the gable wall. Plates centred 43 mm to the back-eave side of it, 2.45 m and 3.90 m up, square and level; four M10 anchors each. Standoffs into the flanges to their stops, set screws tight, outer ends level. **Hold point:** safety stops S1 and S2.

### Step 12: mast onto the standoffs

![Step 12](05-build-plan/step-12.png)

With a helper holding the mast upright, its foot 2.25 m above the ground, hang a crossover plate at each standoff and fit the four U-bolts at each, nuts finger tight. Plumb the mast with a level in two directions, then tighten all nuts evenly.

### Step 13: earth the mast

![Step 13](05-build-plan/step-13.png)

Drive the rod into the ground 400 mm out from the wall, below the mast, leaving 120 mm above ground. Bonding clamp on the mast foot, 25 mm up. Conductor from the clamp to the wall, down it 40 mm off the wall on stand-off clips, and to the rod's clamp. **Hold point:** safety stop S4.

### Step 14: cleat, arm and pod at each gutter corner

![Step 14](05-build-plan/step-14.png)

Hold the cleat with its arm on the verge, upright leg flat, level leg level, 30 to 170 mm in from the eave edge. Drill 5 mm pilot holes and drive the two coach screws. Put the pod's plate on the tab with the pivot bolt, swing the pod until it points along the gutter and 10 degrees toward the house (sight along the lens hood's side to a mark on the gutter 8 m away), and lock the slot bolt. Repeat at the other gutter.

### Step 15: enclosure and valve board on the gable wall

![Step 15](05-build-plan/step-15.png)

Enclosure centred 1.15 m above the ground, 1.8 m toward the front eave from the mast's line, level; four M8 screws into wall plugs through the lugs. Valve board below it, middle 465 mm above the ground; six screws into wall plugs. Connect the supply hose. **Hold point:** safety stop S2 before every wall hole.

### Step 16: spray lines

![Step 16](05-build-plan/step-16.png)

For each zone: from the valve, along the wall base on saddle clips, up the corner, out under the gutter through the fascia clip, up in front of the gutter, and along the lip in the lip clips to the far end. Tees and heads at their marks; end plug at the far end. Flush the line before fitting the end plug.

### Step 17: cables into the enclosure

![Step 17](05-build-plan/step-17.png)

Mast cable from the mast foot, under the lower standoff, down the wall; each pod cable along its arm, round the verge, under the soffit and down the gable corner; valve cable from the enclosure to the valves. Each through its own gland in the enclosure floor; saddle clips every 500 mm; the silicone heat sleeve over each pod cable for its first metre. Connect as section 3.11.1. **Hold point:** safety stops S3, S5 and S6.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of EGD-REQ-001.

*Table 2. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Sensor view clear | R3 | Read a frame from each sensor with the pod on its arm; look at the image edges | No part of the lens hood, hood or arm in any pixel |
| Pod aim | R3 | Angle finder on the lid; sight along the hood's side | 5 degrees nose down and 10 degrees toward the house, each within 1 degree |
| Gutter in view | R3 | Hold a hand warmer in the open gutter at 1.5, 6 and 13 m from its east end | Seen at all three, in the expected pixels |
| Arming | R4 | Feed simulated wind pulses and humidity readings | Arms at 30 km/h sustained or 50 km/h gusts with humidity at or below 20 % for 10 min; key switch arms and disarms |
| Valves fail closed | R9 | Power each valve, then cut power | Opens when powered; closes within 1 s when power is lost |
| Joints hold pressure | R7 | Supply water at 2.5 bar with the heads plugged | No leak at any joint or valve |
| Flow per zone | R7 | Run each zone for 5 min into buckets | 4 L/min, give or take 10 % |
| Water to the farthest head | R5 | Time from opening the valve to water at the far head, at 4 L/min | 49 s or less, so that with 11 s for detection and the valve the total stays within 60 s (36 s and 43 s expected; 47 s and 54 s with the allowance) |
| Supply pressure | R7 | Transducer reading with one zone running | About 2.3 bar at the manifold |
| Fail to wet on sensor loss | R9 | Arm, then unplug a pod cable at the enclosure | Spraying starts and the alarm sounds |
| Alarms | R12 | Low battery (bench supply), no water (supply shut), faulty valve (coil unplugged) | Each raises the siren and status light |
| Battery and charging | R8 | Charge controller on its LiFePO4 profile; check the BMS cold cut-off with the pack below 0 °C | Charges to the pack maker's voltage; no charge below 0 °C |
| Mast and pods steady | R10 | Push the mast top and each pod by hand | Nothing moves at any joint |
| Earth continuity | Safety | Resistance from the mast to the rod | As local practice requires (well under 1 ohm along the conductor) |
| Install time | R11 | Record the time for two people from step 11 to step 17 | 6 h or less |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before any work at height.** Ladder on firm level ground, footed by a second person, tied or stood off at the roof edge; dry, calm weather with no thunder; nobody on the roof covering. Tools tied on.
- **S2. Before drilling into the wall or the verge.** The wall and verge are checked with a detector for cables, pipes and gas; the drill is on the right setting for the wall material; dust mask and eye protection on.
- **S3. Before the battery fuse goes in.** Every wire checked against Figure 22; the charge controller set to its LiFePO4 profile; polarity checked with a meter, not by wire colour; the battery's case undamaged; the enclosure closed apart from the door.
- **S4. Before the mast is left standing.** The earth rod, conductor and clamp are fitted and tight; every U-bolt nut is tight; no work on the mast when thunder is near.
- **S5. Before water is turned on.** Every clip, tee and plug is fitted; the supply is the tank and pump, not the hydrant main; the pressure is 2.5 bar or less.
- **S6. Before the pump-start contact is connected.** The pump keeps its own certified controls and ground-fault protection; the relay connects only to the pump's control input as its maker describes; any mains work is done by a qualified electrician; nothing in EmberGuard carries mains.
- **S7. Before the kit is left armed.** Every check of section 5 passes; the household knows that EmberGuard does not replace evacuation, home hardening or clearing the gutters, and that nobody stays behind for it.

## 7. Tools, skills and workspace

**Tools.** Hacksaw with a 24 teeth per inch blade, pipe cutter; bench vice with soft jaws and a 12 mm round former for bending bar; bench drill or a drill in a stand; drills 2 to 12 mm, step drill to 22 mm; taps M2.5, M3, M4 and M6 with their tap drills; countersink; files and deburring tool; scriber, square, rule, calipers and protractor; hand sheet folder (or hardwood blocks in the vice) and aviation snips for 1 mm stainless; hammer drill with masonry bits; spanners and sockets 10 and 13 mm; set of hex keys; spirit level and digital angle finder; extension ladder with a stand-off; polyethylene line cutter and a punch for the heads; soldering iron, ferrule crimper and wire strippers; multimeter; bench power supply with a current limit (0 to 15 V, 0 to 3 A); buckets, stopwatch and a pressure gauge.

**Skills.** Basic metalwork (marking out, sawing, drilling, tapping, bending bar, folding thin sheet), through-hole soldering and crimping, safe ladder work, and fixing to masonry or timber. All circuits are extra-low voltage, 12.8 V nominal. Any work on the pump's mains supply is outside this plan and is for a qualified electrician.

**Workspace.** A bench about 1.5 x 0.7 m with a metalwork corner kept apart from the electronics; level, firm ground at the gable end for the ladder; a second person for every step on the house.

**Personal protective equipment.** Safety glasses for cutting, drilling and soldering; cut-resistant gloves for sheet and bar; hearing protection for sawing and hammer drilling; dust mask for drilling masonry; no gloves near a turning drill.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/EGD-DWG-101` to `EGD-DWG-113`.
- General arrangement: `cad/drawings/EGD-DWG-001.pdf`, Rev P4.
- Calculations: `docs/04-calcs/01-sizing.md` (EGD-CAL-001 v0.4) and `docs/04-calcs/sizing.py`; line lengths and fill [C2], [C3], supply pressure [C4], mast and anchors [E3], [E4], pod arm [E5].
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (EGD-DDR-003), with EGD-DDR-001 and EGD-DDR-002; open items in `docs/06-design-decisions.md` (EGD-DEC-001).
- Requirements: `docs/03-requirements.md` (EGD-REQ-001 v0.6).
