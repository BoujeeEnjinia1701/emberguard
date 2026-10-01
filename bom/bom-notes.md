# BOM notes

Prices are TRL 3 estimates (2026-09-25) from supplier types, not quotes from named suppliers. Line numbers match the callouts in `media/exploded.png` and Table 1 of EGD-PRC-001. Quantities and lengths follow `cad/src/model.py`.

- Kit parts total $689.00 (17 lines), against the $605 budget Amish approved on 2026-09-26 (EGD-DDR-002). R13 is not met, 14 % over; whether to raise the budget is open for Amish (EGD-DEC-001, item 2). The total is computed by `docs/04-calcs/sizing.py` (EGD-CAL-001 v0.4, G1).
- Changes for construction (EGD-DDR-003, 2026-10-01): line 1 adds slip-on flanges, aluminium wall plates, crossover plates and U-bolts ($48 to $80); line 2 adds the verge cleat, bent arm, pod plate and lens hood to each pod ($28 to $37 each); line 9 adds a pole-mount tilt bracket ($32 to $38); line 13 has longer pod cables and a valve cable ($30 to $33); line 16 adds the valve board, pipe clips, saddle and fascia clips, four M20 glands and the battery strap ($25 to $50). Lines 7 and 14 are respecified at the same price.
- Changes from the first TRL 3 BOM ($571): the ridge-line sensor head (item 2, $45) is replaced by two gutter-corner sensor pods ($56, EGD-DDR-002, O3); item 13 adds two pod cables ($20 to $30); the battery (item 8) goes from 6 Ah to 10 Ah ($32 to $45, O5).
- The TRL 2 indicative total was about $420. Most lines were underpriced at TRL 2 (thermal sensors, enclosures, siren and switch); item 17, a mast earthing kit, was added for the lightning safety note.
- The "Option" row (metal eave runs, $110) is priced but not in the kit total. Under D4 metal eave runs were chosen if the budget allowed; it does not.
- Not included: the water source (tank), the pump and its power supply (out of scope, D6), the supply hose, gutter guards, tools and installation labour. A SwapCell pack for pump option (c) would be priced once in SwapCell and excluded from this kit.
