# BOM notes

Prices are TRL 3 estimates (2026-09-25) from supplier types, not quotes from named suppliers. Line numbers match the callouts in `media/exploded.png` and Table 1 of EGD-PRC-001. Quantities and lengths follow `cad/src/model.py`.

- Kit parts total $605.00 (17 lines), against the $575 budget Amish set on 2026-09-25 when he accepted the TRL 3 recommendations (EGD-DDR-002, O2). R13 is not met, by 5 %; options are in EGD-DDR-002, N1. The total is computed by `docs/04-calcs/sizing.py` (EGD-CAL-001 v0.2, G1).
- Changes from the first TRL 3 BOM ($571): the ridge-line sensor head (item 2, $45) is replaced by two gutter-corner sensor pods ($56, EGD-DDR-002, O3); item 13 adds two pod cables ($20 to $30); the battery (item 8) goes from 6 Ah to 10 Ah ($32 to $45, O5).
- The TRL 2 indicative total was about $420. Most lines were underpriced at TRL 2 (thermal sensors, enclosures, siren and switch); item 17, a mast earthing kit, was added for the lightning safety note.
- The "Option" row (metal eave runs, $110) is priced but not in the kit total. Under D4 metal eave runs were chosen if the budget allowed; it does not.
- Not included: the water source (tank), the pump and its power supply (out of scope, D6), the supply hose, gutter guards, tools and installation labour. A SwapCell pack for pump option (c) would be priced once in SwapCell and excluded from this kit.
