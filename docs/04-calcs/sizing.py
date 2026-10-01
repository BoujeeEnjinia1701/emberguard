"""EmberGuard sizing calculations for EGD-CAL-001 v0.2 (TRL 3, revision 2 design).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md, each with a tag in brackets
([A1], [B3] ...), and writes docs/04-calcs/results.csv with the requirement status table.
Geometry comes from cad/src/model.py (PARAMS and derived), cost from bom/bom.csv and the
budget from project.yaml. First-principles estimates for a paper proof of concept.
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived, sensor_axes  # noqa: E402

D = derived(P)
OUT = []


def say(tag, text):
    line = f"[{tag}] {text}"
    OUT.append(line)
    print(line)


def unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


# ================================================================ A. Viewing geometry (R3)
IFOV_H = math.radians(P["fov_h"] / P["px_h"])
IFOV_V = math.radians(P["fov_v"] / P["px_v"])
PIX_SR = IFOV_H * IFOV_V
say("A1", f"Pixel field of view {math.degrees(IFOV_H):.2f} x {math.degrees(IFOV_V):.2f} deg; "
          f"footprint normal to the line of sight {8 * IFOV_H:.2f} x {8 * IFOV_V:.2f} m at 8 m, "
          f"{14 * IFOV_H:.2f} x {14 * IFOV_V:.2f} m at 14 m")
say("A2", f"Pods {P['pod_out']:.0f} mm beyond the east end of each gutter, centre {P['pod_above_lip']:.0f} mm above the lip "
          f"({D['pod_z']:.0f} mm above ground) over the gutter centreline; sensor aimed along the gutter, "
          f"{P['aim_yaw']:.0f} deg toward the house and {P['aim_down']:.0f} deg down")

HALF_L = D["roof_len"] / 2
COS_P = math.cos(math.radians(P["pitch"]))


def blocked(a, b, n=1500):
    """True if the straight line from a to b passes through the roof slab or the fascia."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    t = np.linspace(0.0, 0.995, n)[:, None]
    q = a + t * (b - a)
    x, y, z = q[:, 0], q[:, 1], q[:, 2]
    inx = np.abs(x) <= HALF_L
    zu = P["wall_h"] + (P["house_d"] / 2 - np.abs(y)) * D["T"]
    slab = inx & (np.abs(y) <= D["eave_y"]) & (z > zu + 1) & (z < zu + P["roof_t"] / COS_P - 1)
    fy0, fy1 = D["eave_y"], D["eave_y"] + P["fascia_t"]
    fas = inx & (np.abs(y) >= fy0) & (np.abs(y) <= fy1) & (z < D["eave_z"] + 40) & (z > D["eave_z"] + 40 - P["fascia_h"])
    return bool((slab | fas).any())


