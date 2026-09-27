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

Status update: items 1 to 9 were decided by Amish, 2026-09-25: go with recommendation (EGD-DDR-001, D1 to D9). Item 10 had no recommendation and stays proposed, awaiting Amish.

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
- **O2** Cost: $571 against $425. Recommendation: raise the budget to about $575 until O3 and O4 are resolved. Decided by Amish, 2026-09-25: go with recommendation (EGD-DDR-002).
- **O3** Gutters hidden from the head. Recommendation: study two corner sensor pods looking along each gutter. Decided by Amish, 2026-09-25: go with recommendation (EGD-DDR-002).
- **O4** Leeward-eave wetting. Recommendation: run only the leeward zone, chosen from the wind vane. Decided by Amish, 2026-09-25: go with recommendation (EGD-DDR-002).
- **O5** A 2 K ember trigger (meets R2 for a centred ember) and a 10 Ah battery (about $13, clears R8). Recommendation: adopt both. Decided by Amish, 2026-09-25: go with recommendation (EGD-DDR-002).

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

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25: "i accept all your recommendations, go with them across all repos." Every open item with a recommendation is now decided in favour of it and recorded in `docs/decisions/0002-recommendations-accepted.md` (EGD-DDR-002 v0.1). EmberGuard stays at `trl: 3`, `trl_target: 3`.

### Decisions applied and what changed

| Item | Decision | Before | After |
| --- | --- | --- | --- |
| O2 Budget | Raise `budget_usd` | $425 | $575 (kit now $605, R13 still not met, 5 % over) |
| O3 Gutter blind spot | Thermal sensors in two gutter-corner pods, 200 mm beyond each gutter end and 500 mm above the lip, looking along the gutter | Ridge-line head saw gutter debris at 0 of 130 stations | Open gutter in view 1.25 to 12.95 m at 118 of 130 stations; R3 met |
| O4 Leeward wetting | Leeward zone only above 2 m/s cross-eave wind | Leeward eave 0.8 mm/h at 8.3 m/s, 2.6 mm/h at 4.2 m/s | 1.5 mm/h and 5.1 mm/h; windward eave dry until a windward detection; R6 still not met |
| O5 Trigger | Persistent-spot trigger lowered | 5 K; 600 °C ember detected to 5.5 m | 2 K; 8.8 m centred, 4.4 m on a pixel corner; R2 at risk |
| O5 Battery | 12.8 V LiFePO4 pack enlarged | 6 Ah, 55.3 Wh usable at end of life against 61.0 Wh | 10 Ah, 92.2 Wh against 67.5 Wh; R8 met |

Files changed: `project.yaml` (`budget_usd` 575); `README.md` (budget, concept, key components, and new sections "Concept rationale", "Burning platform", "Where it could be used" and "What sparked the idea"); EGD-PRB-001 v0.4, EGD-PRC-001 v0.4, EGD-REQ-001 v0.4, EGD-CAL-001 v0.2, EGD-DDR-001 v0.2, new EGD-DDR-002 v0.1; `bom/bom.csv` (items 2, 3, 8, 13; total $571 to $605) and `bom/bom-notes.md`; `cad/src/model.py` (pods replace the head; 10 Ah battery; pod cables) with STEP and STL re-exported (`sensor-head` replaced by `sensor-pod`); `docs/04-calcs/sizing.py` (section A rewritten with gutter end cap and hanger-strap checks; 2 K trigger; leeward-only rule; pod-node energy; mast without head) and `results.csv`; `cad/src/sheets.py` and EGD-DWG-001 at Rev P2; `cad/src/concept_media.py` and all of `media/` re-rendered (hero, blueprint, exploded view with the front pod, flow diagram for the leeward-only case); PDFs in `docs/pdf/` rebuilt. The old ridge-line head is withdrawn from all current documents.

### Requirement status (EGD-CAL-001 v0.2)

Two not met, three at risk, one not verifiable at TRL 3, seven met (was five not met, two at risk, five met).

| ID | Status | Value |
| --- | --- | --- |
| R6 wetting | **Not met** | Leeward eave 1.5 mm/h at 8.3 m/s, 5.1 mm/h at 4.2 m/s; target 5 mm/h |
| R13 cost | **Not met** | $605 against $575 |
| R1 smouldering spot | At risk | Hot debris face seen to 41 m; flat spot to 12.1 m; hanger straps hide debris 42 mm below the lip at 83 of 118 stations, all beyond 7.8 m |
| R2 single ember | At risk | 8.8 m centred, 4.4 m on a pixel corner; 2 K false-trigger rate unknown |
| R10 fire weather | At risk | Enclosure about 71 °C in sun at 60 °C ambient; pods exposed at the gutters; mast 14 MPa (factor 16.6) |
| R11 installation | Not verifiable at TRL 3 | Install time not estimated |
| R3, R4, R5, R7, R8, R9, R12 | Met | Gutters in view; 55 s to water; 965 L per event; 115 Wh usable against 67.5 Wh |

