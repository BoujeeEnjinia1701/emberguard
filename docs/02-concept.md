---
doc_id: EGD-PRC-001
title: EmberGuard design precis
project: EmberGuard
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, components, first-order numbers, safety, media)
---

# EmberGuard design precis

EmberGuard is a slim mast that stands off one gable end of a house with a sensor head just above the ridge. Two small thermal array cameras in the head watch both roof planes and both gutters, while a cup anemometer, a wind vane and a humidity sensor decide when fire weather has arrived. When the system is armed and sees a hot spot or a burst of hot specks on the roof edge, it opens two 12 V valves in turn and feeds a line of micro-sprinklers clipped to each gutter lip, wetting the gutter, fascia and first metre of roof. First-order numbers suggest it can find a 100 cm² smouldering spot anywhere on a 13 m gutter, draws a steady 4 L/min, uses about 960 L in a 4 h ember event and runs for three days armed on a 77 Wh battery. Three things do not yet work on paper: net wetting in wind falls short of the 5 mm/h target, a single cooler ember beyond about 5 m falls below the trigger threshold, and the kit costs about $420 against a $300 budget.

![Hero render](../media/hero.png)

*Figure 1. EmberGuard on the 12 x 8 m reference house, with a 1.75 m person for scale. Mast and sensor head at the east gable, ground unit and valves on the gable wall, spray lines on both gutters (front spray envelopes shown in blue). Grey house, tank and pump are context. Massing model.*

## How it works

1. **Watch.** Outside fire weather the controller samples wind, wind direction, air temperature and humidity once a minute and sleeps between samples.
2. **Arm.** It arms when sustained wind reaches 30 km/h (or gusts 50 km/h) with relative humidity at or below 20 % for 10 min, or when the owner arms it by key switch or phone. These defaults resemble common Red Flag conditions, which vary by region, and are adjustable. Once armed, it stays armed for at least 6 h and runs both thermal sensors at 4 frames per second.
3. **Detect.** Each sensor's frames are compared with a slowly updated background. Two patterns count as embers:
   - a **persistent hot spot**: a cluster of 1 to 4 pixels at least 5 K above its background for 5 s or more, which is what a landed ember or smouldering debris looks like;
   - an **ember shower**: 10 or more short hot flickers per minute across the view, from embers in flight or bouncing on the roof.
   Sun-heated roofing warms slowly and over large areas, so it is rejected by the small-cluster and rate-of-rise tests.
4. **Wet.** On a detection, both valves open together for about 45 s to fill the lines, then alternate every 30 s, so the supply sees a steady 4 L/min. Spraying continues until 30 min after the last detection. A pressure transducer confirms that water is flowing; a dry-contact relay can start a pump that runs on its own supply.
5. **Fail safe.** If sensor data stops while armed (for example the head is damaged by heat), the controller assumes the worst and sprays in the same cycle until the battery or water runs out. Loss of controller power closes the normally closed valves, which saves the tank.
6. **Tell.** A siren and status light at the ground unit, and a phone alert when a network is available, report arming, spraying and faults. An event log records detections, wind and valve actions for later study.

![Water flow](../media/flow.png)

*Figure 2. Water per 4 h ember event. All values are estimates: 12 heads at 40 L/h, two zones alternating, 50 % wind drift at the design wind, and a guess at runoff from the gutter and roof edge.*

## Main components

