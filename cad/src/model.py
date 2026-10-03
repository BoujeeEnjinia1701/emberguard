"""EmberGuard parametric model (build123d), TRL 3 revision 3: constructable design (EGD-DDR-003).

Run from the repo root:
    python cad/src/model.py            export STEP and STL into cad/step and cad/stl
    python cad/src/model.py --check    run the constructability checks and print the table

Exports:
    emberguard-kit.step / .stl        every kit part in its installed position on the reference house
    mast-assembly.step / .stl         mast, wall plates, flanges, standoffs, crossover plates, U-bolts, sensors, panel
    sensor-pod.step / .stl            one gutter-corner sensor pod with its snout, gland, hood, pod plate, arm and cleat
    ground-unit.step / .stl           steel enclosure and contents, valve board, manifold, valves and transducer
    reference-house.step / .stl       the 12 x 8 m reference house (context only, not in the BOM)

Axes (mm): X along the ridge (east is +X), Y across the house (front eave at -Y), Z up from the
ground. The house is centred on the origin; the east gable wall is the plane x = 6,000 and the
east verge (the end of the roof overhang) is the plane x = 6,500.

Revision 3 makes the concept buildable (EGD-DDR-003, made under Amish's 2026-09-30 instruction
to make the design physically buildable; open for his review). Each part is a Comp with a plain
name, a BOM line, a colour and whether it is made or bought. build_components() returns them
keyed by name; build_parts() groups them by BOM line for the calculations, the drawing and the
concept media, which import PARAMS, derived(), sensor_axes() and house_parts() as before.
"""
import math
import sys
from dataclasses import dataclass
from pathlib import Path

# Top-level parameters (mm, degrees). Edit these, not the geometry below.
PARAMS = {
    # reference house (context, EGD-REQ-001)
    "house_l": 12000.0, "house_d": 8000.0, "wall_h": 2700.0,
    "pitch": 22.0, "overhang": 500.0, "roof_t": 200.0,
    "fascia_t": 25.0, "fascia_h": 200.0,
    "gutter_w": 120.0, "gutter_h": 100.0, "gutter_drop": 130.0,   # gutter top 30 mm below the roof underside at the eave
    # 1 mast, wall plates, slip-on flanges, standoffs and crossover plates
    "mast_off": 700.0,            # mast axis from the gable wall
    "mast_od": 40.0, "mast_wall": 2.0,           # 6061-T6 aluminium tube
    "mast_z0": 2250.0, "mast_z1": 4700.0,
    "standoff_z": (2450.0, 3900.0),
    "standoff_od": 33.7, "standoff_wall": 3.2,  # DN25 galvanized pipe
    "wall_plate": (8.0, 140.0, 140.0),          # aluminium plate: thickness, width (Y), height (Z)
    "flange": (105.0, 8.0, 48.0, 40.0),         # slip-on base flange for 33.7 tube: disc dia, disc t, hub dia, hub length
    "xplate": (100.0, 6.0, 100.0),              # crossover plate: X, thickness (Y), Z
    "ub_d": 8.0,                                # U-bolt rod diameter (M8)
    "standoff_past": 50.0,                      # standoff pipe runs this far past the mast axis
    # 2 sensor pods at the east gutter corners (one per gutter), with hoods and brackets
    "pod_out": 200.0,             # pod centre beyond the east end of the gutter (+X)
    "pod_above_lip": 500.0,       # pod centre above the gutter lip, over the gutter centreline
    "pod": (100.0, 80.0, 70.0),   # x, y, z outside (body 64 tall plus a 6 mm lid)
    "pod_wall": 4.0, "pod_lid": 6.0,
    "pod_hood": (150.0, 130.0, 6.0),            # hood plan size; the hood is 1 mm sheet with 10 mm drip flanges
    "hood_gap": 15.0,                           # spacers between the lid and the hood
    "can_hole": 9.5,                            # window in the west wall for the sensor's 9.2 mm can
    "lens_hood": (28.0, 18.0, 20.0),            # lens hood inside width, height and depth (clears 55 x 35 degrees)
    "pod_plate": (120.0, 70.0, 6.0),
    "pod_bolt_sp": 60.0,                        # the two M6 bolts under the pod, along its axis
    "pod_plate_z": 2918.0,                      # top of the pod plate
    "bar": (40.0, 6.0),                         # pod arm flat bar: width, thickness
    "cleat": (80.0, 6.0, 140.0),                # verge cleat: angle leg, thickness, length (along Y)
    "cleat_y": 4400.0, "cleat_top": 2700.0,     # cleat centre (|Y|) and the top of its outstanding leg
    "arm_q": (6530.0, 4400.0),                  # where the arm line starts on the cleat (x, |y|)
    # 3 thermal sensors (MLX90640, 55 x 35 degree lens, 32 x 24 pixels), one in each pod
    "aim_yaw": 10.0,              # degrees off the gutter line, toward the house
    "aim_down": 5.0,              # degrees below horizontal
    "fov_h": 55.0, "fov_v": 35.0, "px_h": 32, "px_v": 24,
    # gutter hangers (context, for the line-of-sight check): straps across the gutter top
    "hanger_pitch": 750.0, "hanger_w": 25.0,
    # 4 anemometer and vane
    "arm_z": 5000.0, "arm_half": 230.0,
    # 5 temperature and humidity shield
    "trh_z": 3300.0,
    # 9 solar panel (faces the equator side, -Y)
    "panel": (350.0, 250.0, 22.0), "panel_tilt": 45.0, "panel_z": 3600.0, "panel_arm_z": 3560.0,
    # ground unit (7 enclosure with 6, 8, 12 inside; 15 on it)
    "box": (160.0, 320.0, 400.0), "box_z": 1150.0, "box_y": -1800.0, "box_wall": 2.0, "lug_t": 2.0,
    "battery": (98.0, 151.0, 95.0),             # 12.8 V 10 Ah LiFePO4 (EGD-DDR-002, O5)
    # 18 sun shade over the enclosure: folded white 1 mm sheet on two bent flat-bar arms (decided 2026-10-02, EGD-DEC-001)
    "shade": (360.0, 440.0, 1.0),               # plate depth (X, out from the wall), width (Y), sheet thickness
    "shade_z": 1480.0, "shade_x0": 3.0,         # top of the plate; plate starts this far off the wall
    "shade_flap": (100.0, 100.0),               # front flap and side flaps hang this far below the plate
    "shade_arm": (40.0, 6.0, 40.0),             # arm flat bar: width, thickness, wall tab length (6063 flat bar, as the pod arm)
    "shade_arm_dy": 120.0,                      # arms this far either side of the enclosure centre line
    # 10 valves and 11 transducer on a manifold on a valve board
    "manifold_z": 520.0, "valve_y": (-2100.0, -1500.0), "man_x": 6048.0,
    "valve_board": (3.0, 1100.0, 270.0), "valve_board_c": (-1800.0, 465.0),
    # 14 spray lines
    "line_od": 16.0, "line_id": 13.2,
    "heads_per_eave": 6, "head_pitch": 2200.0, "line_above_lip": 30.0,
    "line_out": 20.0,             # eave line centre this far outboard of the gutter lip
    "riser_x": 12.0,              # risers run up the gable wall, centre this far off it
    "riser_y": 3975.0,            # riser climbs the gable wall this far from the centre line (25 mm in from the corner)
    "riser_low_z": 250.0, "under_z": 2300.0,    # run along the wall base; cross under the gutter at this height
    "cable_y": 3940.0,            # pod cables come down the gable wall here
}


def derived(p=PARAMS):
    """Dimensions that follow from PARAMS. Used by the calcs, the drawing and the media."""
    T = math.tan(math.radians(p["pitch"]))
    c = math.cos(math.radians(p["pitch"]))
    half_d = p["house_d"] / 2
    eave_y = half_d + p["overhang"]
    eave_z = p["wall_h"] - p["overhang"] * T                  # roof underside at the eave edge
    ridge_under = p["wall_h"] + half_d * T                    # roof underside at the ridge
    ridge_top = ridge_under + p["roof_t"] / c                 # roof surface at the ridge
    eave_top = eave_z + p["roof_t"] / c                       # roof surface at the eave edge
    roof_len = p["house_l"] + 2 * p["overhang"]
    gut_z0 = eave_z - p["gutter_drop"]
    lip_y = eave_y + p["fascia_t"] + p["gutter_w"] - 4
    lip_z = gut_z0 + p["gutter_h"]
    L2 = p["house_l"] / 2
    mast_x = L2 + p["mast_off"]
    line_z = lip_z + p["line_above_lip"]
    line_y = lip_y + p["line_out"]
    n = p["heads_per_eave"]
    head_x = [(i - (n - 1) / 2) * p["head_pitch"] for i in range(n)]
    wx = L2 + p["riser_x"]
    v_out = p["manifold_z"] - 13.45 - 31 - 70 - 10             # valve outlet, below the tee branch and valve body
    zone_len = []
    for s, vy in zip((-1, 1), p["valve_y"]):
        riser = (v_out - 300) + math.hypot(p["man_x"] - wx, 300 - p["riser_low_z"]) \
            + abs(s * p["riser_y"] - vy) + (p["under_z"] - p["riser_low_z"]) \
            + (line_y - p["riser_y"]) + (line_z - p["under_z"])
        zone_len.append(riser + (wx + roof_len / 2))
    bx = p["box"][0]
    return {
        "T": T, "eave_y": eave_y, "eave_z": eave_z, "eave_top": eave_top, "ridge_under": ridge_under,
        "ridge_top": ridge_top, "roof_len": roof_len, "gut_z0": gut_z0, "lip_y": lip_y, "lip_z": lip_z,
        "mast_x": mast_x, "line_z": line_z, "line_y": line_y, "head_x": head_x, "zone_len": zone_len,
        "riser_xpos": p["man_x"], "wall_x": wx, "v_out": v_out,
        "gut_yc": eave_y + p["fascia_t"] + p["gutter_w"] / 2,
        "pod_x": roof_len / 2 + p["pod_out"], "pod_z": gut_z0 + p["gutter_h"] + p["pod_above_lip"],
        "mast_len": p["mast_z1"] - p["mast_z0"],
        "standoff_y": p["mast_od"] / 2 + p["xplate"][1] + p["standoff_od"] / 2,
        "box_c": (L2 + p["lug_t"] + bx / 2, p["box_y"], p["box_z"]),
        "verge_x": roof_len / 2,
    }


