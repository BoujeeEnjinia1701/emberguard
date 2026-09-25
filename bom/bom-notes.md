# BOM notes

Prices are TRL 3 estimates (2026-09-25) from supplier types, not quotes from named suppliers. Line numbers match the callouts in `media/exploded.png` and Table 1 of EGD-PRC-001. Quantities and lengths follow `cad/src/model.py`.

- Kit parts total $571.00 (17 lines), against the $425 budget Amish set on 2026-09-25 (EGD-DDR-001, D1). R13 is not met; options are in EGD-DDR-001, O2. The total is computed by `docs/04-calcs/sizing.py` (EGD-CAL-001, G1).
- The TRL 2 indicative total was about $420. Most lines were underpriced at TRL 2 (thermal sensors, enclosures, siren and switch); item 17, a mast earthing kit, was added for the lightning safety note.
- The "Option" row (metal eave runs, $110) is priced but not in the kit total. Under D4 metal eave runs were chosen if the budget allowed; it does not.
- Not included: the water source (tank), the pump and its power supply (out of scope, D6), the supply hose, tools and installation labour. A SwapCell pack for pump option (c) would be priced once in SwapCell and excluded from this kit.
