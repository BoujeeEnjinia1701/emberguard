# Review note: EmberGuard

## Session 2026-09-25: /populate to a strong TRL 2 (overnight batch)

### What was done

- `docs/01-problem.md` (EGD-PRB-001 v0.2): the problem (ember ignition, timing, power and water in fire weather, cost of commercial systems), users and context, constraints, out of scope, prior work with inline sources, open questions. The scaffold had no co-design checklist, so none was kept or added.
- `docs/03-requirements.md` (EGD-REQ-001 v0.2): 13 measurable requirements (R1 to R13) with targets, planned verification and a concept status column; reference house and assumptions.
- `docs/02-concept.md` (EGD-PRC-001 v0.2): how it works (watch, arm, detect, wet, fail safe, tell), components table numbered to the BOM and exploded view, first-order numbers with assumptions, key design choices, safety section, open questions.
- `cad/src/concept_media.py`: massing model of a 12 x 8 m single-storey house (context) with the kit: gable-end mast, sensor head, two thermal sensors, anemometer and vane, humidity sensor, solar panel, ground enclosure with controller and battery, zone valves, pressure transducer, relay, siren, mast cable and spray lines on both gutters. Tank and pump shown as context in the hero only.
- `media/`: `hero.png` (1.75 m figure), `concept-blueprint.png`, `.pdf` and `.svg` (orthographic views at 1:100), `model.glb` and `viewer.html`, `exploded.png` with BOM callouts, `cutaway.png` (section through the front eave at a spray head), `flow.png` (water per 4 h event, all values marked as estimates). The hero, cutaway and exploded views are custom renders from the same model so the small kit parts read clearly against the house; temporary `media/_views*` folders are removed by the script.
- `bom/bom.csv`: 16 lines with indicative prices, numbered to match the exploded view; `bom/bom-notes.md` updated.
- `README.md`: hero image and links line before "## Problem"; problem, concept, key components and safety updated to match the precis. Pitch sentence unchanged.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml`: unchanged. The pitch and problem still match the concept.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| 100 cm² smouldering spot at 14 m | tens of kelvin of pixel rise | R1 met |
| 10 mm ember, 800 °C / 600 °C, at 8 m | about 5 K / about 3 K against a 5 K trigger | **R2 partly met** |
| Gutter coverage from one gable-end mast | 1.3 m to 13 m of each gutter | R3 met except 1.3 m per gutter |
| Water at farthest head after detection | about 55 s | R5 met |
| Net wetting at 30 km/h wind | about 3.8 mm/h (7.7 mm/h gross, 50 % drift assumed) | **R6 not met** (target 5 mm/h) |
| Steady flow; water per 4 h event | 4 L/min; about 960 L | R7 met, no margin |
| Battery need, 72 h armed plus 4 h spraying | about 64 Wh against about 69 Wh usable | R8 kit part met, thin margin; **not met by the kit alone** with a grid-powered pump |
| Mast bending stress at 120 km/h | about 25 MPa in a 40 x 2 mm aluminium tube | R10 wind met; thermal unverified |
| Kit parts cost | about $420 | **R13 not met** (budget $300, 40 % over) |

Requirements not met or at risk:

- **R6 (net wetting) not met:** wind drift is assumed at 50 %; the true figure is unknown and could be better or much worse.
- **R13 (cost) not met:** about $420 against $300.
- **R2 (single embers) partly met:** a 600 °C ember falls below the proposed 5 K threshold beyond about 5 m. Smouldering spots (R1) are easy to see; single cool embers are not.
- **R8 not met by the kit alone** where the pump needs grid power during an outage.
- **R10 thermal, R11 install time and false-trigger rate** are unverified.

### Proposed, awaiting Amish

1. **Budget.** Parts are about $420 against `budget_usd: 300`. Options: (a) raise `budget_usd` to $425; (b) keep $300 by dropping to one thermal sensor and one zone (watches only one roof plane, about $340, still over); (c) keep $300 for a "sense and control" kit and cost the spray lines and valves as a separate zone kit (about $320 and $100). Recommendation: (a). `project.yaml` is unchanged.
2. **Sensing approach.** Two MLX90640-class thermal arrays (recommended) versus cheap near-infrared flame sensors (about $5, but cannot locate hot spots or reject sunlight) versus a single wide-angle 110 degree array (cheaper, but single embers become invisible beyond a few metres).
3. **Mast position.** Gable end at the ridge line, watching both roof planes (recommended), versus mid-eave on one side (simpler install, one roof plane only), versus two masts.
4. **Eave line material.** UV-stable polyethylene (in the cost) versus copper or galvanized steel eave runs (about $110 more, survives ember contact). Recommendation: metal on the eave runs, polyethylene only for the ground-level risers, if the budget allows.
5. **Water source for the first design case.** Tank with a pump on its own supply (recommended, protects hydrant pressure) versus mains connection.
6. **Pump power in an outage.** (a) Out of scope; homeowner provides a generator or gravity feed (current concept); (b) add a 12 V diaphragm pump and a larger battery (about 160 to 200 Wh more for 4 h of continuous pumping at 4 L/min, estimate); (c) power a 12 V pump from a portfolio SwapCell pack (about 468 Wh). Recommendation: (a) for TRL 2, with (b) or (c) studied at TRL 3. Using SwapCell is only an option here and is not assumed anywhere in the design.
7. **Arming thresholds.** Defaults of 30 km/h sustained or 50 km/h gusts with humidity at or below 20 % for 10 min, plus manual and remote arming. Recommendation: keep as adjustable defaults and review with a local fire agency.
8. **Fail-to-wet on sensor loss while armed** (recommended) versus fail-to-stop.
9. **Normally closed valves** (recommended, close on power loss) versus latching valves (lower energy, but stay open if the controller dies).
10. **First partner** for co-design and field input: a Firewise-style neighbourhood group, a county fire-safe council or a university WUI research group.

### Safety concerns

- False reassurance: people might stay behind or skip home hardening. Every document says EmberGuard does not replace evacuation or hardening.
- Work at height during installation and maintenance.
- Water and electricity: the kit is 12 V only; a mains pump must keep its own certified controls and ground-fault protection.
- LiFePO4 battery: fused, with BMS, inside the steel enclosure.
- Lightning: the mast is the highest point on the house and must be earthed.
- Community water pressure: automatic spraying from mains during a fire can reduce hydrant pressure; flow is capped at 4 L/min and a tank is preferred.

### Problems and gaps

- **Sources not re-verified.** The web search budget for this session was used up, and web fetches were not permitted, so no page could be opened. Sources in EGD-PRB-001 were cited from prior knowledge (DOIs for Caton et al. 2017, Hakes et al. 2017, Manzello et al. 2020, Syphard and Keeley 2019, NIST TN 1635 and TN 2135; home pages for CAL FIRE, CPUC, NFPA, Melexis and Frontline). Mitchell (2006) and AS 5414:2012 are cited without links. Every link and claim should be checked before the documents leave draft. No percentage for ember-caused ignitions is quoted for this reason.
- The detection figures rest on a simple radiometric estimate with no motion blur, smoke attenuation or lens transmission included.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).

### Recommended next step

Review this note and the media, then decide items 1, 4 and 6. If approved, run `/advance-trl3` to check the radiometric detection estimate, spray drift and wetting, energy budget and mast wind load by calculation, and to build the parametric model and drawing sheet.

## Session 2026-09-25: TRL 3

Amish approved all recommendations across all batches on 2026-09-25 and said not to proceed to TRL 4. This session took EmberGuard from TRL 2 to TRL 3 and stopped.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (EGD-DDR-001 v0.1): nine items decided by Amish (D1 to D9) and five left open (O1 to O5).
- `docs/04-calcs/01-sizing.md` (EGD-CAL-001 v0.1) with `docs/04-calcs/sizing.py` and `results.csv`: viewing geometry, radiometry, line fill, pressure, water, a droplet drift screening model, energy, pump power options (b) and (c), mast wind load, enclosure temperature, cost, and a status for every requirement. The script imports the model and reads the BOM and budget.
- `cad/src/model.py`: parametric build123d model (house reference, mast, head, sensors, ground unit, valves, spray lines) exporting `cad/step/` and `cad/stl/` files for the kit assembly, mast assembly, sensor head, ground unit and reference house.
- `cad/src/sheets.py` and `cad/drawings/EGD-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, 1:100 with 1:25 details of the mast and ground unit, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". The concept sheet stays EGD-DWG-010.
- `bom/bom.csv`: 17 priced kit lines with supplier types (item 17, mast earthing kit, added) and one priced option row; `bom/bom-notes.md` updated.
- `cad/src/concept_media.py` now builds from the parametric model; all media in `media/` re-rendered and checked; no `media/_views*` folders remain.
- EGD-PRB-001, EGD-PRC-001 and EGD-REQ-001 raised to v0.3; `README.md` and `project.yaml` (`trl: 3`, `trl_target: 3`, `budget_usd: 425`, evidence list) updated. Pitch and problem lines unchanged (no rewording was recommended).

