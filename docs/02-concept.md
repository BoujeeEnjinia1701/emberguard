---
doc_id: EGD-PRC-001
title: EmberGuard design precis
project: EmberGuard
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, components, first-order numbers, safety, media)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3. Record Amish's decisions (EGD-DDR-001); numbers checked against EGD-CAL-001; gutter blind spot reported; parametric model, drawing EGD-DWG-001 and priced BOM
---

# EmberGuard design precis

EmberGuard is a slim mast that stands off one gable end of a house with a sensor head just above the ridge. Two small thermal array cameras in the head watch both roof planes, while a cup anemometer, a wind vane and a humidity sensor decide when fire weather has arrived. When the system is armed and sees a hot spot or a burst of hot specks on the roof edge, it opens two 12 V valves and feeds a line of micro-sprinklers clipped to each gutter lip, wetting the gutter, fascia and first metre of roof. The TRL 3 calculations (EGD-CAL-001) confirm a steady 4 L/min draw, about 965 L per 4 h ember event, water at the farthest head 55 s after detection and a strong mast. They also show five misses. The head, only 228 mm above the ridge, cannot see into either gutter at all, because the roof edge hides them, and it sees the roof surface at 1 to 3 degrees, so flat hot spots are faint. A 600 °C ember reaches the 5 K trigger only within 5.5 m. Wind drift leaves the leeward eave far short of 5 mm/h. The priced kit costs $571 against the $425 budget Amish set on 2026-09-25. The kit battery covers 72 h armed and 4 h spraying with a thin margin. The general arrangement is drawing EGD-DWG-001 (`cad/drawings/EGD-DWG-001.pdf`), generated from `cad/src/model.py`.

![Hero render](../media/hero.png)

*Figure 1. EmberGuard on the 12 x 8 m reference house, with a 1.75 m person for scale. Mast and sensor head at the east gable, ground unit and valves on the gable wall, spray lines on both gutters (front spray envelopes shown in blue). Grey house, tank and pump are context. Rendered from the parametric model.*

## How it works

1. **Watch.** Outside fire weather the controller samples wind, wind direction, air temperature and humidity once a minute and sleeps between samples.
2. **Arm.** It arms when sustained wind reaches 30 km/h (or gusts 50 km/h) with relative humidity at or below 20 % for 10 min, or when the owner arms it by key switch or phone. These defaults resemble common Red Flag conditions, which vary by region, and are adjustable. Once armed, it stays armed for at least 6 h and runs both thermal sensors at 4 frames per second.
3. **Detect.** Each sensor's frames are compared with a slowly updated background. Two patterns count as embers:
   - a **persistent hot spot**: a cluster of 1 to 4 pixels at least 5 K above its background for 5 s or more, which is what a landed ember or smouldering debris looks like;
   - an **ember shower**: 10 or more short hot flickers per minute across the view, from embers in flight or bouncing on the roof.
   Sun-heated roofing warms slowly and over large areas, so it is rejected by the small-cluster and rate-of-rise tests.
4. **Wet.** On a detection, the valve on the side of the detection opens first so its line fills within 44 to 55 s at 4 L/min, then the second zone fills, and the zones alternate every 30 s, so the supply sees a steady 4 L/min (EGD-CAL-001, C3). Spraying continues until 30 min after the last detection. A pressure transducer confirms that water is flowing; a dry-contact relay can start a pump that runs on its own supply.
5. **Fail safe.** If sensor data stops while armed (for example the head is damaged by heat), the controller assumes the worst and sprays in the same cycle until the battery or water runs out. Loss of controller power closes the normally closed valves, which saves the tank.
6. **Tell.** A siren and status light at the ground unit, and a phone alert when a network is available, report arming, spraying and faults. An event log records detections, wind and valve actions for later study.

![Water flow](../media/flow.png)

*Figure 2. Water per 4 h ember event. All values are estimates: 12 heads at 40 L/h, two zones alternating, wind drift from the screening model in EGD-CAL-001 at an 8.3 m/s cross-wind (97 % on target on the windward eave, 10 % on the leeward), and a guess at runoff from the gutter and roof edge.*

## Main components

