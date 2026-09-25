"""EmberGuard concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; CONCEPT, NOT FOR FABRICATION.

Coordinates in mm. Reference house: single-storey, 12 x 8 m footprint, 2.7 m walls, gable roof
at 22 degrees with the ridge along X and 500 mm overhangs. Gutters run along both long eaves
(front at -Y, back at +Y). The sensor mast stands off the east gable end (+X) at the ridge line.
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

# ---------------- reference house (context) ----------------
L, D, H = 12000.0, 8000.0, 2700.0      # footprint length (X), depth (Y), wall height
PITCH = math.radians(22.0)
OH = 500.0                              # eave and gable overhang
T = math.tan(PITCH)
RIDGE_Z = H + (D / 2) * T               # underside of roof at the ridge, about 4,316 mm
ROOF_T = 200.0
EAVE_Y = D / 2 + OH                     # 4,500 mm
EAVE_Z = H - OH * T                     # roof underside at the eave edge, about 2,498 mm
RL = L + 2 * OH                         # roof and gutter length, 13,000 mm

GREY_WALL = "#D6D3D1"
GREY_ROOF = "#78716C"
GREY_CTX = "#A8A29E"


def tube3(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def path(points, r):
    s = None
    for p, q in zip(points[:-1], points[1:]):
        t = tube3(p, q, r)
        s = t if s is None else s + t
    for p in points[1:-1]:
        s = s + Pos(*p) * Sphere(r)
    return s


walls = Pos(0, 0, H / 2) * Box(L, D, H)
# gable triangles: a block up to the ridge, trimmed by the two roof planes
BIG = 20000.0
gable = Pos(0, 0, H + (RIDGE_Z - H) / 2) * Box(L, D, RIDGE_Z - H)
for s in (-1, 1):
    n = Vector(0, s * math.sin(PITCH), math.cos(PITCH))          # upward normal of this roof plane
    c = Vector(0, s * D / 2, H) + n * (BIG / 2)
    gable = gable - Pos(c.X, c.Y, c.Z) * Rot(-s * math.degrees(PITCH), 0, 0) * Box(L + 10, BIG, BIG)
house = walls + gable

roof = None
slab_len = EAVE_Y / math.cos(PITCH)
for s in (-1, 1):
    yc = s * EAVE_Y / 2
    zu = H + (D / 2 - EAVE_Y / 2) * T
    slab = Pos(0, yc + s * (ROOF_T / 2) * math.sin(PITCH), zu + (ROOF_T / 2) * math.cos(PITCH)) \
        * Rot(-s * math.degrees(PITCH), 0, 0) * Box(RL, slab_len, ROOF_T)
    roof = slab if roof is None else roof + slab

# fascia boards and gutters on both long eaves
GUT_Z0, GUT_H, GUT_W = EAVE_Z - 130, 100.0, 120.0
fascia = None
gutters = None
for s in (-1, 1):
    f = Pos(0, s * (EAVE_Y + 12), EAVE_Z - 60) * Box(RL, 25, 200)
    g = Pos(0, s * (EAVE_Y + 25 + GUT_W / 2), GUT_Z0 + GUT_H / 2) * Box(RL, GUT_W, GUT_H) \
        - Pos(0, s * (EAVE_Y + 25 + GUT_W / 2), GUT_Z0 + GUT_H / 2 + 8) * Box(RL + 10, GUT_W - 8, GUT_H)
    fascia = f if fascia is None else fascia + f
    gutters = g if gutters is None else gutters + g
LIP_Y = EAVE_Y + 25 + GUT_W - 4          # outer gutter lip, about 4,641 mm
LIP_Z = GUT_Z0 + GUT_H                  # top of the lip, about 2,468 mm

# ---------------- water supply (context, homeowner) ----------------
TANK_C = (8700.0, 2800.0)
tank = Pos(TANK_C[0], TANK_C[1], 580) * Box(1200, 1000, 1160)
pump = Pos(7850, 2800, 150) * Box(300, 220, 260)
hose = path([(7700, 2800, 120), (6700, 2800, 120), (6700, -1800, 120), (6280, -1800, 420)], 12)

# ---------------- kit parts ----------------
MX, MY = L / 2 + 700.0, 0.0             # mast axis, 700 mm off the east gable wall at the ridge line
MAST_Z0, MAST_Z1 = 2250.0, 4700.0
HEAD_Z = 4760.0                         # sensor head center

# 1 Mast and two standoff brackets to the gable wall
mast = Pos(MX, MY, (MAST_Z0 + MAST_Z1) / 2) * Cylinder(20, MAST_Z1 - MAST_Z0)
brackets = None
for z in (2450.0, 3900.0):
    b = tube3((L / 2, MY, z), (MX, MY, z), 14) + Pos(L / 2 + 6, MY, z) * Box(12, 140, 140) \
        + Pos(MX, MY, z) * Cylinder(30, 60)
    brackets = b if brackets is None else brackets + b
mast_part = mast + brackets

# 2 Sensor head enclosure: aluminium shell with a sun and heat hood
head = Pos(MX, MY, HEAD_Z) * (Box(160, 240, 120) - Box(140, 220, 100))
hood = Pos(MX, MY, HEAD_Z + 66) * Box(260, 340, 8)
head_part = head + hood

# 3 Two thermal array sensors, each aimed 45 degrees off the house axis toward one gutter, 15 degrees down
sensors = None
for s in (-1, 1):
    y0 = MY + s * 70
    d = Vector(-math.cos(math.radians(15)) * math.cos(math.radians(45)),
               s * math.cos(math.radians(15)) * math.sin(math.radians(45)), -math.sin(math.radians(15)))
    p0 = Vector(MX - 45, y0, HEAD_Z - 10)
    lens = tube3((p0.X, p0.Y, p0.Z), tuple(p0 + d * 70), 14)
    board = Pos(MX - 20, y0, HEAD_Z - 10) * Box(30, 40, 50)
    sensors = lens + board if sensors is None else sensors + lens + board

# 4 Anemometer and wind vane on a crossarm above the head
ARM_Z = 5000.0
anem = tube3((MX, MY, HEAD_Z + 70), (MX, MY, ARM_Z), 10) + tube3((MX, MY - 230, ARM_Z), (MX, MY + 230, ARM_Z), 9)
ax_, ay_ = MX, MY - 230
anem = anem + tube3((ax_, ay_, ARM_Z), (ax_, ay_, ARM_Z + 90), 6) + Pos(ax_, ay_, ARM_Z + 90) * Cylinder(16, 24)
for k in range(3):
    t = math.radians(k * 120 + 20)
    cx, cy = ax_ + 90 * math.cos(t), ay_ + 90 * math.sin(t)
    anem = anem + tube3((ax_, ay_, ARM_Z + 90), (cx, cy, ARM_Z + 90), 3) + Pos(cx, cy, ARM_Z + 90) * Sphere(26)
vx, vy = MX, MY + 230
anem = anem + tube3((vx, vy, ARM_Z), (vx, vy, ARM_Z + 90), 6) + Pos(vx - 80, vy, ARM_Z + 90) * Box(170, 4, 90) \
    + Pos(vx + 80, vy, ARM_Z + 90) * Sphere(14)

# 5 Air temperature and humidity sensor in a stacked-plate radiation shield
trh = None
for k in range(5):
    d = Pos(MX + 90, MY, 3300 + k * 22) * Cylinder(55, 6)
    trh = d if trh is None else trh + d
trh = trh + tube3((MX + 20, MY, 3340), (MX + 90, MY, 3340), 6)

# 9 Solar panel, 10 W, on the mast facing the equator side (-Y here), 45 degree tilt
panel = Pos(MX, MY - 200, 3600) * Rot(-45, 0, 0) * Box(350, 250, 22) + tube3((MX, MY - 20, 3600), (MX, MY - 150, 3600), 10)

# Ground unit on the gable wall
BOX_C = (L / 2 + 85, -1800.0, 1150.0)
# 7 Steel enclosure (closed shell)
enclosure = Pos(*BOX_C) * (Box(160, 320, 400) - Box(140, 300, 380))
# 6 Controller board and 8 battery and 12 relay inside the enclosure
board = Pos(BOX_C[0] - 30, BOX_C[1] - 40, BOX_C[2] + 90) * Box(20, 160, 110)
battery = Pos(BOX_C[0] + 10, BOX_C[1] + 20, BOX_C[2] - 110) * Box(65, 150, 95)
relay = Pos(BOX_C[0] - 30, BOX_C[1] + 100, BOX_C[2] + 90) * Box(25, 50, 60)
# 15 Siren, status light and key switch on the enclosure
siren = Pos(BOX_C[0] + 30, BOX_C[1] - 80, BOX_C[2] + 230) * Cylinder(45, 60) \
    + Pos(BOX_C[0] + 90, BOX_C[1] + 90, BOX_C[2] + 120) * Rot(0, 90, 0) * Cylinder(20, 30)

# 10 Zone valves A and B on a small manifold below the enclosure; 11 pressure transducer
MAN_Z = 450.0
manifold = tube3((L / 2 + 250, -2300, MAN_Z), (L / 2 + 250, -1300, MAN_Z), 14)
valves = manifold
for vy_ in (-2100.0, -1500.0):
    valves = valves + Pos(L / 2 + 250, vy_, MAN_Z) * Box(80, 110, 70) + Pos(L / 2 + 250, vy_, MAN_Z + 60) * Cylinder(24, 60)
xducer = Pos(L / 2 + 250, -1800, MAN_Z + 50) * Cylinder(14, 90) + Pos(L / 2 + 250, -1800, MAN_Z + 105) * Cylinder(18, 20)

# 13 Mast cable: sensor head down the mast to the enclosure
cable = path([(MX + 26, MY, 4650), (MX + 26, MY, 2300), (L / 2 + 120, MY - 400, 2000),
              (BOX_C[0], BOX_C[1], BOX_C[2] + 200)], 6)

# 14 Eave spray lines (both zones), risers and micro-sprinkler heads
HEAD_X = [-5500.0, -3300.0, -1100.0, 1100.0, 3300.0, 5500.0]
LINE_Z = LIP_Z + 30
lines = None
heads = []
for s, vy_ in ((-1, -2100.0), (1, -1500.0)):
    ly = s * LIP_Y
    run = tube3((-RL / 2, ly, LINE_Z), (RL / 2, ly, LINE_Z), 9)
    riser = path([(L / 2 + 250, vy_, MAN_Z), (L / 2 + 250, vy_, 250), (L / 2 + 250, ly, 250),
                  (L / 2 + 250, ly, LINE_Z)], 9)
    zone = run + riser
    for hx in HEAD_X:
        zone = zone + Pos(hx, ly, LINE_Z + 35) * Cylinder(10, 60)
        heads.append((hx, ly, LINE_Z + 65, s))
    lines = zone if lines is None else lines + zone

# spray envelopes (indicative only): cones from each head toward the roof edge
spray = None
for hx, hy, hz, s in [h for h in heads if h[3] < 0]:
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
    Part("Fascia and gutters (existing)", fascia + gutters, "#57534E", None),
    Part("Spray envelope, front zone (indicative)", spray, "#93C5FD", None),
]

kit = [
    Part("Mast and standoff brackets", mast_part, "#94A3B8", 1),
    Part("Sensor head with heat and sun hood", head_part, TEAL, 2),
    Part("Thermal array sensors (2)", sensors, "#C2410C", 3),
    Part("Anemometer and wind vane", anem, "#1F2937", 4),
    Part("Temperature and humidity sensor", trh, "#F5F5F4", 5),
    Part("Controller board", board, "#16A34A", 6),
    Part("Ground enclosure, steel", enclosure, "#115E59", 7),
    Part("Battery, 12.8 V 6 Ah LiFePO4", battery, "#7C3AED", 8),
    Part("Solar panel, 10 W", panel, "#1E3A8A", 9),
    Part("Zone valves A and B with manifold", valves, "#D4A017", 10),
    Part("Pressure transducer", xducer, "#0EA5E9", 11),
    Part("Pump-start relay (dry contact)", relay, "#DB2777", 12),
    Part("Mast cable", cable, "#111827", 13),
    Part("Eave spray lines and heads (2 zones)", lines, "#2563EB", 14),
    Part("Siren, status light and key switch", siren, "#DC2626", 15),
]

import os
outs = {} if os.environ.get("EGD_DETAIL_ONLY") else render_all(
    context + kit, project="EmberGuard", title="Ember watch mast and eave spray concept", dwg_no="EGD-DWG-010",
    key_figures=["Two 32 x 24 px thermal arrays watch both roof planes and gutters",
                 "Arms on wind and humidity; sprays on hot spots (proposed logic)",
                 "Two zones alternate: 4 L/min steady draw (estimate)",
                 "About 960 L per 4 h ember event (estimate)",
                 "72 h armed plus 4 h spraying on a 77 Wh battery (estimate)",
                 "Kit parts about $420 against a $300 budget (indicative)"],
    date="2026-09-25",
    cut=False, context=supply,
    flow={"title": "water per 4 h ember event, litres (all values are estimates)", "unit": "L",
          "stages": [("Tank or mains", 960), ("Valves A and B", 960), ("12 eave heads", 960),
                     ("Lands on edge zone", 480), ("Wets edge fuels", 300)],
          "losses": [(2, "Wind drift (est. 50 %)", 480), (3, "Runoff (est.)", 180)]},
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
g_shift = (0, -1100, 2400)                              # ground unit moved beside the mast top
l_sample = Pos(5100, -LIP_Y, LINE_Z + 40) * Box(1400, 200, 250)
l_shift = (1300, LIP_Y - 1500, 900)
EX = {1: (0, 0, 0), 2: (0, 0, 280), 3: (-300, 0, 330), 4: (0, 0, 560), 5: (330, 0, 0), 9: (0, -250, 0),
      13: (220, 0, 0), 7: (0, 0, 0), 6: (0, -420, 120), 12: (0, -420, 380), 8: (0, -420, -220),
      15: (0, 0, 280), 10: (0, 0, -200), 11: (250, 0, -80), 14: (0, 0, 0)}
ex_parts = []
for p in kit:
    s = p.shape
    if p.bom in (1, 13):
        s = s & upper
    elif p.bom in (6, 7, 8, 12, 15, 10, 11):
        s = Pos(*g_shift) * s
    elif p.bom == 14:
        s = Pos(*l_shift) * (s & l_sample)
    ex_parts.append(Part(p.name, s, p.color, p.bom, EX[p.bom]))
_render(ex_parts, MEDIA / "exploded.png", offsets=True, labels=True, elev=18, azim=-35,
        title="EmberGuard: exploded view", size=(9, 7),
        note="Numbers match bom/bom.csv. Ground unit and a 1.4 m spray-line sample drawn beside the mast top, "
             "not in installed positions. Item 16 (hardware) not shown.")

for d in ("_views", "_views_fig"):
    shutil.rmtree(MEDIA / d, ignore_errors=True)
print({k: str(v) for k, v in outs.items()})