def end_cap_clear(a, b):
    """The gutter end cap (at the east end, up to lip height) must not cut the line."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    t = (HALF_L - a[0]) / (b[0] - a[0])
    return not (0 < t < 1) or a[2] + t * (b[2] - a[2]) > D["lip_z"]


def in_fov(pos, d, tgt):
    v = unit(np.asarray(tgt) - np.asarray(pos))
    d = unit(d)
    r = unit(np.cross(d, [0, 0, 1.0]))
    u = np.cross(r, d)
    h = math.degrees(math.atan2(v @ r, v @ d))
    e = math.degrees(math.atan2(v @ u, v @ d))
    return abs(h) <= P["fov_h"] / 2 and abs(e) <= P["fov_v"] / 2, h, e


def roof_point(x, side, up_slope):
    """Point on the roof surface, up_slope metres (along the slope) from the eave edge."""
    y = side * (D["eave_y"] - up_slope * 1000 * COS_P)
    z = D["eave_top"] + up_slope * 1000 * math.sin(math.radians(P["pitch"]))
    return np.array([x, y, z])


DEBRIS_BELOW_LIP = 42.0                  # debris surface 50 mm above the gutter floor (floor 8 mm thick)


def gutter_point(x, side, below_lip=DEBRIS_BELOW_LIP):
    """Point on the gutter centreline, below_lip mm below the lip (debris surface)."""
    return np.array([x, side * D["gut_yc"], D["lip_z"] - below_lip])


def hanger_clear(pos, tgt):
    """Hanger straps cross the gutter top at lip level every hanger_pitch from the east end.
    The line is shadowed if it is below lip level where it passes over a strap between pod and target."""
    pos, tgt = np.asarray(pos, float), np.asarray(tgt, float)
    xs_h = HALF_L - P["hanger_pitch"] / 2 - np.arange(0, 40) * P["hanger_pitch"]
    for xh in xs_h:
        for xe in (xh - P["hanger_w"] / 2, xh + P["hanger_w"] / 2):
            t = (pos[0] - xe) / (pos[0] - tgt[0])
            if 0 < t < 1 and pos[2] + t * (tgt[2] - pos[2]) < D["lip_z"]:
                return False
    return True


xs = np.arange(-HALF_L + 50, HALF_L, 100.0)
far = {s: [] for s in (-1, 1)}
cover = {}
for s in (-1, 1):
    pos, d = sensor_axes(P, s)
    gut_ok = [x for x in xs if in_fov(pos, d, gutter_point(x, s))[0] and not blocked(pos, gutter_point(x, s))
              and end_cap_clear(pos, gutter_point(x, s))]
    gut_h = [x for x in gut_ok if hanger_clear(pos, gutter_point(x, s))]
    gut_h10 = [x for x in gut_ok if hanger_clear(pos, gutter_point(x, s, 10.0))]
    edge_ok = [x for x in xs if in_fov(pos, d, roof_point(x, s, 0.05))[0] and not blocked(pos, roof_point(x, s, 0.05))]
    strip_ok = [x for x in xs if all(in_fov(pos, d, roof_point(x, s, u))[0] and not blocked(pos, roof_point(x, s, u))
                                     for u in (0.05, 0.5, 1.0))]
    cover[s] = (gut_ok, gut_h, gut_h10, edge_ok, strip_ok)
gable_x = D["mast_x"]
END = HALF_L                              # east end of the gutter; distances below are measured from it
g_ok, g_h, g_h10, e_ok, s_ok = cover[-1]
pos, d = sensor_axes(P, -1)
rng_g = [np.linalg.norm(gutter_point(x, -1) - np.asarray(pos)) / 1000 for x in g_ok]
say("A3", f"Front gutter interior (debris {DEBRIS_BELOW_LIP:.0f} mm below the lip) in view and unobstructed at {len(g_ok)} of {len(xs)} "
          f"stations, from {END - max(g_ok):,.0f} mm to {END - min(g_ok):,.0f} mm from the east end of the gutter; "
          f"range from the sensor {min(rng_g):.1f} to {max(rng_g):.1f} m")
unseen = [x for x in g_ok if x not in g_h]
say("A4", f"With hanger straps across the gutter top every {P['hanger_pitch']:.0f} mm: debris {DEBRIS_BELOW_LIP:.0f} mm below the lip "
          f"visible at {len(g_h)} of {len(g_ok)} stations"
          + (f"; none beyond {(END - min(g_h)) / 1000:.1f} m from the gutter end, where every station is in a strap shadow"
             if unseen else "")
          + f"; debris heaped to 10 mm below the lip visible at {len(g_h10)} of {len(g_ok)}")
bg_ok, bg_h, bg_h10, be_ok, bs_ok = cover[1]
say("A5", f"Roof edge in view from {END - max(e_ok):,.0f} to {END - min(e_ok):,.0f} mm from the gutter end; whole 1 m strip "
          f"from {END - max(s_ok):,.0f} to {END - min(s_ok):,.0f} mm. Back gutter (mirror image): interior at {len(bg_ok)} "
          f"stations, {len(bg_h)} with hanger straps")

# grazing angles from the pod: on the debris surface (horizontal) and on the roof edge
roof_n = {s: unit([0, s * math.sin(math.radians(P["pitch"])), math.cos(math.radians(P["pitch"]))]) for s in (-1, 1)}
graze = {}
for rx_m in (4.0, 8.0, 13.0):
    x = END - rx_m * 1000
    gp = gutter_point(x, -1)
    v = gp - np.asarray(pos)
    g_d = math.degrees(math.asin(abs(unit(v)[2])))
    rp = roof_point(x, -1, 0.05)
    vr = rp - np.asarray(pos)
    g_r = math.degrees(math.asin(abs(unit(vr) @ roof_n[-1])))
    graze[rx_m] = (np.linalg.norm(v) / 1000, g_d, np.linalg.norm(vr) / 1000, g_r)
say("A6", "Grazing angle of the line of sight: " + "; ".join(
    f"{k:.0f} m along the gutter: debris {a:.1f} m at {b:.1f} deg, roof edge {c:.1f} m at {e:.1f} deg"
    for k, (a, b, c, e) in graze.items()))

# former ridge-line head (EGD-CAL-001 v0.1), for reference: 228 mm above the ridge, 45 deg off axis
OLD = {-1: (D["mast_x"] - 45, -70.0, 4750.0), 1: (D["mast_x"] - 45, 70.0, 4750.0)}
old_vis = sum(1 for x in xs if not blocked(OLD[-1], gutter_point(x, -1)))
say("A7", f"For reference, the ridge-line head of revision 1 (4,750 mm above ground) sees debris in the front gutter at "
          f"{old_vis} of {len(xs)} stations")

# ================================================================ B. Radiometry (R1, R2)
H_, C_, K_ = 6.62607015e-34, 2.99792458e8, 1.380649e-23
lam = np.linspace(8e-6, 14e-6, 600)


def band(T):
    """Band radiance 8 to 14 um, W/(m2 sr)."""
    L = 2 * H_ * C_ ** 2 / lam ** 5 / (np.exp(H_ * C_ / (lam * K_ * T)) - 1)
    return float(np.trapezoid(L, lam))


TB, EPS = 300.0, 0.9
LB = band(TB)
dLdT = (band(TB + 0.5) - band(TB - 0.5))
say("B1", f"8 to 14 um band radiance at 300 K {LB:.1f} W/(m2 sr); slope {dLdT / LB * 100:.2f} % per K")
ratio = {t: band(t + 273.15) / LB for t in (300, 400, 600, 800)}
say("B2", "Band radiance relative to a 300 K background: " + ", ".join(f"{t} C {r:.1f} times" for t, r in ratio.items()))


def apparent_rise(t_c, area_m2, rng_m, straddle=1.0):
    """Apparent pixel temperature rise for a hot target filling part of one pixel."""
    f = straddle * area_m2 / (rng_m ** 2 * PIX_SR)
    dl = f * EPS * (band(t_c + 273.15) - LB)
    lo, hi = 0.0, 600.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if band(TB + mid) - LB < dl:
            lo = mid
        else:
            hi = mid
    return lo, f


NETD_1HZ = 0.1
noise4 = NETD_1HZ * math.sqrt(4)
THRESH = 2.0                             # persistent-spot trigger, decided (EGD-DDR-002, O5); was 5 K
OLD_THRESH = 5.0
say("B3", f"Sensor noise about {NETD_1HZ} K rms at 1 Hz, about {noise4:.1f} K at 4 Hz; trigger {THRESH:.0f} K "
          f"(= {THRESH / noise4:.0f} times the 4 Hz noise), lowered from {OLD_THRESH:.0f} K; a 5-sigma threshold would be {5 * noise4:.1f} K")

EMB_A = math.pi / 4 * 0.010 ** 2        # 10 mm ember, projected area of a sphere
for t in (600, 800):
    r8, f8 = apparent_rise(t, EMB_A, 8.0)
    r8w, _ = apparent_rise(t, EMB_A, 8.0, 0.25)
    r5, _ = apparent_rise(t, EMB_A, 5.0)
    say("B4" if t == 600 else "B5",
        f"10 mm ember at {t} C: pixel fill {f8 * 100:.2f} % at 8 m; apparent rise {r8:.1f} K centred in a pixel, "
        f"{r8w:.1f} K on a pixel corner; {r5:.1f} K at 5 m")


def max_range(t_c, area, thr, straddle=1.0):
    lo, hi = 0.5, 100.0
    for _ in range(50):
        mid = (lo + hi) / 2
        if apparent_rise(t_c, area, mid, straddle)[0] >= thr:
            lo = mid
        else:
            hi = mid
    return lo


for thr, tag in ((THRESH, "B6"), (OLD_THRESH, "B7")):
    say(tag, f"Range at which a 10 mm ember reaches a {thr:.0f} K trigger (centred / on a corner): "
             f"600 C {max_range(600, EMB_A, thr):.1f} / {max_range(600, EMB_A, thr, 0.25):.1f} m; "
             f"800 C {max_range(800, EMB_A, thr):.1f} / {max_range(800, EMB_A, thr, 0.25):.1f} m")
R2_RNG = max_range(600, EMB_A, THRESH)
R2_RNG_C = max_range(600, EMB_A, THRESH, 0.25)
say("B8", f"Range from the sensor to the watched gutter: {min(rng_g):.1f} to {max(rng_g):.1f} m; an ember 8 m along the "
          f"gutter from the east end is {graze[8.0][0]:.1f} m from the sensor")

SPOT_A = 0.01                            # 100 cm2


def flat_rise(x):
    """Flat 100 cm2 spot at 300 C on the debris surface at station x (front gutter)."""
    gp = gutter_point(x, -1)
    v = gp - np.asarray(pos)
    rng = np.linalg.norm(v) / 1000
    g = math.asin(abs(unit(v)[2]))
    return apparent_rise(300, SPOT_A * math.sin(g), rng)[0], rng


for k, tag in ((8.0, "B9"), (13.0, "B10")):
    x = END - k * 1000
    flat, rng = flat_rise(x)
    heap, _ = apparent_rise(300, 0.10 * 0.05, rng)
    say(tag, f"100 cm2 hot spot at 300 C in the gutter {k:.0f} m from the east end ({rng:.1f} m range, seen at "
             f"{graze[k][1]:.1f} deg): flat on the debris {flat:.2f} K; as a 100 x 50 mm heap face {heap:.1f} K")
flat_ok = [x for x in g_ok if flat_rise(x)[0] >= THRESH]
FLAT_REACH = (END - min(flat_ok)) / 1000 if flat_ok else 0.0
spot_face_range = max_range(300, 0.10 * 0.05, THRESH)
say("B11", f"A 100 x 50 mm hot face at 300 C reaches the {THRESH:.0f} K trigger out to {spot_face_range:.1f} m (centred); "
           f"a flat 100 cm2 spot on the debris reaches it out to {FLAT_REACH:.1f} m along the gutter")

# ================================================================ C. Water (R5, R6, R7)
Q_HEAD = 40.0                            # L/h at 2 bar
N = P["heads_per_eave"]
q_zone = N * Q_HEAD / 60                 # L/min
area_strip = 1.2 * D["roof_len"] / 1000
rate_on = N * Q_HEAD / area_strip
say("C1", f"Zone flow {q_zone:.1f} L/min ({N} heads x {Q_HEAD:.0f} L/h); strip {area_strip:.1f} m2 per eave; "
          f"{rate_on:.1f} mm/h while the zone runs, {rate_on / 2:.1f} mm/h averaged at 50 % duty")
A_BORE = math.pi / 4 * (P["line_id"] / 1000) ** 2
vols = [L / 1000 * A_BORE * 1000 for L in D["zone_len"]]
say("C2", f"Zone line lengths {D['zone_len'][0] / 1000:.1f} m (front, A) and {D['zone_len'][1] / 1000:.1f} m (back, B); "
          f"volumes {vols[0]:.2f} L and {vols[1]:.2f} L at {P['line_id']} mm bore")
T_DET, T_VALVE = 10.0, 1.0
fill_one = [v / q_zone * 60 for v in vols]
fill_both = sum(vols) / q_zone * 60
say("C3", f"Water at the farthest head after detection, supply 4 L/min: detection side zone first "
          f"{T_DET + T_VALVE + fill_one[0]:.0f} s (A) or {T_DET + T_VALVE + fill_one[1]:.0f} s (B); "
          f"both zones together {T_DET + T_VALVE + fill_both:.0f} s; both together at 8 L/min "
          f"{T_DET + T_VALVE + fill_both / 2:.0f} s")
# supply pressure at the manifold
v = q_zone / 60000 / A_BORE
Re = v * P["line_id"] / 1000 / 1.0e-6
f = 0.316 * Re ** -0.25
dp_full = f * (max(D["zone_len"]) / 1000) / (P["line_id"] / 1000) * 1000 * v ** 2 / 2
dp_fric = dp_full * (1 - (D["roof_len"] / 1000) / max(D["zone_len"]) * 2 / 3)   # flow falls along the eave run
dz = (D["line_z"] + 35 - P["manifold_z"]) / 1000
p_man = 2.0 + (1000 * 9.81 * dz + dp_fric) / 1e5
say("C4", f"Line velocity {v:.2f} m/s, Re {Re:,.0f}; friction about {dp_fric / 1000:.1f} kPa; lift {dz:.2f} m "
          f"({1000 * 9.81 * dz / 1000:.0f} kPa); pressure needed at the manifold about {p_man:.2f} bar for 2.0 bar at the heads")
EVENT_H = 4.0
water = q_zone * 60 * EVENT_H + sum(vols)
say("C5", f"Water per 4 h event: {q_zone * 60 * EVENT_H:.0f} L of spray plus {sum(vols):.1f} L to fill the lines = "
          f"{water:.0f} L ({water / 3.785:.0f} US gal); margin {(1000 - water) / 1000 * 100:.1f} % on 1,000 L")

# droplet drift screening model (2D section normal to the eave)
RHO_A, MU_A, RHO_W, G = 1.2, 1.8e-5, 1000.0, 9.81


def cd(re):
    re = max(re, 1e-6)
    return 24 / re * (1 + 0.15 * re ** 0.687) + 0.42 / (1 + 42500 * re ** -1.16)


EDGE_IN = (D["lip_y"] - D["eave_y"]) / 1000       # horizontal distance from the head to the roof edge
EDGE_UP = (D["eave_top"] - (D["line_z"] + 65)) / 1000
STRIP_IN = EDGE_IN + 1.0 * COS_P                  # 1 m up the slope from the edge
TAN_P = math.tan(math.radians(P["pitch"]))


def land(dia, v0, ang, wind):
    """Horizontal landing position (m inboard of the head, + toward the roof). wind > 0 blows onto the roof."""
    m = RHO_W * math.pi / 6 * dia ** 3
    a = math.pi / 4 * dia ** 2
    x, z = 0.0, 0.0
    vx, vz = v0 * math.cos(math.radians(ang)), v0 * math.sin(math.radians(ang))
    dt = 2e-4
    for _ in range(100000):
        rx, rz = vx - wind, vz
        sp = math.hypot(rx, rz)
        k = 0.5 * RHO_A * cd(RHO_A * sp * dia / MU_A) * a * sp / m
        vx -= k * rx * dt
        vz -= (k * rz + G) * dt
        x += vx * dt
        z += vz * dt
        if x >= EDGE_IN:
            if z <= EDGE_UP + (x - EDGE_IN) * TAN_P:
                return x
        elif z <= -0.05:
            return x
        if x < -3 or x > 8:
            return x
    return x


SIZES = [(0.25e-3, 0.10), (0.5e-3, 0.20), (1.0e-3, 0.40), (1.5e-3, 0.20), (2.0e-3, 0.10)]
ANGLES = (35.0, 50.0, 65.0)


def on_target(v0, wind):
    tot = 0.0
    for dia, wf in SIZES:
        for ang in ANGLES:
            x = land(dia, v0, ang, wind)
            if 0.0 <= x <= STRIP_IN:
                tot += wf / len(ANGLES)
    return tot


AIM = 0.6 * STRIP_IN                     # still-air landing point of a 1 mm droplet at 50 deg: middle of the strip
best_v0 = min(np.arange(2.0, 10.01, 0.25), key=lambda v0: abs(land(1.0e-3, v0, 50.0, 0.0) - AIM))
say("C6", f"Drift screening model: strip from the head to {STRIP_IN:.2f} m inboard (roof edge at {EDGE_IN:.2f} m, "
          f"{EDGE_UP * 1000:.0f} mm above the nozzle); droplet mix 0.25 to 2 mm, launch 35, 50 and 65 deg; launch speed "
          f"{best_v0:.2f} m/s, chosen so a 1 mm droplet at 50 deg lands {AIM:.2f} m inboard in still air")
res = {}
for w in (0.0, 4.2, -4.2, 8.3, -8.3):
    res[w] = on_target(best_v0, w)
say("C7", "Fraction landing on the strip: " + ", ".join(
    f"{'still air' if w == 0 else ('onto roof' if w > 0 else 'off roof')} {abs(w):.1f} m/s {r * 100:.0f} %"
    for w, r in res.items()))
worst_design = min(res[8.3], res[-8.3])
worst_half = min(res[4.2], res[-4.2])
net = rate_on / 2
say("C8", f"Net average wetting at 50 % duty: {net * res[0.0]:.1f} mm/h in still air; worst eave {net * worst_half:.1f} mm/h "
          f"at 4.2 m/s local cross-wind and {net * worst_design:.1f} mm/h at 8.3 m/s; windward eave "
          f"{net * max(res[8.3], res[-8.3]):.1f} mm/h at 8.3 m/s; TRL 2 figure "
          f"{net * 0.5:.1f} mm/h (50 % drift); target 5 mm/h")
need_frac = 5.0 / net
say("C9", f"Meeting 5 mm/h at 50 % duty needs {need_frac * 100:.0f} % on target; with both zones running "
          f"continuously ({2 * q_zone:.0f} L/min, {2 * q_zone * 60 * EVENT_H:.0f} L per event) it needs "
          f"{5.0 / rate_on * 100:.0f} %")

LEE_W = 2.0                              # cross-eave wind above which only the leeward zone runs (m/s)
lee = {w: rate_on * res[-w] for w in (4.2, 8.3)}
say("C10", f"Leeward-only rule (decided, EGD-DDR-002, O4): above {LEE_W:.0f} m/s of cross-eave wind the controller runs only "
           f"the leeward zone, continuously at {q_zone:.0f} L/min, chosen from the wind vane; a detection on the windward side "
           f"returns to alternating zones. Leeward eave {lee[4.2]:.1f} mm/h at 4.2 m/s and {lee[8.3]:.1f} mm/h at 8.3 m/s "
           f"(alternating: {net * res[-4.2]:.1f} and {net * res[-8.3]:.1f} mm/h); windward eave dry until a windward detection, "
           f"then {net * res[8.3]:.1f} mm/h")
LEE_83 = lee[8.3]
LEE_42 = lee[4.2]

# ================================================================ D. Energy (R8)
BUCK = 0.85
loads_33 = {"Two MLX90640 at 4 Hz (18 mA each at 3.3 V, datasheet typical)": 2 * 0.018 * 3.3,
            "Two pod node microcontrollers and RS-485 (22 mA each at 3.3 V)": 2 * 0.022 * 3.3,
            "ESP32 controller, CPU active, radio off (60 mA at 3.3 V)": 0.060 * 3.3,
            "Wi-Fi status bursts, 10 % duty at 120 mA": 0.1 * 0.120 * 3.3,
            "Wind, humidity and pressure sensors": 0.010}
p33 = sum(loads_33.values())
p12_armed = p33 / BUCK + 0.010 * 12.8 + 0.002 * 12.8      # buck loss, charge controller 10 mA, beacon blink 2 mA
E_ARMED = p12_armed * 72
say("D1", "Armed loads at 3.3 V: " + "; ".join(f"{k} {v * 1000:.0f} mW" for k, v in loads_33.items())
    + f"; total {p33 * 1000:.0f} mW")
say("D2", f"Armed draw at the battery {p12_armed:.2f} W (buck at {BUCK * 100:.0f} %, charge controller 10 mA, beacon 2 mA); "
          f"72 h armed {E_ARMED:.1f} Wh")
VALVE_W, HOLD = 6.0, 0.35
p_spray = VALVE_W * HOLD + 0.030 * 12.8 + p12_armed
E_SPRAY = p_spray * EVENT_H + 1.2 * 5 / 60
say("D3", f"Spraying draw {p_spray:.2f} W (one {VALVE_W:.0f} W valve held at {HOLD * 100:.0f} %, relay coil 30 mA, "
          f"armed loads); 4 h spraying {E_SPRAY:.1f} Wh including 5 min of siren")
E_NEED = E_ARMED + E_SPRAY
BAT_AH = 10.0                            # 12.8 V 10 Ah, decided (EGD-DDR-002, O5); was 6 Ah
BAT_WH = 12.8 * BAT_AH
use25, use0, use_eol = BAT_WH * 0.9, BAT_WH * 0.9 * 0.9, BAT_WH * 0.9 * 0.8
say("D4", f"Need {E_NEED:.1f} Wh; battery {BAT_WH:.1f} Wh nominal, {use25:.1f} Wh usable at 90 % depth and 25 C "
          f"(margin {(use25 - E_NEED) / E_NEED * 100:+.0f} %), {use0:.1f} Wh at 0 C "
          f"({(use0 - E_NEED) / E_NEED * 100:+.0f} %), {use_eol:.1f} Wh at 80 % end of life "
          f"({(use_eol - E_NEED) / E_NEED * 100:+.0f} %)")
say("D5", f"Without holding-current reduction the valves would need {VALVE_W * EVENT_H:.0f} Wh instead of "
          f"{VALVE_W * HOLD * EVENT_H:.1f} Wh over 4 h")
PV_W, PSH, DER = 10.0, 4.0, 0.6
say("D6", f"Solar refill (no credit taken in R8): 10 W x {PSH:.0f} peak sun hours x {DER:.1f} = {PV_W * PSH * DER:.0f} Wh per "
          f"clear day against {p12_armed * 24:.1f} Wh per armed day")

# pump power options (b) and (c), studied at TRL 3 (EGD-DDR-001 D6)
p_pump = (p_man + 0.3) * 1e5 * q_zone / 60000          # plus 0.3 bar for suction and valve
ETA_P = 0.30
e_pump = p_pump / ETA_P * EVENT_H
say("D7", f"12 V diaphragm pump at 4 L/min and {p_man + 0.3:.1f} bar: hydraulic {p_pump:.1f} W, "
          f"electrical about {p_pump / ETA_P:.0f} W at {ETA_P * 100:.0f} % wire-to-water; {e_pump:.0f} Wh per 4 h event")
say("D8", f"Option (b), a separate 12.8 V LiFePO4 pump battery: {e_pump / 0.9:.0f} Wh nominal at 90 % depth, "
          f"so a 25 Ah (320 Wh) pack")
SWC_WH_MIN = 452.0
swc_use = SWC_WH_MIN * 0.9 * 0.92
say("D9", f"Option (c), one SwapCell pack (452 Wh at cell minimum, SWC-CAL-001) through a 48 to 12 V converter at 92 %: "
          f"{swc_use:.0f} Wh usable, {swc_use / (p_pump / ETA_P):.1f} h of pumping, {swc_use / e_pump:.1f} events; "
          f"pump current {p_pump / ETA_P / 12.8:.1f} A at 12.8 V, about {p_pump / ETA_P / 0.92 / 46.8:.1f} A from the pack "
          f"(legacy limit 15 A)")

# ================================================================ E. Mast wind load (R10)
RHO = 1.225
U = 120 / 3.6
q = 0.5 * RHO * U ** 2
say("E1", f"Gust 120 km/h: dynamic pressure {q:.0f} Pa")
z_up = P["standoff_z"][1]
items = [  # (name, area m2, Cd, height mm)
    ("Mast above the upper standoff", P["mast_od"] / 1000 * (P["mast_z1"] - z_up) / 1000, 1.2, (P["mast_z1"] + z_up) / 2),
    ("Anemometer, vane and crossarm", 0.022, 1.2, P["arm_z"] + 60),
    ("Solar panel (normal force at 45 deg)", P["panel"][0] / 1000 * P["panel"][1] / 1000, 1.2, P["panel_z"]),
    ("Humidity shield", 0.11 * 0.12, 1.2, P["trh_z"] + 50),
    ("Mast between standoffs", P["mast_od"] / 1000 * (z_up - P["standoff_z"][0]) / 1000, 1.2, (z_up + P["standoff_z"][0]) / 2),
]
F = {n: q * a * c for n, a, c, _ in items}
m_up = sum(q * a * c * (z - z_up) / 1000 for n, a, c, z in items if z > z_up)
say("E2", "Wind forces: " + "; ".join(f"{n} {F[n]:.0f} N" for n in F) + f"; total {sum(F.values()):.0f} N")
ro, ri = P["mast_od"] / 2, P["mast_od"] / 2 - P["mast_wall"]
Zm = math.pi / 4 * (ro ** 4 - ri ** 4) / ro
sig = m_up * 1000 / Zm
say("E3", f"Moment at the upper standoff {m_up:.0f} N m; mast section modulus {Zm:,.0f} mm3; bending stress {sig:.0f} MPa; "
          f"6061-T6 yield 240 MPa (factor {240 / sig:.1f}), heat-affected 110 MPa (factor {110 / sig:.1f})")
# reaction at the upper standoff: moment balance about the lower standoff
span = (z_up - P["standoff_z"][0]) / 1000
m_low = sum(q * a * c * (z - P["standoff_z"][0]) / 1000 for n, a, c, z in items if z > P["standoff_z"][0])
R_up = m_low / span
so, si = P["standoff_od"] / 2, P["standoff_od"] / 2 - P["standoff_wall"]
Zs = math.pi / 4 * (so ** 4 - si ** 4) / so
arm = P["mast_off"] / 1000
sig_s = R_up * arm * 1000 / Zs
say("E4", f"Upper standoff reaction {R_up:.0f} N (wind along the gable); cantilever moment {R_up * arm:.0f} N m on a "
          f"{P['standoff_od']} x {P['standoff_wall']} mm pipe (Z {Zs:,.0f} mm3): {sig_s:.0f} MPa, S235 factor {235 / sig_s:.1f}; "
          f"anchor pull on a 140 mm plate about {R_up * arm / 0.1 / 2:.0f} N per anchor (two anchors, 100 mm lever)")

# pod arm and verge cleat (EGD-DDR-003): wind on one pod at the same gust, masses from the model
from model import pod_components  # noqa: E402
PC = pod_components(P, -1)
RHO_M = {"pod_body_f": 2.7, "pod_lid_f": 2.7, "hood_f": 7.9, "lens_hood_f": 7.9, "pod_plate_f": 2.7, "arm_f": 2.7,
         "cleat_f": 2.7}
m_pod = sum(PC[k].shape.volume * r / 1e6 for k, r in RHO_M.items() if k not in ("arm_f", "cleat_f")) + 0.05
m_arm = PC["arm_f"].shape.volume * 2.7 / 1e6
W_pod = m_pod * 9.81
px_, py_, pz_ = P["pod"]
A_side = (px_ * pz_ + P["pod_hood"][0] * 10 + P["lens_hood"][2] * 20) / 1e6
F_h = q * A_side * 1.2
A_hood = P["pod_hood"][0] * P["pod_hood"][1] / 1e6
F_up = q * A_hood * 1.0
bw_, bt_ = P["bar"]
Z_weak = bw_ * bt_ ** 2 / 6
h_rise = (D["pod_z"] + 10 - P["cleat_top"] - bt_) / 1000
L_arm = math.hypot(D["pod_x"] - P["arm_q"][0], D["gut_yc"] - P["arm_q"][1]) / 1000 - 0.05
s_rise = F_h * h_rise * 1000 / Z_weak
s_run = max(W_pod, F_up - W_pod) * L_arm * 1000 / Z_weak
M_cl = F_h * (h_rise + 0.04) + max(W_pod, F_up) * (D["pod_x"] - D["verge_x"]) / 1000
pull = M_cl / 0.035 / 2
say("E5", f"Pod arm (40 x 6 mm flat bar) and verge cleat: pod, hood and plate {m_pod:.2f} kg ({W_pod:.1f} N), arm {m_arm:.2f} kg; "
          f"at 120 km/h {F_h:.1f} N sideways on {A_side:.4f} m2 and up to {F_up:.1f} N of lift on the hood; "
          f"rise {s_rise:.0f} MPa and run {s_run:.0f} MPa in weak-axis bending (6063-T6 yield 160 MPa, factor "
          f"{160 / max(s_rise, s_run):.0f}; {50 / max(s_rise, s_run):.0f} even if annealed in bending); "
          f"pull about {pull:.0f} N on each of the two 8 mm coach screws into the verge")

# ================================================================ F. Thermal (R10)
T_AMB = 60.0
box = P["box"]
a_sun = box[1] / 1000 * box[2] / 1000
a_out = 2 * (box[0] * box[1] + box[0] * box[2] + box[1] * box[2]) / 1e6 - a_sun
for alpha, tag in ((0.6, "F1"), (0.25, "F2")):
    dt = alpha * 800 * a_sun / (a_out * 15.0)
    say(tag, f"Ground enclosure in sun at {T_AMB:.0f} C ambient, absorptance {alpha}: about +{dt:.0f} K, "
             f"{T_AMB + dt:.0f} C inside (800 W/m2 on the {a_sun:.3f} m2 face, 15 W/(m2 K) on {a_out:.2f} m2)")
say("F3", "Component limits: MLX90640 -40 to 85 C; ESP32 module -40 to 85 C; LiFePO4 discharge -20 to 60 C, "
          "charge 0 to 45 C (typical datasheet values)")
hood_a = P["pod_hood"][0] * P["pod_hood"][1] / 1e6
dt_hood = 0.4 * 1000 * hood_a / (2 * hood_a * 25.0)
say("F4", f"Stainless pod hood in full sun at 8 m/s wind: about +{dt_hood:.0f} K above ambient; the shaded pod runs a few "
          f"kelvin above ambient. The pods sit 0.5 m above the gutters, where embers land, so radiant and ember "
          f"exposure is higher than for the former ridge-line head")

# ================================================================ G. Cost (R13)
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
kit = [r for r in rows if not r["item"].startswith("Option")]
opts = [r for r in rows if r["item"].startswith("Option")]
total = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in kit)
budget = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
say("G1", f"Kit parts {len(kit)} lines, total ${total:,.2f} against budget ${budget:,.0f}: "
          f"{(total - budget) / budget * 100:+.0f} %")
big = sorted(kit, key=lambda r: -float(r["qty"]) * float(r["unit_cost_usd"]))[:4]
say("G2", "Largest lines: " + "; ".join(f"{r['item']} ${float(r['qty']) * float(r['unit_cost_usd']):.0f}" for r in big))
for r in opts:
    say("G3", f"{r['item']}: ${float(r['unit_cost_usd']):.0f}, kit would be ${total + float(r['unit_cost_usd']):,.0f}")
say("G4", f"TRL 2 indicative total $420; TRL 3 revision 1 total $571; change ${total - 571:+.0f} since revision 1")

# ================================================================ Requirement table
flat_far = flat_rise(END - 13000.0)[0]
R1_STATUS = "Met" if FLAT_REACH >= 13.0 and len(g_h) == len(g_ok) else "At risk"
R3_STATUS = "Met" if (END - max(g_ok)) <= 1500 and (END - min(g_ok)) >= 12950 else "Not met"
REQ = [
    ("R6", "Wet the gutter and roof edge", f"Leeward-only rule: leeward eave {LEE_83:.1f} mm/h at 8.3 m/s, {LEE_42:.1f} mm/h "
     f"at 4.2 m/s; windward eave wetted only after a windward detection (screening model)", "5 mm/h net at 30 km/h",
     "Not met"),
    ("R13", "Stay within the budget", f"${total:,.0f}", f"${budget:,.0f} kit parts", "Not met" if total > budget else "Met"),
    ("R1", "Detect a smouldering ignition", f"Gutter debris in view {(END - max(g_ok)) / 1000:.2f} to {(END - min(g_ok)) / 1000:.2f} m "
     f"from the gutter end; 100 x 50 mm hot face reaches {THRESH:.0f} K to {spot_face_range:.0f} m; flat 100 cm2 spot reaches it "
     f"to {FLAT_REACH:.1f} m ({flat_far:.1f} K at 13 m); hanger straps hide debris {DEBRIS_BELOW_LIP:.0f} mm below the lip at "
     f"{len(g_ok) - len(g_h)} of {len(g_ok)} stations", "100 cm2 at 300 C, 1.5 to 13 m along the gutters, 10 s", R1_STATUS),
    ("R2", "Detect single landed embers", f"600 C ember reaches the {THRESH:.0f} K trigger to {R2_RNG:.1f} m centred in a pixel, "
     f"{R2_RNG_C:.1f} m on a pixel corner; false-trigger rate at {THRESH:.0f} K unknown", "10 mm, 600 C, within 8 m, 10 s",
     "Met" if R2_RNG_C >= 8.0 else "At risk"),
    ("R10", "Survive fire weather", f"Mast {sig:.0f} MPa (factor {240 / sig:.1f}); standoff factor {235 / sig_s:.1f}; "
     f"pod arm factor {160 / max(s_rise, s_run):.0f}; "
     f"enclosure {T_AMB + 0.6 * 800 * a_sun / (a_out * 15):.0f} C in sun at 60 C ambient; pods exposed at the gutters",
     "120 km/h; -10 to 60 C", "At risk"),
    ("R11", "Install without roof work or mains", "Mast on wall plates, pod arms on verge cleats, lip clips, 12 V only; "
     "install time not estimated", "No penetrations; 12 V; 6 h, two people", "Not verifiable at TRL 3"),
    ("R3", "Watch both roof planes", f"Gutter interiors in view {(END - max(g_ok)) / 1000:.2f} to {(END - min(g_ok)) / 1000:.2f} m "
     f"from the east end, both gutters (open gutter; see R1 for hanger straps)", "Both gutters, 1.5 m to far end", R3_STATUS),
    ("R4", "Arm only in fire weather", "Arming logic as specified; defaults adjustable", "30 km/h or 50 km/h gusts, RH 20 % or less, 10 min", "Met"),
    ("R5", "Start water quickly", f"{T_DET + T_VALVE + fill_one[1]:.0f} s worst zone, detection-side zone first",
     "60 s", "Met"),
    ("R7", "Use little water", f"{q_zone:.0f} L/min; {water:.0f} L per 4 h event", "4 L/min; 1,000 L", "Met"),
    ("R8", "Work through a grid outage", f"{E_NEED:.0f} Wh needed; {use25:.0f} Wh usable at 25 C, {use0:.0f} Wh at 0 C, "
     f"{use_eol:.0f} Wh at end of life", "72 h armed plus 4 h spraying on the kit battery",
     "Met" if use_eol >= E_NEED else "At risk"),
    ("R9", "Fail safely", "Normally closed valves; fail-to-wet on sensor loss; alarms", "As specified", "Met"),
    ("R12", "Tell people what it is doing", "Siren, beacon, log; phone alerts need a network", "As specified", "Met"),
]
ORDER = {"Not met": 0, "At risk": 1, "Not verifiable at TRL 3": 2, "Met": 3}
REQ.sort(key=lambda r: ORDER[r[4]])
with (ROOT / "docs" / "04-calcs" / "results.csv").open("w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["id", "requirement", "value_trl3", "target", "status"])
    w.writerows(REQ)
counts = {}
for r in REQ:
    counts[r[4]] = counts.get(r[4], 0) + 1
say("H1", "Requirement status: " + ", ".join(f"{k} {v}" for k, v in counts.items()))
say("H2", "Wrote docs/04-calcs/results.csv")