### Requirement status (EGD-CAL-001, Table 2)

Five not met, two at risk, one not verifiable at TRL 3, five met.

| ID | Status | Value |
| --- | --- | --- |
| R1 smouldering spot | **Not met** | Gutter interiors hidden; flat 100 cm² spot 2.8 K at 8.2 m against a 5 K trigger; a 100 x 50 mm hot debris face is seen to 26 m |
| R2 single ember | **Not met** | 600 °C ember 2.4 K at 8 m; reaches 5 K within 5.5 m |
| R3 watch both gutters | **Not met** | Roof edges in view 1.25 to 13.15 m from the mast; gutter interiors not visible from 228 mm above the ridge |
| R6 net wetting | **Not met** | Leeward eave 0.8 mm/h at 30 km/h (2.6 mm/h at half that); windward 7.4 mm/h; target 5 mm/h |
| R13 cost | **Not met** | $571 against $425 |
| R8 kit battery | At risk | 61.0 Wh needed; 69.1 Wh usable at 25 °C, 62.2 Wh at 0 °C, 55.3 Wh at end of life |
| R10 fire weather | At risk | Mast 27 MPa (factor 8.9), standoffs factor 3.5; enclosure about 71 °C in sun at 60 °C ambient |
| R11 installation | Not verifiable at TRL 3 | Install time not estimated |
| R4, R5, R7, R9, R12 | Met | Water at the farthest head in 55 s; 4 L/min and 965 L per event |

