---
doc_id: EGD-CAL-001
title: EmberGuard sizing calculations
project: EmberGuard
doc_type: Calculation
version: "0.5"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (viewing geometry, radiometry, water, spray drift, energy, pump options, mast wind load, thermal, cost, requirement status)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). Section A rewritten for gutter-corner sensor pods; 2 K trigger; leeward-only spray rule; 10 Ah battery; mast without a sensor head; cost at $605 against $575
- version: "0.3"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish ($605); R13 from not met to met
- version: "0.4"
  date: '2026-10-01'
  author: Amish Chadha
  change: Design for construction (EGD-DDR-003). Line routes, fill and pressure from the constructable model; new wind check on the pod arm and verge cleat [E5]; cost $689 against $605, R13 met to not met
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
---

# EmberGuard sizing calculations

On paper, the constructable EmberGuard meets seven of its thirteen requirements, has three at risk, misses one, is over its value-engineering cost target on one and has one that cannot be verified at TRL 3. Version 0.4 checks the design after it was made buildable (EGD-DDR-003): new spray-line routes, a pod arm on a verge cleat, and the parts added for construction, which raise the kit to $689, USD 84 over the $605 value-engineering target (R13). Version 0.2 checked the design after Amish accepted the open recommendations on 2026-09-25 (EGD-DDR-002): the thermal sensors move from a head above the ridge to pods at the gable-end corners of the gutters, the trigger drops from 5 K to 2 K, only the leeward spray zone runs in wind, the battery grows to 10 Ah and the budget rises to $575. On 2026-09-26 Amish approved a budget of $605 to cover the priced BOM (EGD-DDR-002). The pods fix the main finding of version 0.1: they see the inside of each open gutter from 1.25 m to 12.95 m, where the old head saw none of it (R3 now met). Hanger straps across the gutter top still shadow debris lying deep in the gutter beyond 7.8 m, and flat hot spots fade below the trigger near the far end, so R1 is at risk. Single embers reach the 2 K trigger to 8.8 m only when centred in a pixel (R2 at risk). The leeward-only rule roughly doubles the water on the leeward eave but still gives only 1.5 mm/h in the design wind (R6 not met). The kit as first priced cost $605, exactly the approved budget; the parts added for construction take it to $689, USD 84 over the $605 value-engineering target (R13). The battery now has a wide margin (R8 met). Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [A3], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that EmberGuard protects a house. Nothing here justifies staying behind during a fire, skipping home hardening or relying on the system in place of evacuation. See EGD-PRC-001, Safety.

## Scope and method