Table 1. Main components. Numbers match `bom/bom.csv` and Figure 4. Items 16 and 17 are not modelled.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Mast and standoff brackets | 40 x 2 mm 6061-T6 aluminium tube, 2.45 m, two 700 mm DN25 galvanized pipe standoffs to the gable wall | Head 4.76 m above ground and 0.23 m above the ridge |
| 2 | Sensor head with heat and sun hood | Cast aluminium box about 160 x 240 x 120 mm with a stainless hood; holds a small head node that digitizes the sensors | Lens apertures face down and away from the sky |
| 3 | Thermal array sensors (2) | MLX90640 BAB, 32 x 24 pixels, 55 x 35 degree field of view (decided, D2) | Each aimed 45 degrees off the house axis toward one roof edge, 15 degrees down |
| 4 | Anemometer and wind vane | Weather-station cup anemometer (pulse) and vane on a 460 mm crossarm | Above the head, clear of the ridge |
| 5 | Temperature and humidity sensor | Digital sensor in a five-plate radiation shield | On the mast, clear of spray |
| 6 | Controller boards | Ground controller (ESP32 class) with valve drivers, and a head node linked over RS-485 | Firmware beyond a labelled sketch is TRL 4 work |
| 7 | Ground enclosure | Steel IP65 box about 160 x 320 x 400 mm on the gable wall at 1 m, light-coloured | Steel for heat and ember resistance; light finish and shade for battery temperature |
| 8 | Battery | 12.8 V 6 Ah LiFePO4 with built-in BMS | About 77 Wh nominal, 69 Wh usable |
| 9 | Solar panel | 10 W panel on the mast with a LiFePO4 charge controller | Keeps the battery full between events; no credit taken during smoke |
| 10 | Zone valves A and B | Two 12 V DC normally closed solenoid valves on a small manifold (decided, D9) | Front and back eave; closed on power loss; zero-minimum-pressure type |
| 11 | Pressure transducer | 0 to 10 bar, 0.5 to 4.5 V | Confirms water flow; warns of a dry supply |
| 12 | Pump-start relay | Isolated dry contact | Signals the pump's own certified controls; no mains inside EmberGuard |
| 13 | Mast cable | Shielded outdoor cable, heat sleeve on the mast | Power and RS-485 to the head |
| 14 | Eave spray lines and heads | 16 mm UV-stable polyethylene line clipped to each gutter lip, six micro-sprinklers per eave, risers down the gable wall; 17.7 m and 21.3 m per zone | Metal eave runs decided if the budget allows (D4); it does not, so they are a $110 priced option |
| 15 | Siren, status light and key switch | 12 V siren, LED beacon, keyed arm switch | Key switch also disarms |
| 16 | Hardware and fittings | Clamps, fittings, glands, fuses | Not modelled |
| 17 | Mast earthing kit | Earth rod, clamp, conductor and mast bond | Added at TRL 3 for lightning protection; not modelled |

![Cutaway](../media/cutaway.png)

*Figure 3. Section through the front eave at the east spray head, looking west: wall, roof overhang, fascia, gutter, spray line and head (14) on the gutter lip, and the indicative spray envelope over the gutter and roof edge.*

![Exploded view](../media/exploded.png)

*Figure 4. Exploded view with BOM numbers. The ground unit and a 1.4 m sample of spray line are drawn beside the mast top, not in their installed positions.*

## Numbers checked at TRL 3

All values come from EGD-CAL-001 (`docs/04-calcs/sizing.py`); the tags in brackets are its output lines. They are paper estimates.

Table 2. Key numbers.

| Quantity | Value | Basis | Requirement |
| --- | --- | --- | --- |
| Pixel footprint | 0.24 x 0.20 m at 8 m, 0.42 x 0.36 m at 14 m | 1.72 x 1.46 degree pixels [A1] | |
| Head above the roof | 228 mm above the ridge surface | Model [A2] | |
| Roof edge in view | 1.25 m to 13.15 m from the mast, each side | Line of sight on the model [A3] | |
| Gutter interiors in view | None | Roof slab and fascia block every line of sight [A4] | R3 **not met** |
| Grazing angle on the roof | 0.9 to 3.2 degrees | [A6] | |
| 100 cm² spot at 300 °C | Flat: 2.8 K at 8.2 m. Debris face 100 x 50 mm: 42.7 K, seen to 26 m | 5 K trigger [B9] to [B11] | R1 **not met** (gutters hidden) |
| 10 mm ember at 8 m | 600 °C: 2.4 K; 800 °C: 3.6 K (centred in a pixel) | [B4], [B5] | R2 **not met**; 5 K reached within 5.5 m |
| Flow and application | 4 L/min per zone; 15.4 mm/h while running, 7.7 mm/h at 50 % duty | [C1] | |
| Line fill | Water at the farthest head 47 s (A) and 55 s (B) after detection | Detection-side zone first [C3] | R5 met |
| Supply pressure | About 2.3 bar at the manifold | Friction and 2.1 m lift [C4] | |
| Water per event | 965 L (255 US gal) | 4 h at 4 L/min plus line fill [C5] | R7 met, 3.5 % margin |
| Net wetting at 30 km/h | Windward eave 7.4 mm/h; leeward eave 0.8 mm/h (2.6 mm/h at half the wind) | Droplet screening model [C7], [C8] | R6 **not met** |
| Energy | 48.2 Wh for 72 h armed plus 12.7 Wh for 4 h spraying = 61.0 Wh | 0.67 W armed, 3.15 W spraying [D2] to [D4] | R8 at risk |
| Battery | 69.1 Wh usable at 25 °C, 62.2 Wh at 0 °C, 55.3 Wh at end of life | 12.8 V 6 Ah LiFePO4 [D4] | |
| Pump on its own battery (studied) | About 57 W, 229 Wh per event; a 25 Ah LiFePO4 pack or one SwapCell pack (1.6 events) | [D7] to [D9] | Out of kit scope (D6) |
| Mast at 120 km/h | 205 N; 58 N·m at the upper standoff; 27 MPa (factor 8.9) | [E2], [E3] | R10 wind met |
| Standoffs | 203 N reaction; 66 MPa in DN25 pipe (factor 3.5); about 710 N per wall anchor | [E4] | |
| Enclosure in sun at 60 °C | About 71 °C (mid-grey), 65 °C (light) | [F1], [F2] | R10 at risk |
| Kit parts cost | $571 against $425 | `bom/bom.csv` [G1] | R13 **not met** |

