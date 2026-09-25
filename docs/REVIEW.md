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
