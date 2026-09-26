"""EmberGuard concept media (refreshed at TRL 3 from the parametric model).

Run from the repo root:  python cad/src/concept_media.py
Geometry comes from cad/src/model.py (PARAMS, build_parts, house_parts); only the water tank,
pump and indicative spray envelopes are added here. CONCEPT, NOT FOR FABRICATION.

Coordinates in mm. Reference house: single-storey, 12 x 8 m footprint, 2.7 m walls, gable roof
at 22 degrees with the ridge along X and 500 mm overhangs. Gutters run along both long eaves
(front at -Y, back at +Y). The weather mast stands off the east gable end (+X) at the ridge line;
the two thermal sensor pods sit beyond the east ends of the gutters, looking west along them.
The house, water tank and pump are grey context with no BOM number; kit parts are colored.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
from build123d import Box, Cylinder, Sphere, Cone, Pos, Rot, Solid, Plane, Vector
import concept
from concept import Part, render_all, _render

# ---------------- geometry from the parametric model (cad/src/model.py) ----------------
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived, build_parts, house_parts, tube as tube3, path  # noqa: E402

DV = derived(P)
L, D, H = P["house_l"], P["house_d"], P["wall_h"]
LIP_Y, LINE_Z = DV["lip_y"], DV["line_z"]
MX, MY = DV["mast_x"], 0.0
GREY_WALL = "#D6D3D1"
GREY_ROOF = "#78716C"
GREY_CTX = "#A8A29E"
hp = house_parts(P)
house, roof = hp["walls"], hp["roof"]
fg = hp["fascia_gutters"]

# ---------------- water supply (context, homeowner) ----------------
TANK_C = (8700.0, 2800.0)
tank = Pos(TANK_C[0], TANK_C[1], 580) * Box(1200, 1000, 1160)
pump = Pos(7850, 2800, 150) * Box(300, 220, 260)
hose = path([(7700, 2800, 120), (6700, 2800, 120), (6700, -1800, 120), (DV["riser_xpos"], -1800, P["manifold_z"])], 12)

# ---------------- kit parts ----------------
KP = build_parts(P)
heads = [(hx, -LIP_Y, LINE_Z + 65, -1) for hx in DV["head_x"]]

# spray envelopes (indicative only): cones from each front head toward the roof edge
spray = None
for hx, hy, hz, s in heads:
    c = Pos(hx, hy, hz) * Rot(s * 35, 0, 0) * Pos(0, 0, 140) * Cone(10, 200, 280)
    spray = c if spray is None else spray + c

TEAL = "#0F766E"
# Water supply is shown in the hero only, so the orthographic views stay at 1:100 on the sheet
supply = [
    Part("Water tank, 1,000 L (homeowner supply, not in kit)", tank, "#E7E5E4", None),
    Part("Pump (homeowner, not in kit)", pump + hose, GREY_CTX, None),
]
context = [
    Part("House walls (context)", house, GREY_WALL, None),
    Part("Roof (context)", roof, GREY_ROOF, None),
    Part("Fascia and gutters (existing)", fg, "#57534E", None),
    Part("Spray envelope, front zone (indicative)", spray, "#93C5FD", None),
]

ORDER = ("mast", "pods", "sensors", "anem", "trh", "board", "enclosure", "battery", "panel", "valves", "xducer",
         "relay", "cable", "lines", "siren")
kit = [Part(KP[k][0], KP[k][1], KP[k][3], KP[k][2]) for k in ORDER]

import os
outs = {} if os.environ.get("EGD_DETAIL_ONLY") else render_all(
    context + kit, project="EmberGuard", title="Ember watch mast and eave spray concept", dwg_no="EGD-DWG-010",
    key_figures=["Two 32 x 24 px thermal arrays in gutter-corner pods look along each gutter",
                 "Open gutter in view 1.25 to 12.95 m; hanger straps hide deep debris beyond 7.8 m",
                 "Leeward zone only in wind: 4 L/min steady draw",
                 "About 965 L per 4 h ember event",
                 "67.5 Wh needed against 115 Wh usable (10 Ah battery)",
                 "Kit parts $605 against a $575 budget (TRL 3 estimate)"],
    date="2026-09-25",
    cut=False, context=supply,
    # EGD-CAL-001 v0.2 C5, C7 and C10: 965 L per event; at the 8.3 m/s design cross-wind the leeward-only rule runs
    # the leeward zone continuously and the screening model puts 10 % of its spray on the strip
    flow={"title": "water per 4 h ember event, litres (all values are estimates; leeward zone only, 8.3 m/s cross-wind)",
          "unit": "L",
          "stages": [("Tank or mains", 965), ("Leeward valve", 965), ("6 leeward heads", 960),
                     ("Lands on edge strip", 96), ("Wets edge fuels", 67)],
          "losses": [(1, "Line fill", 5), (2, "Wind drift (model)", 864), (3, "Runoff (guess)", 29)]},
)

# ---------------- custom detail views ----------------
# render_all draws the whole house; these views zoom in where the kit is small against the house.
import shutil
from concept import human_figure
MEDIA = ROOT / "media"

# Hero: re-rendered from a viewpoint nearer the east gable so the mast and ground unit read clearly.
# The scale figure stands in front of the front wall, clear of the mast, tank and spray lines.
fig = human_figure(1750.0, x=2500.0, y=-6200.0, z=0.0)
_render(context + supply + kit + [fig], MEDIA / "hero.png", elev=20, azim=-38, title="EmberGuard",
        note="Grey figure: 1.75 m person for scale. Grey house, tank and pump are context, not part of the kit.")

# Cutaway: a 300 mm slice through the front eave at the easternmost spray head (x = 5,500 mm), looking west.
# Shows how the spray line sits on the gutter lip and wets the gutter, fascia and first metre of roof.
slice_box = Pos(5500, -4250, 2550) * Box(300, 1500, 1300)
cut_parts = []
for p in context + kit:
    if p.name.startswith(("Water tank", "Pump")):
        continue
    try:
        s = p.shape & slice_box
    except Exception:
        continue
    if s is not None and s.volume > 1:
        cut_parts.append(Part(p.name, s, p.color, p.bom))
_render(cut_parts, MEDIA / "cutaway.png", elev=8, azim=-14, title="EmberGuard: cutaway through the front eave",
        note="Section at the east spray head (x = 5.5 m), looking west: wall, roof overhang, fascia, gutter, "
             "spray line (14) and indicative spray envelope (blue).")

# Exploded view: the mast-top assembly, with the ground unit and a 1.4 m sample of spray line
# moved up beside it so every numbered part is legible. Numbers match bom/bom.csv.
upper = Pos(MX, MY, 4000) * Box(2000, 2000, 1700)      # keeps the mast above z = 3,150 mm
pod_box = Pos(DV["pod_x"], -DV["gut_yc"], DV["pod_z"]) * Box(500, 400, 700)   # front pod and its sensor only
p_shift = (-900, DV["gut_yc"] - 700, 4300 - DV["pod_z"])  # front pod moved beside the mast top
g_shift = (0, -1100, 2400)                              # ground unit moved beside the mast top
l_sample = Pos(5100, -LIP_Y, LINE_Z + 40) * Box(1400, 200, 250)
l_shift = (1300, LIP_Y - 1500, 900)
EX = {1: (0, 0, 0), 2: (0, 0, 0), 3: (-350, 0, 0), 4: (0, 0, 560), 5: (330, 0, 0), 9: (0, -250, 0),
      13: (220, 0, 0), 7: (0, 0, 0), 6: (0, -420, 120), 12: (0, -420, 380), 8: (0, -420, -220),
      15: (0, 0, 280), 10: (0, 0, -200), 11: (250, 0, -80), 14: (0, 0, 0)}
ex_parts = []
for p in kit:
    s = p.shape
    if p.bom in (1, 13):
        s = s & upper
    elif p.bom in (2, 3):
        s = Pos(*p_shift) * (s & pod_box)
    elif p.bom in (6, 7, 8, 12, 15, 10, 11):
        s = Pos(*g_shift) * s
    elif p.bom == 14:
        s = Pos(*l_shift) * (s & l_sample)
    ex_parts.append(Part(p.name, s, p.color, p.bom, EX[p.bom]))
_render(ex_parts, MEDIA / "exploded.png", offsets=True, labels=True, elev=18, azim=-35,
        title="EmberGuard: exploded view", size=(9, 7),
        note="Numbers match bom/bom.csv. Front pod, ground unit and a spray-line sample drawn beside the mast, "
             "not in installed positions. Item 16 not shown.")

for d in ("_views", "_views_fig"):
    shutil.rmtree(MEDIA / d, ignore_errors=True)
print({k: str(v) for k, v in outs.items()})