def sensor_axes(p=PARAMS, side=-1):
    """Sensor position and unit aim vector for the pod watching the front (-1) or back (+1) gutter.

    The pod sits over the gutter centreline beyond the east end of the gutter and looks west (-X)
    along it, yawed slightly toward the house so the roof edge strip is also in view."""
    D = derived(p)
    yw, dn = math.radians(p["aim_yaw"]), math.radians(p["aim_down"])
    d = (-math.cos(dn) * math.cos(yw), -side * math.cos(dn) * math.sin(yw), -math.sin(dn))
    pos = (D["pod_x"] - p["pod"][0] / 2, side * D["gut_yc"], D["pod_z"])
    return pos, d


# ---------------- geometry helpers ----------------

def tube(a, b, r):
    from build123d import Solid, Plane, Vector
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def pipe(a, b, ro, ri):
    """Hollow tube from a to b."""
    from build123d import Solid, Plane, Vector
    a = Vector(*a); b = Vector(*b); d = b - a
    pl = Plane(origin=a, z_dir=d.normalized())
    return Solid.make_cylinder(ro, d.length, pl) - Solid.make_cylinder(ri, d.length, pl)


def path(points, r):
    from build123d import Pos, Sphere
    s = None
    for a, b in zip(points[:-1], points[1:]):
        t = tube(a, b, r)
        s = t if s is None else s + t
    for q in points[1:-1]:
        s = s + Pos(*q) * Sphere(r)
    return s


def fuse(shapes):
    out = None
    for s in shapes:
        if s is None:
            continue
        out = s if out is None else out + s
    return out


def box(c, size):
    from build123d import Box, Pos
    return Pos(*c) * Box(*size)


def ubolt(center, axis, around, r_in, d, leg, legs_dir):
    """U-bolt round a pipe. center: pipe axis point; axis: 'x','y' or 'z' (pipe direction);
    around: unit vector from the pipe axis toward the bend (the side the U wraps); legs_dir is
    the opposite way, where the legs run (length leg from the pipe axis). r_in: inside radius."""
    from build123d import Torus, Box, Pos, Plane, Vector, Solid
    rr = r_in + d / 2
    c = Vector(*center)
    a = {"x": Vector(1, 0, 0), "y": Vector(0, 1, 0), "z": Vector(0, 0, 1)}[axis]
    u = Vector(*around).normalized()
    w = a.cross(u)
    pl = Plane(origin=c, x_dir=u, z_dir=a)
    tor = pl * Torus(rr, d / 2)
    half = pl * Pos(rr + d, 0, 0) * Box(2 * (rr + d), 4 * (rr + d), 4 * d)
    bend = tor & half
    legs = None
    for sgn in (-1, 1):
        p0 = c + w * (sgn * rr)
        p1 = p0 - u * leg
        t = tube(tuple(p0), tuple(p1), d / 2)
        legs = t if legs is None else legs + t
    return bend + legs


@dataclass
class Comp:
    name: str
    shape: object
    bom: int
    color: str
    made: bool = False


# ---------------- reference house (context) ----------------

def house_parts(p=PARAMS):
    """Reference house envelopes: walls with gables, roof, fascia and gutters. No BOM numbers."""
    from build123d import Box, Pos, Rot, Vector
    D = derived(p)
    L, Dp, H = p["house_l"], p["house_d"], p["wall_h"]
    pit = math.radians(p["pitch"])
    walls = Pos(0, 0, H / 2) * Box(L, Dp, H)
    big = 20000.0
    gable = Pos(0, 0, H + (D["ridge_under"] - H) / 2) * Box(L, Dp, D["ridge_under"] - H)
    for s in (-1, 1):
        n = Vector(0, s * math.sin(pit), math.cos(pit))
        cc = Vector(0, s * Dp / 2, H) + n * (big / 2)
        gable = gable - Pos(cc.X, cc.Y, cc.Z) * Rot(-s * p["pitch"], 0, 0) * Box(L + 10, big, big)
    roof = None
    slab_len = D["eave_y"] / math.cos(pit)
    for s in (-1, 1):
        yc = s * D["eave_y"] / 2
        zu = H + (Dp / 2 - D["eave_y"] / 2) * D["T"]
        slab = Pos(0, yc + s * (p["roof_t"] / 2) * math.sin(pit), zu + (p["roof_t"] / 2) * math.cos(pit)) \
            * Rot(-s * p["pitch"], 0, 0) * Box(D["roof_len"], slab_len, p["roof_t"])
        roof = slab if roof is None else roof + slab
    fascia, gutters = None, None
    gw, gh = p["gutter_w"], p["gutter_h"]
    for s in (-1, 1):
        f = Pos(0, s * (D["eave_y"] + p["fascia_t"] / 2), D["eave_z"] - p["fascia_h"] / 2 + 40) \
            * Box(D["roof_len"], p["fascia_t"], p["fascia_h"])
        yc = s * (D["eave_y"] + p["fascia_t"] + gw / 2)
        g = Pos(0, yc, D["gut_z0"] + gh / 2) * Box(D["roof_len"], gw, gh) \
            - Pos(0, yc, D["gut_z0"] + gh / 2 + 8) * Box(D["roof_len"] + 10, gw - 8, gh)
        fascia = f if fascia is None else fascia + f
        gutters = g if gutters is None else gutters + g
    return {"walls": walls + gable, "roof": roof, "fascia_gutters": fascia + gutters}


# ---------------- 1, 4, 5, 9, 13, 17: the mast and what it carries ----------------