### Still awaiting Amish

- **O1** First co-design partner (no recommendation; to be picked per area later).
- **N1** Cost of the revised kit, $605 against $575. Recommendation: find about $30 of savings (lighter mast, unbranded breakouts), with a budget of about $610 as the fallback. **Decided by Amish, 2026-09-26: budget set to $605 to cover the priced BOM; see "Session 2026-09-26: budget approved".**
- **N2** Leeward wetting at the design wind. Recommendation: study coarser, lower-angle droplets or a second leeward row of heads on paper at the next TRL 3 revision.
- **N3** Hanger-strap shadow. Recommendation: study pods about 1 m above the lip on paper, and list gutter guards as an installation precondition.
- **N4** Pitch wording. The pitch still says "Roof-edge sensor mast". Recommendation: "Gutter-corner thermal sensors and a weather mast that detect ember showers and trigger a gutter and eave sprinkler zone." Pitch unchanged until Amish decides.

### Cross-repo actions

None. Pump option (c) still only studies a SwapCell pack; nothing in EmberGuard's baseline depends on another repo.

### Write-up sections and inspiration

`README.md` now has "Concept rationale", "Burning platform" (UNEP 2022 projections, Radeloff et al. 2018 WUI growth, NIST on the Camp Fire, the Royal Commission on Black Summer), "Where it could be used" (five industries; United States, Canada, Australia, Chile, South Africa and Mediterranean Europe) and "What sparked the idea". The inspiration point is the CSIRO survey of about 1,150 houses after the Ash Wednesday fires of 16 February 1983 (*Ecos* 43, 1985), which found that burning debris lodging in gaps, at ridges and at gutters most often set houses alight, and that people present could save houses by attacking small fires early with a few buckets of water. EGD-PRB-001 needed no change to its account of the idea's origin. All sources were opened on 2026-09-25 except the Radeloff et al. paper, whose figures were checked through a PNNL summary of it; the Chile figure comes from a UN Connecting Business initiative page citing ReliefWeb.

### Safety concerns

- The pods sit at the gutter ends, where embers land and radiant heat is higher; their survival time is unknown. Fail to wet on sensor loss (D8) covers a lost pod.
- Hanger straps hide deep debris far from the pods, so gutters must still be kept clean; the precis safety note now says so.
- In wind the windward eave is not sprayed until a detection on that side.
- Pod brackets hang beyond the gutter ends and must be clamped to sound fascia; their wind load is not yet checked.
- Battery enclosure temperature, work at height, 12 V only, earthing and hydrant pressure notes are unchanged.

### TRL 4

TRL 4 remains on hold by Amish's instruction. Nothing past TRL 3 was started: no trials, thermal video, spray tests, PCB, firmware beyond the arming and spray rules described in the precis, or purchasing.

### Recommended next step

A decision on N1 to N4, then a further TRL 3 revision that studies higher pods and a leeward head arrangement on paper, checks the pod brackets for wind, and re-prices the kit.


## Session 2026-09-26: sources strengthened

- "Where it could be used", country table: the uncited "Mediterranean Europe" row is replaced by "Greece (Mediterranean Europe)", citing the European Parliament motion for a resolution B8-0391/2018 on the July 2018 Mati fire (at least 98 dead; thousands of houses and vehicles destroyed), with NOAA Climate.gov's event report alongside. Old source: none. Both links were opened on 2026-09-26.
- All other rows, "Concept rationale", "Burning platform" and "What sparked the idea" already rested on primary or reputable secondary sources and are unchanged. No budget change. No controlled doc changed.

## Session 2026-09-26: budget approved

Amish wrote, in chat on 2026-09-26: "i approve all the budget items." N1 is decided: budget set to $605 to cover the priced BOM (EGD-DDR-002 v0.2).

- `project.yaml` `budget_usd` $575 to $605; README budget and cost lines updated.
- R13 target $575 to $605; status **not met to met**, with no margin ($605 kit; the $110 metal eave option stays outside the kit).
- Requirement counts (EGD-CAL-001 v0.3): one not met (R6), three at risk, one not verifiable, eight met.
- Documents: EGD-PRB-001 v0.5, EGD-PRC-001 v0.5, EGD-REQ-001 v0.5, EGD-CAL-001 v0.3 (script re-run, `results.csv` regenerated), EGD-DDR-002 v0.2; `bom/bom-notes.md`; blueprint key figure in `cad/src/concept_media.py` and `media/` regenerated; PDFs rebuilt.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26.

### What was done

