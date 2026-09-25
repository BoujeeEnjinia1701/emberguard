"""EmberGuard parametric model (build123d), TRL 3, massing-plus level of detail.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    emberguard-kit.step / .stl        every kit part in its installed position on the reference house
    mast-assembly.step / .stl         mast, standoffs, sensor head, thermal sensors, wind and humidity sensors, panel
    sensor-head.step / .stl           sensor head enclosure, hood and the two thermal sensors
    ground-unit.step / .stl           steel enclosure and contents, siren, valve manifold and pressure transducer
    reference-house.step / .stl       the 12 x 8 m reference house (context only, not in the BOM)

Axes (mm): X along the ridge (east is +X), Y across the house (front eave at -Y), Z up from the
ground. The house is centered on the origin. The mast stands off the east gable wall at the ridge
line. Main dimensions and interfaces only: gable-wall standoffs, head height and sensor aim,
enclosure and valve positions, spray-line runs on the gutter lips. Not fabrication detail; not
for fabrication.

The same PARAMS and derived() feed docs/04-calcs/sizing.py (EGD-CAL-001), the drawing
EGD-DWG-001 (cad/src/sheets.py) and the concept media (cad/src/concept_media.py).
"""
import math
from pathlib import Path

# Top-level parameters (mm, degrees). Edit these, not the geometry below.
PARAMS = {
    # reference house (context, EGD-REQ-001)
    "house_l": 12000.0, "house_d": 8000.0, "wall_h": 2700.0,
    "pitch": 22.0, "overhang": 500.0, "roof_t": 200.0,
    "fascia_t": 25.0, "fascia_h": 200.0,
    "gutter_w": 120.0, "gutter_h": 100.0, "gutter_drop": 130.0,   # gutter top 30 mm below the roof underside at the eave
    # 1 mast and standoffs
    "mast_off": 700.0,            # mast axis from the gable wall
    "mast_od": 40.0, "mast_wall": 2.0,           # 6061-T6 aluminium tube
    "mast_z0": 2250.0, "mast_z1": 4700.0,
    "standoff_z": (2450.0, 3900.0),
    "standoff_od": 33.7, "standoff_wall": 3.2,  # DN25 galvanized pipe
    "wall_plate": (12.0, 140.0, 140.0),
    # 2 sensor head and hood
    "head_z": 4760.0,             # head center
    "head": (160.0, 240.0, 120.0),              # x, y, z outside
    "hood": (260.0, 340.0, 8.0),
    # 3 thermal sensors (MLX90640, 55 x 35 degree lens, 32 x 24 pixels)
    "aim_az": 45.0,               # degrees off the house axis (toward -X), one sensor to each side
    "aim_down": 15.0,             # degrees below horizontal
    "fov_h": 55.0, "fov_v": 35.0, "px_h": 32, "px_v": 24,
    "sensor_y": 70.0,             # sensor offset from the mast plane
    # 4 anemometer and vane
    "arm_z": 5000.0, "arm_half": 230.0,
    # 5 temperature and humidity shield
    "trh_z": 3300.0,
    # 9 solar panel
    "panel": (350.0, 250.0, 22.0), "panel_tilt": 45.0, "panel_z": 3600.0,
    # ground unit (7 enclosure with 6, 8, 12 inside; 15 on it)
    "box": (160.0, 320.0, 400.0), "box_z": 1150.0, "box_y": -1800.0,
    "battery": (65.0, 150.0, 95.0),
    # 10 valves and 11 transducer on a manifold below the box
    "manifold_z": 450.0, "valve_y": (-2100.0, -1500.0),
    # 14 spray lines
    "line_od": 16.0, "line_id": 13.2,
    "heads_per_eave": 6, "head_pitch": 2200.0, "line_above_lip": 30.0,
    "riser_x": 250.0,             # risers run down the gable wall this far outside it
    "riser_low_z": 250.0,
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
    mast_x = p["house_l"] / 2 + p["mast_off"]
    line_z = lip_z + p["line_above_lip"]
    n = p["heads_per_eave"]
    head_x = [(i - (n - 1) / 2) * p["head_pitch"] for i in range(n)]
    # spray line per zone: eave run plus riser from the valve down, across and up the gable wall
    rx = p["house_l"] / 2 + p["riser_x"]
    zone_len = []
    for s, vy in zip((-1, 1), p["valve_y"]):
        riser = (p["manifold_z"] - p["riser_low_z"]) + abs(s * lip_y - vy) + (line_z - p["riser_low_z"])
        zone_len.append(roof_len + riser + (rx - roof_len / 2))
    return {
        "T": T, "eave_y": eave_y, "eave_z": eave_z, "eave_top": eave_top, "ridge_under": ridge_under,
        "ridge_top": ridge_top, "roof_len": roof_len, "gut_z0": gut_z0, "lip_y": lip_y, "lip_z": lip_z,
        "mast_x": mast_x, "line_z": line_z, "head_x": head_x, "zone_len": zone_len,
        "head_above_ridge": p["head_z"] - ridge_top, "riser_xpos": rx,
        "mast_len": p["mast_z1"] - p["mast_z0"],
        "box_c": (p["house_l"] / 2 + p["box"][0] / 2 + 5, p["box_y"], p["box_z"]),
    }


def sensor_axes(p=PARAMS, side=-1):
    """Sensor position and unit aim vector for the sensor watching the front (-1) or back (+1) eave."""
    D = derived(p)
    az, dn = math.radians(p["aim_az"]), math.radians(p["aim_down"])
    d = (-math.cos(dn) * math.cos(az), side * math.cos(dn) * math.sin(az), -math.sin(dn))
    pos = (D["mast_x"] - 45, side * p["sensor_y"], p["head_z"] - 10)
    return pos, d


# ---------------- geometry helpers ----------------

def tube(a, b, r):
    from build123d import Solid, Plane, Vector
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


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
        out = s if out is None else out + s
    return out


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


# ---------------- kit parts ----------------

def sensor_head(p=PARAMS, at_origin=False):
    """Head shell, hood and both thermal sensors. At the installed position unless at_origin."""
    from build123d import Box, Pos
    D = derived(p)
    mx, hz = (0.0, 0.0) if at_origin else (D["mast_x"], p["head_z"])
    hx, hy, hh = p["head"]
    shell = Pos(mx, 0, hz) * (Box(hx, hy, hh) - Box(hx - 20, hy - 20, hh - 20))
    hood = Pos(mx, 0, hz + hh / 2 + 6) * Box(*p["hood"])
    sensors = None
    for s in (-1, 1):
        pos, d = sensor_axes(p, s)
        px, py, pz = (pos[0] - D["mast_x"] + mx, pos[1], pos[2] - p["head_z"] + hz)
        lens = tube((px, py, pz), (px + d[0] * 70, py + d[1] * 70, pz + d[2] * 70), 14)
        board = Pos(mx - 20, py, pz) * Box(30, 40, 50)
        sensors = lens + board if sensors is None else sensors + lens + board
    return shell + hood, sensors


def build_parts(p=PARAMS):
    """EmberGuard kit parts keyed by name. Returns {key: (label, shape, bom_no, color)}."""
    from build123d import Box, Cylinder, Pos, Rot, Sphere
    D = derived(p)
    mx, hz = D["mast_x"], p["head_z"]
    L2 = p["house_l"] / 2
    out = {}

    # 1 Mast and two standoffs to the gable wall
    ro, ri = p["mast_od"] / 2, p["mast_od"] / 2 - p["mast_wall"]
    ml = D["mast_len"]
    mast = Pos(mx, 0, (p["mast_z0"] + p["mast_z1"]) / 2) * (Cylinder(ro, ml) - Cylinder(ri, ml + 2))
    for z in p["standoff_z"]:
        mast = mast + tube((L2, 0, z), (mx, 0, z), p["standoff_od"] / 2) \
            + Pos(L2 + p["wall_plate"][0] / 2, 0, z) * Box(*p["wall_plate"]) \
            + Pos(mx, 0, z) * Cylinder(ro + 10, 60)
    out["mast"] = ("Mast and standoff brackets", mast, 1, "#94A3B8")

    # 2 and 3 Sensor head with hood; two thermal sensors
    head, sensors = sensor_head(p)
    out["head"] = ("Sensor head with heat and sun hood", head, 2, "#0F766E")
    out["sensors"] = ("Thermal array sensors (2)", sensors, 3, "#C2410C")

    # 4 Anemometer and vane on a crossarm above the head
    az = p["arm_z"]; ah = p["arm_half"]
    anem = tube((mx, 0, hz + p["head"][2] / 2 + 10), (mx, 0, az), 10) + tube((mx, -ah, az), (mx, ah, az), 9)
    anem = anem + tube((mx, -ah, az), (mx, -ah, az + 90), 6) + Pos(mx, -ah, az + 90) * Cylinder(16, 24)
    for k in range(3):
        t = math.radians(k * 120 + 20)
        cx, cy = mx + 90 * math.cos(t), -ah + 90 * math.sin(t)
        anem = anem + tube((mx, -ah, az + 90), (cx, cy, az + 90), 3) + Pos(cx, cy, az + 90) * Sphere(26)
    anem = anem + tube((mx, ah, az), (mx, ah, az + 90), 6) + Pos(mx - 80, ah, az + 90) * Box(170, 4, 90) \
        + Pos(mx + 80, ah, az + 90) * Sphere(14)
    out["anem"] = ("Anemometer and wind vane", anem, 4, "#1F2937")

    # 5 Temperature and humidity sensor in a five-plate shield on a side arm
    trh = fuse(Pos(mx + 90, 0, p["trh_z"] + k * 22) * Cylinder(55, 6) for k in range(5))
    trh = trh + tube((mx + ro, 0, p["trh_z"] + 40), (mx + 90, 0, p["trh_z"] + 40), 6)
    out["trh"] = ("Temperature and humidity sensor", trh, 5, "#F5F5F4")

    # 9 Solar panel, facing the equator side (-Y), on a short arm
    panel = Pos(mx, -200, p["panel_z"]) * Rot(-p["panel_tilt"], 0, 0) * Box(*p["panel"]) \
        + tube((mx, -ro, p["panel_z"]), (mx, -150, p["panel_z"]), 10)
    out["panel"] = ("Solar panel, 10 W", panel, 9, "#1E3A8A")

    # 7 Ground enclosure (steel shell) on the gable wall, with 6, 8 and 12 inside and 15 on it
    bc = D["box_c"]; bx, by, bh = p["box"]
    out["enclosure"] = ("Ground enclosure, steel", Pos(*bc) * (Box(bx, by, bh) - Box(bx - 20, by - 20, bh - 20)), 7, "#115E59")
    out["board"] = ("Controller board", Pos(bc[0] - 30, bc[1] - 40, bc[2] + 90) * Box(20, 160, 110), 6, "#16A34A")
    out["battery"] = ("Battery, 12.8 V 6 Ah LiFePO4", Pos(bc[0] + 10, bc[1] + 20, bc[2] - 110) * Box(*p["battery"]), 8, "#7C3AED")
    out["relay"] = ("Pump-start relay (dry contact)", Pos(bc[0] - 30, bc[1] + 100, bc[2] + 90) * Box(25, 50, 60), 12, "#DB2777")
    siren = Pos(bc[0] + 30, bc[1] - 80, bc[2] + bh / 2 + 30) * Cylinder(45, 60) \
        + Pos(bc[0] + bx / 2 + 10, bc[1] + 90, bc[2] + 120) * Rot(0, 90, 0) * Cylinder(20, 30)
    out["siren"] = ("Siren, status light and key switch", siren, 15, "#DC2626")

    # 10 Zone valves A and B on a manifold; 11 pressure transducer
    rx, mz = D["riser_xpos"], p["manifold_z"]
    vy = p["valve_y"]
    man = tube((rx, min(vy) - 200, mz), (rx, max(vy) + 200, mz), 14)
    valves = man
    for y in vy:
        valves = valves + Pos(rx, y, mz) * Box(80, 110, 70) + Pos(rx, y, mz + 60) * Cylinder(24, 60)
    out["valves"] = ("Zone valves A and B with manifold", valves, 10, "#D4A017")
    yc = (vy[0] + vy[1]) / 2
    out["xducer"] = ("Pressure transducer", Pos(rx, yc, mz + 50) * Cylinder(14, 90) + Pos(rx, yc, mz + 105) * Cylinder(18, 20),
                     11, "#0EA5E9")

    # 13 Mast cable from the head down the mast to the enclosure
    cable = path([(mx + ro + 6, 0, p["mast_z1"] - 50), (mx + ro + 6, 0, p["mast_z0"] + 50),
                  (L2 + 120, -400, p["mast_z0"] - 250), (bc[0], bc[1], bc[2] + bh / 2)], 6)
    out["cable"] = ("Mast cable", cable, 13, "#111827")

    # 14 Eave spray lines, risers and micro-sprinkler heads (zone A front, zone B back)
    r = p["line_od"] / 2
    lines = None
    for s, y in zip((-1, 1), vy):
        ly = s * D["lip_y"]
        run = tube((-D["roof_len"] / 2, ly, D["line_z"]), (rx, ly, D["line_z"]), r)
        riser = path([(rx, y, mz), (rx, y, p["riser_low_z"]), (rx, ly, p["riser_low_z"]), (rx, ly, D["line_z"])], r)
        zone = run + riser
        for hx in D["head_x"]:
            zone = zone + Pos(hx, ly, D["line_z"] + 35) * Cylinder(10, 60)
        lines = zone if lines is None else lines + zone
    out["lines"] = ("Eave spray lines and heads (2 zones)", lines, 14, "#2563EB")
    return out


MAST_KEYS = ("mast", "head", "sensors", "anem", "trh", "panel", "cable")
GROUND_KEYS = ("enclosure", "board", "battery", "relay", "siren", "valves", "xducer")


def assembly(p=PARAMS, with_house=False):
    from build123d import Compound
    kids = [v[1] for v in build_parts(p).values()]
    if with_house:
        kids += list(house_parts(p).values())
    return Compound(children=kids)


def main():
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    head, sensors = sensor_head(at_origin=True)
    groups = {
        "emberguard-kit": assembly(),
        "mast-assembly": Compound(children=[parts[k][1] for k in MAST_KEYS]),
        "sensor-head": Compound(children=[head, sensors]),
        "ground-unit": Compound(children=[parts[k][1] for k in GROUND_KEYS]),
        "reference-house": Compound(children=list(house_parts().values())),
    }
    for name, c in groups.items():
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"), tolerance=0.5, angular_tolerance=0.3)
    D = derived()
    print("exported:", ", ".join(groups))
    print(f"ridge surface {D['ridge_top']:.0f} mm, head {PARAMS['head_z']:.0f} mm ({D['head_above_ridge']:.0f} mm above the ridge), "
          f"gutter lip y {D['lip_y']:.0f} z {D['lip_z']:.0f} mm, zone lines {D['zone_len'][0] / 1000:.1f} and "
          f"{D['zone_len'][1] / 1000:.1f} m")


if __name__ == "__main__":
    main()