Table 1. Main components. Numbers match `bom/bom.csv` and Figure 4.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Mast and standoff brackets | 40 x 2 mm aluminium tube, 2.45 m, two 700 mm galvanized steel standoffs to the gable wall | Head about 4.76 m above ground and about 0.25 m above the ridge |
| 2 | Sensor head with heat and sun hood | Cast aluminium box about 160 x 240 x 120 mm with a stainless hood; holds a small head node that digitizes the sensors | Lens apertures face down and away from the sky |
| 3 | Thermal array sensors (2) | MLX90640, 32 x 24 pixels, 55 x 35 degree field of view | Each aimed 45 degrees off the house axis toward one gutter, 15 degrees down |
| 4 | Anemometer and wind vane | Weather-station cup anemometer (pulse) and vane on a 460 mm crossarm | Above the head, clear of the ridge |
| 5 | Temperature and humidity sensor | Digital sensor in a five-plate radiation shield | On the mast, clear of spray |
| 6 | Controller boards | Ground controller (ESP32 class) with valve drivers, and a head node linked over RS-485 | Firmware beyond a labelled sketch is TRL 4 work |
| 7 | Ground enclosure | Steel IP65 box about 160 x 320 x 400 mm on the gable wall at 1 m | Steel for heat and ember resistance |
| 8 | Battery | 12.8 V 6 Ah LiFePO4 with built-in BMS | About 77 Wh nominal, 69 Wh usable |
| 9 | Solar panel | 10 W panel on the mast with a LiFePO4 charge controller | Keeps the battery full between events; no credit taken during smoke |
| 10 | Zone valves A and B | Two 12 V DC normally closed solenoid valves on a small manifold | Front and back eave; closed on power loss |
| 11 | Pressure transducer | 0 to 10 bar, 0.5 to 4.5 V | Confirms water flow; warns of a dry supply |
| 12 | Pump-start relay | Isolated dry contact | Signals the pump's own certified controls; no mains inside EmberGuard |
| 13 | Mast cable | Shielded outdoor cable, heat sleeve on the mast | Power and RS-485 to the head |
| 14 | Eave spray lines and heads | 16 mm line clipped to each gutter lip, six micro-sprinklers per eave, risers down the gable wall | Line material proposed, awaiting Amish (see decision 4) |
| 15 | Siren, status light and key switch | 12 V siren, LED beacon, keyed arm switch | Key switch also disarms |
| 16 | Hardware and fittings | Clamps, fittings, glands, fuses | Not modelled |

![Cutaway](../media/cutaway.png)

*Figure 3. Section through the front eave at the east spray head, looking west: wall, roof overhang, fascia, gutter, spray line and head (14) on the gutter lip, and the indicative spray envelope over the gutter and roof edge.*

![Exploded view](../media/exploded.png)

*Figure 4. Exploded view with BOM numbers. The ground unit and a 1.4 m sample of spray line are drawn beside the mast top, not in their installed positions.*

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3. Assumptions are stated with each number and in EGD-REQ-001.

Table 2. First-order numbers.

| Quantity | Estimate | Basis |
| --- | --- | --- |
| Sensor pixel size | about 1.7 x 1.5 degrees; 0.42 x 0.36 m at 14 m, 0.24 x 0.20 m at 8 m | 55 x 35 degrees over 32 x 24 pixels |
| Sensor noise | about 0.1 K at 1 Hz, higher at 4 Hz | Melexis MLX90640 datasheet figure |
| Signal from a 100 cm² smouldering spot at 300 to 400 °C, at 14 m | tens of kelvin of apparent pixel rise | Pixel fill about 6.6 %; 8 to 14 µm radiance about 10 to 16 times that of a 300 K background, emissivity 0.9 |
| Signal from a 10 mm ember | 800 °C: about 5 K at 8 m, about 1.7 K at 14 m. 600 °C: about 3 K at 8 m, about 8 K at 5 m | Pixel fill 0.2 % at 8 m, 0.07 % at 14 m, 0.5 % at 5 m; band radiance about 42 times (800 °C) or 29 times (600 °C) background, emissivity 0.9; 1.6 % radiance change per kelvin near 300 K |
| Gutter coverage | each gutter from about 1.3 m to 13 m from the gable end | Aim 45 degrees off axis, 15 degrees down, mast at the ridge line |
| Spray flow | 240 L/h (4 L/min) per zone; steady 4 L/min with zones alternating | 6 heads x 40 L/h per zone |
| Application rate | 15.4 mm/h while a zone runs; 7.7 mm/h gross average; about 3.8 mm/h net | 1.2 x 13 m strip per zone; 50 % duty; 50 % wind drift assumed |
| Water per event | about 960 L (254 US gal) for 4 h of spraying | 4 L/min x 240 min |
| Line fill time | about 45 s; water at the farthest head about 55 s after detection | About 21 m of 13 mm bore line (about 2.9 L) at 4 L/min, plus 10 s detection |
| Energy, 72 h armed | about 43 Wh | 0.6 W average at 12 V for head node, two sensors at 4 Hz, controller and radio |
| Energy, 4 h spraying | about 20 Wh | One valve open at a time, about 5 W holding |
| Battery | about 64 Wh needed against about 69 Wh usable | 12.8 V 6 Ah LiFePO4 at 90 % depth; no solar credit. Thin margin; holding-current reduction on the valves would save about 12 Wh |
| Mast wind load at 120 km/h | about 200 N total; about 55 N·m at the upper bracket; about 25 MPa bending stress | 667 Pa dynamic pressure; drag coefficients 1.1 to 1.3; 40 x 2 mm tube, section modulus about 2,170 mm³ |
| Kit parts cost | about $420 | `bom/bom.csv`, indicative prices |