## Key design choices

Amish decided the TRL 2 review items on 2026-09-25 by accepting each recommendation (EGD-DDR-001). The choices below are therefore decided, except where marked.

- **Thermal arrays, not simple flame sensors (decided, D2).** Near-infrared flame sensors respond to flames and sunlight and cannot say where on the roof a hot spot is. A 32 x 24 thermal array locates hot spots, measures their size and ignores sun-warmed roofing.
- **Watch where embers land, not the sky.** Landed embers and smouldering debris persist for seconds to minutes and are what actually ignites a house. At TRL 3 this holds for the roof edge only; the gutters are out of sight (EGD-CAL-001, A4). How to watch them is open (EGD-DDR-001, O3).
- **Arm on weather, trigger on embers (decided, D7).** Adjustable defaults of 30 km/h sustained or 50 km/h gusts with humidity at or below 20 % for 10 min, plus manual and remote arming, reviewed with a local fire agency. The 5 K trigger threshold is still proposed; a 2 K threshold is under review (O5).
- **Gable-end mast above the ridge (decided, D3).** One mast sees both roof planes. Its low height above the ridge is the cause of the gutter blind spot.
- **Two alternating zones.** Halves the peak flow, so a small pump can keep up, and suits a 1,000 L tank (decided, D5). Running only the leeward zone is under review for R6 (O4).
- **Low-voltage kit, pump by dry contact (decided, D6).** No mains wiring on the house; the pump keeps its own certified controls and its own power, provided by the homeowner.
- **Fail to wet on sensor loss (decided, D8), fail closed on power loss (decided, D9).** Losing the head during the fire is likely; losing the controller should not drain the tank.
- **Polyethylene eave runs (D4).** Metal eave runs were chosen if the budget allowed; it does not, so they are a priced option.

## Safety

> **Safety:** EmberGuard is not a substitute for evacuation orders, home hardening or professional fire protection. Leave when told to leave. Never stay behind to operate, watch or repair the system during a fire.

> **Safety:** Installing the mast and spray lines means working at height near a roof edge. Use a stable ladder, a second person and fall protection where required; do not work on a wet or mossy roof.

> **Safety:** Water, pumps and electricity. The kit is 12 V DC only. Any mains-powered pump must keep its own certified controls and ground-fault protection; the EmberGuard relay only signals it through an isolated dry contact. Do not wire EmberGuard into mains circuits.

> **Safety:** The LiFePO4 battery is safer than other lithium chemistries but can still overheat if shorted or damaged. Use a pack with a built-in BMS and low-temperature charge cut-off, fuse the battery output, and keep the battery inside the steel enclosure. In full sun at 60 °C ambient a dark enclosure reaches about 71 °C, above the battery's rating; use a light finish and shade it.

> **Safety:** A tall metal mast on the gable is exposed to lightning. Bond it to a proper earth electrode (BOM item 17) and follow local lightning-protection practice. The wall anchors carry about 710 N each at 120 km/h; check them for each wall.

> **Safety:** Automatic sprinklers on mains water can reduce pressure for firefighters. Prefer a dedicated tank; if using mains, keep the flow at or below 4 L/min and follow local fire-agency guidance.

> **Safety:** False reassurance is a hazard in itself. The system cannot see into the gutters at all, and it can miss embers outside its view (vents, decks, the far gable), and it can fail in fire conditions. Keep gutters clean and harden the house as if EmberGuard were not there.

## Open questions

- [ ] How should the gutters be watched: corner sensor pods looking along each gutter, a taller mast, or a narrower requirement (EGD-DDR-001, O3)?
- [ ] Does real wind drift, including the recirculation behind the ridge, leave enough water on the leeward eave (R6)? Would running only the leeward zone meet it (O4)?
- [ ] Can a 2 K persistent-spot threshold reject sun glints, hot vents, chimneys, birds and vehicles (O5)? This needs recorded thermal video, at TRL 4 or later.
- [ ] How long do ember showers last at a single house, and is a 4 h spraying design case reasonable?
- [ ] How hot does the sensor head get under radiant heat before the front arrives, and for how long does it keep working?
- [ ] How can the kit reach $425, or should the budget move again (O2)?
- [ ] Should a second mast or a third sensor cover vents, decks and the far gable?
- [ ] Should EmberGuard log and share anonymised ember arrival data with WUI researchers?
