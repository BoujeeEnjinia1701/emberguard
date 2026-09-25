---
doc_id: EGD-CAL-001
title: EmberGuard sizing calculations
project: EmberGuard
doc_type: Calculation
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (viewing geometry, radiometry, water, spray drift, energy, pump options, mast wind load, thermal, cost, requirement status)
---

# EmberGuard sizing calculations

On paper, EmberGuard meets five of its thirteen requirements, has two at risk, misses five and has one that cannot be verified at TRL 3. The most important finding is geometric: from a head 228 mm above the ridge, the roof slab and fascia hide the inside of both gutters along their whole length, and the roof surface itself is seen at a grazing angle of only 1 to 3 degrees. The design therefore cannot watch gutters (R1, R3). Single cool embers fall below the 5 K trigger beyond 5.5 m (R2), a droplet model puts far less water than 5 mm/h on the leeward eave in the design wind (R6), and the priced kit costs $571 against the new $425 budget (R13). The water, fill time, arming, fail-safe and alert requirements are met, the mast is strong, and the kit battery has a thin margin (R8 at risk). Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [A3], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that EmberGuard protects a house. Nothing here justifies staying behind during a fire, skipping home hardening or relying on the system in place of evacuation. See EGD-PRC-001, Safety.

## Scope and method

The note checks every requirement in EGD-REQ-001 v0.3 against the design in EGD-PRC-001 v0.3 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, `derived()` and `sensor_axes()`, so the house, head height, sensor aim, line lengths and mast dimensions are the ones in the STEP files and on drawing EGD-DWG-001. It reads `bom/bom.csv` and `budget_usd` in `project.yaml`, and writes the requirement table to `docs/04-calcs/results.csv`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The reference case is unchanged from TRL 2: a 12 x 8 m single-storey house with a 22 degree gable roof, 500 mm overhangs and 13 m gutters on both long eaves, a 1,000 L tank with its own pump (EGD-DDR-001, D5), and a 4 h ember event within 72 h armed.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Sensor | MLX90640 BAB, 55 x 35 degrees over 32 x 24 pixels; NETD 0.1 K rms at 1 Hz, scaled by the square root of the frame rate; 18 mA typical supply | [Melexis MLX90640 datasheet](https://www.melexis.com/-/media/files/documents/datasheets/mlx90640-datasheet-melexis.pdf) |
| Targets | Emissivity 0.9; 8 to 14 µm band; 300 K background; ember a 10 mm sphere (78.5 mm² projected); a hot spot is 100 cm² flat, or a 100 x 50 mm face of a debris heap | EGD-REQ-001; heap face assumed |
| Radiometry | Apparent pixel rise from the fraction of the pixel's solid angle the target fills; no smoke, lens, blur or point-spread loss; "on a corner" means a quarter of the signal in one pixel | Screening model |
| Line of sight | Straight lines from each sensor checked against the roof slab and fascia of the model house | `cad/src/model.py` |
| Water | 6 heads per eave at 40 L/h and 2 bar (catalogue class, part not named); strip 1.2 m wide along 13 m of eave; 13.2 mm bore line | EGD-REQ-001 |
| Drift | Droplets of 0.25, 0.5, 1.0, 1.5 and 2.0 mm (10, 20, 40, 20 and 10 % of volume), launched at 35, 50 and 65 degrees from the head toward the roof; sphere drag; uniform cross-wind normal to the eave; landing counted on target from the head to 1 m up the roof | Screening model; droplet mix assumed |
| Energy | Buck converter 85 %; ESP32 60 mA active with the radio mostly off; head node 22 mA; charge controller 10 mA; valve 6 W held at 35 % by PWM; LiFePO4 90 % usable, 90 % of that at 0 °C, 80 % at end of life | Typical part figures |
| Wind | 120 km/h gust, air 1.225 kg/m³; drag coefficients 1.2 (tube, panel, anemometer) and 1.3 (head) | Screening values, not a wind-load standard |
| Thermal | 800 W/m² on one enclosure face; 15 W/(m² K) combined film coefficient | Screening values |

## A. Viewing geometry (R3)

- **Pixels.** Each pixel spans 1.72 x 1.46 degrees, 0.24 x 0.20 m at 8 m and 0.42 x 0.36 m at 14 m, normal to the line of sight [A1].
- **Height above the roof.** The head centre is at 4,760 mm and the roof surface at the ridge at 4,532 mm, so the sensors look out from only 228 mm above the roof [A2].
- **Roof edge.** With the TRL 2 aim (45 degrees off the house axis, 15 degrees down), each sensor sees its roof edge from 1.25 m to 13.15 m from the mast, and the whole 1 m strip from 1.25 m to 11.25 m [A3], [A5]. The TRL 2 coverage of "1.3 m to 13 m" holds for the roof edge.
- **Gutters.** No point of either gutter interior (debris 50 mm above the gutter floor) is visible at any of 130 stations along each gutter; the roof slab and fascia hide it [A4], [A5]. Seeing even the gutter lip over the eave edge from the ridge line would need a head 10.6 m above ground, and seeing debris in the gutter 17.9 m [A7], [A8]. **R3 is not met**, and the TRL 2 claim that the head "watches both gutters" is withdrawn from all documents.
- **Grazing angle.** The line of sight meets the roof at 2.6 to 3.2 degrees near the mast, 1.6 degrees at mid-length and 0.9 degrees at the far end [A6]. A head 1.0 m or 1.5 m above the ridge would raise this to 6.7 or 10.0 degrees at 8 m [A9] to [A11], which would help roof-edge detection but not the gutters. Options are in EGD-DDR-001, O3.

## B. Radiometry (R1, R2)

- **Band radiance.** The 8 to 14 µm radiance of a 300 K surface changes by 1.53 % per kelvin [B1]. A target at 300, 400, 600 and 800 °C is 9.9, 15.0, 26.8 and 40.0 times brighter than the background in this band [B2]. The TRL 2 ratios (10 to 16, 29 and 42) were close.
- **Noise and trigger.** Noise is about 0.2 K at 4 Hz. The proposed 5 K trigger is 25 times that; a 5-sigma threshold would be 1.0 K [B3].
- **Single embers (R2).** A 10 mm ember fills 0.16 % of a pixel at 8 m. Centred in a pixel, a 600 °C ember gives 2.4 K and an 800 °C ember 3.6 K; on a pixel corner, 0.6 K and 0.9 K [B4], [B5]. A 600 °C ember reaches the 5 K trigger within 5.5 m centred and 2.8 m on a corner [B6]. The TRL 2 figures (about 3 K at 8 m, threshold reached within about 5 m) are corrected. With a 2 K trigger, the reach would be 8.8 m centred and 4.4 m on a corner [B7]. The roof edge lies 5.0 to 14.0 m from the sensor [B8]. **R2 is not met.**
- **Smouldering spots (R1).** A flat 100 cm² spot at 300 °C on the roof edge, seen at 1.6 degrees from 8.2 m, gives only 2.8 K, and 0.58 K at the far end [B9], [B10]. A spot with some height, such as a 100 x 50 mm face of a smouldering debris heap, gives 42.7 K at 8.2 m and reaches the 5 K trigger out to 26 m [B9], [B11]. So hot debris with height on the roof edge is easy to see, flat spots are not, and anything inside the gutter is not visible at all (section A). **R1 is not met** for the gutters it names.

## C. Water (R5, R6, R7)

- **Flow and rate.** Each zone draws 4.0 L/min over a 15.6 m² strip: 15.4 mm/h while it runs and 7.7 mm/h averaged at 50 % duty [C1].
- **Lines and fill (R5).** The model's zone lines are 17.7 m (front, A) and 21.3 m (back, B), holding 2.43 L and 2.92 L [C2]. With a 4 L/min supply, opening the zone on the side of the detection first puts water at its farthest head 47 s or 55 s after detection; opening both together from 4 L/min would take 91 s, or 51 s if the supply gives 8 L/min [C3]. R5 is **met** with the detection-side zone filled first; the precis now says so.
- **Pressure.** Friction is about 6.8 kPa and the lift from the valves to the heads 2.08 m (20 kPa), so the supply must hold about 2.27 bar at the manifold for 2.0 bar at the heads [C4].
- **Water per event (R7).** 960 L of spray and 5.3 L of line fill make 965 L per 4 h event, 3.5 % inside 1,000 L [C5]. **Met**, with little margin.
- **Drift (R6).** In the screening model the heads are tuned so a 1 mm droplet at 50 degrees lands 0.64 m inboard in still air, with a 4.25 m/s launch speed [C6]. All the spray lands on the strip in still air. With a cross-wind blowing onto the roof, 97 to 100 % still lands on the strip; blowing off the roof, only 33 % at 4.2 m/s and 10 % at 8.3 m/s (30 km/h) [C7]. The leeward eave therefore gets 2.6 mm/h at 4.2 m/s and 0.8 mm/h at 8.3 m/s, and the windward eave 7.4 mm/h at 8.3 m/s [C8]. The TRL 2 figure of 3.8 mm/h rested on a flat 50 % drift guess; the model says the windward eave does better and the leeward much worse. Meeting 5 mm/h at 50 % duty needs 65 % of the spray on target [C9]. **R6 is not met.** The model ignores the recirculation behind the ridge, which may reduce or reverse the local wind at the leeward eave, so the true figure could be better; it needs a spray trial in wind, which is TRL 4 work.

## D. Energy (R8) and pump power options

- **Armed.** The 3.3 V loads total 439 mW [D1]. With buck losses, the charge controller's 10 mA and a beacon blink, the battery supplies 0.67 W, or 48.2 Wh in 72 h [D2].
- **Spraying.** One valve held at 35 % of its 6 W rating, the relay coil and the armed loads draw 3.15 W, 12.7 Wh over 4 h including 5 min of siren [D3]. Without holding-current reduction the valves alone would need 24 Wh [D5].
- **Battery.** The need is 61.0 Wh. The 12.8 V 6 Ah pack gives 69.1 Wh usable at 25 °C (13 % margin), 62.2 Wh at 0 °C (2 %) and 55.3 Wh at end of life (9 % short) [D4]. **R8 is at risk.** A 10 Ah pack (EGD-DDR-001, O5) would clear all three cases. The TRL 2 figures (43 Wh armed, 20 Wh spraying, 64 Wh total) are corrected.
- **Solar.** Not credited in R8. On a clear day the 10 W panel gives about 24 Wh against 16.1 Wh per armed day [D6].
- **Pump options (EGD-DDR-001, D6).** A 12 V diaphragm pump at 4 L/min and 2.6 bar needs about 17 W of hydraulic power and about 57 W electrical, 229 Wh per 4 h event [D7]. Option (b), a separate 12.8 V LiFePO4 pump battery, needs 254 Wh, so a 25 Ah pack [D8]. Option (c), one SwapCell pack through a 48 to 12 V converter, gives about 374 Wh usable, 6.5 h of pumping or 1.6 events, drawing about 1.3 A from the pack against its 15 A legacy limit [D9]. Under SwapCell interface v0.3, EmberGuard would be a host without CAN: it fits the 10 kΩ coding resistor in the INTERLOCK loop (item W) and drives WAKE high only while the pump must run, so the pack sleeps while EmberGuard is armed. The charge-while-discharging mode (item C) is needed only if the pack also sits on a charger, and the vehicle latch rating (item V) does not apply. Under the portfolio rule the pack would be priced once in SwapCell and excluded from this kit's budget. Neither option is adopted; pump power stays with the homeowner.

## E. Mast wind load (R10)

- At a 120 km/h gust the dynamic pressure is 681 Pa [E1], and the mast, head, anemometer, panel and shield carry about 205 N in total, 71 N of it on the solar panel [E2].
- The moment at the upper standoff is 58 N·m. The 40 x 2 mm tube (section modulus 2,161 mm³) sees 27 MPa, 8.9 times below the 6061-T6 yield and 4.1 times below a heat-affected value [E3]. The TRL 2 figures (55 N·m, 25 MPa) are close.
- The upper standoff reaction is 203 N; as a 700 mm cantilever from the wall, the DN25 pipe sees 66 MPa (factor 3.5 on S235), and each of two wall anchors carries about 710 N of pull [E4]. The anchors and the gable wall's capacity must be checked for each house. The wind part of R10 is **met** on paper.

## F. Thermal (R10)

- A steel ground enclosure with a mid-grey finish (absorptance 0.6) in full sun at 60 °C ambient reaches about 71 °C inside; a light finish (0.25) about 65 °C [F1], [F2]. LiFePO4 is rated for discharge to about 60 °C and charge to 45 °C; the electronics and sensors are rated to 85 °C [F3]. The battery would therefore exceed its limit at the top of the R10 range unless the enclosure is light-coloured and shaded. The BOM now specifies a light powder coat; a sun shade is not yet designed.
- Under its stainless hood in full sun, the hood runs about 8 K above ambient and the shaded head a few kelvin above ambient [F4].
- Radiant heat from an approaching fire front is not estimated; it depends on the fire and needs data. **R10 is at risk.**

## G. Cost (R13)

- The 17 priced kit lines total $571.00 against the $425 budget set in EGD-DDR-001 (D1), 34 % over [G1]. The largest lines are the two thermal sensors ($96), spray lines and heads ($52), mast and standoffs ($48) and the sensor head ($45) [G2].
- The TRL 2 indicative total of $420 rose by $151 [G4]: most lines were underpriced at TRL 2, and a mast earthing kit (item 17, $26) was added because the lightning safety note required one.
- Metal eave runs would add $110, for $681 [G3]; under D4 they are a priced option, not in the kit. **R13 is not met.** Options are in EGD-DDR-001, O2.

## Requirement status

*Table 2. Status of every requirement in EGD-REQ-001 v0.3 [H1]. Not met items first. Also written to `docs/04-calcs/results.csv`.*

| ID | Requirement | Value at TRL 3 | Target | Status |
| --- | --- | --- | --- | --- |
| R1 | Detect a smouldering ignition | Gutter interiors hidden everywhere; flat 100 cm² spot 2.8 K at 8.2 m, 0.58 K at 13.9 m; a 100 x 50 mm hot face is seen to 26 m | 100 cm² at 300 °C along the gutters, 1.5 to 13 m, in 10 s | **Not met** |
| R2 | Detect single landed embers | 600 °C ember 2.4 K at 8 m (centred); reaches 5 K within 5.5 m | 10 mm, 600 °C, within 8 m, in 10 s | **Not met** |
| R3 | Watch both roof planes | Roof edge in view 1.25 to 13.15 m from the mast; gutter interiors not visible | Both gutters, 1.5 m to the far end | **Not met** |
| R6 | Wet the gutter and roof edge | Leeward eave 0.8 mm/h at 8.3 m/s, 2.6 mm/h at 4.2 m/s; windward eave 7.4 mm/h at 8.3 m/s (screening model) | 5 mm/h net at 30 km/h | **Not met** |
| R13 | Stay within the budget | $571 | $425 | **Not met** |
| R8 | Work through a grid outage (kit) | 61.0 Wh needed; 69.1 Wh usable at 25 °C, 62.2 Wh at 0 °C, 55.3 Wh at end of life | 72 h armed plus 4 h spraying on the kit battery | At risk |
| R10 | Survive fire weather | Mast 27 MPa (factor 8.9); standoff factor 3.5; enclosure about 71 °C in sun at 60 °C ambient | 120 km/h gusts; -10 to 60 °C | At risk |
| R11 | Install without roof work or mains wiring | Clamped mast and lip clips, 12 V only; install time not estimated | No penetrations; 12 V; 6 h, two people | Not verifiable at TRL 3 |
| R4 | Arm only in fire weather | Arming logic and defaults as decided (D7) | 30 km/h or 50 km/h gusts with RH 20 % or less for 10 min | Met |
| R5 | Start water quickly | 55 s worst zone, detection-side zone first | 60 s | Met |
| R7 | Use little water | 4 L/min; 965 L per event | 4 L/min; 1,000 L | Met |
| R9 | Fail safely | Normally closed valves; fail to wet on sensor loss; alarms | As specified | Met |
| R12 | Tell people what it is doing | Siren, beacon and log; phone alerts need a network | As specified | Met |

## Corrections to the TRL 2 documents

- Gutter coverage: the gutter interiors are not visible from the head (was "each gutter from about 1.3 m to 13 m") [A4]; the roof edge is in view from 1.25 m to 13.15 m [A3].
- Ember signal at 8 m: 2.4 K at 600 °C and 3.6 K at 800 °C (was about 3 K and 5 K); 5 K reached within 5.5 m (was about 5 m) [B4] to [B6].
- Line lengths: 17.7 m and 21.3 m per zone, 39 m in all (was about 21 m per zone and 44 m) [C2]; fill with the detection-side zone first (was "both valves open together") [C3].
- Water per event: 965 L (was about 960 L) [C5].
- Net wetting: 0.8 to 2.6 mm/h on the leeward eave (was 3.8 mm/h with 50 % drift assumed) [C8].
- Energy: 48.2 Wh armed, 12.7 Wh spraying, 61.0 Wh in all (was 43, 20 and 64 Wh) [D2] to [D4].
- Mast: 58 N·m and 27 MPa (was 55 N·m and 25 MPa) [E3].
- Cost: $571 (was about $420) [G1].