## Key design choices

All are proposed, awaiting Amish. Alternatives and the recommendation for each are in `docs/REVIEW.md`.

- **Thermal arrays, not simple flame sensors.** Near-infrared flame sensors respond to flames and sunlight and cannot say where on the roof a hot spot is. A 32 x 24 thermal array locates hot spots, measures their size and ignores sun-warmed roofing. Cost is about $40 each against a few dollars for a flame sensor.
- **Watch where embers land, not the sky.** Flying embers are small, fast and hard to see at a few pixels per second. Landed embers and smouldering gutter debris persist for seconds to minutes and are what actually ignites a house.
- **Arm on weather, trigger on embers.** Weather alone would spray for days; ember detection alone would risk false starts on a hot still afternoon. Requiring both keeps water use low and false starts rare.
- **Gable-end mast above the ridge.** One mast sees both roof planes and both gutters. A mast at the middle of one eave would see only one side.
- **Two alternating zones.** Halves the peak flow, so a small pump or a weak mains supply can keep up, and suits a 1,000 L tank.
- **Low-voltage kit, pump by dry contact.** No mains wiring on the house; the pump keeps its own certified controls.
- **Fail to wet on sensor loss, fail closed on power loss.** Losing the head during the fire is likely; losing the controller should not drain the tank.

## Safety

> **Safety:** EmberGuard is not a substitute for evacuation orders, home hardening or professional fire protection. Leave when told to leave. Never stay behind to operate, watch or repair the system during a fire.

> **Safety:** Installing the mast and spray lines means working at height near a roof edge. Use a stable ladder, a second person and fall protection where required; do not work on a wet or mossy roof.

> **Safety:** Water, pumps and electricity. The kit is 12 V DC only. Any mains-powered pump must keep its own certified controls and ground-fault protection; the EmberGuard relay only signals it through an isolated dry contact. Do not wire EmberGuard into mains circuits.

> **Safety:** The LiFePO4 battery is safer than other lithium chemistries but can still overheat if shorted or damaged. Use a pack with a built-in BMS, fuse the battery output, and keep the battery inside the steel enclosure.

> **Safety:** A tall metal mast on the gable is exposed to lightning. Bond it to a proper earth electrode and follow local lightning-protection practice.

> **Safety:** Automatic sprinklers on mains water can reduce pressure for firefighters. Prefer a dedicated tank; if using mains, keep the flow at or below 4 L/min and follow local fire-agency guidance.

> **Safety:** False reassurance is a hazard in itself. The system can miss embers outside its view (vents, decks, the first 1.3 m of each gutter, the far gable), and it can fail in fire conditions. Keep gutters clean and harden the house as if EmberGuard were not there.

## Open questions

- [ ] Does real wind drift at 30 km/h and above leave enough water on the roof edge (R6)? Larger droplets, lower spray angles or heads inside the gutter may help.
- [ ] How long do ember showers last at a single house, and is a 4 h spraying design case reasonable?
- [ ] How reliably can the detection logic tell embers from sun glints, hot vents, chimneys, birds and passing vehicles? This needs recorded thermal video, at TRL 4 or later.
- [ ] How hot does the sensor head get under radiant heat before the front arrives, and for how long does it keep working?
- [ ] Should the eave lines be metal (copper or galvanized steel) so they survive ember contact, at a cost of about $110 more?
- [ ] Is a pre-wet cycle on arming (for example 10 min every hour in extreme wind) worth the water?
- [ ] Should a second mast or a third sensor cover vents, decks and the far gable?
- [ ] Should EmberGuard log and share anonymised ember arrival data with WUI researchers?