def mast_components(p=PARAMS):
    from build123d import Box, Cylinder, Pos, Rot, Sphere, Torus
    D = derived(p)
    mx, L2 = D["mast_x"], p["house_l"] / 2
    ro, ri = p["mast_od"] / 2, p["mast_od"] / 2 - p["mast_wall"]
    sy = D["standoff_y"]
    so = p["standoff_od"] / 2
    wt, ww, wh = p["wall_plate"]
    fd, ft, hd, hl = p["flange"]
    xl, xt, xh = p["xplate"]
    ud = p["ub_d"]
    C = {}

    # mast tube with two 12 mm grommet holes for the sensor leads, and an end cap with a cable grommet
    mast = pipe((mx, 0, p["mast_z0"]), (mx, 0, p["mast_z1"]), ro, ri)
    for (hx, hy), hz in (((1, 0), p["trh_z"] + 170), ((0, -1), p["panel_arm_z"] - 60)):
        mast = mast - tube((mx, 0, hz), (mx + hx * 30, hy * 30, hz), 6)
    C["mast"] = Comp("Mast tube", mast, 1, "#94A3B8", True)
    cap = Pos(mx, 0, p["mast_z0"] - 4) * Cylinder(ro + 1.5, 8) - Pos(mx, 0, p["mast_z0"] - 4) * Cylinder(7, 10)
    cap = cap + (Pos(mx, 0, p["mast_z0"] + 5) * (Cylinder(ri, 10) - Cylinder(ri - 1.5, 10)))
    C["mast_cap"] = Comp("Mast end cap with grommet", cap, 16, "#1F2937")

    wall_plates, flanges, pipes, xplates, ubs, nuts = [], [], [], [], [], []
    for z in p["standoff_z"]:
        # wall plate on the gable wall, slip-on flange bolted to it, standoff pipe in the flange
        wp = box((L2 + wt / 2, sy, z), (wt, ww, wh))
        for dy in (-50, 50):
            for dz in (-50, 50):
                wp = wp - tube((L2 - 1, sy + dy, z + dz), (L2 + wt + 1, sy + dy, z + dz), 5.5)
        for a in range(4):
            t = math.radians(45 + 90 * a)
            wp = wp - tube((L2 - 1, sy + 40 * math.cos(t), z + 40 * math.sin(t)),
                           (L2 + wt + 1, sy + 40 * math.cos(t), z + 40 * math.sin(t)), 4.5)
        wall_plates.append(wp)
        fl = tube((L2 + wt, sy, z), (L2 + wt + ft, sy, z), fd / 2) + tube((L2 + wt + ft, sy, z), (L2 + wt + ft + hl, sy, z), hd / 2)
        fl = fl - tube((L2 + wt + 3, sy, z), (L2 + wt + ft + hl + 1, sy, z), so)
        for a in range(4):
            t = math.radians(45 + 90 * a)
            fl = fl - tube((L2 + wt - 1, sy + 40 * math.cos(t), z + 40 * math.sin(t)),
                           (L2 + wt + ft + 1, sy + 40 * math.cos(t), z + 40 * math.sin(t)), 4.5)
        flanges.append(fl)
        x_end = mx + p["standoff_past"]
        pipes.append(pipe((L2 + wt + 3, sy, z), (x_end, sy, z), so, so - p["standoff_wall"]))
        # crossover plate between mast and standoff; two U-bolts round each
        xp = box((mx, ro + xt / 2, z), (xl, xt, xh))
        holes = [(-(ro + ud / 2), 30), ((ro + ud / 2), 30), (-(ro + ud / 2), -30), ((ro + ud / 2), -30),
                 (-35, so + ud / 2), (-35, -(so + ud / 2)), (35, so + ud / 2), (35, -(so + ud / 2))]
        for hx, hz in holes:
            xp = xp - tube((mx + hx, ro - 1, z + hz), (mx + hx, ro + xt + 1, z + hz), ud / 2 + 0.5)
        xplates.append(xp)
        for dz in (30, -30):            # round the mast, legs out through the plate to the +Y side
            ubs.append(ubolt((mx, 0, z + dz), "z", (0, -1, 0), ro, ud, ro + xt + 14, None))
            for sx in (-1, 1):
                nuts.append(Pos(mx + sx * (ro + ud / 2), ro + xt + 3.25, z + dz) * Rot(90, 0, 0) * Cylinder(7.5, 6.5))
        for dx in (35, -35):            # round the standoff, legs out through the plate to the -Y side
            ubs.append(ubolt((mx + dx, sy, z), "x", (0, 1, 0), so, ud, sy - ro + 14, None))
            for sz in (-1, 1):
                nuts.append(Pos(mx + dx, ro - 3.25, z + sz * (so + ud / 2)) * Rot(90, 0, 0) * Cylinder(7.5, 6.5))
    C["wall_plates"] = Comp("Wall plates (2)", fuse(wall_plates), 1, "#A8A29E", True)
    C["flanges"] = Comp("Slip-on base flanges (2)", fuse(flanges), 1, "#57534E")
    C["standoffs"] = Comp("Standoff pipes (2)", fuse(pipes), 1, "#78716C", True)
    C["xplates"] = Comp("Crossover plates (2)", fuse(xplates), 1, "#1D4ED8", True)
    C["ubolts"] = Comp("U-bolts (8) with nyloc nuts", fuse(ubs + nuts), 1, "#111827")
    anchors = []
    for z in p["standoff_z"]:
        for dy in (-50, 50):
            for dz in (-50, 50):
                anchors.append(tube((L2 + wt, sy + dy, z + dz), (L2 + wt + 7, sy + dy, z + dz), 8.5))
    C["wall_anchors"] = Comp("Wall anchors (8)", fuse(anchors), 16, "#111827")

    # 4 anemometer and vane on a crossarm, on a sleeve over the mast top
    az, ah = p["arm_z"], p["arm_half"]
    sleeve = Pos(mx, 0, p["mast_z1"] - 5) * Cylinder(ro + 6, 70) - Pos(mx, 0, p["mast_z1"] - 15) * Cylinder(ro + 0.25, 70)
    anem = sleeve + tube((mx, 0, p["mast_z1"] + 30), (mx, 0, az), 10) + tube((mx, -ah, az), (mx, ah, az), 9)
    anem = anem + tube((mx, -ah, az), (mx, -ah, az + 90), 6) + Pos(mx, -ah, az + 90) * Cylinder(16, 24)
    for k in range(3):
        t = math.radians(k * 120 + 20)
        cx, cy = mx + 90 * math.cos(t), -ah + 90 * math.sin(t)
        anem = anem + tube((mx, -ah, az + 90), (cx, cy, az + 90), 3) + Pos(cx, cy, az + 90) * Sphere(26)
    anem = anem + tube((mx, ah, az), (mx, ah, az + 90), 6) + Pos(mx - 80, ah, az + 90) * Box(170, 4, 90) \
        + Pos(mx + 80, ah, az + 90) * Sphere(14)
    C["anem"] = Comp("Anemometer and wind vane on the mast-top sleeve", anem, 4, "#1F2937")

    # 5 temperature and humidity sensor: shield plates on a centre rod, arm and mast clamp
    tz = p["trh_z"]
    plates = fuse(Pos(mx + 90, 0, tz + k * 22) * (Cylinder(55, 6) - Cylinder(5, 8)) for k in range(5))
    rod = tube((mx + 90, 0, tz - 10), (mx + 90, 0, tz + 125), 5)
    clamp = Pos(mx, 0, tz + 125) * (Cylinder(ro + 6, 30) - Cylinder(ro, 32))
    arm = tube((mx + ro + 6, 0, tz + 125), (mx + 95, 0, tz + 125), 6)
    C["trh"] = Comp("Temperature and humidity shield, arm and clamp", plates + rod + clamp + arm, 5, "#F5F5F4")

    # 9 solar panel facing the equator side (-Y), on a clamp, arm and tilt rail
    pw, ph_, pt = p["panel"]
    tilt = math.radians(p["panel_tilt"])
    pc = (mx, -200.0, p["panel_z"])
    nb = (0.0, math.sin(tilt), -math.cos(tilt))           # unit normal out of the panel back
    inpl = (0.0, -math.sin(tilt), -math.cos(tilt))         # down the slope, away from the mast
    panel = Pos(*pc) * Rot(p["panel_tilt"], 0, 0) * Box(pw, ph_, pt)
    za = p["panel_arm_z"]
    # where a horizontal line at za meets the panel back plane
    back = [pc[i] + pt / 2 * nb[i] for i in range(3)]
    tpar = (back[2] - za) / (-inpl[2])
    hit = [back[i] + tpar * inpl[i] for i in range(3)]
    rail_c = [hit[i] + 2.0 * nb[i] for i in range(3)]
    rail = Pos(*rail_c) * Rot(p["panel_tilt"], 0, 0) * Box(200, 40, 4)
    pclamp = Pos(mx, 0, za) * (Cylinder(ro + 6, 30) - Cylinder(ro, 32))
    # rail back face: y = yb0 + (z - zb0) on the panel's 45 degree slope; the hinge block's top edge meets it
    rb = [rail_c[i] + 2.0 * nb[i] for i in range(3)]
    y_touch = rb[1] + (za + 8 - rb[2]) / math.tan(tilt)
    y_arm = -190.0
    parm = box((mx, (-(ro + 4) + y_arm) / 2, za), (20, abs(y_arm + ro + 4), 20))
    hinge = box((mx, (y_arm + y_touch) / 2, za), (36, abs(y_touch - y_arm), 16))
    C["panel"] = Comp("Solar panel, 10 W", panel, 9, "#1E3A8A")
    C["panel_mount"] = Comp("Panel clamp, arm and tilt rail", pclamp + parm + hinge + rail, 9, "#475569")
    return C


# ---------------- 2, 3: sensor pods ----------------

def _pod_xf(p, side):
    """Transform from pod coordinates (origin at the pod centre, +X east, level) to the house."""
    from build123d import Pos, Rot
    D = derived(p)
    return Pos(D["pod_x"], side * D["gut_yc"], D["pod_z"]) * Rot(0, 0, side * p["aim_yaw"]) * Rot(0, -p["aim_down"], 0)


def _pod_pt(p, side, local):
    """A pod-coordinate point in house coordinates."""
    from build123d import Vector
    loc = _pod_xf(p, side).position
    ry = math.radians(-p["aim_down"]); rz = math.radians(side * p["aim_yaw"])
    x, y, z = local
    # rotate about Y (pitch), then about Z (yaw)
    x1 = x * math.cos(ry) + z * math.sin(ry); z1 = -x * math.sin(ry) + z * math.cos(ry); y1 = y
    x2 = x1 * math.cos(rz) - y1 * math.sin(rz); y2 = x1 * math.sin(rz) + y1 * math.cos(rz)
    return (loc.X + x2, loc.Y + y2, loc.Z + z1)


def arm_frame(p=PARAMS, side=-1):
    """The pod arm runs in a straight line from the cleat to below the pod centre."""
    D = derived(p)
    qx, qy = p["arm_q"][0], side * p["arm_q"][1]
    dx, dy = D["pod_x"] - qx, side * D["gut_yc"] - qy
    L = math.hypot(dx, dy)
    return (qx, qy), (dx / L, dy / L), L