- `cad/src/product_model.py` (new): `product_parts()` returns 78 parts, each with a colour, a render material, a BOM line, a group and an explode offset, plus `TITLE` and `RENDER_VIEWS` (hero, exploded and a sensor pod detail view). It imports `PARAMS`, `derived()`, `sensor_axes()` and `house_parts()` from `model.py`; every size, the pod position and aim, the gutter and spray-line geometry and every interface come from them. Parts by group: shell 16 (the front sensor pod, its thermal sensor, hood and bracket), internal 2 (pod node board and chips), accessory 55 (mast and weather head, humidity shield, solar panel, ground unit and contents, valves, spray line, cables) and context 5. The mast and the rest of the kit are in the accessory group so that the detail view (shell and internal) shows the pod alone.
- It adds, as appearance detail only:
  - Sensor pod (items 2 and 3): filleted die-cast body with side ribs and a lens bezel, a back cover on a parting line with four screws, a lit green status light, a label with an accent band, the stainless hood as a bent sheet with drip flanges on four spacers, the black sensor snout with a dark germanium lens along the `sensor_axes()` aim, a cable gland, the post and arm with a filleted gutter-end clamp and two bolts.
  - Weather head and mast (items 1, 4, 5 and 9): mast-top adapter, stub, tee and crossarm; three-cup anemometer with hemispherical cups; wind vane with a shaped tail fin, nose weight and accent; mast end cap; galvanized standoffs with filleted wall plates, pipe flanges, four anchors each and split clamp collars with bolts; five-plate radiation shield on three rods with its probe and arm; solar panel with an aluminium frame, dark cells, busbars, junction box, arm and clamp.
  - Ground unit (items 6, 7, 8, 12 and 15): light grey steel body and door with a seam, hinges, four screws, a teal name plate and a warning label; key switch, piezo siren and a lit green status beacon; four bottom cable glands; controller board, battery with label and relay inside.
  - Valves and transducer (items 10 and 11) on a brass manifold; black polyethylene spray line (item 14) on the gutter lip with three lip clips, a micro-sprinkler head with a teal spinner cap and the riser elbow; mast cable and pod cable (item 13) with cable ties and the silicone heat sleeve at the pod.
  - Context (grey, no BOM number): a compact corner of the reference house at the east end of the front eave, with lap-siding lines, the roof overhang with shingle courses, the fascia, the gutter with an end cap and two hangers.
- `README.md`: hero image now `media/render-hero.png`; exploded render link added. The renders themselves are produced later by the orchestrator.
- Self-check previews (matplotlib) were reviewed for the hero, exploded and detail views.

### Differences from model.py (Proposed, awaiting Amish)

1. **Render layout.** For a compact product render the mast and everything on it is drawn at y = -3.60 m (installed on the ridge line, y = 0) and 1.15 m lower, so that both standoffs still meet the gable wall below the roof next to the front gutter corner; its 700 mm offset from the wall, its length and every height on it relative to the mast are unchanged. The ground unit is drawn at y = -3.33 m (installed -1.80 m) at its `model.py` height, the valve manifold just below it at 0.79 m (installed 0.45 m) and 120 mm in from the riser line, and only the east 0.9 m of the front spray line and the top 420 mm of its riser are shown. The front pod, gutter corner and spray line are at their `model.py` positions. Recommendation: accept as a render-only layout and say so in figure captions ("not the installed spacing").
2. **Sensor aim.** `model.py` draws the lens barrel along -X; the appearance model draws the snout along the `sensor_axes()` aim (10 degrees toward the house, 5 degrees down), which is the decided aim. Recommendation: draw the barrel on the aim in `model.py` at the next model session.
3. **Hood.** `model.py` shows the hood as a 6 mm slab on the pod top; the appearance model shows the BOM's bent 0.8 mm class stainless sheet (drawn 1.5 mm) with drip flanges on four spacers, inside the same 150 x 130 mm envelope, leaving an air gap as a heat shield. Recommendation: adopt the spaced hood in `model.py` and EGD-DWG-001.
4. **Enclosure colour and door.** `model.py` colours the ground enclosure dark teal; the appearance model uses the light grey finish the BOM and EGD-CAL-001 section F call for (R10), with a hinged door on the +X face. Recommendation: change the `model.py` colour to light grey at the next media refresh.
5. **Spray line colour.** `model.py` draws the spray line blue for legibility; the appearance model shows black UV-stable polyethylene, as bought. Recommendation: keep `model.py` as it is.
6. **Cable routes.** The mast and pod cables are drawn along the mast, under the lower standoff, down the house corner and into bottom glands on the ground unit, following the render layout. Recommendation: accept as appearance only; installers set the real routes.

### Scope

This is an appearance model only: no tolerances, no fabrication detail, no PCB layout. `trl` stays 3 and TRL 4 remains on hold. No BOM, model, drawing or document other than `README.md` and this note was changed.