TRL 2 figures corrected in all documents: gutter coverage (now none), ember signal (2.4 K, not about 3 K), line lengths (17.7 and 21.3 m), water (965 L), net wetting, energy (61.0 Wh, not 64 Wh), mast stress (27 MPa) and cost ($571, not about $420).

### Decisions recorded (EGD-DDR-001)

Decided by Amish, 2026-09-25, going with each recommendation: D1 budget raised to $425; D2 two MLX90640 thermal arrays; D3 gable-end mast at the ridge line; D4 metal eave runs if the budget allows (it does not, so they are a $110 priced option); D5 tank with its own pump first; D6 pump power out of the kit's scope, with options (b) and (c) studied (R8 redefined); D7 adjustable arming defaults reviewed with a fire agency; D8 fail to wet on sensor loss; D9 normally closed valves.

### Still awaiting Amish

- **O1** First co-design partner (no recommendation; to be picked per area later).
- **O2** Cost: $571 against $425. Recommendation: raise the budget to about $575 until O3 and O4 are resolved.
- **O3** Gutters hidden from the head. Recommendation: study two corner sensor pods looking along each gutter.
- **O4** Leeward-eave wetting. Recommendation: run only the leeward zone, chosen from the wind vane.
- **O5** A 2 K ember trigger (meets R2 for a centred ember) and a 10 Ah battery (about $13, clears R8). Recommendation: adopt both.

### Safety concerns

- The gutter blind spot makes false reassurance worse: EmberGuard cannot see the place where embers most often lodge. The precis safety section now says so.
- Battery temperature: a dark steel enclosure in sun at 60 °C ambient reaches about 71 °C, above the LiFePO4 rating. The BOM specifies a light finish; a sun shade is not designed.
- Wall anchors carry about 710 N each at 120 km/h and must be checked for each wall; mast earthing (item 17) is now in the BOM.
- Work at height, the 12 V only rule with a dry contact to the pump, hydrant pressure and evacuation notes are unchanged.

### Citations

Checked on 2026-09-25 with web search and DOI records: Caton et al. 2017, Hakes et al. 2017, Syphard and Keeley 2019, NIST TN 1635 and NIST TN 2135 (titles, authors, years match). Manzello et al. 2020, Mitchell (2006, *Fire Safety Journal* 41, now linked), AS 5414-2012 (now linked) and the MLX90640 datasheet (18 mA typical, NETD 0.1 K at 1 Hz, used in EGD-CAL-001) were found by title. Not re-checked: the CAL FIRE, CPUC, NFPA and Frontline home pages and the NFPA 1140 statement.

### TRL 4 material

None found. `build-log/README.md` is the scaffold file and was not changed. No test, build or firmware work was started.

### Recommended next step

TRL 4 is on hold by Amish's instruction. The next step is a decision on O2 to O5, then a second TRL 3 revision (still TRL 3) that models the corner sensor pods or another fix for the gutter blind spot, re-runs EGD-CAL-001, and re-prices the kit. For reference only, TRL 4 would need: a heated-target and ember trial with the chosen sensor, recorded thermal video for false-trigger rates, a spray trial in wind on a roof-edge mock-up, a battery and enclosure heat test, a TST report with `environment: lab`, and build-log entries.