def pod_components(p=PARAMS, side=-1, local=False):
    """One sensor pod and its mount at the installed position. Keys end in _f (front) or _b (back).
    local=True draws the pod's own parts (box, lid, lens hood, hood, sensor, node board) level and
    centred on the origin, for the making sketches."""
    from build123d import Box, Cylinder, Pos, Rot, Plane, Vector
    D = derived(p)
    sfx = "f" if side < 0 else "b"
    xf = Pos(0, 0, 0) if local else _pod_xf(p, side)
    px, py, pz = p["pod"]
    w, lt = p["pod_wall"], p["pod_lid"]
    bh = pz - lt                                   # body height (64)
    zb0, zb1 = -pz / 2, -pz / 2 + bh               # body bottom and top in pod coordinates
    C = {}

    # body: die-cast box, drilled: sensor window and four tapped M2.5 holes west, cable gland hole east,
    # two M6 holes in the floor, two tapped M3 holes for the lens hood
    body = Pos(0, 0, (zb0 + zb1) / 2) * Box(px, py, bh) - Pos(0, 0, (zb0 + zb1) / 2 + w / 2) * Box(px - 2 * w, py - 2 * w, bh - w)
    body = body - tube((-px / 2 - 1, 0, 0), (-px / 2 + w + 1, 0, 0), p["can_hole"] / 2)
    for hy in (-10, 10):
        for hz in (-10, 10):
            body = body - tube((-px / 2 - 1, hy, hz), (-px / 2 + w + 1, hy, hz), 1.05)
    for hz in (-15, 15):
        body = body - tube((-px / 2 - 1, 0, hz), (-px / 2 + w + 1, 0, hz), 1.25)
    body = body - tube((px / 2 - w - 1, 0, -15), (px / 2 + 1, 0, -15), 8.1)
    sp = p["pod_bolt_sp"] / 2
    for bx_ in (-sp, sp):
        body = body - tube((bx_, 0, zb0 - 1), (bx_, 0, zb0 + w + 1), 3.25)
    lid = Pos(0, 0, zb1 + lt / 2) * Box(px, py, lt)
    for hx in (-35, 35):
        for hy in (-28, 28):
            lid = lid - tube((hx, hy, zb1 - 1), (hx, hy, zb1 + lt + 1), 1.65)
    C[f"pod_body_{sfx}"] = Comp("Pod box, drilled", xf * body, 2, "#0F766E")
    C[f"pod_lid_{sfx}"] = Comp("Pod lid", xf * lid, 2, "#115E59")

    # lens hood: 1 mm stainless, a short rectangular tube sized to the 55 x 35 degree view, two flanges
    hw, hh, hd = p["lens_hood"]                    # inside width (Y), inside height (Z), depth (X)
    x0, x1 = -px / 2 - hd, -px / 2 - 1
    lh = box(((x0 + x1) / 2, 0, hh / 2 + 0.5), (x1 - x0, hw + 2, 1)) + box(((x0 + x1) / 2, 0, -hh / 2 - 0.5), (x1 - x0, hw + 2, 1)) \
        + box(((x0 + x1) / 2, hw / 2 + 0.5, 0), (x1 - x0, 1, hh + 2)) + box(((x0 + x1) / 2, -hw / 2 - 0.5, 0), (x1 - x0, 1, hh + 2))
    for sg in (-1, 1):
        fl = box((-px / 2 - 0.5, 0, sg * (hh / 2 + 1 + 5.5)), (1, hw + 2, 11))
        fl = fl - tube((-px / 2 - 2, 0, sg * 15), (-px / 2 + 1, 0, sg * 15), 1.7)
        lh = lh + fl
    C[f"lens_hood_{sfx}"] = Comp("Lens hood", xf * lh, 2, "#475569", True)
    lhs = fuse(tube((-px / 2 - 1, 0, sg * 15), (-px / 2 - 3, 0, sg * 15), 2.75) for sg in (-1, 1))
    C[f"lens_hood_screws_{sfx}"] = Comp("Lens hood screws (2), M3", xf * lhs, 16, "#111827")
    # thermal sensor breakout on the inside of the west wall, can through the window, on 1 mm washers
    xi = -px / 2 + w                               # inside face of the west wall
    brd = box((xi + 1 + 0.8, 0, 0), (1.6, 25, 25))
    can = tube((-px / 2, 0, 0), (xi + 1, 0, 0), 4.6)
    wsh = fuse(tube((xi, hy, hz), (xi + 1, hy, hz), 2.5) for hy in (-10, 10) for hz in (-10, 10))
    C[f"sensor_{sfx}"] = Comp("Thermal array sensor on its breakout", xf * (brd + can + wsh), 3, "#C2410C")
    zf = zb0 + w                                   # inside floor
    nb = box((24, 0, zf + 12 + 0.8), (34, 40, 1.6)) + box((24, 0, zf + 12 + 1.6 + 2), (20, 14, 4))
    nst = fuse(tube((xx, yy, zf), (xx, yy, zf + 12), 1.6) for xx in (10, 38) for yy in (-16, 16))
    C[f"node_{sfx}"] = Comp("Pod node board on standoffs", xf * (nb + nst), 2, "#16A34A")
    # cable gland in the east wall
    cg = tube((px / 2, 0, -15), (px / 2 + 14, 0, -15), 11) - tube((px / 2 - 1, 0, -15), (px / 2 + 15, 0, -15), 4)
    cg = cg + (tube((px / 2 - w - 4, 0, -15), (px / 2 - w, 0, -15), 11) - tube((px / 2 - w - 5, 0, -15), (px / 2 - w + 1, 0, -15), 8.1))
    cg = cg + (tube((px / 2 - w, 0, -15), (px / 2, 0, -15), 8.0) - tube((px / 2 - w - 1, 0, -15), (px / 2 + 1, 0, -15), 4))
    C[f"cgland_{sfx}"] = Comp("Pod cable gland, M16", xf * cg, 2, "#1F2937")
    # hood: 1 mm sheet with 10 mm drip flanges, on four 15 mm spacers screwed into the lid
    hx_, hy_, _ = p["pod_hood"]
    hz0 = zb1 + lt + p["hood_gap"]
    top = box((-15, 0, hz0 + 0.5), (hx_, hy_, 1.0))
    flg = box((-15 - hx_ / 2 + 0.5, 0, hz0 - 4.5), (1.0, hy_, 10)) + box((-15 + hx_ / 2 - 0.5, 0, hz0 - 4.5), (1.0, hy_, 10)) \
        + box((-15, -hy_ / 2 + 0.5, hz0 - 4.5), (hx_, 1.0, 10)) + box((-15, hy_ / 2 - 0.5, hz0 - 4.5), (hx_, 1.0, 10))
    hood = top + flg
    for hx in (-35, 35):
        for hy in (-28, 28):
            hood = hood - tube((hx, hy, hz0 - 1), (hx, hy, hz0 + 2), 2.2)
    C[f"hood_{sfx}"] = Comp("Hood", xf * hood, 2, "#E5E7EB", True)
    hsp = fuse(tube((hx, hy, zb1 + lt), (hx, hy, hz0), 4) for hx in (-35, 35) for hy in (-28, 28))
    C[f"hood_spacers_{sfx}"] = Comp("Hood spacers (4) and M4 screws", xf * hsp, 2, "#374151")

    # spacers under the pod, pod plate, arm and cleat, in house coordinates
    zp = p["pod_plate_z"]
    pts = [_pod_pt(p, side, (bx_, 0, zb0)) for bx_ in (-sp, sp)]
    above = xf * Pos(0, 0, zb0 + 500) * Box(1000, 1000, 1000)          # everything above the pod's tilted floor
    spc = fuse(Pos(q[0], q[1], (zp + q[2] + 2) / 2) * Cylinder(6, q[2] + 2 - zp) for q in pts) - above
    bolts = fuse(Pos(q[0], q[1], (zp - p["pod_plate"][2] + q[2] + w + 4) / 2) * Cylinder(2.5, q[2] + w + 4 - (zp - p["pod_plate"][2])) for q in pts)
    bolts = bolts - (xf * Pos(0, 0, zb0 + w / 2) * Box(px, py, w) - fuse(xf * tube((bx_, 0, zb0 - 1), (bx_, 0, zb0 + w + 1), 3.25) for bx_ in (-sp, sp)))
    heads = fuse(xf * tube((bx_, 0, zb0 + w), (bx_, 0, zb0 + w + 4), 5) for bx_ in (-sp, sp))
    bolts = bolts + heads
    C[f"pod_spacers_{sfx}"] = Comp("Pod spacers and M6 bolts", spc + bolts, 2, "#111827")
    (qx, qy), (ux, uy), L = arm_frame(p, side)
    bw, bt = p["bar"]
    cxp, cyp = D["pod_x"], side * D["gut_yc"]
    yaw = side * p["aim_yaw"]
    plx, ply, plt = p["pod_plate"]
    plate = Pos(cxp, cyp, zp - plt / 2) * Rot(0, 0, yaw) * Box(plx, ply, plt)
    plate = plate - Pos(cxp, cyp, zp - plt / 2) * Cylinder(4.25, plt + 2)
    for q in pts:
        plate = plate - Pos(q[0], q[1], zp - plt / 2) * Cylinder(2.5, plt + 2)           # tapped M6
    # arc slot for the second arm bolt: radius 35 about the pivot, +-12 degrees about the arm line
    ang = math.atan2(uy, ux)
    for k in range(-12, 13, 2):
        a = ang + math.radians(k)
        plate = plate - Pos(cxp + 35 * math.cos(a), cyp + 35 * math.sin(a), zp - plt / 2) * Cylinder(3.25, plt + 2)
    C[f"pod_plate_{sfx}"] = Comp("Pod plate", plate, 2, "#0369A1", True)
    tb = L - 25.0
    zc = p["cleat_top"]
    zt = zp - plt                                  # top of the tab
    rot = math.degrees(ang)
    def seg(t0, t1, z0, z1):
        tm = (t0 + t1) / 2
        return Pos(qx + ux * tm, qy + uy * tm, (z0 + z1) / 2) * Rot(0, 0, rot) * Box(t1 - t0, bw, z1 - z0)
    armbar = seg(-10, tb, zc, zc + bt) + seg(tb - bt, tb, zc + bt, zt - bt) + seg(tb - bt, tb + 80, zt - bt, zt)
    for t in (10, 50):
        armbar = armbar - Pos(qx + ux * t, qy + uy * t, zc + bt / 2) * Cylinder(3.25, bt + 2)
    for t in (tb + 25, tb + 60):
        armbar = armbar - Pos(qx + ux * t, qy + uy * t, zt - bt / 2) * Cylinder(3.25 if t > tb + 30 else 4.25, bt + 2)
    C[f"arm_{sfx}"] = Comp("Pod arm", armbar, 2, "#B45309", True)
    cl, ct, clen = p["cleat"]
    vx = D["verge_x"]
    cy = side * p["cleat_y"]
    legA = box((vx + ct / 2, cy, zc - cl / 2), (ct, clen, cl))
    legB = box((vx + cl / 2, cy, zc - ct / 2), (cl, clen, ct))
    cleat = legA + legB
    for dy in (-40, 40):
        cleat = cleat - tube((vx - 1, cy + dy, zc - 45), (vx + ct + 1, cy + dy, zc - 45), 4.5)
    for t in (10, 50):
        cleat = cleat - Pos(qx + ux * t, qy + uy * t, zc - ct / 2) * Cylinder(3.25, ct + 2)
    C[f"cleat_{sfx}"] = Comp("Verge cleat", cleat, 2, "#7C2D12", True)
    # fixings: two coach screws into the verge, two M6 bolts arm to cleat, pivot M8 and slot M6
    fx = fuse(tube((vx + ct, cy + dy, zc - 45), (vx + ct + 6, cy + dy, zc - 45), 7) for dy in (-40, 40))
    for t in (10, 50):
        x_, y_ = qx + ux * t, qy + uy * t
        fx = fx + Pos(x_, y_, (zc - ct - 6 + zc + bt + 6) / 2) * Cylinder(3, 2 * ct + 2 * bt) \
            + Pos(x_, y_, zc + bt + 3) * Cylinder(5.5, 6) + Pos(x_, y_, zc - ct - 3) * Cylinder(5.5, 6)
    for t, r in ((tb + 25, 4), (tb + 60, 3)):
        x_, y_ = qx + ux * t, qy + uy * t
        fx = fx + Pos(x_, y_, (zt - bt - 6 + zp + 6) / 2) * Cylinder(r, zp + 6 - (zt - bt - 6)) \
            + Pos(x_, y_, zp + 3) * Cylinder(r + 2.5, 6) + Pos(x_, y_, zt - bt - 3) * Cylinder(r + 2.5, 6)
    C[f"pod_fix_{sfx}"] = Comp("Pod mount screws and bolts", fx, 16, "#111827")
    return C


