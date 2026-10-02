---
doc_id: EGD-PRB-001
title: EmberGuard problem statement
project: EmberGuard
doc_type: Problem statement
version: "0.6"
status: Draft
date: '2026-10-02'
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
  change: Populate to TRL 2 (problem, users, context, constraints, out of scope, prior work with sources)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3. Budget raised to $425 and tank-first water source decided (EGD-DDR-001); journal sources checked; Mitchell (2006) linked
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). Budget constraint at $575
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish ($605)
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: First co-design partner to approach, decided on 2026-10-02 (EGD-DEC-001)
---

# EmberGuard problem statement

Wildfire embers ignite homes well ahead of the fire front, often in gutters, on roof edges and in debris near the eaves, while the occupants have evacuated and fire crews are elsewhere. A house that could sense an ember shower and wet its own most vulnerable edges for a few hours, without grid power and without drawing much water, would remove one common ignition path. EmberGuard is a low-cost, open, garage-buildable attempt at that for a single house.

## The problem

Post-fire investigations and reviews agree that most homes lost in wildland-urban interface (WUI) fires are ignited by embers (firebrands) and the small spot fires they start, rather than by direct flame contact from the main fire front ([Caton et al. 2017, Fire Technology](https://doi.org/10.1007/s10694-016-0589-z); [Maranghides and Mell 2009, NIST TN 1635](https://doi.org/10.6028/NIST.TN.1635)). Embers are lofted by wind and can land a kilometre or more ahead of the flame front ([Manzello et al. 2020, Progress in Energy and Combustion Science](https://doi.org/10.1016/j.pecs.2019.100801)). They collect where wind eddies drop them: in gutters full of dry leaves and needles, at the roof-to-wall junction, in corners and against vents. Fire-safety guidance for homeowners therefore stresses clean gutters, ember-resistant vents and a non-combustible zone next to the house ([CAL FIRE, Ready for Wildfire](https://readyforwildfire.org)). Structure loss in recent California fires correlates strongly with local factors near the house and with wind-driven events ([Syphard and Keeley 2019, Fire](https://doi.org/10.3390/fire2030049)).

Three gaps remain for an ordinary household:

- **Timing.** Ember showers can arrive hours before the flame front and continue after it passes, often at night, when no one is home. Gutter debris that was clean in spring may be full again by autumn.
- **Power and water.** Fires coincide with high wind and grid shutoffs. Utilities de-energize lines in fire weather ([CPUC, Public Safety Power Shutoffs](https://www.cpuc.ca.gov/psps)), so anything that needs mains power may be dead when it is needed. Municipal water pressure can also drop when many houses and fire crews draw at once, which is why fire agencies advise evacuees not to leave sprinklers running ([CAL FIRE, Ready for Wildfire](https://readyforwildfire.org)).
- **Cost and control.** Commercial exterior sprinkler systems exist, some with remote activation and foam or retardant (for example [Frontline Wildfire Defense](https://www.frontlinewildfire.com)), but they are priced for high-value homes, closed and cloud-dependent. Timer-based or manually started roof sprinklers waste water for hours before and after the embers arrive, or never start because no one is there.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Homeowner in a WUI area | Automatic protection of gutters and roof edges during ember attack while evacuated; low cost; runs through a power cut | Single-storey or two-storey house, pitched roof with gutters; seasonal fire weather with strong dry winds |
| Renter or low-income household | A removable kit that needs no roof penetration and no mains wiring | Cannot modify the building; limited budget |
| Rural property with a tank | Uses a limited stored supply (1,000 to 5,000 L) as efficiently as possible | Well or rainwater tank; pump on its own supply or a generator |
| Community wildfire group (Firewise-style) | An open design that neighbours can build, audit and maintain together; data on ember arrival | Neighbourhood preparedness programs, maker spaces |
| Fire service and researchers | Systems that do not rob hydrant pressure; logged ember arrival times and wind data after a fire | Post-fire investigations, WUI research |

## Constraints

- Garage-buildable prototype; the budget in `project.yaml` is $605 USD for kit parts, raised from $300 to $425 (EGD-DDR-001, D1) and then to $575 (EGD-DDR-002, O2) by Amish on 2026-09-25, and to $605 on 2026-09-26 to cover the revised priced BOM of $605 (EGD-CAL-001 v0.3, section G).
- Low-voltage only on the house (12 V DC nominal). No mains wiring by the homeowner; a mains pump is switched only through its own certified controls by a dry contact.
- Must work through a grid outage of at least three days with the system armed.
- Water draw small enough for a household tank or a domestic mains connection, well below the demand of a garden hose on full, so that it does not compete with fire-fighting supply.
- No roof penetrations: mast, cable and spray lines attach with clamps and brackets to walls, fascia and gutter lips.
- Must tolerate what arrives before the fire front: wind to about 120 km/h (75 mph) in gusts, smoke, ash, low humidity, radiant heat and ember impact. Survival once the flame front reaches the house is not required, but the electronics should fail to a safe state.
- Build from off-the-shelf parts: thermal array sensors, a weather-station anemometer, a common microcontroller, irrigation solenoid valves and micro-sprinklers.

## Out of scope

- Fighting the main fire front, direct flame contact or crown fire. EmberGuard wets edges against embers; it is not a fire-suppression system.
- Whole-roof or whole-property deluge systems, foam or retardant injection.
- Replacing evacuation, home hardening (ember-resistant vents, Class A roofing, gutter guards, defensible space) or professional fire protection.
- Certified detection for life safety. EmberGuard is not a smoke alarm or a listed fire detector.
- Design of the water source, tank or pump, and power for the pump in an outage (decided, EGD-DDR-001, D6). EmberGuard interfaces to an existing supply; the first design case is a tank with its own pump (D5).

## Prior work

- **Ember science.** Firebrand generation, transport and ignition of fuel beds are reviewed by [Manzello et al. 2020](https://doi.org/10.1016/j.pecs.2019.100801) and, for buildings, by [Caton et al. 2017](https://doi.org/10.1007/s10694-016-0589-z) and its companion on building components ([Hakes et al. 2017, Fire Technology](https://doi.org/10.1007/s10694-016-0601-7)). NIST case studies of the 2007 Witch Creek and Guejito fires and the 2018 Camp Fire document ember-driven ignitions and fire timelines ([NIST TN 1635](https://doi.org/10.6028/NIST.TN.1635); [NIST TN 2135](https://doi.org/10.6028/NIST.TN.2135)).
- **Exterior sprinklers.** Wind-driven wetting of a structure against embers was analysed by Mitchell ([2006, "Wind-enabled ember dousing," *Fire Safety Journal* 41](https://www.sciencedirect.com/science/article/abs/pii/S0379711206000567)), which argues that modest, well-placed water can be effective when it reaches the surfaces where embers land. Australia has a standard for bushfire water spray systems ([Standards Australia AS 5414-2012, *Bushfire water spray systems*](https://webstore.ansi.org/standards/sai/54142012)). Commercial systems such as [Frontline Wildfire Defense](https://www.frontlinewildfire.com) offer remote-activated roof and perimeter sprinklers.
- **Guidance and standards.** [NFPA 1140](https://www.nfpa.org) (Standard for Wildland Fire Protection, which absorbed NFPA 1144) covers structure ignition hazards in the WUI. California Building Code Chapter 7A sets WUI construction rules including ember-resistant vents. [CAL FIRE's Ready for Wildfire](https://readyforwildfire.org) gives homeowner hardening and evacuation advice.
- **Sensing.** Low-cost thermal array sensors such as the [Melexis MLX90640](https://www.melexis.com/en/product/MLX90640/) (32 x 24 pixels, 55 or 110 degree field of view) make continuous thermal watching of a roof edge affordable. Weather-station cup anemometers and vanes are cheap and robust.

No open, low-cost design was found that combines ember-specific sensing, wind and humidity arming, low water use and outage-proof operation. On 2026-09-25 the titles, authors and years of Caton et al. 2017, Hakes et al. 2017, Syphard and Keeley 2019, NIST TN 1635 and NIST TN 2135 were checked against their DOI records, and Manzello et al. 2020, Mitchell (2006), AS 5414-2012 and the MLX90640 datasheet were found by title; the agency and company home pages and NFPA 1140 were not re-checked (see `docs/REVIEW.md`).

## Open questions

- Which users to involve first, and through which partner: a Firewise-style neighbourhood group, a county fire-safe council or a university WUI research group? Decided by Amish on 2026-10-02: the first candidate to approach is a recognised Firewise USA neighbourhood group in a wildland-urban interface area whose houses have gable ends with timber verges; in Texas, through the Texas A&M Forest Service, which supports such groups. Not yet agreed with any partner (EGD-DDR-001, O1).
- The first target is a house with a tank and its own pump (decided by Amish, 2026-09-25, EGD-DDR-001, D5).
- Would local fire agencies support an automatic system that draws from mains during a fire, given the pressure concern? Needs a conversation before any field trial.