The note checks every requirement in EGD-REQ-001 v0.6 against the design in EGD-PRC-001 v0.6 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, `derived()` and `sensor_axes()`, so the house, pod position, sensor aim, line lengths and mast dimensions are the ones in the STEP files and on drawing EGD-DWG-001 Rev P4. It reads `bom/bom.csv` and `budget_usd` in `project.yaml`, and writes the requirement table to `docs/04-calcs/results.csv`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The reference case is unchanged: a 12 x 8 m single-storey house with a 22 degree gable roof, 500 mm overhangs and 13 m gutters on both long eaves, a 1,000 L tank with its own pump (EGD-DDR-001, D5), and a 4 h ember event within 72 h armed.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Sensor | MLX90640 BAB, 55 x 35 degrees over 32 x 24 pixels; NETD 0.1 K rms at 1 Hz, scaled by the square root of the frame rate; 18 mA typical supply | [Melexis MLX90640 datasheet](https://www.melexis.com/-/media/files/documents/datasheets/mlx90640-datasheet-melexis.pdf) |
| Targets | Emissivity 0.9; 8 to 14 µm band; 300 K background; ember a 10 mm sphere (78.5 mm² projected); a hot spot is 100 cm² flat on the debris, or a 100 x 50 mm face of a debris heap | EGD-REQ-001; heap face assumed |
| Radiometry | Apparent pixel rise from the fraction of the pixel's solid angle the target fills; no smoke, lens, blur or point-spread loss; "on a corner" means a quarter of the signal in one pixel | Screening model |
| Gutter | Debris surface 42 mm below the lip on the gutter centreline; hanger straps 25 mm wide across the top at lip level every 750 mm from the east end; an end cap at lip height | Assumed typical fixing |
| Line of sight | Straight lines from each pod sensor checked against the roof slab, fascia, gutter end cap and hanger straps of the model house | `cad/src/model.py` |
| Water | 6 heads per eave at 40 L/h and 2 bar (catalogue class, part not named); strip 1.2 m wide along 13 m of eave; 13.2 mm bore line | EGD-REQ-001 |
| Drift | Droplets of 0.25, 0.5, 1.0, 1.5 and 2.0 mm (10, 20, 40, 20 and 10 % of volume), launched at 35, 50 and 65 degrees from the head toward the roof; sphere drag; uniform cross-wind normal to the eave; landing counted on target from the head to 1 m up the roof | Screening model; droplet mix assumed |
| Energy | Buck converter 85 %; ESP32 60 mA active with the radio mostly off; two pod nodes at 22 mA each; charge controller 10 mA; valve 6 W held at 35 % by PWM; LiFePO4 90 % usable, 90 % of that at 0 °C, 80 % at end of life | Typical part figures |
| Wind | 120 km/h gust, air 1.225 kg/m³; drag coefficient 1.2 on tube, panel and anemometer | Screening values, not a wind-load standard |
| Thermal | 800 W/m² on one enclosure face; 15 W/(m² K) combined film coefficient | Screening values |

## A. Viewing geometry (R3)

- **Pixels.** Each pixel spans 1.72 x 1.46 degrees, 0.24 x 0.20 m at 8 m and 0.42 x 0.36 m at 14 m, normal to the line of sight [A1].
- **Pods.** Each pod sits 200 mm beyond the east end of its gutter with its centre 500 mm above the lip (2,968 mm above ground), over the gutter centreline. The sensor looks along the gutter, 10 degrees toward the house and 5 degrees down [A2].
- **Open gutter.** The debris surface inside the front gutter is in view and unobstructed at 118 of 130 stations, from 1.25 m to 12.95 m from the east end of the gutter, at ranges of 1.5 to 13.1 m; the back gutter is the mirror image [A3], [A5]. **R3 is met** for an open gutter. The roof edge is in view from 0.45 m, and the whole 1 m strip from 1.25 m to 12.95 m [A5].
- **Hanger straps.** Looking along a gutter from 0.5 m above the lip, each strap casts a shadow on the debris behind it that lengthens with distance. With straps every 750 mm, debris 42 mm below the lip is visible at only 35 of 118 stations and at none beyond 7.8 m; debris heaped to within 10 mm of the lip is visible at 95 of 118 [A4]. A deep, level bed of needles far from the pod is therefore hidden, while a heap or a flame rising from the debris is seen. Options are in EGD-DDR-002, N3.
- **Grazing angle.** The line of sight meets the debris surface at 7.4 degrees at 4 m, 3.8 degrees at 8 m and 2.4 degrees at 13 m, and the roof edge at 3.7, 1.9 and 1.2 degrees [A6].
- **Former head.** For reference, the ridge-line head of version 0.1 saw the front gutter debris at 0 of 130 stations [A7].

## B. Radiometry (R1, R2)

- **Band radiance.** The 8 to 14 µm radiance of a 300 K surface changes by 1.53 % per kelvin [B1]. A target at 300, 400, 600 and 800 °C is 9.9, 15.0, 26.8 and 40.0 times brighter than the background in this band [B2].
- **Noise and trigger.** Noise is about 0.2 K at 4 Hz. The persistent-spot trigger is now 2 K, ten times that noise (EGD-DDR-002, O5); version 0.1 used 5 K. A 5-sigma threshold would be 1.0 K [B3]. The false-trigger rate at 2 K is unknown and needs recorded thermal video (TRL 4, on hold).
- **Single embers (R2).** A 10 mm ember fills 0.16 % of a pixel at 8 m. Centred in a pixel, a 600 °C ember gives 2.4 K and an 800 °C ember 3.6 K; on a pixel corner, 0.6 K and 0.9 K [B4], [B5]. With the 2 K trigger a 600 °C ember is detected to 8.8 m centred and 4.4 m on a corner; with the former 5 K trigger, 5.5 m and 2.8 m [B6], [B7]. An ember 8 m along the gutter is 8.2 m from the sensor [B8]. **R2 is at risk:** met for a centred ember, not for one on a pixel corner, and the 2 K false-trigger rate is unverified.
- **Smouldering spots (R1).** A flat 100 cm² spot at 300 °C on the debris, 8 m along the gutter, gives 6.7 K; at 13 m, seen at 2.4 degrees, 1.6 K [B9], [B10]. A flat spot reaches the 2 K trigger out to 12.1 m along the gutter. A 100 x 50 mm face of a smouldering heap gives 43 K at 8 m and 18 K at 13 m, and reaches the trigger out to 41 m [B9] to [B11]. **R1 is at risk:** hot debris with height is easy to see along the whole gutter, but a flat spot beyond 12.1 m and deep debris in the hanger-strap shadows beyond 7.8 m (section A) are not.

## C. Water (R5, R6, R7)

- **Flow and rate.** Each zone draws 4.0 L/min over a 15.6 m² strip: 15.4 mm/h while it runs and 7.7 mm/h averaged at 50 % duty [C1].
- **Lines and fill (R5).** The zone lines, routed up the gable corner and under the gutter as built (EGD-DDR-003, P11), are 17.5 m (front, A) and 21.1 m (back, B), holding 2.39 L and 2.88 L [C2]. Opening the zone on the side of the detection first puts water at its farthest head 47 s or 54 s after detection [C3]. **Met.**
- **Pressure.** Friction is about 6.8 kPa and the lift from the valves to the heads 2.08 m (20 kPa), so the supply must hold about 2.27 bar at the manifold [C4].
- **Water per event (R7).** 960 L of spray and 5.3 L of line fill make 965 L per 4 h event, 3.5 % inside 1,000 L [C5]. **Met.** The leeward-only rule keeps the draw at 4 L/min, so this is unchanged.
- **Drift.** The screening model is unchanged from version 0.1 [C6]. All the spray lands on the strip in still air; with the wind blowing onto the roof, 97 to 100 %; blowing off the roof, 33 % at 4.2 m/s and 10 % at 8.3 m/s (30 km/h) [C7]. Alternating zones would give the leeward eave 2.6 mm/h and 0.8 mm/h [C8], [C9].
- **Leeward-only rule (R6).** Under the rule decided in EGD-DDR-002 (O4), above 2 m/s of cross-eave wind only the leeward zone runs, continuously. The leeward eave then gets 5.1 mm/h at 4.2 m/s and 1.5 mm/h at 8.3 m/s. The windward eave is dry until a detection on its side returns the system to alternating zones, when it gets 7.4 mm/h [C10]. **R6 is not met** at the 30 km/h design wind. The model ignores the recirculation behind the ridge, which may reduce the local wind at the leeward eave; at half the design wind the rule would meet 5 mm/h. Options are in EGD-DDR-002, N2; a spray trial in wind is TRL 4 work, on hold.

## D. Energy (R8) and pump power options

- **Armed.** The 3.3 V loads total 512 mW, including two pod nodes in place of the former head node [D1]. With buck losses, the charge controller's 10 mA and a beacon blink, the battery supplies 0.76 W, or 54.4 Wh in 72 h [D2].
- **Spraying.** One valve held at 35 % of its 6 W rating, the relay coil and the armed loads draw 3.24 W, 13.1 Wh over 4 h including 5 min of siren [D3]. Without holding-current reduction the valves alone would need 24 Wh [D5].
- **Battery.** The need is 67.5 Wh. The 12.8 V 10 Ah pack (EGD-DDR-002, O5) gives 115.2 Wh usable at 25 °C (71 % margin), 103.7 Wh at 0 °C (54 %) and 92.2 Wh at end of life (37 %) [D4]. **R8 is met.** Version 0.1 had 61.0 Wh against a 6 Ah pack that fell 9 % short at end of life.
- **Solar.** Not credited in R8. On a clear day the 10 W panel gives about 24 Wh against 18.1 Wh per armed day [D6].
- **Pump options (EGD-DDR-001, D6).** A 12 V diaphragm pump at 4 L/min and 2.6 bar needs about 17 W of hydraulic power and about 57 W electrical, 229 Wh per 4 h event [D7]. Option (b), a separate 12.8 V LiFePO4 pump battery, needs 254 Wh, so a 25 Ah pack [D8]. Option (c), one SwapCell pack through a 48 to 12 V converter, gives about 374 Wh usable, 6.5 h of pumping or 1.6 events, drawing about 1.3 A from the pack against its 15 A legacy limit [D9]. Under SwapCell interface v0.3, EmberGuard would be a host without CAN: it fits the 10 kΩ coding resistor in the INTERLOCK loop (item W) and drives WAKE high only while the pump must run. Under the portfolio rule the pack would be priced once in SwapCell and excluded from this kit's budget. Neither option is adopted; pump power stays with the homeowner.

## E. Mast wind load (R10)

- At a 120 km/h gust the dynamic pressure is 681 Pa [E1]. With the sensor head gone, the mast, anemometer, panel and shield carry about 174 N in total, 71 N of it on the solar panel [E2].
- The moment at the upper standoff is 31 N·m, and the 40 x 2 mm tube sees 14 MPa, 16.6 times below the 6061-T6 yield and 7.6 times below a heat-affected value [E3].
- The upper standoff reaction is 153 N; the DN25 pipe standoff sees 50 MPa (factor 4.7 on S235), and each wall anchor carries about 535 N of pull [E4]; the 140 mm wall plates under the flanges keep this lever. The wind part of R10 is **met** on paper for the mast.
- The pod arm (40 x 6 mm flat bar, bent twice) carries a pod, hood and plate of about 0.83 kg. At 120 km/h about 7 N pushes sideways and up to 13 N lifts the hood; the arm's rise and run see about 8 and 7 MPa, a factor of 19 on 6063-T6 (6 even if the bends were annealed), and each of the two coach screws into the verge sees about 70 N of pull [E5]. **Met** on paper.

## F. Thermal (R10)

- A steel ground enclosure with a mid-grey finish (absorptance 0.6) in full sun at 60 °C ambient reaches about 71 °C inside; a light finish (0.25) about 65 °C [F1], [F2]. LiFePO4 is rated for discharge to about 60 °C and charge to 45 °C; the electronics and sensors are rated to 85 °C [F3]. The battery would exceed its limit at the top of the R10 range unless the enclosure is light-coloured and shaded.
- Under its stainless hood in full sun, a pod runs a few kelvin above ambient and the hood about 8 K. The pods sit 0.5 m above the gutters, where embers land, so their radiant and ember exposure is higher than the old ridge-line head's [F4].
- Radiant heat from an approaching fire front is not estimated; it depends on the fire and needs data. **R10 is at risk.**

## G. Cost (R13)

- The 17 priced kit lines total $689.00 against the $605 value-engineering target (`budget_usd`, a hypothetical control target set on 2026-09-26), 14 % over [G1]. The parts added to make the kit buildable (EGD-DDR-003) account for the $84 rise: flanges, crossover plates and U-bolts, pod mounts and lens hoods, the panel tilt bracket, longer cables, and the valve board, clips, glands and strap. The largest lines are the two thermal sensors ($96), the mast, standoffs and crossover plates ($80), the two sensor pods ($74) and the spray lines and heads ($52) [G2].
- Since version 0.1 the total rose by $34 [G4]: the pods and their cables cost $21 more than the head and mast cable, and the 10 Ah battery $13 more than the 6 Ah pack.
- Metal eave runs would add $110, for $799 [G3]; under D4 they are a priced option, not in the kit. **R13 is over the value-engineering target by USD 84.** The savings worth trying are in the Value engineering section of EGD-DEC-001.

## Requirement status

*Table 2. Status of every requirement in EGD-REQ-001 v0.6 [H1]. Not met items first. Also written to `docs/04-calcs/results.csv`.*

| ID | Requirement | Value at TRL 3 | Target | Status |
| --- | --- | --- | --- | --- |
| R6 | Wet the gutter and roof edge | Leeward-only rule: leeward eave 1.5 mm/h at 8.3 m/s, 5.1 mm/h at 4.2 m/s; windward eave wetted only after a windward detection (screening model) | 5 mm/h net at 30 km/h | **Not met** |
| R1 | Detect a smouldering ignition | Gutter debris in view 1.25 to 12.95 m; hot face reaches 2 K to 41 m; flat spot to 12.1 m (1.6 K at 13 m); hanger straps hide deep debris at 83 of 118 stations, all beyond 7.8 m | 100 cm² at 300 °C along the gutters, 1.5 to 13 m, in 10 s | At risk |
| R2 | Detect single landed embers | 600 °C ember reaches 2 K to 8.8 m centred, 4.4 m on a pixel corner; false-trigger rate unknown | 10 mm, 600 °C, within 8 m, in 10 s | At risk |
| R13 | Stay near the value-engineering target | $689 | $605 kit parts | **Over the value-engineering target by USD 84** |
| R10 | Survive fire weather | Mast 14 MPa (factor 16.6); standoff factor 4.7; pod arm factor 19; enclosure about 71 °C in sun at 60 °C ambient; pods exposed at the gutters | 120 km/h gusts; -10 to 60 °C | At risk |
| R11 | Install without roof work or mains wiring | Mast on wall plates, pod arms on verge cleats, lip clips, 12 V only; install time not estimated | No penetrations; 12 V; 6 h, two people | Not verifiable at TRL 3 |
| R3 | Watch both roof planes | Gutter interiors in view 1.25 to 12.95 m from the east end, both gutters (open gutter) | Both gutters, 1.5 m to the far end | Met |
| R4 | Arm only in fire weather | Arming logic and defaults as decided (D7) | 30 km/h or 50 km/h gusts with RH 20 % or less for 10 min | Met |
| R5 | Start water quickly | 54 s worst zone, detection-side zone first | 60 s | Met |
| R7 | Use little water | 4 L/min; 965 L per event | 4 L/min; 1,000 L | Met |
| R8 | Work through a grid outage (kit) | 67.5 Wh needed; 115.2 Wh usable at 25 °C, 103.7 Wh at 0 °C, 92.2 Wh at end of life | 72 h armed plus 4 h spraying on the kit battery | Met |
| R9 | Fail safely | Normally closed valves; fail to wet on sensor loss; alarms | As specified | Met |
| R12 | Tell people what it is doing | Siren, beacon and log; phone alerts need a network | As specified | Met |

## Changes in version 0.4

- Design for construction (EGD-DDR-003): zone lines 17.5 m and 21.1 m (were 17.7 m and 21.3 m), fill 47 s and 54 s (was 55 s) [C2], [C3]; manifold 520 mm above the ground (was 450 mm), so the lift is 2.01 m and the supply still needs about 2.3 bar [C4].
- New wind check on the pod arm and verge cleat [E5].
- Cost: $689 against $605 (was $605) [G1]; R13 met to over the value-engineering target.

## Changes in version 0.3

- Budget: $605, approved by Amish on 2026-09-26 to cover the priced BOM (was $575) [G1]; R13 not met to met, with no margin.

## Changes from version 0.1

- Gutter coverage: the inside of each open gutter is in view from 1.25 m to 12.95 m (was none from the ridge-line head) [A3]; R3 not met to met.
- Hanger straps: a new check; deep debris is hidden beyond 7.8 m [A4].
- Trigger: 2 K (was 5 K); a 600 °C ember is detected to 8.8 m centred (was 5.5 m) [B6]; R2 not met to at risk.
- Flat 100 cm² spot: 6.7 K at 8 m from the pod (was 2.8 K at 8.2 m from the head) [B9]; R1 not met to at risk.
- Leeward eave at 8.3 m/s: 1.5 mm/h under the leeward-only rule (was 0.8 mm/h alternating) [C10]; R6 still not met.
- Energy: 67.5 Wh needed (was 61.0 Wh) against 115.2 Wh usable (was 69.1 Wh) [D4]; R8 at risk to met.
- Mast: 14 MPa and 535 N per anchor (was 27 MPa and 710 N) [E3], [E4].
- Cost: $605 against $575 (was $571 against $425) [G1].