def pod_cable_path(p=PARAMS, side=-1):
    """Pod cable: out of the east gland, down the arm, round the verge under the overhang, down the wall."""
    D = derived(p)
    (qx, qy), (ux, uy), L = arm_frame(p, side)
    g = _pod_pt(p, side, (p["pod"][0] / 2 + 14, 0, -15))
    vx = D["verge_x"]
    zc = p["cleat_top"]
    cy = side * p["cleat_y"]
    wy = side * p["cable_y"]
    nx, ny = -uy * side, ux * side                 # beside the bar, away from the house end
    t1 = L - 40
    soff = lambda y: p["wall_h"] - (abs(y) - p["house_d"] / 2) * D["T"] - 8 - 4.5   # just under the soffit # noqa: E731
    ye = side * (p["cleat_y"] + p["cleat"][2] / 2 + 8)            # just past the end of the cleat
    a0 = (qx + 28 * nx, qy + 28 * ny)
    pts = [g, (g[0] + 10, g[1], g[2] - 20), (qx + ux * t1 + 28 * nx, qy + uy * t1 + 28 * ny, zc + 10),
           (a0[0], a0[1], zc + 10), (vx + 12, ye, zc + 12), (vx + 12, ye, soff(ye)),
           (D["wall_x"] - 2, ye, soff(ye)), (D["wall_x"] - 2, wy, soff(wy) - 10), (D["wall_x"] - 2, wy, 900 if side > 0 else 880)]
    return pts


# ---------------- 6, 7, 8, 10, 11, 12, 15: ground unit and valve board ----------------

def ground_components(p=PARAMS):
    from build123d import Box, Cylinder, Pos, Rot
    D = derived(p)
    L2 = p["house_l"] / 2
    bc = D["box_c"]
    bx, by, bh = p["box"]
    w = p["box_wall"]
    xb = L2 + p["lug_t"]                           # back of the box
    C = {}
    # body (door on the +X face is a separate part), drilled: four bottom glands, siren hole
    body = box((xb + (bx - w) / 2, bc[1], bc[2]), (bx - w, by, bh)) - box((xb + w + (bx - 2 * w) / 2 + 1, bc[1], bc[2]), (bx - 2 * w + 2, by - 2 * w, bh - 2 * w))
    gy = [-100, -40, 40, 100]
    gx = xb + 135
    for dy in gy:
        body = body - tube((gx, bc[1] + dy, bc[2] - bh / 2 - 1), (gx, bc[1] + dy, bc[2] - bh / 2 + w + 1), 10.25)
    body = body - tube((bc[0] + 30, bc[1] - 80, bc[2] + bh / 2 - w - 1), (bc[0] + 30, bc[1] - 80, bc[2] + bh / 2 + 1), 8)
    C["box_body"] = Comp("Ground enclosure body, drilled", body, 7, "#CBD5E1")
    door = box((xb + bx - w / 2, bc[1], bc[2]), (w, by, bh)) - tube((xb + bx - w - 1, bc[1] + 90, bc[2] + 120), (xb + bx + 1, bc[1] + 90, bc[2] + 120), 11)
    C["box_door"] = Comp("Ground enclosure door", door, 7, "#E2E8F0")
    lugs, screws = [], []
    for sy_ in (-1, 1):
        for sz in (-1, 1):
            yc = bc[1] + sy_ * (by / 2 - 20)
            z0 = bc[2] + sz * (bh / 2 - 30)
            z1 = bc[2] + sz * (bh / 2 + 25)
            lg = box((L2 + p["lug_t"] / 2, yc, (z0 + z1) / 2), (p["lug_t"], 30, abs(z1 - z0)))
            zh = bc[2] + sz * (bh / 2 + 12)
            lg = lg - tube((L2 - 1, yc, zh), (L2 + 3, yc, zh), 4.5)
            lugs.append(lg)
            screws.append(tube((L2 + p["lug_t"], yc, zh), (L2 + p["lug_t"] + 5, yc, zh), 7))
    C["box_lugs"] = Comp("Enclosure wall lugs (4)", fuse(lugs), 7, "#374151")
    C["box_screws"] = Comp("Lug screws (4) into wall plugs", fuse(screws), 16, "#111827")
    # gear plate on four studs, controller and relay on standoffs, battery strapped against it
    gp_x = xb + w + 10
    gp = box((gp_x + 1, bc[1], bc[2]), (2, by - 30, bh - 30))
    studs = fuse(tube((xb + w, bc[1] + sy_ * 130, bc[2] + sz * 170), (gp_x, bc[1] + sy_ * 130, bc[2] + sz * 170), 3)
                 for sy_ in (-1, 1) for sz in (-1, 1))
    C["gear_plate"] = Comp("Gear plate on its studs", gp + studs, 7, "#9CA3AF")
    gpf = gp_x + 2
    ctrl = box((gpf + 10 + 10, bc[1] - 40, bc[2] + 90), (20, 160, 110))
    cst = fuse(tube((gpf, bc[1] - 40 + yy, bc[2] + 90 + zz), (gpf + 10, bc[1] - 40 + yy, bc[2] + 90 + zz), 2.5)
               for yy in (-70, 70) for zz in (-45, 45))
    C["board"] = Comp("Controller board on standoffs", ctrl + cst, 6, "#16A34A")
    rel = box((gpf + 10 + 12.5, bc[1] + 100, bc[2] + 90), (25, 50, 60))
    rst = fuse(tube((gpf, bc[1] + 100, bc[2] + 90 + zz), (gpf + 10, bc[1] + 100, bc[2] + 90 + zz), 2.5) for zz in (-22, 22))
    C["relay"] = Comp("Pump-start relay (dry contact)", rel + rst, 12, "#DB2777")
    bdx, bdy, bdz = p["battery"]
    zf = bc[2] - bh / 2 + w
    bat_c = (gpf + bdx / 2, bc[1] + 20, zf + bdz / 2)
    C["battery"] = Comp("Battery, 12.8 V 10 Ah LiFePO4", box(bat_c, (bdx, bdy, bdz)), 8, "#7C3AED")
    st, sw = 1.5, 25
    zs = zf + 50
    strap = box((gpf + bdx + st / 2, bat_c[1], zs), (st, bdy + 2 * st, sw))
    for sg in (-1, 1):
        strap = strap + box((gpf + (bdx + st) / 2, bat_c[1] + sg * (bdy / 2 + st / 2), zs), (bdx + st, st, sw)) \
            + box((gpf + st / 2, bat_c[1] + sg * (bdy / 2 + st + 10), zs), (st, 20, sw))
        strap = strap - tube((gpf - 1, bat_c[1] + sg * (bdy / 2 + st + 10), zs), (gpf + st + 1, bat_c[1] + sg * (bdy / 2 + st + 10), zs), 2.2)
    C["strap"] = Comp("Battery strap", strap, 16, "#64748B", True)
    # siren on the top, key switch through the door, glands in the bottom
    siren = Pos(bc[0] + 30, bc[1] - 80, bc[2] + bh / 2 + 30) * Cylinder(45, 60)
    key = tube((xb + bx, bc[1] + 90, bc[2] + 120), (xb + bx + 8, bc[1] + 90, bc[2] + 120), 20) \
        + tube((xb + bx - w - 35, bc[1] + 90, bc[2] + 120), (xb + bx, bc[1] + 90, bc[2] + 120), 10.8)
    C["siren"] = Comp("Siren and status light", siren, 15, "#DC2626")
    C["key"] = Comp("Key switch", key, 15, "#991B1B")
    gl = fuse(tube((gx, bc[1] + dy, bc[2] - bh / 2 - 16), (gx, bc[1] + dy, bc[2] - bh / 2), 13.5)
              - tube((gx, bc[1] + dy, bc[2] - bh / 2 - 17), (gx, bc[1] + dy, bc[2] - bh / 2 + 1), 5)
              + (tube((gx, bc[1] + dy, bc[2] - bh / 2), (gx, bc[1] + dy, bc[2] - bh / 2 + w), 10.25)
                 - tube((gx, bc[1] + dy, bc[2] - bh / 2 - 1), (gx, bc[1] + dy, bc[2] - bh / 2 + w + 1), 5))
              + (tube((gx, bc[1] + dy, bc[2] - bh / 2 + w), (gx, bc[1] + dy, bc[2] - bh / 2 + w + 5), 13)
                 - tube((gx, bc[1] + dy, bc[2] - bh / 2 + w - 1), (gx, bc[1] + dy, bc[2] - bh / 2 + w + 6), 10.2))
              for dy in gy)
    C["box_glands"] = Comp("Enclosure cable glands (4), M20", gl, 16, "#1F2937")

    # valve board, stand-off pipe clips, manifold with two tees, valves, transducer
    vt, vw, vh = p["valve_board"]
    vyc, vzc = p["valve_board_c"]
    vb = box((L2 + vt / 2, vyc, vzc), (vt, vw, vh))
    holes = [(dy, dz) for dy in (-500, 0, 500) for dz in (-105, 105)]
    for dy, dz in holes:
        vb = vb - tube((L2 - 1, vyc + dy, vzc + dz), (L2 + vt + 1, vyc + dy, vzc + dz), 3.5)
    for cy_ in (-500, 500):
        for dz in (-12, 12):
            vb = vb - tube((L2 - 1, vyc + cy_, p["manifold_z"] + dz), (L2 + vt + 1, vyc + cy_, p["manifold_z"] + dz), 2.75)
    C["valve_board"] = Comp("Valve board", vb, 10, "#A3A3A3", True)
    mxv, mz = p["man_x"], p["manifold_z"]
    r_m = 13.45
    clips = None
    for cy_ in (-500, 500):
        ring = Pos(mxv, vyc + cy_, mz) * Rot(90, 0, 0) * (Cylinder(r_m + 2, 24) - Cylinder(r_m, 26))
        foot = box(((L2 + vt + mxv - r_m - 1) / 2, vyc + cy_, mz), (mxv - r_m - 1 - L2 - vt, 24, 40))
        c_ = ring + foot
        clips = c_ if clips is None else clips + c_
    C["pipe_clips"] = Comp("Stand-off pipe clips (2)", clips, 16, "#525252")
    y0, y1 = vyc - vw / 2 + 30, vyc + vw / 2 + 40
    man = pipe((mxv, y0, mz), (mxv, y1, mz), r_m, r_m - 2.3)
    for vy in p["valve_y"]:
        man = man + Pos(mxv, vy, mz) * Rot(90, 0, 0) * Cylinder(r_m + 3, 40)
        man = man + tube((mxv, vy, mz - r_m - 3), (mxv, vy, mz - r_m - 31), r_m)
    yt = (p["valve_y"][0] + p["valve_y"][1]) / 2
    man = man + Pos(mxv, yt, mz) * Rot(90, 0, 0) * Cylinder(r_m + 3, 40)
    man = man + tube((mxv, y1, mz), (mxv, y1 + 40, mz), 9)        # hose connector for the supply
    C["manifold"] = Comp("Manifold: pipe, tees and hose connector", man, 16, "#A16207")
    vv = None
    for vy in p["valve_y"]:
        zt = mz - r_m - 31
        body = box((mxv, vy, zt - 35), (80, 110, 70))
        coil = tube((mxv + 40, vy, zt - 35), (mxv + 100, vy, zt - 35), 24)
        outlet = tube((mxv, vy, zt - 70), (mxv, vy, zt - 80), 10)
        v_ = body + coil + outlet
        vv = v_ if vv is None else vv + v_
    C["valves"] = Comp("Zone valves A and B", vv, 10, "#D4A017")
    C["xducer"] = Comp("Pressure transducer", tube((mxv, yt, mz + r_m + 3), (mxv, yt, mz + r_m + 93), 14)
                       + tube((mxv, yt, mz + r_m + 93), (mxv, yt, mz + r_m + 113), 18), 11, "#0EA5E9")
    # sun shade (BOM 18): folded white sheet on two bent flat-bar arms bolted to the gable wall above the enclosure
    sdep, swid, st_ = p["shade"]
    sz, sx0 = p["shade_z"], p["shade_x0"]
    sff, ssf = p["shade_flap"]
    aw, at_, atab = p["shade_arm"]
    yc = bc[1]
    x1 = L2 + sx0 + sdep
    sheet_ = box(((L2 + sx0 + x1) / 2, yc, sz - st_ / 2), (sdep, swid, st_))
    sheet_ += box((x1 - st_ / 2, yc, sz - sff / 2), (st_, swid, sff))
    for sg in (-1, 1):
        sheet_ += box(((L2 + sx0 + x1) / 2, yc + sg * (swid / 2 - st_ / 2), sz - ssf / 2), (sdep, st_, ssf))
    C["shade"] = Comp("Sun shade, folded white sheet", sheet_, 18, "#F8FAFC", True)
    arms_, scr = None, []
    za = sz - st_
    for sg in (-1, 1):
        ya = yc + sg * p["shade_arm_dy"]
        run = x1 - 10 - L2
        a_ = box((L2 + run / 2, ya, za - at_ / 2), (run, aw, at_)) + box((L2 + at_ / 2, ya, za - atab / 2), (at_, aw, atab))
        zh = za - atab / 2
        a_ = a_ - tube((L2 - 1, ya, zh), (L2 + at_ + 1, ya, zh), 3.25)
        arms_ = a_ if arms_ is None else arms_ + a_
        scr.append(tube((L2 + at_, ya, zh), (L2 + at_ + 4, ya, zh), 6))
    C["shade_arms"] = Comp("Sun shade arms (2), bent flat bar", arms_, 18, "#B45309", True)
    C["shade_screws"] = Comp("Sun shade wall screws (2)", fuse(scr), 18, "#111827")
    return C


