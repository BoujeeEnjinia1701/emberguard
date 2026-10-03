"""EmberGuard product appearance model (build123d), TRL 3, matching the constructable design (EGD-DDR-003, 2026-10-02).

Finished-product look for photoreal renders: the gutter-corner sensor pod (a filleted die-cast
body with a back cover and parting line, four cover screws, a lit status light, a label, the
stainless sun and heat hood on four spacers, the sensor window under its stainless lens hood, a
cable gland and the silicone heat sleeve) on its pod plate, bent flat-bar arm and verge cleat
with coach screws; the weather head on the mast top (sleeve, crossarm, three-cup anemometer and
wind vane); the aluminium mast with its end cap, two galvanized standoffs in slip-on flanges on
aluminium wall plates, crossover plates, U-bolts and anchors; the five-plate temperature and
humidity shield on its centre rod and mast clamp; the 10 W solar panel facing the equator at 45
degrees on a clamp, arm and tilt rail; the light grey steel ground unit on its wall lugs, with a
door, seam, screws, name plate, glands, siren, lit status beacon and key switch, the gear plate,
controller, battery with its strap and pump-start relay inside it, and the folded white sun shade
on two arms above it; the valve board with its pipe clips, manifold, two zone valves on their own
tees and the pressure transducer; the black polyethylene spray line on the gutter lip with lip
clips, a micro-sprinkler head, and the riser up the gable corner on wall clips and under the
gutter on a fascia clip; and the mast and pod cables. Context is a compact corner of the
reference house at the east end of the front eave: lap-sided walls, the roof overhang with
shingle courses, the fascia and the gutter with its end cap and hangers.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every size, the pod position and aim, the gutter and spray-line geometry and every interface
come from PARAMS, derived(), sensor_axes() and house_parts() in model.py. Axes as model.py: X
along the ridge (east +X), Y across the house (front eave at -Y), Z up from the ground.
RENDER LAYOUT, NOT THE INSTALLED LAYOUT: the front pod, the gutter corner and the spray line are
at their model.py positions. For a compact product render the mast and everything on it is
drawn at y = MAST_Y (installed on the ridge line, y = 0) and MAST_DZ lower, so that both
standoffs still meet the gable wall below the roof; its offset from the wall, its length and
every height on it relative to the mast are unchanged. The ground unit is drawn at y = GROUND_Y
(installed -1800 mm) at its model.py height, and only the east 1.2 m of the front spray line and its
riser are shown. The valve board is drawn just below the enclosure (VALVE_Z) instead of 520 mm above
the ground. Captions must say the mast and ground unit are drawn closer than installed (decided
2026-10-02). See docs/REVIEW.md, sessions 2026-09-26 and 2026-10-02.

Groups: "shell" is the front sensor pod with its thermal sensor, hood and bracket, so the detail
view shows it alone; "internal" is the pod node board; "accessory" is the rest of the kit (the
mast with the weather head and its other sensors, the ground unit and its contents, the valves,
the spray line and the cables).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Cone, Cylinder, Plane, Pos, RegularPolygon, Rot, Solid, Sphere,
                       Vector, extrude, fillet)
from model import (PARAMS, derived, sensor_axes, house_parts, build_components, pod_components, pod_cable_path,
                   ground_components, spray_components, _pod_xf)

TITLE = "EmberGuard: ember-detecting gutter and eave sprinkler system"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); weather mast on the "
             "gable wall with the ground unit below it, thermal sensor pod over the end of the front gutter "
             "and the spray line on the gutter lip. Compact render layout, not the installed spacing"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): weather head, mast, "
             "standoffs, humidity shield and solar panel; sensor pod, hood, back cover, node board and "
             "thermal sensor; ground unit door, controller, battery and relay; valves; spray line and head"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 18, "az": -135,
     "note": "Detail from the front left and above (about 18 deg elevation): the thermal sensor pod on its "
             "post and gutter clamp, with the sensor lens looking west along the gutter under the stainless "
             "hood; shown without the house"},
]

# ---------------------------------------------------------------- render layout (not installed)
MAST_Y = -3600.0        # mast axis Y in the render (installed 0, on the ridge line)
MAST_DZ = -1150.0       # mast and everything on it drawn this much lower than installed
GROUND_Y = -3330.0      # ground unit centre Y in the render (installed -1800)
VALVE_Z = 790.0         # manifold centre Z in the render (installed 520)
CROP = ((5350.0, 6560.0), (-4760.0, -2700.0), (560.0, 3700.0))   # context corner, x, y, z ranges
LINE_X0 = 5360.0        # west end of the spray line section shown

# Colours (restrained product palette; kit accent)
C_ACCENT = "#0F766E"
C_POD = "#D7DADD"
C_POD2 = "#BCC1C6"
C_DARK = "#2B2F36"
C_BLACK = "#1C1F24"
C_LENS = "#15181C"
C_STEEL = "#C3C8CE"
C_ALU = "#CDD2D7"
C_GALV = "#A9AFB5"
C_WHITE = "#EEF0F1"
C_ENCL = "#DDE0E3"
C_ENCL2 = "#C5CAD0"
C_LABEL = "#F4F4F2"
C_PCB = "#166534"
C_CHIP = "#111827"
C_BATT = "#3B4A5A"
C_RELAY = "#1E3A5F"
C_BRASS = "#C9A227"
C_CELL = "#1B2A4A"
C_LINE = "#23272D"
C_SLEEVE = "#B4532A"
C_LED_G = "#22C55E"
C_RED = "#9F2A2A"
C_WALL = "#DAD6CE"
C_ROOF = "#62666B"
C_TRIM = "#ECEBE7"
C_GUTTER = "#E3E5E7"


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _rod(a, b, r):
    a, b = Vector(*a), Vector(*b)
    d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _pipe(points, r):
    """Round tube through `points` with spherical joints (clean bends)."""
    out = None
    for a, c in zip(points, points[1:]):
        seg = _rod(a, c, r)
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _edges_par(s, axis):
    return s.edges().filter_by(axis)


def _top(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _xmax(s):
    return s.faces().sort_by(Axis.X)[-1].edges()


def _xmin(s):
    return s.faces().sort_by(Axis.X)[0].edges()


def _ymin(s):
    return s.faces().sort_by(Axis.Y)[0].edges()


def _hex_x(x, y, z, af, length):
    """Hex prism along X (across flats `af`), from x to x + length."""
    return Pos(x, y, z) * extrude(Plane.YZ * RegularPolygon(af / 1.732, 6), amount=length)


def _hex_z(x, y, z, af, h):
    return Pos(x, y, z - h / 2) * extrude(RegularPolygon(af / 1.732, 6), amount=h)


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def product_parts(P=PARAMS):
    D = derived(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    L2 = P["house_l"] / 2                     # gable wall outer face, x = 6000
    x_end = D["roof_len"] / 2                 # gutter and roof end, x = 6500
    (cx0, cx1), (cy0, cy1), (cz0, cz1) = CROP
    crop = _box((cx0 + cx1) / 2, (cy0 + cy1) / 2, (cz0 + cz1) / 2, cx1 - cx0, cy1 - cy0, cz1 - cz0)

    # ================================================================ sensor pod (BOM 2, 3), front gutter
    # The pod body is built level at the origin and placed with model.py's own pod transform (aim and tilt);
    # the mount, hoods, spacers and gland are model.py's constructable parts, coloured.
    s = -1
    px, py, pz = P["pod"]
    cx = cy = cz = 0.0
    xf = _pod_xf(P, s)
    PC = pod_components(P, s)

    def addp(name, shape, color, material, bom, group, explode):
        add(name, xf * shape, color, material, bom, group, explode)

    back_t = 10.0                                            # back cover thickness (+X end)
    xb = cx + px / 2 - back_t                                # parting plane between body and back cover
    body = _box((cx - px / 2 + xb) / 2, cy, cz, xb - (cx - px / 2), py, pz)
    body = _fillet_try(body, _edges_par(body, Axis.X), [8.0, 6.0, 4.0])
    body = _fillet_try(body, _xmin(body), [3.0, 2.0, 1.0])
    for dz in (-18, -9, 0, 9, 18):                           # shallow cooling ribs on the sides
        for sy in (-1, 1):
            body -= _box(cx - 5, cy + sy * py / 2, cz + dz, 50, 1.6, 2.4)
    addp("Sensor pod body (die-cast)", body, C_POD, "painted", 2, "shell", (0, 0, 0))

    cover = _box(xb + back_t / 2 + 0.6, cy, cz, back_t - 1.2, py, pz)
    cover = _fillet_try(cover, _edges_par(cover, Axis.X), [8.0, 6.0, 4.0])
    cover = _fillet_try(cover, _xmax(cover), [2.5, 1.5, 1.0])
    addp("Sensor pod back cover", cover, C_POD2, "painted", 2, "shell", (110, 0, 0))
    scr = None
    for sy in (-1, 1):
        for sz in (-1, 1):
            q = _xcyl(cx + px / 2 + 0.6, cy + sy * (py / 2 - 8), cz + sz * (pz / 2 - 8), 3.2, 1.6)
            q = _fillet_try(q, _xmax(q), [0.6, 0.3])
            q -= _box(cx + px / 2 + 1.3, cy + sy * (py / 2 - 8), cz + sz * (pz / 2 - 8), 1.0, 3.6, 0.8)
            scr = q if scr is None else scr + q
    addp("Back cover screws", scr, C_STEEL, "metal", 16, "shell", (140, 0, 0))
    led = _xcyl(cx + px / 2 + 0.8, cy + 20, cz + 18, 3.0, 2.0) + Pos(cx + px / 2 + 1.8, cy + 20, cz + 18) * Sphere(2.6)
    led &= _box(cx + px / 2 + 2, cy + 20, cz + 18, 5, 8, 8)
    addp("Pod status light, green (lit)", led, C_LED_G, "emissive", 2, "shell", (140, 0, 0))
    ring = _xcyl(cx + px / 2 + 0.8, cy + 20, cz + 18, 4.6, 1.2) - _xcyl(cx + px / 2 + 0.8, cy + 20, cz + 18, 3.1, 3)
    addp("Pod status light bezel", ring, C_BLACK, "plastic", 2, "shell", (140, 0, 0))

    # label and accent band on the -Y side (seen from the front)
    fy = cy - py / 2
    lab = _box(cx - 8, fy - 0.2, cz - 6, 56, 0.4, 24)
    addp("Pod label", lab, C_LABEL, "paper", 2, "shell", (0, -60, 0))
    ink = _box(cx - 24, fy - 0.5, cz - 1, 18, 0.3, 7) + _box(cx + 4, fy - 0.5, cz + 1, 26, 0.3, 3) \
        + _box(cx - 8, fy - 0.5, cz - 13, 44, 0.3, 2)
    addp("Pod label print", ink, C_DARK, "paper", 2, "shell", (0, -60, 0))
    band = _box(cx - 5, fy - 0.2, cz + 22, 80, 0.4, 5)
    addp("Pod accent band", band, C_ACCENT, "painted", 2, "shell", (0, -60, 0))

    # constructable parts from model.py: hood on four spacers, lens hood over the sensor window, plate, arm, cleat, gland
    add("Pod sun and heat hood (stainless)", PC["hood_f"].shape, C_STEEL, "metal", 2, "shell", (0, 0, 120))
    add("Hood spacers", PC["hood_spacers_f"].shape, C_STEEL, "metal", 2, "shell", (0, 0, 60))
    add("Lens hood (stainless)", PC["lens_hood_f"].shape, C_STEEL, "metal", 2, "shell", (-90, 0, 0))
    add("Lens hood screws", PC["lens_hood_screws_f"].shape, C_STEEL, "metal", 16, "shell", (-90, 0, 0))
    lens = _xcyl(cx - px / 2 - 0.4, cy, cz, P["can_hole"] / 2, 0.8)
    addp("Thermal sensor lens (germanium)", lens, C_LENS, "screen", 3, "shell", (-90, 0, 0))

    # pod node and MLX90640 breakout inside the pod
    brd = _box(cx - px / 2 + 30, cy, cz, 1.6, 60, 60)
    addp("Pod node board", brd, C_PCB, "plastic", 2, "internal", (200, 0, 0))
    chips = _box(cx - px / 2 + 27.5, cy + 14, cz + 14, 3.0, 14, 12) + _box(cx - px / 2 + 27.5, cy - 16, cz - 16, 2.4, 10, 8) \
        + _xcyl(cx - px / 2 + 24, cy, cz, 5.0, 8.0)
    addp("Thermal array and node chips", chips, C_CHIP, "plastic", 3, "internal", (200, 0, 0))

    # mount: spacers, pod plate, arm, verge cleat and coach screws
    add("Pod plate and spacers (aluminium)", PC["pod_plate_f"].shape + PC["pod_spacers_f"].shape, C_ALU, "metal", 2, "shell", (0, 0, -60))
    add("Pod arm (flat bar)", PC["arm_f"].shape, C_ALU, "metal", 2, "shell", (0, 0, -140))
    add("Verge cleat (angle)", PC["cleat_f"].shape, C_ALU, "metal", 2, "shell", (0, 0, -220))
    add("Cleat coach screws and pod bolts", PC["pod_fix_f"].shape, C_STEEL, "metal", 16, "shell", (0, 0, -220))
    add("Pod cable gland", PC["cgland_f"].shape, C_BLACK, "plastic", 16, "shell", (0, 0, -40))

    # ================================================================ weather head on the mast (BOM 4)
    mx, my = D["mast_x"], MAST_Y
    mast_c = build_components(P)
    ro = P["mast_od"] / 2
    zt = P["mast_z1"] + MAST_DZ
    az_, ah = P["arm_z"] + MAST_DZ, P["arm_half"]
    adapt = _zcyl(mx, my, zt + 15, ro + 6, 30)
    adapt = _fillet_try(adapt, _top(adapt), [4.0, 2.0])
    adapt -= _box(mx + ro + 6, my, zt + 15, 4, 3, 40)
    ab = _xcyl(mx + ro + 8, my, zt + 15, 4.0, 10.0)
    add("Mast-top adapter", adapt + ab, C_DARK, "painted", 4, "accessory", (0, 0, 70))
    stub = _zcyl(mx, my, (zt + 30 + az_) / 2, 10.0, az_ - zt - 30)
    tee = _zcyl(mx, my, az_, 16.0, 36.0)
    tee = _fillet_try(tee, _top(tee) + _bottom(tee), [3.0, 1.5])
    arm = _ycyl(mx, my, az_, 9.0, 2 * ah)
    for sy in (-1, 1):
        arm += _ycyl(mx, my + sy * ah, az_, 11.0, 20.0)
    add("Weather head stub, tee and crossarm", stub + tee + arm, C_ALU, "metal", 4, "accessory", (0, 0, 140))

    # anemometer at -Y end
    ax, ay = mx, my - ah
    abody = _zcyl(ax, ay, az_ + 45, 17.0, 70.0)
    abody = _fillet_try(abody, _top(abody), [4.0, 2.0])
    add("Anemometer body", abody, C_WHITE, "plastic", 4, "accessory", (0, 0, 230))
    hub = _zcyl(ax, ay, az_ + 90, 15.0, 20.0)
    hub = _fillet_try(hub, _top(hub), [6.0, 4.0])
    cups = None
    for k in range(3):
        t = math.radians(k * 120 + 20)
        ex, ey = ax + 90 * math.cos(t), ay + 90 * math.sin(t)
        hub += _rod((ax, ay, az_ + 90), (ex, ey, az_ + 90), 3.5)
        # hemispherical cup, open face toward the tangent direction
        c = Rot(0, 90, 0) * Sphere(26) - Rot(0, 90, 0) * Sphere(24) - Pos(-30, 0, 0) * Box(60, 70, 70)
        c = Pos(ex, ey, az_ + 90) * Rot(0, 0, math.degrees(t) + 90) * c
        cups = c if cups is None else cups + c
    add("Anemometer hub and arms", hub, C_WHITE, "plastic", 4, "accessory", (0, 0, 260))
    add("Anemometer cups", cups, C_WHITE, "plastic", 4, "accessory", (0, 0, 260))

    # wind vane at +Y end
    vx, vy = mx, my + ah
    vbody = _zcyl(vx, vy, az_ + 45, 15.0, 70.0)
    vbody = _fillet_try(vbody, _top(vbody), [4.0, 2.0])
    add("Wind vane body", vbody, C_WHITE, "plastic", 4, "accessory", (0, 0, 230))
    rod = _xcyl(vx, vy, az_ + 90, 4.0, 200.0) + _zcyl(vx, vy, az_ + 90, 10.0, 16.0)
    nose = Pos(vx + 80, vy, az_ + 90) * Sphere(14)
    fin = _box(vx - 80, vy, az_ + 90, 170, 4, 90)
    fin -= Pos(vx - 165, vy, az_ + 135) * Rot(0, 40, 0) * Box(90, 10, 60)
    fin -= Pos(vx + 5, vy, az_ + 150) * Rot(0, -30, 0) * Box(80, 10, 60)
    fin = _fillet_try(fin, _edges_par(fin, Axis.Y), [3.0, 2.0])
    add("Wind vane rod and nose", rod + nose, C_DARK, "painted", 4, "accessory", (0, 0, 260))
    add("Wind vane tail fin", fin, C_WHITE, "plastic", 4, "accessory", (0, 0, 260))
    fband = _box(vx - 120, vy - 2.2, az_ + 90, 40, 0.4, 30) + _box(vx - 120, vy + 2.2, az_ + 90, 40, 0.4, 30)
    add("Vane fin accent", fband, C_ACCENT, "painted", 4, "accessory", (0, 0, 260))

    # ================================================================ mast and standoffs (BOM 1)
    z0 = P["mast_z0"] + MAST_DZ
    ml = D["mast_len"]
    tubeo = _zcyl(mx, my, z0 + ml / 2, ro, ml)
    add("Mast tube (6061-T6)", tubeo, C_ALU, "metal", 1, "accessory", (0, 0, 0))
    cap = _zcyl(mx, my, z0 - 6, ro + 1.5, 12)
    cap = _fillet_try(cap, _bottom(cap), [3.0, 1.5])
    add("Mast end cap", cap, C_BLACK, "rubber", 1, "accessory", (0, 0, -60))
    # standoffs, wall plates, flanges, crossover plates, U-bolts and anchors: model.py's parts, moved with the mast
    MC = mast_c
    S_mast = Pos(0, my, MAST_DZ)
    add("Standoff pipes (DN25, galvanized)", S_mast * MC["standoffs"].shape, C_GALV, "metal", 1, "accessory", (150, 0, 0))
    add("Standoff wall plates", S_mast * MC["wall_plates"].shape, C_ALU, "metal", 1, "accessory", (-160, 0, 0))
    add("Slip-on base flanges", S_mast * MC["flanges"].shape, C_GALV, "metal", 1, "accessory", (-80, 0, 0))
    add("Crossover plates", S_mast * MC["xplates"].shape, C_ALU, "metal", 1, "accessory", (60, 0, 0))
    add("U-bolts with nyloc nuts", S_mast * MC["ubolts"].shape, C_STEEL, "metal", 1, "accessory", (90, 0, 0))
    add("Wall plate anchors", S_mast * MC["wall_anchors"].shape, C_STEEL, "metal", 16, "accessory", (-120, 0, 0))

    # ================================================================ temperature and humidity shield (BOM 5)
    tz = P["trh_z"] + MAST_DZ
    plates5 = None
    for k in range(5):
        pz_ = tz + k * 22
        pl = Pos(mx + 90, my, pz_ - 3) * Cone(55, 47, 6)
        if k < 4:
            pl -= _zcyl(mx + 90, my, pz_, 30, 10)
        plates5 = pl if plates5 is None else plates5 + pl
    plates5 = plates5 + _zcyl(mx + 90, my, tz + 57.5, 5.0, 135.0)
    add("Radiation shield (five plates)", plates5, C_WHITE, "plastic", 5, "accessory", (160, 0, 0))
    tarm = _xcyl((mx + ro + 6 + mx + 95) / 2, my, tz + 125, 6.0, 89 - ro) + _zcyl(mx, my, tz + 125, ro + 6, 30)
    add("Shield arm and mast clamp", tarm, C_DARK, "painted", 5, "accessory", (80, 0, 0))
    probe = _zcyl(mx + 90, my, tz + 14, 7.0, 40.0)
    add("Temperature and humidity probe", probe, C_BLACK, "plastic", 5, "accessory", (160, 0, -60))

    # ================================================================ solar panel (BOM 9), facing -Y
    pw, ph, pt = P["panel"]
    pzc = P["panel_z"] + MAST_DZ
    tilt = P["panel_tilt"]
    frame = Box(pw, ph, pt) - Pos(0, 0, 4) * Box(pw - 16, ph - 16, pt)
    frame = _fillet_try(frame, _edges_par(frame, Axis.Z), [3.0, 2.0])
    cells = Pos(0, 0, pt / 2 - 5) * Box(pw - 16, ph - 16, 2)
    grid = None
    for i in range(1, 6):
        g = Pos(-(pw - 16) / 2 + i * (pw - 16) / 6, 0, pt / 2 - 3.8) * Box(1.6, ph - 16, 0.4)
        grid = g if grid is None else grid + g
    for j in range(1, 4):
        grid += Pos(0, -(ph - 16) / 2 + j * (ph - 16) / 4, pt / 2 - 3.8) * Box(pw - 16, 1.6, 0.4)
    jbox = Pos(0, 40, -pt / 2 - 10) * Box(80, 50, 20)
    loc = Pos(mx, my - 200, pzc) * Rot(tilt, 0, 0)
    add("Solar panel frame", loc * frame, C_ALU, "metal", 9, "accessory", (0, -260, 0))
    add("Solar cells", loc * cells, C_CELL, "screen", 9, "accessory", (0, -260, 0))
    add("Cell busbars", loc * grid, "#C9CED6", "metal", 9, "accessory", (0, -260, 0))
    add("Panel junction box", loc * jbox, C_BLACK, "plastic", 9, "accessory", (0, -260, 0))
    add("Panel clamp, arm and tilt rail", S_mast * MC["panel_mount"].shape, C_DARK, "painted", 9, "accessory", (0, -140, 0))

    # ================================================================ ground unit (BOM 6, 7, 8, 12, 15)
    bx, by, bh = P["box"]
    gcx, gcy, gcz = D["box_c"][0], GROUND_Y, D["box_c"][2]
    door_t = 14.0
    xf = gcx + bx / 2                                         # front (+X) face
    shell = _box(gcx - door_t / 2, gcy, gcz, bx - door_t, by, bh)
    shell = _fillet_try(shell, _edges_par(shell, Axis.X), [8.0, 6.0, 4.0])
    shell -= _box(gcx - door_t / 2 + 5, gcy, gcz, bx - door_t, by - 4, bh - 4)
    add("Ground enclosure body (steel)", shell, C_ENCL, "painted", 7, "accessory", (0, -600, 0))
    door = _box(xf - door_t / 2 + 0.5, gcy, gcz, door_t - 1.0, by, bh)
    door = _fillet_try(door, _edges_par(door, Axis.X), [8.0, 6.0, 4.0])
    door = _fillet_try(door, _xmax(door), [3.0, 2.0, 1.0])
    door -= _box(xf, gcy, gcz, 1.2, by - 30, bh - 30) - _box(xf, gcy, gcz, 2, by - 32, bh - 32)
    add("Ground enclosure door", door, C_ENCL2, "painted", 7, "accessory", (260, -600, 0))
    dscr = None
    for sy in (-1, 1):
        for sz in (-1, 1):
            q = _xcyl(xf + 0.6, gcy + sy * (by / 2 - 9), gcz + sz * (bh / 2 - 9), 3.6, 1.4)
            q -= _box(xf + 1.2, gcy + sy * (by / 2 - 9), gcz + sz * (bh / 2 - 9), 1.0, 4.2, 0.8)
            dscr = q if dscr is None else dscr + q
    add("Door screws", dscr, C_STEEL, "metal", 16, "accessory", (290, -600, 0))
    hinges = _fuse(_zcyl(xf - 2, gcy - by / 2 - 3, gcz + oz, 5.0, 40) for oz in (-120, 120))
    add("Door hinges", hinges, C_GALV, "metal", 7, "accessory", (260, -600, 0))
    plate = _box(xf + 0.3, gcy, gcz + 150, 0.6, 180, 26)
    add("Ground unit name plate", plate, C_ACCENT, "painted", 7, "accessory", (290, -600, 0))
    ptxt = _box(xf + 0.7, gcy - 40, gcz + 150, 0.3, 80, 7) + _box(xf + 0.7, gcy + 50, gcz + 150, 0.3, 50, 4)
    add("Name plate lettering", ptxt, C_LABEL, "paper", 7, "accessory", (290, -600, 0))
    wl = _box(xf + 0.3, gcy, gcz - 110, 0.6, 150, 60)
    add("Warning and wiring label", wl, C_LABEL, "paper", 7, "accessory", (290, -600, 0))
    wli = _box(xf + 0.7, gcy - 50, gcz - 100, 0.3, 30, 30) - _box(xf + 0.7, gcy - 50, gcz - 100, 1, 22, 22) \
        + _box(xf + 0.7, gcy + 20, gcz - 96, 0.3, 90, 3) + _box(xf + 0.7, gcy + 20, gcz - 110, 0.3, 90, 3) \
        + _box(xf + 0.7, gcy + 20, gcz - 124, 0.3, 60, 3)
    add("Warning label print", wli, C_DARK, "paper", 7, "accessory", (290, -600, 0))

    # key switch on the door (model.py side cylinder position)
    kx, ky, kz = xf, gcy + 90, gcz + 120
    kb = _xcyl(kx + 3, ky, kz, 16.0, 6.0)
    kb = _fillet_try(kb, _xmax(kb), [1.5, 1.0])
    kb -= _xcyl(kx + 5, ky, kz, 10.0, 4.0)
    add("Key switch bezel", kb, C_STEEL, "metal", 15, "accessory", (290, -600, 0))
    core = _xcyl(kx + 4, ky, kz, 9.6, 6.0) - _box(kx + 7, ky, kz, 2.0, 2.2, 9.0)
    add("Key switch cylinder", core, "#9A9FA6", "metal", 15, "accessory", (290, -600, 0))

    # siren and status beacon on the top (model.py siren position)
    top = gcz + bh / 2
    sir = _zcyl(gcx + 30, gcy - 80, top + 30, 45.0, 60.0)
    sir = _fillet_try(sir, _top(sir), [8.0, 5.0])
    for k in range(4):
        sir -= _zcyl(gcx + 30, gcy - 80, top + 60, 34 - 8 * k, 1.6) - _zcyl(gcx + 30, gcy - 80, top + 60, 32 - 8 * k, 3)
    add("Siren (12 V piezo)", sir, C_DARK, "plastic", 15, "accessory", (0, -600, 150))
    bb = _zcyl(gcx + 30, gcy + 90, top + 8, 22.0, 16.0)
    bb = _fillet_try(bb, _top(bb), [3.0, 1.5])
    add("Beacon base", bb, C_DARK, "plastic", 15, "accessory", (0, -600, 150))
    dome = _zcyl(gcx + 30, gcy + 90, top + 26, 18.0, 20.0) + Pos(gcx + 30, gcy + 90, top + 36) * Sphere(18.0)
    add("Status beacon, green (lit)", dome, C_LED_G, "emissive", 15, "accessory", (0, -600, 150))

    # cable glands on the underside
    gls = None
    for gy in (-110, -40, 40, 110):
        g = _hex_z(gcx, gcy + gy, gcz - bh / 2 - 2.5, 22.0, 5.0) + _zcyl(gcx, gcy + gy, gcz - bh / 2 - 10, 9.0, 10.0)
        g = _fillet_try(g, _bottom(g), [2.0, 1.0])
        gls = g if gls is None else gls + g
    add("Enclosure cable glands", gls, C_BLACK, "plastic", 16, "accessory", (0, -600, -70))

    # wall lugs, gear plate, controller, relay, battery and strap: model.py's parts, moved with the ground unit
    GC = ground_components(P)
    GS = Pos(0, GROUND_Y - D["box_c"][1], 0)
    add("Enclosure wall lugs (4)", GS * GC["box_lugs"].shape, C_DARK, "painted", 7, "accessory", (-100, -600, 0))
    add("Lug screws (4)", GS * GC["box_screws"].shape, C_STEEL, "metal", 16, "accessory", (-100, -600, 0))
    EI = (150, -600, 0)
    add("Gear plate on its studs", GS * GC["gear_plate"].shape, C_STEEL, "metal", 7, "accessory", (60, -600, 0))
    brd = GS * GC["board"].shape
    add("Controller board", brd, C_PCB, "plastic", 6, "accessory", EI)
    bb_ = brd.bounding_box()
    comp = _box(bb_.max.X + 3, gcy - 70, gcz + 110, 6, 40, 40) + _box(bb_.max.X + 2, gcy + 10, gcz + 70, 4, 30, 20) \
        + _box(bb_.max.X + 3.5, gcy - 20, gcz + 50, 7, 60, 14)
    add("Controller module and drivers", comp, C_CHIP, "plastic", 6, "accessory", EI)
    bat = GS * GC["battery"].shape
    add("Battery, 12.8 V 10 Ah LiFePO4", bat, C_BATT, "plastic", 8, "accessory", (240, -600, 0))
    bbat = bat.bounding_box()
    blab = _box(bbat.max.X + 0.2, (bbat.min.Y + bbat.max.Y) / 2, (bbat.min.Z + bbat.max.Z) / 2, 0.4, 110, 50)
    add("Battery label", blab, C_LABEL, "paper", 8, "accessory", (240, -600, 0))
    add("Battery strap", GS * GC["strap"].shape, C_ALU, "metal", 16, "accessory", (300, -600, 0))
    add("Pump-start relay", GS * GC["relay"].shape, C_RELAY, "plastic", 12, "accessory", EI)

    # sun shade: folded white sheet on two bent flat-bar arms (BOM 18)
    add("Sun shade (folded white sheet)", GS * GC["shade"].shape, C_WHITE, "painted", 18, "accessory", (0, -600, 260))
    add("Sun shade arms", GS * GC["shade_arms"].shape, C_ALU, "metal", 18, "accessory", (0, -600, 200))
    add("Sun shade wall screws", GS * GC["shade_screws"].shape, C_STEEL, "metal", 18, "accessory", (-60, -600, 200))

    # ================================================================ valve board, manifold, valves, transducer (BOM 10, 11, 16)
    # model.py's parts; the board is drawn just below the enclosure (VALVE_Z) instead of 520 mm above the ground
    VS = Pos(0, GROUND_Y - D["box_c"][1], VALVE_Z - P["manifold_z"])
    add("Valve board (aluminium)", VS * GC["valve_board"].shape, C_ALU, "metal", 16, "accessory", (0, -600, -120))
    add("Stand-off pipe clips", VS * GC["pipe_clips"].shape, C_GALV, "metal", 16, "accessory", (0, -600, -120))
    add("Manifold, tees and hose connector", VS * GC["manifold"].shape, C_BRASS, "metal", 16, "accessory", (0, -600, -140))
    add("Zone valves A and B (12 V)", VS * GC["valves"].shape, C_DARK, "plastic", 10, "accessory", (0, -600, -190))
    xd = VS * GC["xducer"].shape
    add("Pressure transducer", xd, C_STEEL, "metal", 11, "accessory", (0, -600, -60))

    # ================================================================ spray line on the front gutter lip (BOM 14)
    # model.py's front line, heads, clips and riser, cut to the part of the house shown
    SC = spray_components(P)
    ly, lz = s * D["line_y"], D["line_z"]
    win_ = _box((LINE_X0 + 6700) / 2, (cy0 + cy1) / 2, (cz0 + cz1) / 2, 6700 - LINE_X0, cy1 - cy0, cz1 - cz0)
    add("Spray line and riser (16 mm polyethylene)", SC["lines"].shape & win_, C_LINE, "plastic", 14, "accessory", (0, -120, 0))
    hs = SC["heads"].shape & win_
    add("Micro-sprinkler head", hs, C_DARK, "plastic", 14, "accessory", (0, -120, 80))
    caps = None
    for hx in D["head_x"]:
        if LINE_X0 < hx < x_end:
            cp = _zcyl(hx, ly, lz + 80, 7, 8)
            cp = _fillet_try(cp, _top(cp), [2.5, 1.5])
            caps = cp if caps is None else caps + cp
    add("Sprinkler spinner cap", caps, C_ACCENT, "plastic", 14, "accessory", (0, -120, 120))
    add("Gutter-lip clips", SC["lip_clips"].shape & win_, C_BLACK, "plastic", 14, "accessory", (0, -120, 0))
    add("Riser and fascia clips", (SC["wall_clips"].shape + SC["fascia_clips"].shape) & win_, C_DARK, "plastic", 16, "accessory", (0, -120, 0))

    # ================================================================ cables (BOM 13)
    # the mast cable runs inside the tube, out under the end cap and the lower standoff; the pod cable follows model.py's
    # route along the arm, round the verge and down the gable corner
    zc = gcz - bh / 2 - 45                                     # cable run just below the ground unit
    zl = P["standoff_z"][0] + MAST_DZ
    sy_ = D["standoff_y"]
    mcab = _pipe([(mx, my, z0 - 12), (mx, my, z0 - 40), (mx - 70, my + sy_, zl - 40), (L2 + 60, my + sy_, zl - 40),
                  (L2 + 60, my + sy_, zc), (gcx, my + sy_, zc), (gcx, gcy - 110, zc), (gcx, gcy - 110, gcz - bh / 2 - 12)], 5.0)
    add("Mast cable", mcab, C_BLACK, "rubber", 13, "accessory", (0, 0, 0))
    pts = pod_cable_path(P, -1)
    zrun = pts[-1][2]
    gxc = L2 + P["lug_t"] + 135
    route = pts + [(L2 + 8, gcy - 100, zrun), (gxc, gcy - 100, zrun), (gxc, gcy - 100, gcz - bh / 2 - 12)]
    pcab = _pipe(route, 4.5)
    add("Pod cable", pcab, C_BLACK, "rubber", 13, "accessory", (0, 0, 0))
    sleeve = _pipe(pts[:3], 7.5)
    add("Pod cable heat sleeve (silicone)", sleeve, C_SLEEVE, "fabric", 13, "accessory", (0, 0, -40))

    # ================================================================ context: house corner (no BOM)
    H = house_parts(P)
    walls = H["walls"] & crop
    # lap siding lines on the front (-Y) and gable (+X) faces
    for k in range(int(cz0 // 150) + 1, int(D["eave_z"] // 150) + 12):
        z = k * 150.0
        walls -= _box((cx0 + L2) / 2, -P["house_d"] / 2, z, L2 - cx0 + 2, 3.0, 2.0)
        walls -= _box(L2, (cy0 + cy1) / 2, z, 3.0, cy1 - cy0 + 2, 2.0)
    add("House walls (context)", walls, C_WALL, "painted", None, "context", (0, 0, 0))
    roof = H["roof"] & crop
    pit = math.radians(P["pitch"])
    c_ = math.cos(pit)
    for k in range(1, 12):
        yy = -D["eave_y"] + k * 140.0 * c_
        if yy > cy1:
            break
        zz = P["wall_h"] + (P["house_d"] / 2 + yy) * D["T"] + P["roof_t"] / c_
        roof -= Pos(0.5 * (cx0 + cx1), yy, zz) * Rot(P["pitch"], 0, 0) * Box(cx1 - cx0 + 50, 3.0, 6.0)
    add("Roof overhang (context)", roof, C_ROOF, "painted", None, "context", (0, 0, 0))
    fg = H["fascia_gutters"] & crop
    add("Fascia and gutter (context)", fg, C_GUTTER, "painted", None, "context", (0, 0, 0))
    gw, gh = P["gutter_w"], P["gutter_h"]
    gyc = s * D["gut_yc"]
    endcap = _box(x_end + 1, gyc, D["gut_z0"] + gh / 2, 2.0, gw, gh)
    add("Gutter end cap (context)", endcap, C_GUTTER, "painted", None, "context", (0, 0, 0))
    hang = None
    for k in range(2):
        hx = x_end - 375 - k * P["hanger_pitch"]
        h = _box(hx, gyc, D["lip_z"] - 3, P["hanger_w"], gw, 3.0)
        hang = h if hang is None else hang + h
    add("Gutter hangers (context)", hang, C_GUTTER, "metal", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:38s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.1f} cm3")
