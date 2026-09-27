"""EmberGuard product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: the gutter-corner sensor pod (a filleted die-cast
body with a back cover and parting line, four cover screws, a lit status light, a label, a
stainless sun and heat hood on spacers, the thermal sensor snout with its dark infrared lens
aimed along the gutter, a cable gland and the silicone heat sleeve, and the post, arm and gutter
clamp); the weather head on the mast top (adapter, stub, crossarm, three-cup anemometer and
wind vane); the aluminium mast with its end cap, two galvanized standoffs with wall plates,
anchor bolts and split clamp collars; the five-plate temperature and humidity shield; the 10 W
solar panel with a frame, cell grid, junction box and arm; the light grey steel ground unit
with a door, seam, screws, name plate, glands, siren, lit status beacon and key switch, and the
controller board, battery and pump-start relay inside it; the two zone valves and the pressure
transducer on their manifold; the black polyethylene spray line on the gutter lip with lip
clips, a micro-sprinkler head and the riser elbow; and the mast and pod cables. Context is a
compact corner of the reference house at the east end of the front eave: lap-sided walls, the
roof overhang with shingle courses, the fascia and the gutter with its end cap and hangers.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every size, the pod position and aim, the gutter and spray-line geometry and every interface
come from PARAMS, derived(), sensor_axes() and house_parts() in model.py. Axes as model.py: X
along the ridge (east +X), Y across the house (front eave at -Y), Z up from the ground.
RENDER LAYOUT, NOT THE INSTALLED LAYOUT: the front pod, the gutter corner and the spray line are
at their model.py positions. For a compact product render the mast and everything on it is
drawn at y = MAST_Y (installed on the ridge line, y = 0) and MAST_DZ lower, so that both
standoffs still meet the gable wall below the roof; its offset from the wall, its length and
every height on it relative to the mast are unchanged. The ground unit is drawn at y = GROUND_Y
(installed -1800 mm) at its model.py height, the valve manifold just below it (VALVE_Z) instead
of 450 mm above the ground, and only the east 0.9 m of the front spray line and the top of its
riser are shown. See docs/REVIEW.md, session 2026-09-26.

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
from model import PARAMS, derived, sensor_axes, house_parts

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
VALVE_Z = 790.0         # manifold centre Z in the render (installed 450)
CROP = ((5350.0, 6560.0), (-4760.0, -3100.0), (700.0, 3700.0))   # context corner, x, y, z ranges
LINE_X0 = 5360.0        # west end of the spray line section shown
RISER_SHOWN = 420.0     # length of the riser top shown below the line

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
    s = -1
    px, py, pz = P["pod"]
    cx, cy, cz = D["pod_x"], s * D["gut_yc"], D["pod_z"]
    back_t = 10.0                                            # back cover thickness (+X end)
    xb = cx + px / 2 - back_t                                # parting plane between body and back cover
    body = _box((cx - px / 2 + xb) / 2, cy, cz, xb - (cx - px / 2), py, pz)
    body = _fillet_try(body, _edges_par(body, Axis.X), [8.0, 6.0, 4.0])
    body = _fillet_try(body, _xmin(body), [3.0, 2.0, 1.0])
    # front bezel boss around the lens aperture and shallow cooling ribs on the sides
    pos, d = sensor_axes(P, s)
    body += _xcyl(cx - px / 2 - 2, pos[1], pos[2], 22.0, 4.0)
    for dz in (-18, -9, 0, 9, 18):
        for sy in (-1, 1):
            body -= _box(cx - 5, cy + sy * py / 2, cz + dz, 50, 1.6, 2.4)
    add("Sensor pod body (die-cast)", body, C_POD, "painted", 2, "shell", (0, 0, 0))

    cover = _box(xb + back_t / 2 + 0.6, cy, cz, back_t - 1.2, py, pz)
    cover = _fillet_try(cover, _edges_par(cover, Axis.X), [8.0, 6.0, 4.0])
    cover = _fillet_try(cover, _xmax(cover), [2.5, 1.5, 1.0])
    add("Sensor pod back cover", cover, C_POD2, "painted", 2, "shell", (110, 0, 0))
    scr = None
    for sy in (-1, 1):
        for sz in (-1, 1):
            q = _xcyl(cx + px / 2 + 0.6, cy + sy * (py / 2 - 8), cz + sz * (pz / 2 - 8), 3.2, 1.6)
            q = _fillet_try(q, _xmax(q), [0.6, 0.3])
            q -= _box(cx + px / 2 + 1.3, cy + sy * (py / 2 - 8), cz + sz * (pz / 2 - 8), 1.0, 3.6, 0.8)
            scr = q if scr is None else scr + q
    add("Back cover screws", scr, C_STEEL, "metal", 16, "shell", (140, 0, 0))
    led = _xcyl(cx + px / 2 + 0.8, cy + 20, cz + 18, 3.0, 2.0) + Pos(cx + px / 2 + 1.8, cy + 20, cz + 18) * Sphere(2.6)
    led &= _box(cx + px / 2 + 2, cy + 20, cz + 18, 5, 8, 8)
    add("Pod status light, green (lit)", led, C_LED_G, "emissive", 2, "shell", (140, 0, 0))
    ring = _xcyl(cx + px / 2 + 0.8, cy + 20, cz + 18, 4.6, 1.2) - _xcyl(cx + px / 2 + 0.8, cy + 20, cz + 18, 3.1, 3)
    add("Pod status light bezel", ring, C_BLACK, "plastic", 2, "shell", (140, 0, 0))

    # label and accent band on the -Y side (seen from the front)
    fy = cy - py / 2
    lab = _box(cx - 8, fy - 0.2, cz - 6, 56, 0.4, 24)
    add("Pod label", lab, C_LABEL, "paper", 2, "shell", (0, -60, 0))
    ink = _box(cx - 24, fy - 0.5, cz - 1, 18, 0.3, 7) + _box(cx + 4, fy - 0.5, cz + 1, 26, 0.3, 3) \
        + _box(cx - 8, fy - 0.5, cz - 13, 44, 0.3, 2)
    add("Pod label print", ink, C_DARK, "paper", 2, "shell", (0, -60, 0))
    band = _box(cx - 5, fy - 0.2, cz + 22, 80, 0.4, 5)
    add("Pod accent band", band, C_ACCENT, "painted", 2, "shell", (0, -60, 0))

    # stainless sun and heat hood (model.py envelope 150 x 130, offset -15 in X), bent sheet on spacers
    hx_, hy_, ht_ = P["pod_hood"]
    hcx, htop = cx - 15, cz + pz / 2 + 5 + ht_ / 2
    sheet = 1.5
    hood = _box(hcx, cy, htop - sheet / 2, hx_, hy_, sheet)
    for sy in (-1, 1):
        hood += _box(hcx, cy + sy * (hy_ / 2 - sheet / 2), htop - 14, hx_, sheet, 28)
    hood += _box(hcx - hx_ / 2 + sheet / 2, cy, htop - 9, sheet, hy_, 18)
    hood = _fillet_try(hood, _edges_par(hood, Axis.Z), [1.2, 0.8])
    add("Pod sun and heat hood (stainless)", hood, C_STEEL, "metal", 2, "shell", (0, 0, 120))
    sp = _fuse(_zcyl(cx + ox, cy + oy, (cz + pz / 2 + htop - sheet) / 2, 4.0, htop - sheet - cz - pz / 2)
               for ox in (-30, 30) for oy in (-24, 24))
    add("Hood spacers", sp, C_STEEL, "metal", 2, "shell", (0, 0, 60))

    # thermal sensor snout and lens along the model.py aim (BOM 3)
    dv = Vector(*d)
    p0 = Vector(pos[0] + 2, pos[1], pos[2])
    snout = Solid.make_cylinder(16.0, 44.0, Plane(origin=p0, z_dir=dv))
    lip = Solid.make_cylinder(19.0, 6.0, Plane(origin=p0 + dv * 38.0, z_dir=dv))
    snout = snout + lip - Solid.make_cylinder(13.0, 4.0, Plane(origin=p0 + dv * 41.0, z_dir=dv))
    add("Thermal sensor snout", snout, C_BLACK, "plastic", 3, "shell", (-90, 0, 0))
    lens = Solid.make_cylinder(13.0, 1.2, Plane(origin=p0 + dv * 40.6, z_dir=dv))
    add("Thermal sensor lens (germanium)", lens, C_LENS, "screen", 3, "shell", (-90, 0, 0))

    # pod node and MLX90640 breakout inside the pod (model.py board envelope)
    brd = _box(pos[0] + 30, pos[1], pos[2], 1.6, 60, 60)
    add("Pod node board", brd, C_PCB, "plastic", 2, "internal", (200, 0, 0))
    chips = _box(pos[0] + 27.5, pos[1] + 14, pos[2] + 14, 3.0, 14, 12) + _box(pos[0] + 27.5, pos[1] - 16, pos[2] - 16, 2.4, 10, 8) \
        + _xcyl(pos[0] + 24, pos[1], pos[2], 5.0, 8.0)
    add("Thermal array and node chips", chips, C_CHIP, "plastic", 3, "internal", (200, 0, 0))

    # bracket: post, arm and gutter-end clamp (model.py geometry, BOM 2)
    z_arm = D["lip_z"] + 20
    post = _rod((cx, cy, cz - pz / 2 + 1), (cx, cy, z_arm), 10.0) + Pos(cx, cy, z_arm) * Sphere(10.0) \
        + _rod((cx, cy, z_arm), (x_end - 30, cy, z_arm), 10.0)
    post += _zcyl(cx, cy, cz - pz / 2 - 6, 16.0, 12.0)
    add("Pod post and arm (aluminium)", post, C_ALU, "metal", 2, "shell", (0, 0, 0))
    clamp = _box(x_end - 30, cy, z_arm - 30, 40, P["gutter_w"] + 20, 80)
    clamp = _fillet_try(clamp, _edges_par(clamp, Axis.X), [6.0, 4.0, 2.0])
    add("Gutter-end clamp", clamp, C_DARK, "painted", 2, "shell", (0, 0, 0))
    bolts = None
    for sy in (-1, 1):
        b = _hex_x(x_end - 10, cy + sy * 45, z_arm - 30, 13.0, 6.0)
        b += _xcyl(x_end - 1, cy + sy * 45, z_arm - 30, 4.0, 6.0)
        bolts = b if bolts is None else bolts + b
    add("Clamp bolts", bolts, C_STEEL, "metal", 16, "shell", (40, 0, 0))

    # pod cable gland on the underside
    gx = cx + 30
    gl = _hex_z(gx, cy, cz - pz / 2 - 2.5, 17.0, 5.0) + _zcyl(gx, cy, cz - pz / 2 - 10, 7.0, 10.0)
    gl = _fillet_try(gl, _bottom(gl), [2.0, 1.0])
    add("Pod cable gland", gl, C_BLACK, "plastic", 16, "shell", (0, 0, -40))

    # ================================================================ weather head on the mast (BOM 4)
    mx, my = D["mast_x"], MAST_Y
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
    pipes, plates, anchors, collars, cbolts = [], [], [], [], []
    wt, ww, wh = P["wall_plate"]
    for z in P["standoff_z"]:
        z += MAST_DZ
        pipes.append(_xcyl((L2 + wt + mx) / 2, my, z, P["standoff_od"] / 2, mx - L2 - wt - 20))
        pl = _box(L2 + wt / 2, my, z, wt, ww, wh)
        pl = _fillet_try(pl, _edges_par(pl, Axis.X), [8.0, 5.0])
        pl += _xcyl(L2 + wt + 6, my, z, P["standoff_od"] / 2 + 5, 12)
        plates.append(pl)
        for oy in (-50, 50):
            for oz in (-50, 50):
                a = _hex_x(L2 + wt, my + oy, z + oz, 17.0, 8.0) + _xcyl(L2 + wt + 10, my + oy, z + oz, 5.0, 6.0)
                anchors.append(a)
        col = _zcyl(mx, my, z, ro + 10, 60)
        col = _fillet_try(col, _top(col) + _bottom(col), [3.0, 1.5])
        col -= _box(mx, my, z, 2 * ro + 30, 2.0, 70)
        col += _box(mx - ro - 16, my, z, 14, 26, 50)
        collars.append(col)
        for oz in (-14, 14):
            cbolts.append(_ycyl(mx - ro - 16, my, z + oz, 3.5, 40)
                          + Pos(mx - ro - 16, my - 20, z + oz) * Rot(90, 0, 0) * extrude(RegularPolygon(6.4, 6), amount=5))
    add("Standoff pipes (DN25, galvanized)", _fuse(pipes), C_GALV, "metal", 1, "accessory", (150, 0, 0))
    add("Standoff wall plates", _fuse(plates), C_GALV, "metal", 1, "accessory", (-160, 0, 0))
    add("Wall plate anchors", _fuse(anchors), C_STEEL, "metal", 16, "accessory", (-120, 0, 0))
    add("Mast clamp collars", _fuse(collars), C_GALV, "metal", 1, "accessory", (60, 0, 0))
    add("Collar bolts", _fuse(cbolts), C_STEEL, "metal", 16, "accessory", (60, 0, 0))

    # ================================================================ temperature and humidity shield (BOM 5)
    tz = P["trh_z"] + MAST_DZ
    plates5 = None
    for k in range(5):
        pz_ = tz + k * 22
        pl = Pos(mx + 90, my, pz_ - 3) * Cone(55, 47, 6)
        if k < 4:
            pl -= _zcyl(mx + 90, my, pz_, 30, 10)
        plates5 = pl if plates5 is None else plates5 + pl
    plates5 = plates5 + _fuse(_zcyl(mx + 90 + 42 * math.cos(math.radians(a)), my + 42 * math.sin(math.radians(a)),
                                    tz + 44, 3.0, 100) for a in (0, 120, 240))
    add("Radiation shield (five plates)", plates5, C_WHITE, "plastic", 5, "accessory", (160, 0, 0))
    tarm = _xcyl((mx + ro + mx + 90) / 2, my, tz + 40, 6.0, 90 - ro) + _zcyl(mx + ro + 4, my, tz + 40, 12, 30)
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
    loc = Pos(mx, my - 200, pzc) * Rot(-tilt, 0, 0)
    add("Solar panel frame", loc * frame, C_ALU, "metal", 9, "accessory", (0, -260, 0))
    add("Solar cells", loc * cells, C_CELL, "screen", 9, "accessory", (0, -260, 0))
    add("Cell busbars", loc * grid, "#C9CED6", "metal", 9, "accessory", (0, -260, 0))
    add("Panel junction box", loc * jbox, C_BLACK, "plastic", 9, "accessory", (0, -260, 0))
    parm = _ycyl(mx, my - (ro + 150) / 2 - 10, pzc, 10.0, 150 - ro) + _ycyl(mx, my - ro - 8, pzc, 13.0, 30)
    add("Panel arm and clamp", parm, C_DARK, "painted", 9, "accessory", (0, -140, 0))

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

    # contents at their model.py offsets from the box centre
    EI = (150, -600, 0)
    add("Controller board", _box(gcx - 30, gcy - 40, gcz + 90, 3, 160, 110), C_PCB, "plastic", 6, "accessory", EI)
    comp = _box(gcx - 24, gcy - 70, gcz + 110, 9, 40, 40) + _box(gcx - 26, gcy + 10, gcz + 70, 5, 30, 20) \
        + _box(gcx - 25, gcy - 20, gcz + 50, 7, 60, 14)
    add("Controller module and drivers", comp, C_CHIP, "plastic", 6, "accessory", EI)
    bat = _box(gcx + 10, gcy + 20, gcz - 110, *P["battery"])
    bat = _fillet_try(bat, bat.edges(), [4.0, 2.0])
    add("Battery, 12.8 V 10 Ah LiFePO4", bat, C_BATT, "plastic", 8, "accessory", (240, -600, 0))
    blab = _box(gcx + 10 + P["battery"][0] / 2 + 0.2, gcy + 20, gcz - 110, 0.4, 110, 50)
    add("Battery label", blab, C_LABEL, "paper", 8, "accessory", (240, -600, 0))
    rel = _box(gcx - 30, gcy + 100, gcz + 90, 25, 50, 60)
    rel = _fillet_try(rel, rel.edges(), [2.0, 1.0])
    add("Pump-start relay", rel, C_RELAY, "plastic", 12, "accessory", EI)

    # ================================================================ valves and transducer (BOM 10, 11)
    vxm = D["riser_xpos"] - 120
    vys = (gcy - 130, gcy + 130)
    man = _ycyl(vxm, gcy, VALVE_Z, 14, 420)
    for yy in (gcy - 210, gcy + 210):
        man += _ycyl(vxm, yy, VALVE_Z, 17, 12)
    add("Manifold and hose connectors", man, C_BRASS, "metal", 10, "accessory", (0, -600, -140))
    vb = None
    coils = None
    for yy in vys:
        b = _box(vxm, yy, VALVE_Z, 80, 110, 70)
        b = _fillet_try(b, b.edges(), [6.0, 3.0])
        vb = b if vb is None else vb + b
        c = _zcyl(vxm, yy, VALVE_Z + 65, 24, 60)
        c = _fillet_try(c, _top(c), [5.0, 3.0])
        coils = c if coils is None else coils + c
    add("Zone valve bodies A and B", vb, C_DARK, "plastic", 10, "accessory", (0, -600, -140))
    add("Zone valve coils (12 V)", coils, C_BLACK, "plastic", 10, "accessory", (0, -600, -90))
    xd = _zcyl(vxm, gcy, VALVE_Z + 45, 14, 80) + _zcyl(vxm, gcy, VALVE_Z + 95, 18, 20)
    xd = _fillet_try(xd, _top(xd), [4.0, 2.0])
    xd += _hex_z(vxm, gcy, VALVE_Z + 22, 22.0, 10.0)
    add("Pressure transducer", xd, C_STEEL, "metal", 11, "accessory", (0, -600, -60))

    # ================================================================ spray line on the front gutter lip (BOM 14)
    ly, lz = s * D["lip_y"], D["line_z"]
    r = P["line_od"] / 2
    rx = D["riser_xpos"]
    z_rc = lz - RISER_SHOWN
    line = _pipe([(LINE_X0, ly, lz), (rx, ly, lz), (rx, ly, z_rc)], r)
    line += _zcyl(rx, ly, z_rc + 12, r + 3, 24) + Pos(LINE_X0, ly, lz) * Rot(0, 90, 0) * Cylinder(r + 2.5, 20)
    add("Spray line (16 mm polyethylene)", line, C_LINE, "plastic", 14, "accessory", (0, -120, 0))
    heads = [hx for hx in D["head_x"] if LINE_X0 < hx < rx]
    hs, caps = None, None
    for hx in heads:
        h = _zcyl(hx, ly, lz + 12, 3.5, 24) + _zcyl(hx, ly, lz + 30, 10.0, 16.0)
        h = _fillet_try(h, _top(h), [2.0, 1.0])
        h += _zcyl(hx, ly, lz + 48, 2.5, 20) + _zcyl(hx, ly, lz + 60, 12, 5)
        hs = h if hs is None else hs + h
        cp = _zcyl(hx, ly, lz + 66, 7, 8)
        cp = _fillet_try(cp, _top(cp), [2.5, 1.5])
        caps = cp if caps is None else caps + cp
    add("Micro-sprinkler head", hs, C_DARK, "plastic", 14, "accessory", (0, -120, 80))
    add("Sprinkler spinner cap", caps, C_ACCENT, "plastic", 14, "accessory", (0, -120, 80))
    clips = None
    for xq in (5420.0, 5850.0, 6150.0):
        c = _box(xq, ly - 2, lz - 14, 16, 22, 50) - _xcyl(xq, ly, lz, r + 0.5, 20) \
            - _box(xq, ly + 4, lz - 30, 20, 10, 20)
        c = _fillet_try(c, _edges_par(c, Axis.X), [1.5, 0.8])
        clips = c if clips is None else clips + c
    add("Gutter-lip clips", clips, C_BLACK, "plastic", 14, "accessory", (0, -120, 0))

    # ================================================================ cables (BOM 13)
    zc = gcz - bh / 2 - 45                                     # cable run just below the ground unit
    zs = P["standoff_z"][0] + MAST_DZ - 40                    # cable run under the lower standoff
    mcab = _pipe([(mx, my + 36, zt - 30), (mx, my + 36, zs), (L2 + 60, my + 36, zs), (L2 + 60, my + 36, zc),
                  (gcx, my + 36, zc), (gcx, gcy - 110, zc), (gcx, gcy - 110, gcz - bh / 2 - 12)], 5.0)
    add("Mast cable", mcab, C_BLACK, "rubber", 13, "accessory", (0, 0, 0))
    ties = _fuse(_zcyl(mx, my, z, ro + 2, 8) + _box(mx, my + 20, z, 2 * ro + 4, 40, 8) + _zcyl(mx, my + 36, z, 7.5, 8)
                 - _zcyl(mx, my, z, ro - 1, 10) - _zcyl(mx, my + 36, z, 4.5, 10)
                 for z in (z0 + 700, z0 + 1150, z0 + 2000, zt - 150))
    add("Cable ties", ties, C_BLACK, "plastic", 16, "accessory", (0, 0, 0))
    zu = D["gut_z0"] - 40
    route = [(gx, cy, cz - pz / 2 - 15), (gx, cy, zu), (L2 + 30, cy, zu), (L2 + 30, -4000 - 12, zu),
             (L2 + 30, -4000 - 12, zc + 20), (L2 + 30, gcy - 40, zc + 20), (gcx, gcy - 40, zc + 20),
             (gcx, gcy - 40, gcz - bh / 2 - 12)]
    pcab = _pipe(route, 4.5)
    add("Pod cable", pcab, C_BLACK, "rubber", 13, "accessory", (0, 0, 0))
    sleeve = _pipe([(gx, cy, cz - pz / 2 - 18), (gx, cy, zu), (gx - 420, cy, zu)], 7.5)
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