# ---------------- 14: spray lines ----------------

def spray_components(p=PARAMS):
    from build123d import Box, Cylinder, Pos, Rot
    D = derived(p)
    L2 = p["house_l"] / 2
    r = p["line_od"] / 2
    wx, ly, lz = D["wall_x"], D["line_y"], D["line_z"]
    xw = -D["roof_len"] / 2
    C = {}
    lines, clips, lipc, heads, fclip = [], [], [], [], []
    for s, vy in zip((-1, 1), p["valve_y"]):
        y_r, y_l = s * p["riser_y"], s * ly
        pts = [(p["man_x"], vy, D["v_out"]), (p["man_x"], vy, 300), (wx, vy, p["riser_low_z"]),
               (wx, y_r, p["riser_low_z"]), (wx, y_r, p["under_z"]), (wx, y_l, p["under_z"]), (wx, y_l, lz), (xw + 5, y_l, lz)]
        lines.append(path(pts, r))
        lines.append(Pos(xw + 2.5, y_l, lz) * Rot(0, 90, 0) * Cylinder(r + 1, 5))      # end plug
        # saddle clips on the wall: along the base and up the corner
        ys = [vy + s * k for k in range(400, int(abs(y_r - vy)), 600)]
        for yy in ys:
            clips.append(box((L2 + 10, yy, p["riser_low_z"] + 10), (20, 15, 4)) + box((L2 + 10, yy, p["riser_low_z"] - 10), (20, 15, 4)))
        for zz in range(500, int(p["under_z"]), 500):
            clips.append(box((L2 + 10, y_r - 10 * s, zz), (20, 4, 15)) + box((L2 + 10, y_r + 10 * s, zz), (20, 4, 15)))
        # stand-off pipe clip screwed up into the fascia's lower edge
        fz = D["eave_z"] + 40 - p["fascia_h"]
        fy = s * (D["eave_y"] + p["fascia_t"] / 2)
        fclip.append(box((wx, fy, (fz + p["under_z"] + r + 2) / 2), (20, 20, fz - p["under_z"] - r - 2))
                     + (Pos(wx, fy, p["under_z"]) * Rot(90, 0, 0) * (Cylinder(r + 2, 20) - Cylinder(r, 22))))
        # gutter lip clips: hook over the lip, strap up the outside, ring round the line
        lyo = s * (D["lip_y"] + 4)                 # outer face of the gutter lip
        for hx in D["head_x"]:
            for dx in (-450, 450):
                cx = hx + dx
                hook = box((cx, s * (D["lip_y"] + 1), D["lip_z"] + 0.5), (12, 8, 1)) \
                    + box((cx, s * (D["lip_y"] - 3.5), D["lip_z"] - 6), (12, 1, 12)) \
                    + box((cx, lyo + s * 0.5, (D["lip_z"] + lz) / 2), (12, 1, lz - D["lip_z"] + 1)) \
                    + box((cx, (lyo + s * 1 + y_l - s * (r + 1)) / 2, lz), (12, abs(y_l - s * (r + 1) - lyo - s * 1), 1.5)) \
                    + Pos(cx, y_l, lz) * Rot(0, 90, 0) * (Cylinder(r + 1.5, 12) - Cylinder(r, 13))
                lipc.append(hook)
        for hx in D["head_x"]:
            heads.append(Pos(hx, y_l, lz) * Rot(0, 90, 0) * Cylinder(r + 2, 24)
                         + tube((hx, y_l, lz + r + 2), (hx, y_l, lz + 30), 4)
                         + Pos(hx, y_l, lz + 50) * Cylinder(10, 40) + Pos(hx, y_l, lz + 73) * Cylinder(13, 6))
    C["lines"] = Comp("Spray lines and risers (2 zones)", fuse(lines), 14, "#2563EB")
    C["heads"] = Comp("Micro-sprinklers on tees (12)", fuse(heads), 14, "#0F766E")
    C["lip_clips"] = Comp("Gutter-lip clips (24)", fuse(lipc), 14, "#57534E")
    C["wall_clips"] = Comp("Saddle clips on the wall", fuse(clips), 16, "#525252")
    C["fascia_clips"] = Comp("Stand-off clips under the fascia (2)", fuse(fclip), 16, "#525252")
    return C


# ---------------- 13, 17: cables and earthing ----------------

def cable_components(p=PARAMS):
    from build123d import Cylinder, Pos
    D = derived(p)
    mx, L2 = D["mast_x"], p["house_l"] / 2
    bc = D["box_c"]
    bh = p["box"][2]
    sy = D["standoff_y"]
    gx = L2 + p["lug_t"] + 135
    zl = p["standoff_z"][0]
    zbot = bc[2] - bh / 2 - 16
    C = {}
    inside = tube((mx, 0, p["mast_z1"] - 10), (mx, 0, p["mast_z0"] - 15), 5.5)
    mc = path([(mx, 0, p["mast_z0"] - 15), (mx, 0, p["mast_z0"] - 40), (mx - 70, sy, zl - 40), (L2 + 60, sy, zl - 40),
               (L2 + 60, 130, zl - 40), (L2 + 8, 130, zl - 60), (L2 + 8, 130, 920), (L2 + 8, bc[1] + 40, 920),
               (gx, bc[1] + 40, 920), (gx, bc[1] + 40, zbot)], 5.5)
    C["mast_cable"] = Comp("Mast cable", inside + mc, 13, "#111827")
    pods = None
    for s, dy in ((-1, -100), (1, 100)):
        pts = pod_cable_path(p, s)
        z_run = pts[-1][2]
        pts += [(L2 + 8, bc[1] + dy, z_run), (gx, bc[1] + dy, z_run), (gx, bc[1] + dy, zbot)]
        c = path(pts, 4.5)
        pods = c if pods is None else pods + c
    C["pod_cables"] = Comp("Pod cables (2)", pods, 13, "#111827")
    vc = path([(gx, bc[1] - 40, zbot), (gx, bc[1] - 40, 700), (p["man_x"] + 100, bc[1] - 40, 700),
               (p["man_x"] + 80, p["valve_y"][0], 700), (p["man_x"] + 80, p["valve_y"][0], p["manifold_z"] - 40)], 4)
    vc = vc + path([(p["man_x"] + 80, bc[1] - 40, 700), (p["man_x"] + 80, p["valve_y"][1], 700),
                    (p["man_x"] + 80, p["valve_y"][1], p["manifold_z"] - 40)], 4)
    C["valve_cable"] = Comp("Valve cable", vc, 13, "#111827")
    # 17 earthing: bonding clamp on the mast foot, conductor to the wall and down, earth rod
    ez = p["mast_z0"] + 25
    clamp = Pos(mx, 0, ez) * (Cylinder(p["mast_od"] / 2 + 5, 25) - Cylinder(p["mast_od"] / 2, 27))
    cond = path([(mx - p["mast_od"] / 2 - 5, 0, ez), (L2 + 40, -60, ez), (L2 + 40, -60, 60), (L2 + 400, -60, 60),
                 (L2 + 400, -60, 120)], 3)
    rod = tube((L2 + 400, -60, 130), (L2 + 400, -60, -1070), 8) + Pos(L2 + 400, -60, 110) * (Cylinder(14, 30) - Cylinder(8, 32))
    C["earth"] = Comp("Mast earthing: clamp, conductor and rod", clamp + cond + rod, 17, "#15803D")
    return C


def build_components(p=PARAMS):
    C = {}
    C.update(mast_components(p))
    for s in (-1, 1):
        C.update(pod_components(p, s))
    C.update(ground_components(p))
    C.update(spray_components(p))
    C.update(cable_components(p))
    return C


# BOM-line groups for the calculations, the general arrangement and the concept media
GROUPS = {
    "mast": ("Mast, wall plates, flanges, standoffs and crossover plates", 1, "#94A3B8",
             ("mast", "mast_cap", "wall_plates", "flanges", "standoffs", "xplates", "ubolts", "wall_anchors")),
    "pods": ("Sensor pods (2) with hoods and brackets", 2, "#0F766E",
             tuple(f"{k}_{s}" for s in "fb" for k in ("pod_body", "pod_lid", "lens_hood", "lens_hood_screws", "node",
                                                      "cgland", "hood", "hood_spacers", "pod_spacers", "pod_plate",
                                                      "arm", "cleat", "pod_fix"))),
    "sensors": ("Thermal array sensors (2)", 3, "#C2410C", ("sensor_f", "sensor_b")),
    "anem": ("Anemometer and wind vane", 4, "#1F2937", ("anem",)),
    "trh": ("Temperature and humidity sensor", 5, "#F5F5F4", ("trh",)),
    "panel": ("Solar panel, 10 W", 9, "#1E3A8A", ("panel", "panel_mount")),
    "enclosure": ("Ground enclosure, steel", 7, "#CBD5E1", ("box_body", "box_door", "box_lugs", "box_screws", "gear_plate",
                                                           "box_glands", "strap")),
    "shade": ("Enclosure sun shade, folded white sheet", 18, "#F8FAFC", ("shade", "shade_arms", "shade_screws")),
    "board": ("Controller board", 6, "#16A34A", ("board",)),
    "battery": ("Battery, 12.8 V 10 Ah LiFePO4", 8, "#7C3AED", ("battery",)),
    "relay": ("Pump-start relay (dry contact)", 12, "#DB2777", ("relay",)),
    "siren": ("Siren, status light and key switch", 15, "#DC2626", ("siren", "key")),
    "valves": ("Zone valves A and B on the valve board", 10, "#D4A017", ("valves", "valve_board", "manifold", "pipe_clips")),
    "xducer": ("Pressure transducer", 11, "#0EA5E9", ("xducer",)),
    "cable": ("Mast, pod and valve cables", 13, "#111827", ("mast_cable", "pod_cables", "valve_cable")),
    "lines": ("Eave spray lines and heads (2 zones)", 14, "#2563EB", ("lines", "heads", "lip_clips", "wall_clips", "fascia_clips")),
    "earth": ("Mast earthing kit", 17, "#15803D", ("earth",)),
}


def build_parts(p=PARAMS, comps=None):
    """EmberGuard kit parts grouped by BOM line. Returns {key: (label, shape, bom_no, color)}."""
    C = comps or build_components(p)
    return {k: (lab, fuse([C[c].shape for c in keys]), bom, col) for k, (lab, bom, col, keys) in GROUPS.items()}


MAST_KEYS = ("mast", "anem", "trh", "panel")
POD_KEYS = ("pods", "sensors")
GROUND_KEYS = ("enclosure", "shade", "board", "battery", "relay", "siren", "valves", "xducer")


def sensor_pods(p=PARAMS, at_origin=False, sides=(-1, 1)):
    """Pod parts and the thermal sensors, kept for older callers."""
    from build123d import Pos
    D = derived(p)
    shells, sensors = None, None
    for s in sides:
        C = pod_components(p, s)
        sfx = "f" if s < 0 else "b"
        sh = fuse([v.shape for k, v in C.items() if not k.startswith("sensor_")])
        se = C[f"sensor_{sfx}"].shape
        if at_origin:
            mv = Pos(-D["pod_x"], -s * D["gut_yc"], -D["pod_z"])
            sh, se = mv * sh, mv * se
        shells = sh if shells is None else shells + sh
        sensors = se if sensors is None else sensors + se
    return shells, sensors


def assembly(p=PARAMS, with_house=False):
    from build123d import Compound
    kids = [v[1] for v in build_parts(p).values()]
    if with_house:
        kids += list(house_parts(p).values())
    return Compound(children=kids)


# ---------------- constructability checks ----------------

def fov_solid(p=PARAMS, side=-1, reach=1500.0):
    """The thermal sensor's 55 x 35 degree view as a solid pyramid from the can face, out to reach mm."""
    from build123d import Plane, Rectangle, loft, Sketch, Pos
    px = p["pod"][0]
    th, tv = math.tan(math.radians(p["fov_h"] / 2)), math.tan(math.radians(p["fov_v"] / 2))
    a = 1.0                                         # half size of the lens aperture, mm
    s0 = Plane(origin=(-px / 2 - 0.01, 0, 0), x_dir=(0, 1, 0), z_dir=(-1, 0, 0)) * Rectangle(2 * a, 2 * a)
    s1 = Plane(origin=(-px / 2 - reach, 0, 0), x_dir=(0, 1, 0), z_dir=(-1, 0, 0)) * Rectangle(2 * (a + reach * th), 2 * (a + reach * tv))
    return _pod_xf(p, side) * loft([s0, s1])


def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def _gap(a, b_):
    return a.distance_to(b_)


def checks(p=PARAMS):
    """Pairs that must touch (the joint is made there) or stay apart by a clearance (mm).
    Returns a list of (description, overlap volume mm3, gap mm, expectation, ok)."""
    C = build_components(p)
    H = house_parts(p)
    S = lambda k: C[k].shape  # noqa: E731
    rows = []

    def chk(desc, a, b_, expect):
        v = _vol(a, b_)
        gp = _gap(a, b_)
        ok = v < 1.0 and (gp < 0.05 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    walls, roof, fg = H["walls"], H["roof"], H["fascia_gutters"]
    # mast
    chk("Wall plates on the gable wall", S("wall_plates"), walls, "touch")
    chk("Flanges on the wall plates", S("flanges"), S("wall_plates"), "touch")
    chk("Standoff pipes in the flanges", S("standoffs"), S("flanges"), "touch")
    chk("Crossover plates on the mast", S("xplates"), S("mast"), "touch")
    chk("Crossover plates on the standoffs", S("xplates"), S("standoffs"), "touch")
    chk("Standoffs clear of the mast", S("standoffs"), S("mast"), 5.0)
    chk("U-bolts clear of the wall plates", S("ubolts"), S("wall_plates"), 5.0)
    chk("Mast clear of the roof verge", S("mast"), roof, 100.0)
    chk("Wind sensors clear of the roof", S("anem"), roof, 100.0)
    chk("Mast-top sleeve on the mast (slip fit)", S("anem"), S("mast"), 0.2)
    chk("Humidity shield clamp on the mast", S("trh"), S("mast"), "touch")
    chk("Panel clamp on the mast", S("panel_mount"), S("mast"), "touch")
    chk("Panel on its tilt rail", S("panel"), S("panel_mount"), "touch")
    chk("Panel clear of the mast", S("panel"), S("mast"), 50.0)
    chk("Panel clear of the standoffs and crossover plates", S("panel"), S("standoffs") + S("xplates") + S("ubolts"), 50.0)
    chk("Humidity shield clear of the standoffs", S("trh"), S("standoffs") + S("xplates") + S("ubolts"), 50.0)
    chk("Mast cable clear of the crossover hardware", S("mast_cable"), S("xplates") + S("ubolts") + S("flanges") + S("wall_plates"), 1.0)
    # pods
    for sfx, nm in (("f", "front"), ("b", "back")):
        k = lambda n: f"{n}_{sfx}"  # noqa: E731
        chk(f"Cleat ({nm}) on the verge", S(k("cleat")), roof, "touch")
        chk(f"Cleat ({nm}) clear of the fascia and gutter", S(k("cleat")), fg, 10.0)
        chk(f"Arm ({nm}) on the cleat", S(k("arm")), S(k("cleat")), "touch")
        chk(f"Arm ({nm}) clear of the roof, fascia and gutter", S(k("arm")), roof + fg, 5.0)
        chk(f"Pod plate ({nm}) on the arm", S(k("pod_plate")), S(k("arm")), "touch")
        chk(f"Spacers ({nm}) on the pod plate", S(k("pod_spacers")), S(k("pod_plate")), "touch")
        chk(f"Pod ({nm}) on its spacers", S(k("pod_body")), S(k("pod_spacers")), "touch")
        chk(f"Pod ({nm}) clear of the arm", S(k("pod_body")), S(k("arm")), 5.0)
        chk(f"Lid ({nm}) on the pod", S(k("pod_lid")), S(k("pod_body")), "touch")
        chk(f"Hood spacers ({nm}) on the lid", S(k("hood_spacers")), S(k("pod_lid")), "touch")
        chk(f"Hood ({nm}) on its spacers", S(k("hood")), S(k("hood_spacers")), "touch")
        chk(f"Hood ({nm}) clear of the lid (air gap)", S(k("hood")), S(k("pod_lid")), 4.0)
        chk(f"Lens hood ({nm}) on the west wall", S(k("lens_hood")), S(k("pod_body")), "touch")
        chk(f"Sensor ({nm}) on the west wall", S(k("sensor")), S(k("pod_body")), "touch")
        view = fov_solid(p, -1 if sfx == "f" else 1, 1500.0)
        chk(f"Field of view ({nm}) clear of the lens hood", view, S(k("lens_hood")), 0.5)
        chk(f"Field of view ({nm}) clear of the pod hood", view, S(k("hood")), 0.5)
        chk(f"Field of view ({nm}) clear of the arm, cleat and plate", view, S(k("arm")) + S(k("cleat")) + S(k("pod_plate")), 0.5)
        chk(f"Node board ({nm}) on the pod floor", S(k("node")), S(k("pod_body")), "touch")
        chk(f"Node board ({nm}) clear of the sensor", S(k("node")), S(k("sensor")), 2.0)
        chk(f"Node board ({nm}) clear of the pod bolts", S(k("node")), S(k("pod_spacers")), 2.0)
        chk(f"Node board ({nm}) clear of the cable gland", S(k("node")), S(k("cgland")), 1.0)
        chk(f"Cable gland ({nm}) in the east wall", S(k("cgland")), S(k("pod_body")), "touch")
        chk(f"Pod ({nm}) clear of the roof and gutter", S(k("pod_body")) + S(k("hood")) + S(k("lens_hood")), roof + fg, 50.0)
    # ground unit
    chk("Enclosure lugs on the gable wall", S("box_lugs"), walls, "touch")
    chk("Enclosure on its lugs", S("box_body"), S("box_lugs"), "touch")
    chk("Enclosure clear of the wall (lug gap)", S("box_body"), walls, 1.0)
    chk("Door on the body", S("box_door"), S("box_body"), "touch")
    chk("Gear plate on its studs, in the body", S("gear_plate"), S("box_body"), "touch")
    chk("Controller on the gear plate", S("board"), S("gear_plate"), "touch")
    chk("Relay on the gear plate", S("relay"), S("gear_plate"), "touch")
    chk("Battery on the enclosure floor", S("battery"), S("box_body"), "touch")
    chk("Battery against the gear plate", S("battery"), S("gear_plate"), "touch")
    chk("Strap round the battery", S("strap"), S("battery"), "touch")
    chk("Strap on the gear plate", S("strap"), S("gear_plate"), "touch")
    chk("Battery clear of the controller and relay", S("battery"), S("board") + S("relay"), 10.0)
    chk("Battery clear of the door", S("battery"), S("box_door"), 5.0)
    chk("Controller and relay clear of the door", S("board") + S("relay"), S("box_door"), 5.0)
    chk("Key switch clear of the controller and relay", S("key"), S("board") + S("relay"), 5.0)
    chk("Key switch through the door", S("key"), S("box_door"), "touch")
    chk("Siren on the enclosure top", S("siren"), S("box_body"), "touch")
    chk("Glands in the enclosure floor", S("box_glands"), S("box_body"), "touch")
    chk("Glands clear of the battery", S("box_glands"), S("battery"), 3.0)
    chk("Sun shade arms on the gable wall", S("shade_arms"), walls, "touch")
    chk("Sun shade on its arms", S("shade"), S("shade_arms"), "touch")
    chk("Sun shade clear of the enclosure", S("shade"), S("box_body") + S("box_door") + S("box_lugs"), 25.0)
    chk("Sun shade clear of the siren", S("shade") + S("shade_arms"), S("siren"), 50.0)
    chk("Sun shade clear of the key switch", S("shade") + S("shade_arms"), S("key"), 50.0)
    chk("Sun shade screws clear of the lugs", S("shade_screws"), S("box_lugs"), 50.0)
    chk("Sun shade clear of the lines and cables", S("shade") + S("shade_arms"), S("lines") + S("mast_cable") + S("pod_cables") + S("valve_cable"), 20.0)
    door_open = box((p["house_l"] / 2 + p["lug_t"] + p["box"][0] + 160, derived(p)["box_c"][1], derived(p)["box_c"][2]), (320, p["box"][1] + 4, p["box"][2]))
    chk("Door swung open 90 degrees clear of the sun shade", door_open, S("shade") + S("shade_arms"), 25.0)
    chk("Valve board on the wall", S("valve_board"), walls, "touch")
    chk("Pipe clips on the valve board", S("pipe_clips"), S("valve_board"), "touch")
    chk("Manifold in the pipe clips", S("manifold"), S("pipe_clips"), "touch")
    chk("Valves clear of the valve board", S("valves"), S("valve_board"), 2.0)
    chk("Valves clear of the enclosure", S("valves"), S("box_body") + S("box_lugs"), 50.0)
    # spray lines
    chk("Spray lines clear of the gutter and fascia", S("lines"), fg, 5.0)
    chk("Spray lines clear of the roof", S("lines"), roof, 5.0)
    chk("Spray lines clear of the walls (on clips)", S("lines"), walls, 3.0)
    chk("Spray lines clear of the valve board", S("lines"), S("valve_board"), 5.0)
    chk("Lip clips on the gutter lips", S("lip_clips"), fg, "touch")
    chk("Lip clips round the lines", S("lip_clips"), S("lines"), "touch")
    chk("Fascia clips on the fascia", S("fascia_clips"), fg, "touch")
    chk("Fascia clips round the lines", S("fascia_clips"), S("lines"), "touch")
    chk("Wall clips on the wall", S("wall_clips"), walls, "touch")
    chk("Heads clear of the gutter", S("heads"), fg, 5.0)
    # cables and earthing
    chk("Pod cables clear of the spray lines", S("pod_cables"), S("lines"), 5.0)
    chk("Pod cables clear of the gutter and fascia", S("pod_cables"), fg, 5.0)
    chk("Pod cables clear of the roof (under the soffit)", S("pod_cables"), roof, 1.0)
    chk("Cables clear of the valves and board", S("mast_cable") + S("pod_cables"), S("valves") + S("valve_board") + S("manifold"), 20.0)
    chk("Earth conductor clear of the wall plates", S("earth"), S("wall_plates") + S("flanges"), 10.0)
    chk("Earth clamp on the mast foot", S("earth"), S("mast"), "touch")
    return rows


def print_checks(rows):
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else f">= {exp:g} mm"
        print(f"{'ok ' if ok else 'BAD'}  {desc:<62} overlap {v:9.1f} mm3  gap {gp:8.2f} mm  ({e})")
        bad += 0 if ok else 1
    print(f"{len(rows) - bad} of {len(rows)} checks pass")
    return bad


def main():
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    C = build_components()
    parts = build_parts(comps=C)
    pod, pod_sensor = sensor_pods(at_origin=True, sides=(-1,))
    gkeys = [k for g in GROUND_KEYS for k in GROUPS[g][3]]
    groups = {
        "emberguard-kit": Compound(children=[v[1] for v in parts.values()]),
        "mast-assembly": Compound(children=[parts[k][1] for k in MAST_KEYS]),
        "sensor-pod": Compound(children=[pod, pod_sensor]),
        "ground-unit": Compound(children=[C[k].shape for k in gkeys]),
        "reference-house": Compound(children=list(house_parts().values())),
    }
    for name, c in groups.items():
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"), tolerance=0.5, angular_tolerance=0.3)
    D = derived()
    print("exported:", ", ".join(groups))
    print(f"ridge surface {D['ridge_top']:.0f} mm, pods at x {D['pod_x']:.0f}, z {D['pod_z']:.0f} mm "
          f"({PARAMS['pod_above_lip']:.0f} mm above the lip), "
          f"gutter lip y {D['lip_y']:.0f} z {D['lip_z']:.0f} mm, zone lines {D['zone_len'][0] / 1000:.1f} and "
          f"{D['zone_len'][1] / 1000:.1f} m")


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks(checks()) else 0)
    main()
