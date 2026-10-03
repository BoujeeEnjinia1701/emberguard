"""EmberGuard prototype build plan pictures (EGD-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|wiring ...]
With no argument it draws everything; a name such as "step-05" or "joint-03" or "EGD-DWG-104"
draws that one picture only (one picture per process keeps memory low). Every picture is drawn
from cad/src/model.py (build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        the kit pulled apart, numbered in build order
    cad/drawings/EGD-DWG-101 to 113        making sketches for the made and drilled components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, house_parts, pod_components, arm_frame  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-02"
D = derived(P)
_C = None
_H = None


def C():
    global _C
    if _C is None:
        _C = build_components(P)
    return _C


def H():
    global _H
    if _H is None:
        _H = house_parts(P)
    return _H


def _fuse(shapes):
    out = None
    for s in shapes:
        if s is None:
            continue
        out = s if out is None else out + s
    return out


def S(*ks):
    return _fuse([C()[k].shape for k in ks])


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def win(sh, x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return sh & (Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0))


def mv(shape, d):
    from build123d import Pos
    return Pos(*d) * shape


MX = D["mast_x"]
SY = D["standoff_y"]
ZL, ZU = P["standoff_z"]
L2 = P["house_l"] / 2
PODF = (D["pod_x"], -D["gut_yc"], D["pod_z"])
BC = D["box_c"]
COL = {"plate": "#A8A29E", "flange": "#57534E", "standoff": "#78716C", "xplate": "#1D4ED8", "bolt": "#111827",
       "mast": "#94A3B8", "anem": "#1F2937", "trh": "#E7E5E4", "panel": "#1E3A8A", "pmount": "#475569",
       "pod": "#0F766E", "lid": "#115E59", "sensor": "#C2410C", "node": "#16A34A", "lhood": "#64748B",
       "hood": "#D6D3D1", "pplate": "#0369A1", "arm": "#B45309", "cleat": "#7C2D12", "box": "#CBD5E1",
       "door": "#E2E8F0", "lugs": "#374151", "gear": "#9CA3AF", "board": "#16A34A", "relay": "#DB2777",
       "battery": "#7C3AED", "strap": "#64748B", "siren": "#DC2626", "key": "#991B1B", "glands": "#1F2937",
       "vboard": "#A3A3A3", "manifold": "#A16207", "valves": "#D4A017", "xducer": "#0EA5E9", "clips": "#525252",
       "lines": "#2563EB", "heads": "#0F766E", "lipclip": "#57534E", "cable": "#111827", "earth": "#15803D",
       "shade": "#F59E0B", "wall": "#E7E5E4", "roof": "#A8A29E", "gutter": "#78716C"}


def ctx_house(x0, x1, y0, y1, z0, z1, names=("walls", "roof", "fascia_gutters")):
    out = []
    lab = {"walls": "House wall (context)", "roof": "Roof overhang (context)", "fascia_gutters": "Fascia and gutter (context)"}
    for n in names:
        s = win(H()[n], x0, x1, y0, y1, z0, z1)
        if s is not None and s.volume > 1:
            out.append(part(lab[n], s, "#E5E7EB", alpha=0.6))
    return out


# ----------------------------------------------------------------- overview
def overview():
    """The kit pulled apart in three panels (the mast group, one sensor pod, the ground unit with the
    valve board and a spray-line sample), each at its own scale, numbered in build order with one key."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from build123d import Pos
    INK, ACC = "#111827", "#0F766E"
    lo_e = win(S("earth"), MX - 60, MX + 60, -100, 100, 2200, 2400)
    rod = Pos(MX - (L2 + 400) + 260, 60, 2300 + 1100 - 900) * win(S("earth"), L2 + 380, L2 + 420, -100, 0, -1100, 140)
    A = [("Wall plates (2)", S("wall_plates"), COL["plate"], (-760, 0, 0)),
         ("Slip-on base flanges (2)", S("flanges"), COL["flange"], (-540, 0, 0)),
         ("Standoff pipes (2)", S("standoffs"), COL["standoff"], (-260, 0, -120)),
         ("Crossover plates (2) and U-bolts (8)", S("xplates", "ubolts"), COL["xplate"], (0, 220, 0)),
         ("Mast tube with end cap", S("mast", "mast_cap"), COL["mast"], (200, 0, 0)),
         ("Anemometer and vane on the mast-top sleeve", S("anem"), COL["anem"], (200, 0, 300)),
         ("Humidity shield, arm and clamp", S("trh"), COL["trh"], (520, 0, 0)),
         ("Solar panel and tilt mount", S("panel", "panel_mount"), COL["panel"], (200, -350, 0))]
    B = [("Pod box, drilled, and lid", S("pod_body_f", "pod_lid_f"), COL["pod"], (0, 0, 0)),
         ("Thermal sensor", S("sensor_f"), COL["sensor"], (-40, 0, 75)),
         ("Pod node board and cable gland", S("node_f", "cgland_f"), COL["node"], (160, 0, 60)),
         ("Lens hood", S("lens_hood_f", "lens_hood_screws_f"), COL["lhood"], (-150, 0, -20)),
         ("Hood on four spacers", S("hood_f", "hood_spacers_f"), COL["hood"], (0, 0, 120)),
         ("Pod plate and spacers", S("pod_plate_f", "pod_spacers_f"), COL["pplate"], (0, 0, -90)),
         ("Pod arm", S("arm_f"), COL["arm"], (0, 0, -190)),
         ("Verge cleat with its screws", S("cleat_f", "pod_fix_f"), COL["cleat"], (-140, 0, -300))]
    sample = win(S("lines", "lip_clips", "heads"), 5250, 5750, -4800, -4500, 2400, 2700)
    Cg = [("Ground enclosure, drilled, with lugs and glands", S("box_body", "box_lugs", "box_glands"), COL["box"], (0, 0, 0)),
          ("Gear plate", S("gear_plate"), COL["gear"], (300, 0, 0)),
          ("Controller board and relay", S("board", "relay"), COL["board"], (480, 0, 0)),
          ("Battery and strap", S("battery", "strap"), COL["battery"], (480, 0, -120)),
          ("Siren and key switch", S("siren", "key"), COL["siren"], (0, 0, 180)),
          ("Enclosure door", S("box_door"), COL["door"], (700, 0, 0)),
          ("Sun shade, folded sheet and two arms", S("shade", "shade_arms", "shade_screws"), COL["shade"], (0, 0, 420)),
          ("Valve board and pipe clips", S("valve_board", "pipe_clips"), COL["vboard"], (0, 0, 0)),
          ("Manifold, valves and transducer", S("manifold", "valves", "xducer"), COL["valves"], (280, 0, 0)),
          ("Spray line, lip clips and a head (sample)", Pos(L2 + 300 - 5500, -1800 + D["line_y"], 150 - D["line_z"]) * sample, COL["lines"], (0, 0, 0))]
    A.append(("Earth clamp and rod (rod shortened)", lo_e + rod, COL["earth"], (0, 0, 0)))
    panels = [(A, "Mast and what it carries", (0.33, 0.06, 0.30, 0.84), 16, -55),
              (B, "One sensor pod (two are built), larger scale", (0.64, 0.50, 0.35, 0.40), 20, -60),
              (Cg, "Ground unit, valve board and a spray-line sample", (0.64, 0.06, 0.35, 0.42), 18, -45)]
    order = [it[0] for it in A[:-1]] + [it[0] for it in B] + [it[0] for it in Cg] + [A[-1][0]]
    num = {n: k + 1 for k, n in enumerate(order)}
    fig = plt.figure(figsize=(13, 8.6), dpi=150)
    fig.text(0.02, 0.975, "EmberGuard prototype kit: every component, pulled apart", fontsize=12, fontweight="bold", color=INK, va="top")
    fig.text(0.02, 0.945, "Numbered in build order. Three groups, each drawn at its own scale; not at the installed spacing",
             fontsize=8.5, color="#374151", va="top")
    fig.text(0.02, 0.012, bv.BANNER, fontsize=6.5, color="#B45309")
    fig.text(0.98, 0.012, "github.com/BoujeeEnjinia1701/emberguard", fontsize=6.5, color=ACC, ha="right", family="monospace")
    for items, cap, rect, el, az in panels:
        ax = fig.add_axes(rect); ax.set_axis_off()
        W, Hh = int(rect[2] * 13 * 150), int(rect[3] * 8.6 * 150)
        parts = [part(n, sh, col, explode=e) for n, sh, col, e in items]
        Sq = max(W, Hh) if Hh > W else 0    # a tall panel: render square, then crop (the rasterizer fits the short side)
        if not Sq:
            Sq = None
        if Sq:
            img, proj, verts = bv._raster([(p_, p_.color, 1.0, p_.explode) for p_ in parts], el, az, Sq, Sq)
            ox, oy = (Sq - W) // 2, (Sq - Hh) // 2
            img = img[oy:oy + Hh, ox:ox + W]
        else:
            img, proj, verts = bv._raster([(p_, p_.color, 1.0, p_.explode) for p_ in parts], el, az, W, Hh)
            ox = oy = 0
        ax.imshow(img, interpolation="bilinear")
        for p_, v in zip(parts, verts):
            x, y = proj(bv._anchor(v))
            x, y = x - ox, y - oy
            ax.text(x, y, str(num[p_.name]), fontsize=7.5, fontweight="bold", color="white", ha="center", va="center",
                    bbox=dict(boxstyle="circle,pad=0.3", fc=ACC, ec="white", lw=0.8))
        fig.text(rect[0] + 0.005, rect[1] + rect[3] + 0.005, cap, fontsize=8.5, fontweight="bold", color=INK)
    top, step_ = 0.89, 0.0305
    for k, n in enumerate(order):
        yk = top - k * step_
        col = [it[2] for it in A + B + Cg if it[0] == n][0]
        fig.text(0.025, yk, str(k + 1), fontsize=7.5, fontweight="bold", color="white", ha="center", va="center",
                 bbox=dict(boxstyle="circle,pad=0.3", fc=ACC, ec="white", lw=0.8))
        fig.patches.append(plt.Rectangle((0.040, yk - 0.007), 0.011, 0.014, transform=fig.transFigure, fc=col, ec=INK, lw=0.5))
        fig.text(0.057, yk, n, fontsize=7.8, color=INK, va="center")
    out = OUT / "overview.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    import build123d as b
    c = C()
    base = dict(project="EmberGuard", date=DATE)
    out = []
    L = lambda k: c[k].shape  # noqa: E731
    walls = part("House wall", win(H()["walls"], L2 - 30, L2, SY - 110, SY + 110, ZL - 110, ZL + 110), "#E5E7EB")

    def sheet(no, *a, **k):
        if only and only != no:
            return
        out.append(bv.component_sheet(*a, dwg_no=no, **k, **base))

    # 101 wall plate (the lower one, drawn standing as on the wall)
    wp = win(L("wall_plates"), L2 - 1, L2 + 20, -200, 300, ZL - 100, ZL + 100)
    sheet("EGD-DWG-101", Part("Wall plate", wp, COL["plate"]),
          [walls, part("Flange", win(L("flanges"), L2, L2 + 100, -200, 300, ZL - 100, ZL + 100), "#9CA3AF"),
           part("Standoff", win(L("standoffs"), L2, MX + 60, -200, 300, ZL - 100, ZL + 100), "#9CA3AF")],
          title="EmberGuard wall plate (make 2): making sketch", material="Aluminium plate 8 mm, 6082 or 5083 class",
          view_shape=b.Pos(-L2, -SY, -ZL) * wp, inset_view=(20, -40),
          notes=["Make two. Cut 140 x 140 mm from 8 mm aluminium plate; square",
                 "  the edges and round the corners to about 3 mm.",
                 "Anchor holes: four 11 mm holes on a 100 mm square (20 mm in",
                 "  from each edge), for M10 wall anchors.",
                 "Flange holes: four 9 mm holes on an 80 mm circle, at 45 degrees",
                 "  to the edges; countersink them on the wall side for M8",
                 "  countersunk screws, so the heads sit flush against the wall.",
                 "Check the flange you bought: its hole circle sets these four holes.",
                 "Fit: the flange bolts to the outer face with four M8 countersunk",
                 "  screws and nyloc nuts; the plate goes on the gable wall with four",
                 "  anchors, its centre 43 mm to the side of the mast's line.",
                 "Check: the flange sits flat and no screw head stands proud at the back."])
    # 102 standoff pipe, laid along X
    so = win(L("standoffs"), L2, MX + 100, -200, 300, ZL - 100, ZL + 100)
    sheet("EGD-DWG-102", Part("Standoff pipe", so, COL["standoff"]),
          [walls, part("Mast", win(L("mast"), MX - 50, MX + 50, -100, 100, ZL - 300, ZL + 300), "#9CA3AF"),
           part("Flange and plate", win(L("flanges") + L("wall_plates"), L2, L2 + 100, -200, 300, ZL - 100, ZL + 100), "#9CA3AF"),
           part("Crossover plate", win(L("xplates"), MX - 60, MX + 60, -50, 50, ZL - 60, ZL + 60), "#9CA3AF")],
          title="EmberGuard standoff pipe (make 2): making sketch", material="Galvanized steel pipe DN25 (33.7 x 3.2 mm)",
          view_shape=b.Pos(-L2, -SY, -ZL) * so, inset_view=(20, -50),
          notes=["Make two. Cut 739 mm lengths of DN25 (33.7 mm outside) galvanized",
                 "  steel pipe; square both ends with a file and deburr inside and out.",
                 "No threads and no holes: the flange grips the pipe with its set",
                 "  screws and the U-bolts clamp it at the mast.",
                 "Paint the cut ends with zinc-rich paint.",
                 "Fit: one end goes 45 mm into the flange hub (to its stop) and the",
                 "  set screws are tightened; the pipe then runs past the mast, which",
                 "  it passes 6 mm to the side of, and ends 50 mm beyond the mast's line.",
                 "Fit a plastic end cap on the outer end.",
                 "Check: length 739 mm within 2 mm; both ends square."])
    # 103 crossover plate, plate in the XZ plane
    xp = win(L("xplates"), MX - 60, MX + 60, -10, 60, ZL - 60, ZL + 60)
    sheet("EGD-DWG-103", Part("Crossover plate", xp, COL["xplate"]),
          [part("Mast", win(L("mast"), MX - 50, MX + 50, -100, 100, ZL - 250, ZL + 250), "#9CA3AF"),
           part("Standoff", win(L("standoffs"), MX - 250, MX + 60, -100, 100, ZL - 60, ZL + 60), "#9CA3AF"),
           part("U-bolts", win(L("ubolts"), MX - 80, MX + 80, -60, 80, ZL - 80, ZL + 80), "#6B7280")],
          title="EmberGuard crossover plate (make 2): making sketch", material="Aluminium plate 6 mm, 6082 or 5083 class",
          view_shape=b.Pos(-MX, -20, -ZL) * xp, inset_view=(18, -35),
          notes=["Make two. Cut 100 x 100 mm from 6 mm aluminium plate; deburr.",
                 "Mark a centre cross. Measure sideways from the vertical centre line",
                 "  and up or down from the horizontal one.",
                 "Mast U-bolt holes: four 9 mm holes, 24 mm each side of centre,",
                 "  30 mm above and 30 mm below centre.",
                 "Standoff U-bolt holes: four 9 mm holes, 35 mm each side of centre,",
                 "  20.9 mm above and 20.9 mm below centre.",
                 "Check the U-bolts you bought: their leg spacing sets these holes",
                 "  (M8 U-bolts for 40 mm tube and for 33.7 mm pipe).",
                 "Fit: the plate stands upright between the mast and the standoff;",
                 "  the mast touches one face, the standoff the other. Two U-bolts",
                 "  wrap the mast, two wrap the standoff, nyloc nuts on the far face.",
                 "Check: all eight holes line up with the U-bolt legs by hand."])
    # 104 mast tube, laid along X
    mt = L("mast")
    sheet("EGD-DWG-104", Part("Mast tube", mt, COL["mast"]),
          [part("Standoffs and crossover plates", L("standoffs") + L("xplates"), "#9CA3AF"),
           part("Anemometer", L("anem"), "#9CA3AF"), part("Panel", L("panel"), "#9CA3AF")],
          title="EmberGuard mast tube: making sketch", material="Aluminium tube 40 x 2 mm, 6061-T6",
          view_shape=b.Rot(0, 90, 0) * b.Pos(-MX, 0, -P["mast_z0"]) * mt, inset_view=(15, -50),
          notes=["Cut 2,450 mm of 40 x 2 mm 6061-T6 tube; square and deburr both ends.",
                 "Measure from the bottom end. Drill two 12 mm holes through one wall",
                 "  only and fit a rubber grommet in each:",
                 "  - at 1,220 mm, on the side that will face east (away from the",
                 "    wall), for the humidity sensor lead;",
                 "  - at 1,250 mm, turned 90 degrees to face south (toward the",
                 "    panel), for the panel lead.",
                 "Pull the mast cable through the tube before the end cap goes on.",
                 "Fit: the plastic end cap with its grommet goes in the bottom end;",
                 "  the mast-top sleeve slides 40 mm over the top end (two set screws).",
                 "The mast stands 700 mm off the gable wall, bottom 2.25 m above",
                 "  the ground, top 4.70 m.",
                 "Check: length 2,450 mm within 2 mm; no burrs to cut the cable."])
    # 105 pod box, drilled (pod frame, level)
    pl = pod_components(P, -1, local=True)
    body = pl["pod_body_f"].shape
    sheet("EGD-DWG-105", Part("Pod box", c["pod_body_f"].shape, COL["pod"]),
          [part("Lid, hood, lens hood, plate and arm", L("pod_lid_f") + L("hood_f") + L("lens_hood_f") + L("pod_plate_f") + L("pod_spacers_f")
                + win(L("arm_f"), 6550, 6800, -4700, -4450, 2850, 2950), "#9CA3AF")],
          title="EmberGuard pod box (make 2): drilling sketch", material="Bought die-cast aluminium box about 100 x 80 x 70 mm, 4 mm walls",
          view_shape=body, inset_view=(20, -50),
          notes=["Bought box with its lid; drill the body only. West wall is the",
                 "  short end that faces along the gutter; heights from the floor.",
                 "West wall: one 9.5 mm window, centred, 35 mm up; four holes",
                 "  tapped M2.5 at 10 mm each side and 10 mm above and below the",
                 "  window, for the sensor board; two holes tapped M3, 15 mm above",
                 "  and 15 mm below the window, for the lens hood.",
                 "East wall: one 16.2 mm hole, centred, 20 mm up, for the M16 gland.",
                 "Floor: two 6.5 mm holes on the centre line, 30 mm each side of",
                 "  the middle, for the M6 bolts down to the pod plate.",
                 "Lid: four holes tapped M4 at 35 mm each side and 28 mm in front",
                 "  and behind the middle, for the hood spacers.",
                 "Clamp the box in soft jaws; centre punch lightly; deburr inside.",
                 "Check: the sensor's 9.2 mm can passes the window without touching."])
    # 106 lens hood
    lh = pl["lens_hood_f"].shape
    sheet("EGD-DWG-106", Part("Lens hood", c["lens_hood_f"].shape, COL["lhood"]),
          [part("Pod box", L("pod_body_f") + L("pod_lid_f"), "#9CA3AF")],
          title="EmberGuard lens hood (make 2): making sketch", material="Stainless steel sheet 1 mm, 304 class",
          view_shape=b.Pos(P["pod"][0] / 2, 0, 0) * lh, inset_view=(18, -150),
          notes=["A short rectangular tube that shades the sensor window without",
                 "  cutting into its 55 x 35 degree view.",
                 "Cut a cross-shaped blank: a 30 x 20 mm centre opening edged by four",
                 "  19 mm sides (two 30 mm wide, two 20 mm wide), plus a 11 mm flange",
                 "  on the outer end of the top and bottom sides.",
                 "Fold the four sides 90 degrees to make a tube 28 mm wide and 18 mm",
                 "  tall inside, 20 mm deep; fold the two flanges 90 degrees outward.",
                 "Drill a 3.4 mm hole in the middle of each flange.",
                 "Fit: the flanges lie flat on the west wall of the pod, the opening",
                 "  centred on the window, wide side horizontal; two M3 stainless",
                 "  screws into the tapped holes.",
                 "Check: from the window, the inside edges are at least 31 degrees off",
                 "  the axis sideways and 19 degrees up and down."])
    # 107 pod hood
    hd = pl["hood_f"].shape
    sheet("EGD-DWG-107", Part("Hood", c["hood_f"].shape, COL["hood"]),
          [part("Pod box and lid", L("pod_body_f") + L("pod_lid_f") + L("hood_spacers_f"), "#9CA3AF")],
          title="EmberGuard pod hood (make 2): making sketch", material="Stainless steel sheet 1 mm, 304 class",
          view_shape=hd, inset_view=(25, -50),
          notes=["Cut a 170 x 150 mm blank: the 150 x 130 mm top with a 10 mm",
                 "  flange on each edge. Drill a 3 mm relief hole at each corner.",
                 "Fold all four flanges 90 degrees down (drip edges).",
                 "Drill four 4.4 mm holes for the spacers: 35 mm each side and 28 mm",
                 "  in front and behind a point 15 mm east of the top's middle",
                 "  (the hood hangs 40 mm further over the west end, the lens end).",
                 "Fit: four 15 mm M4 aluminium spacers screw into the lid; the hood",
                 "  sits on them and four M4 screws hold it. The 15 mm air gap",
                 "  keeps sun and radiant heat off the box.",
                 "Check: the flanges stand 5 mm or more clear of the lid all round."])
    # 108 pod plate, unrotated
    (qx, qy), (ux, uy), Lr = arm_frame(P, -1)
    yaw = -P["aim_yaw"]
    pp = b.Rot(0, 0, -yaw) * b.Pos(-PODF[0], -PODF[1], -(P["pod_plate_z"])) * L("pod_plate_f")
    sheet("EGD-DWG-108", Part("Pod plate", L("pod_plate_f"), COL["pplate"]),
          [part("Pod and spacers", L("pod_body_f") + L("pod_spacers_f"), "#9CA3AF"), part("Arm", L("arm_f"), "#9CA3AF")],
          title="EmberGuard pod plate (make 2, a front and a back): making sketch", material="Aluminium plate 6 mm, 6082 class",
          view_shape=pp, inset_view=(12, -80),
          notes=["Cut 120 x 70 mm from 6 mm plate; deburr. Mark a centre cross;",
                 "  the long centre line is the pod's axis (it points along the gutter).",
                 "Pivot: one 8.5 mm hole at the centre.",
                 "Pod bolts: two holes on the long centre line, 30 mm each side of",
                 "  centre; drill 5 mm and tap M6.",
                 "Slot: a curved slot 6.5 mm wide on a 35 mm radius about the centre,",
                 "  from 25 to 49 degrees off the long centre line, on the side away",
                 "  from the house and toward the pod's east (back) end. Chain drill",
                 "  and file.",
                 "The front pod's plate and the back pod's plate are mirror images.",
                 "Fit: the pod stands on two spacers on this plate; the plate turns",
                 "  on the arm's pivot bolt and the slot bolt locks the aim (10 degrees",
                 "  toward the house).",
                 "Check: the pod bolts screw in by hand."])
    # 109 pod arm, laid square
    rot = math.degrees(math.atan2(uy, ux))
    ar = b.Rot(0, 0, -rot) * b.Pos(-qx, -qy, -P["cleat_top"]) * L("arm_f")
    tb = Lr - 25
    sheet("EGD-DWG-109", Part("Pod arm", L("arm_f"), COL["arm"]),
          [part("Verge cleat", L("cleat_f"), "#9CA3AF"), part("Pod plate and pod", L("pod_plate_f") + L("pod_body_f") + L("pod_lid_f"), "#9CA3AF")],
          title="EmberGuard pod arm (make 2): making sketch", material="Aluminium flat bar 40 x 6 mm, 6060 or 6063-T6",
          view_shape=ar, inset_view=(20, -40),
          notes=["Cut 540 mm of 40 x 6 mm flat bar; it is trimmed after bending.",
                 "Bend 1: up 90 degrees, its outside face 236 mm from the start end.",
                 "Bend 2: forward 90 degrees, so the top of the tab is 212 mm above",
                 "  the underside of the run. Bend cold in a vice round a 12 mm",
                 "  former; trim the tab to 80 mm beyond the rise's outside face.",
                 "Run: two 6.5 mm holes on the centre line, 20 and 60 mm from the start.",
                 "Tab: an 8.5 mm pivot hole 25 mm, and a 6.5 mm hole 60 mm, beyond",
                 "  the rise's outside face.",
                 "Mark the holes after bending; the drawing gives finished positions.",
                 "Fit: the run lies flat on the cleat (two M6 bolts); the pod plate",
                 "  lies flat on the tab (M8 pivot bolt and an M6 bolt in the slot).",
                 "Check: the tab is level when the run is level, within 1 degree."])
    # 110 verge cleat
    cl = L("cleat_f")
    sheet("EGD-DWG-110", Part("Verge cleat", cl, COL["cleat"]),
          [part("Roof end and fascia", win(H()["roof"] + H()["fascia_gutters"], 6250, 6500, -4700, -4200, 2300, 2900), "#9CA3AF"),
           part("Arm", L("arm_f"), "#9CA3AF")],
          title="EmberGuard verge cleat (make 2, a front and a back): making sketch", material="Aluminium equal angle 80 x 80 x 6 mm",
          view_shape=b.Pos(-D["verge_x"], P["cleat_y"], -P["cleat_top"]) * cl, inset_view=(25, -35),
          notes=["Cut 140 mm of 80 x 80 x 6 mm angle; square and deburr.",
                 "Upright leg (against the verge board): two 9 mm holes 45 mm down",
                 "  from the top face, 40 mm each side of the middle, for 8 mm",
                 "  coach screws.",
                 "Flat leg (sticks out east, level): two 6.5 mm holes on the arm's",
                 "  line, which runs at 47 degrees outward: 37 and 64 mm out from the",
                 "  face on the verge, 7 and 37 mm toward the gutter from the middle.",
                 "  Easiest: drill them through the arm on assembly.",
                 "The two cleats are mirror images.",
                 "Fit: the upright leg on the end of the roof overhang (the verge or",
                 "  barge board), 30 to 170 mm in from the eave edge, top 232 mm",
                 "  above the gutter lip; the arm's run on top of the flat leg.",
                 "Check: the flat leg is level and the screws reach solid timber."])
    # 111 ground enclosure, drilled
    sheet("EGD-DWG-111", Part("Ground enclosure", L("box_body") + L("box_door"), COL["box"]),
          [part("Gable wall", win(H()["walls"], L2 - 100, L2, -2400, -1200, 300, 1600), "#E5E7EB"),
           part("Valve board", L("valve_board") + L("valves") + L("manifold"), "#9CA3AF")],
          title="EmberGuard ground enclosure: drilling sketch", material="Bought steel IP65 wall box 400 x 320 x 160 mm, light-coloured",
          view_shape=b.Pos(-BC[0], -BC[1], -BC[2]) * (L("box_body") + L("box_door")), inset_view=(18, -40),
          notes=["Bought box, door on the front (it faces east, away from the wall).",
                 "Take out the gear plate before drilling. Measure from the box's centre",
                 "  line (left and right as seen facing the door).",
                 "Bottom: four 20.5 mm holes for M20 glands, 25 mm behind the door",
                 "  face (clear of the battery), at 100 and 40 mm left and 40 and",
                 "  100 mm right: front pod, valves, mast, back pod cables.",
                 "Top: one 16 mm hole for the siren's lead, 80 mm left of centre,",
                 "  110 mm out from the back; the siren's gasket seals it.",
                 "Door: one 22 mm hole for the key switch, 90 mm right of centre",
                 "  and 120 mm above the middle.",
                 "Pilot drill 4 mm, open with a step drill, deburr, touch up the paint.",
                 "Fit: four lugs on the back corners; M8 screws into wall plugs.",
                 "Check: no swarf left inside; the door gasket is undamaged."])
    # 114 sun shade
    sh = L("shade") + L("shade_arms")
    sheet("EGD-DWG-114", Part("Sun shade and arms", sh, COL["shade"]),
          [part("Gable wall", win(H()["walls"], L2 - 100, L2, -2400, -1200, 900, 1700), "#E5E7EB"),
           part("Ground enclosure", L("box_body") + L("box_door") + L("siren"), "#9CA3AF")],
          title="EmberGuard sun shade (make 1): making sketch", material="Aluminium sheet 1 mm, 5052 class, painted white; arms of 40 x 6 mm flat bar",
          view_shape=b.Pos(-L2, -BC[1], -P["shade_z"]) * sh, inset_view=(20, -40),
          notes=["Cut a blank 640 x 460 mm from 1 mm sheet; deburr; paint it white",
                 "  (or buy pre-coated white sheet and touch up the cut edges).",
                 "Mark a top plate 360 mm deep and 440 mm wide in the middle of the",
                 "  blank. A 100 mm flap goes along its outer edge and a 100 mm flap",
                 "  along each side. Cut a small relief at each corner where flaps meet.",
                 "Fold all three flaps 90 degrees down in a sheet folder or between",
                 "  hardwood blocks in the vice.",
                 "Arms: cut two 400 mm lengths of 40 x 6 mm flat bar. Bend 40 mm of",
                 "  one end 90 degrees over a 12 mm former; drill a 6.5 mm hole in the",
                 "  middle of that wall tab. Rivet the plate to the arms (two 4 mm",
                 "  rivets each, 100 and 250 mm from the wall end).",
                 "Fit: the tabs go on the gable wall 120 mm either side of the",
                 "  enclosure's centre line, the plate's top 1,480 mm above the ground,",
                 "  level, on two M6 screws into wall plugs. The plate stands 130 mm",
                 "  above the box and clears the siren by about 60 mm.",
                 "Check: the door swings fully open under the front flap; the shade is level."])
    # 112 battery strap
    st = L("strap")
    sheet("EGD-DWG-112", Part("Battery strap", st, COL["strap"]),
          [part("Battery and gear plate", L("battery") + L("gear_plate"), "#9CA3AF")],
          title="EmberGuard battery strap: making sketch", material="Aluminium strip 25 x 1.5 mm, 1050 or 5052",
          view_shape=b.Pos(-BC[0], -BC[1], -BC[2]) * st, inset_view=(25, -30),
          notes=["Cut 25 mm wide strip about 395 mm long.",
                 "Mark the battery's front width (151 mm) in the middle and its depth",
                 "  (98 mm) each side of that, then a 20 mm foot on each end.",
                 "Fold 90 degrees at each mark so the strap fits round the battery's",
                 "  front and sides and the feet turn outward against the gear plate.",
                 "Drill one 4.5 mm hole in the middle of each foot.",
                 "Line the inside with 2 mm closed-cell foam tape.",
                 "Fit: the battery stands on the box floor against the gear plate;",
                 "  the strap goes round it 50 mm above the floor; M4 screws and",
                 "  nyloc nuts through the gear plate.",
                 "Check: the battery cannot move when you push it."])
    # 113 valve board
    vb = L("valve_board")
    sheet("EGD-DWG-113", Part("Valve board", vb, COL["vboard"]),
          [part("Gable wall", win(H()["walls"], L2 - 100, L2, -2500, -1100, 200, 750), "#E5E7EB"),
           part("Clips, manifold and valves", L("pipe_clips") + L("manifold") + L("valves") + L("xducer"), "#9CA3AF")],
          title="EmberGuard valve board: making sketch", material="Aluminium sheet 3 mm, 5052 class",
          view_shape=b.Rot(0, 90, 0) * b.Pos(-L2, 1800, -465) * vb, inset_view=(18, -40),
          notes=["Cut 1,100 x 270 mm from 3 mm sheet; round the corners; deburr.",
                 "Wall holes: six 7 mm holes, 105 mm above and below the middle,",
                 "  at the middle and 500 mm each side of it.",
                 "Pipe clip holes: two pairs of 5.5 mm holes, 500 mm each side of",
                 "  the middle, 55 mm above the middle, 24 mm apart up and down.",
                 "Fit: the board goes on the gable wall below the enclosure, its",
                 "  middle 465 mm above the ground and below the enclosure's centre;",
                 "  six screws into wall plugs. The manifold's centre is 45 mm off it,",
                 "  in two stand-off pipe clips; the valves hang from its tees, 5 mm clear.",
                 "Check: the board is level and flat on the wall."])
    return out


# ----------------------------------------------------------------- joints
def joint_at(parts, anchors, out, title, subtitle=None, elev=24, azim=-58, size=(8, 6), dpi=160, cut=None):
    """Like build_views.joint, but each leader ends at a chosen point on a visible face of its part
    (anchors: one 3D point per part, or None for the kit's default), so no leader ends on a neighbour."""
    import numpy as np
    if cut:
        parts = bv._cut(parts, cut)
    parts = [p_ for p_ in parts if bv._has_volume(p_.shape)]
    W, Hh = int(size[0] * dpi), int(size[1] * dpi * bv.PIC_HEIGHT)
    img, proj, verts = bv._raster([(p_, p_.color, p_.alpha, (0, 0, 0)) for p_ in parts], elev, azim, W, Hh)
    fig, ax = bv._frame(size, dpi, title, subtitle)
    ax.imshow(img, interpolation="bilinear")
    pts = [np.asarray(anchors.get(p_.name), float) if anchors.get(p_.name) is not None else bv._anchor(v)
           for p_, v in zip(parts, verts)]
    bv._draw_labels(ax, proj, pts, [p_.name for p_ in parts], W, Hh)
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white")
    import matplotlib.pyplot as plt
    plt.close(fig)
    return out


def joints(only=None):
    out = []
    c = C()

    def jt(n, parts, title, sub, anchors=None, **kw):
        if only and only != n:
            return
        if anchors:
            out.append(joint_at(parts, anchors, OUT / f"joint-{n:02d}.png", f"Joint {n}: {title}", subtitle=sub, **kw))
        else:
            out.append(bv.joint(parts, OUT / f"joint-{n:02d}.png", f"Joint {n}: {title}", subtitle=sub, **kw))
    from model import _pod_pt
    pp = lambda q: _pod_pt(P, -1, q)  # noqa: E731
    (aqx, aqy), (aux, auy), aL = arm_frame(P, -1)
    at = lambda t, z, off=0.0: (aqx + aux * t - auy * off, aqy + auy * t + aux * off, z)  # noqa: E731
    w = lambda k, *bx: win(S(*k) if isinstance(k, tuple) else S(k), *bx)  # noqa: E731
    bx = (L2 - 60, L2 + 75, SY, SY + 80, ZL - 80, ZL + 80)          # the half beyond the standoff's centre line
    jt(1, [part("Gable wall", win(H()["walls"], *bx), "#E7E5E4"), part("Wall plate", w("wall_plates", *bx), COL["plate"]),
           part("Slip-on flange", w("flanges", *bx), COL["flange"]), part("Standoff pipe in the flange hub", w("standoffs", *bx), COL["standoff"]),
           part("M10 wall anchor heads", w("wall_anchors", *bx), COL["bolt"])],
       "wall plate, flange and standoff (lower, cut open)",
       "Cut through the standoff's centre line. Plate on the wall, flange bolted to it, pipe in the hub to its stop",
       anchors={"Gable wall": (L2 - 30, SY + 40, ZL + 75), "Wall plate": (L2 + 8, SY + 2, ZL + 66),
                "Slip-on flange": (L2 + 40, SY + 1, ZL + 24), "Standoff pipe in the flange hub": (L2 + 70, SY, ZL - 15),
                "M10 wall anchor heads": (L2 + 15, SY + 50, ZL + 58)},
       elev=15, azim=-70, size=(8, 6))
    bx = (MX - 70, MX + 70, -45, 75, ZL - 65, ZL + 65)
    jt(2, [part("Mast", w("mast", *bx), COL["mast"]), part("Crossover plate", w("xplates", *bx), COL["xplate"]),
           part("Standoff pipe", w("standoffs", *bx), COL["standoff"]), part("U-bolts and nyloc nuts", w("ubolts", *bx), COL["bolt"])],
       "crossover plate between the mast and a standoff",
       "Seen from the standoff side. The mast touches one face, the standoff the other; two U-bolts round each",
       anchors={"Mast": (MX, 15, ZL + 64), "Crossover plate": (MX - 45, 26, ZL + 45),
                "Standoff pipe": (MX - 65, SY + 12, ZL + 12), "U-bolts and nyloc nuts": (MX + 35, SY + 20, ZL + 12)},
       elev=22, azim=55, size=(8, 6))
    bx = (MX - 200, MX + 200, -320, 40, 3440, 3720)
    jt(3, [part("Mast", w("mast", *bx), COL["mast"]), part("Clamp, arm and tilt rail", w("panel_mount", *bx), COL["pmount"]),
           part("Solar panel (faces south and up)", w("panel", *bx), COL["panel"])],
       "solar panel mount on the mast",
       "Seen from the east. Clamp on the mast, arm out to the hinge, rail on the panel back at 45 degrees",
       elev=8, azim=-5, size=(8, 6))
    bx = (PODF[0] - 110, PODF[0] - 10, PODF[1] - 60, PODF[1] + 60, PODF[2] - 50, PODF[2] + 45)
    jt(4, [part("Pod box and lid (cut open)", w(("pod_body_f", "pod_lid_f"), *bx), COL["pod"]),
           part("Thermal sensor, can in the window", w("sensor_f", *bx), COL["sensor"]),
           part("Lens hood", w(("lens_hood_f", "lens_hood_screws_f"), *bx), COL["lhood"])],
       "thermal sensor and lens hood on the pod's west wall",
       "Cut through the middle of the pod, seen from the house side. Board inside on 1 mm washers; hood outside",
       anchors={"Pod box and lid (cut open)": pp((-20, 0, -33)), "Thermal sensor, can in the window": pp((-44.4, 0, 11)),
                "Lens hood": pp((-68, 0, 10))},
       cut="+Y", elev=12, azim=-95, size=(8, 6))
    bx = (PODF[0] - 90, PODF[0] + 90, PODF[1] - 80, PODF[1] + 80, P["pod_plate_z"] - 30, PODF[2] - 15)
    jt(5, [part("Pod box", w("pod_body_f", *bx), COL["pod"]), part("Spacers and M6 bolts", w("pod_spacers_f", *bx), COL["bolt"]),
           part("Pod plate", w("pod_plate_f", *bx), COL["pplate"]), part("Arm (top tab and rise)", w("arm_f", *bx), COL["arm"]),
           part("Pivot and slot bolts", w("pod_fix_f", *bx), "#374151")],
       "pod on its plate and the arm's top tab",
       "Two spacers of different height tip the pod 5 degrees nose down; the plate turns on the pivot to aim it",
       anchors={"Pod box": pp((-40, 0, -25)), "Spacers and M6 bolts": (pp((30, 0, -35))[0], pp((30, 0, -35))[1], P["pod_plate_z"] + 8),
                "Pod plate": (PODF[0] - 55, PODF[1] - 10, P["pod_plate_z"] - 3), "Arm (top tab and rise)": at(aL - 28, P["pod_plate_z"] - 25, -20),
                "Pivot and slot bolts": at(aL + 35, P["pod_plate_z"] - 15)},
       elev=-10, azim=-75, size=(8, 6))
    vx = D["verge_x"]
    bx = (vx - 120, vx + 110, -P["cleat_y"] - 110, -P["cleat_y"] + 110, 2560, 2760)
    jt(6, [part("Roof overhang end (verge)", win(H()["roof"], *bx), COL["roof"]),
           part("Fascia and gutter end", win(H()["fascia_gutters"], *bx), COL["gutter"]),
           part("Verge cleat", w("cleat_f", *bx), COL["cleat"]), part("Pod arm (run)", w("arm_f", *bx), COL["arm"]),
           part("Coach screws and M6 bolts", w("pod_fix_f", *bx), COL["bolt"])],
       "verge cleat and pod arm at the front gutter corner",
       "Seen from the east. Cleat screwed to the verge; the arm's run bolted flat on the cleat's level leg",
       anchors={"Roof overhang end (verge)": (vx, -P["cleat_y"] + 90, 2700), "Fascia and gutter end": (vx, -4520, 2480),
                "Verge cleat": (vx + 6, -P["cleat_y"] + 55, 2640), "Pod arm (run)": at(80, P["cleat_top"] + 6),
                "Coach screws and M6 bolts": (vx + 12, -P["cleat_y"] - 40, 2655)},
       elev=22, azim=-25, size=(8, 6))
    jt(7, [part("Enclosure body (door off)", S("box_body"), COL["box"]), part("Gear plate", S("gear_plate"), COL["gear"]),
           part("Controller board", S("board"), COL["board"]), part("Pump-start relay", S("relay"), COL["relay"]),
           part("Battery", S("battery"), COL["battery"]), part("Battery strap", S("strap"), COL["strap"]),
           part("Cable glands", S("box_glands"), COL["glands"])],
       "inside the ground enclosure",
       "Door off, seen from the front. Battery on the floor, strapped to the gear plate; boards on standoffs above",
       elev=12, azim=-15, size=(8, 6))
    bx = (L2 - 20, L2 + 180, BC[1] - 200, BC[1] + 200, 880, 1010)
    jt(8, [part("Gable wall", win(H()["walls"], *bx), "#E7E5E4"), part("Enclosure bottom", w("box_body", *bx), COL["box"]),
           part("Wall lugs and screws", w(("box_lugs", "box_screws"), *bx), COL["lugs"]),
           part("Cable glands (4)", w("box_glands", *bx), COL["glands"]),
           part("Cables into the glands", w(("mast_cable", "pod_cables", "valve_cable"), *bx), COL["cable"])],
       "enclosure bottom, lugs and glands, seen from below",
       "Four glands near the door side; the lugs hold the box 2 mm off the wall",
       anchors={"Gable wall": (L2 - 10, BC[1] - 190, 960), "Enclosure bottom": (BC[0] + 50, BC[1] - 10, 950),
                "Wall lugs and screws": (L2 + 2, BC[1] - 140, 930), "Cable glands (4)": (L2 + 2 + 135, BC[1] + 100, 934),
                "Cables into the glands": (L2 + 60, BC[1] - 100, 880)},
       elev=-35, azim=-40, size=(8, 6))
    bx = (L2 - 10, L2 + 170, -2380, -1140, 370, 660)
    jt(9, [part("Valve board", w("valve_board", *bx), COL["vboard"]), part("Stand-off pipe clips", w("pipe_clips", *bx), COL["clips"]),
           part("Manifold and tees", w("manifold", *bx), COL["manifold"]), part("Zone valves A and B", w("valves", *bx), COL["valves"]),
           part("Pressure transducer", w("xducer", *bx), COL["xducer"]), part("Risers from the valves", w("lines", *bx), COL["lines"])],
       "valve board, manifold and valves",
       "The manifold sits in two clips 45 mm off the board; the valves hang from its tees, coils facing out",
       elev=15, azim=-35, size=(8, 6))
    ly = D["line_y"]
    bx = (5900, 6000, -ly - 40, -(D["eave_y"] + P["fascia_t"]) + 1, D["gut_z0"] - 5, D["line_z"] + 20)
    jt(10, [part("Gutter (context)", win(H()["fascia_gutters"], *bx), COL["gutter"]),
            part("Gutter-lip clip", w("lip_clips", *bx), COL["lipclip"]), part("Spray line", w("lines", *bx), COL["lines"])],
       "spray line on a gutter-lip clip",
       "Seen along the gutter (section). The clip hooks over the lip and holds the line 20 mm in front of it, 30 mm above",
       anchors={"Gutter (context)": (5900, -4560, D["gut_z0"] + 4), "Gutter-lip clip": (5950 + 6, -(D["lip_y"] + 4.5), D["lip_z"] + 15),
                "Spray line": (5900, -ly, D["line_z"] + 8)},
       elev=10, azim=-10, size=(8, 6))
    bx = (L2 - 60, L2 + 90, -ly - 30, -3900, 2240, 2560)
    jt(11, [part("House wall corner", win(H()["walls"], *bx), "#E7E5E4"), part("Roof overhang", win(H()["roof"], *bx), COL["roof"]),
            part("Fascia and gutter", win(H()["fascia_gutters"], *bx), COL["gutter"]),
            part("Riser and eave line", w("lines", *bx), COL["lines"]),
            part("Stand-off clip under the fascia", w("fascia_clips", *bx), COL["clips"])],
       "riser round the eave corner (front zone)",
       "Up the gable wall, out under the gutter, up in front of it and along the lip", elev=-8, azim=-50, size=(8, 6))
    bx = (MX - 140, MX + 60, -90, 90, 2180, 2470)
    jt(12, [part("Mast foot", w("mast", *bx), COL["mast"]), part("End cap with grommet", w("mast_cap", *bx), COL["bolt"]),
            part("Mast cable", w("mast_cable", *bx), "#4B5563"), part("Earth clamp and conductor", w("earth", *bx), COL["earth"]),
            part("Lower standoff and crossover plate", w(("standoffs", "xplates", "ubolts"), *bx), COL["xplate"])],
       "mast foot: cable out, earth bond on",
       "The cable leaves through the end cap and runs under the lower standoff; the earth clamp is 25 mm up",
       elev=10, azim=-60, size=(8, 6))
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    out = []

    def st(n, done, new, title, sub, **kw):
        if only and only != n:
            return
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))
    w = lambda ks, *bx: win(S(*ks), *bx)  # noqa: E731
    lo = (L2 - 1, L2 + 120, SY - 90, SY + 90, ZL - 90, ZL + 90)
    if not only or only == 1:
        st(1, [part("Wall plate", w(("wall_plates",), *lo), COL["plate"])],
           [part("Slip-on flange", w(("flanges",), *lo), COL["flange"], (120, 0, 0))],
           "flange onto each wall plate", "Four M8 countersunk screws from the back of the plate, nyloc nuts on the flange. Make two",
           elev=20, azim=-60, label_done=True)
    if not only or only == 2:
        from build123d import Pos
        z0, z1 = P["mast_z0"], P["mast_z1"]
        up = Pos(0, 0, (z1 - 400) - (z0 + 400) - 150)          # the foot drawn just below the top: mast shown shortened
        mast_short = win(S("mast"), MX - 50, MX + 50, -50, 50, z1 - 400, z1 + 1) + up * win(S("mast"), MX - 50, MX + 50, -50, 50, z0 - 1, z0 + 400)
        st(2, [part("Mast tube (shown shortened)", mast_short, COL["mast"])],
           [part("End cap with grommet (mast cable through first)", up * S("mast_cap"), COL["bolt"], (0, 0, -120)),
            part("Anemometer and vane on the mast-top sleeve", S("anem"), COL["anem"], (0, 0, 200))],
           "end cap and wind sensors on the mast", "Pull the mast cable through first. Sleeve 40 mm over the top, two set screws. Mast drawn shortened",
           elev=12, azim=-55)
    if not only or only == 3:
        st(3, [part("Mast (upper part shown)", win(S("mast", "anem"), MX - 400, MX + 400, -400, 400, 3150, 5300), COL["mast"])],
           [part("Humidity shield, arm and clamp", S("trh"), COL["trh"], (350, 0, 0)),
            part("Panel clamp, arm and tilt rail with the panel", S("panel", "panel_mount"), COL["panel"], (0, -450, 0))],
           "humidity shield and solar panel onto the mast", "Clamps at 3.43 m and 3.56 m from the ground (1.18 and 1.31 m up the mast); leads in through the grommets",
           elev=12, azim=-50)
    pod_box = [part("Pod box", S("pod_body_f"), COL["pod"])]
    if not only or only == 4:
        st(4, pod_box, [part("Thermal sensor (from inside)", S("sensor_f"), COL["sensor"], (0, 0, 110)),
                        part("Node board on standoffs", S("node_f"), COL["node"], (0, 0, 110)),
                        part("Lens hood (from outside)", S("lens_hood_f", "lens_hood_screws_f"), COL["lhood"], (-110, 0, 0))],
           "sensor, node board and lens hood into the pod", "Seen from the west (lens) end. Sensor board on four M2.5 screws and 1 mm washers, can in the window; hood on two M3 screws",
           elev=22, azim=-140)
    pod_in = pod_box + [part("Sensor, node board, lens hood", S("sensor_f", "node_f", "lens_hood_f"), COL["pod"])]
    if not only or only == 5:
        st(5, pod_in, [part("M16 cable gland", S("cgland_f"), COL["glands"], (90, 0, 0)), part("Lid", S("pod_lid_f"), COL["lid"], (0, 0, 80)),
                       part("Hood spacers (4)", S("hood_spacers_f"), COL["bolt"], (0, 0, 140)), part("Hood", S("hood_f"), COL["hood"], (0, 0, 210))],
           "cable gland, lid and hood on the pod", "Pod cable in through the gland; lid screws even; spacers into the lid, hood on four M4 screws",
           elev=20, azim=-55)
    pod_all = [part("Pod", S("pod_body_f", "pod_lid_f", "sensor_f", "node_f", "lens_hood_f", "hood_f", "hood_spacers_f", "cgland_f"), COL["pod"])]
    if not only or only == 6:
        st(6, pod_all, [part("Spacers and M6 bolts", S("pod_spacers_f"), COL["bolt"], (0, 0, -70)),
                        part("Pod plate", S("pod_plate_f"), COL["pplate"], (0, 0, -130))],
           "pod plate under the pod", "Short spacer under the lens end, tall one under the back end; bolts from inside the pod into the plate",
           elev=10, azim=-70)
    if not only or only == 7:
        st(7, [part("Verge cleat", S("cleat_f"), COL["cleat"])],
           [part("Pod arm", S("arm_f"), COL["arm"], (0, 0, 120))],
           "arm onto the cleat", "Run flat on the cleat's level leg; two M6 bolts with nyloc nuts. Make a front and a back pair",
           elev=25, azim=-40, label_done=True)
    box_ = [part("Enclosure body", S("box_body"), COL["box"])]
    if not only or only == 8:
        st(8, box_, [part("Wall lugs (4)", S("box_lugs"), COL["lugs"], (-120, 0, 0)),
                     part("M20 cable glands (4)", S("box_glands"), COL["glands"], (0, 0, -120)),
                     part("Siren and status light", S("siren"), COL["siren"], (0, 0, 120)),
                     part("Door with key switch", S("box_door", "key"), "#93C5FD", (220, 0, 0))],
           "lugs, glands, siren and key switch on the enclosure", "Lugs on the back corners; glands from below; siren on its gasket; key switch through the door",
           elev=18, azim=-40)
    box2 = [part("Enclosure with glands and lugs", S("box_body", "box_glands", "box_lugs", "siren"), COL["box"])]
    if not only or only == 9:
        st(9, box2, [part("Gear plate with controller and relay", S("gear_plate", "board", "relay"), COL["board"], (250, 0, 0)),
                     part("Battery (not connected)", S("battery"), COL["battery"], (420, 0, 0)),
                     part("Battery strap", S("strap"), COL["strap"], (560, 0, 0))],
           "gear plate, controller, relay and battery into the enclosure", "Gear plate on its four studs; battery on the floor against it, strap with two M4 screws",
           elev=15, azim=-35)
    if not only or only == 10:
        st(10, [part("Valve board", S("valve_board"), COL["vboard"])],
           [part("Stand-off pipe clips", S("pipe_clips"), COL["clips"], (60, 0, 0)),
            part("Manifold and tees", S("manifold"), COL["manifold"], (140, 0, 0)),
            part("Zone valves A and B", S("valves"), COL["valves"], (220, 0, -60)),
            part("Pressure transducer", S("xducer"), COL["xducer"], (140, 0, 120))],
           "clips, manifold, valves and transducer on the valve board", "Thread sealant on every joint; valve arrows pointing down (water flows down)",
           elev=15, azim=-35)
    gx = (L2 - 400, L2 + 900, -500, 600, 1900, 5150)
    house_m = ctx_house(*gx, names=("walls", "roof"))
    if not only or only == 11:
        st(11, [], [part("Wall plates with flanges and anchors", S("wall_plates", "flanges", "wall_anchors"), COL["plate"], (450, 0, 0)),
                    part("Standoff pipes", S("standoffs"), COL["standoff"], (900, 0, 0))],
           "wall plates and standoffs on the gable wall", "Plates 2.45 m and 3.90 m up, centres 43 mm to the side of the mast line; four M10 anchors each; pipes in to their stops",
           context=ctx_house(L2 - 150, L2 + 900, -350, 450, 2250, 4100, names=("walls",)), elev=12, azim=-40)
    mast_all = S("mast", "mast_cap", "anem", "trh", "panel", "panel_mount")
    if not only or only == 12:
        st(12, [part("Wall plates, flanges, standoffs", S("wall_plates", "flanges", "standoffs", "wall_anchors"), COL["plate"])],
           [part("Mast with its sensors and panel", mast_all, COL["mast"], (0, -500, 0)),
            part("Crossover plates and U-bolts", S("xplates", "ubolts"), COL["xplate"], (0, 250, 0))],
           "mast onto the standoffs", "Mast upright, bottom 2.25 m up; a crossover plate at each standoff, two U-bolts round each pipe",
           context=house_m, elev=15, azim=-50)
    if not only or only == 13:
        ge = (L2 - 300, L2 + 900, -600, 400, -1200, 2700)
        st(13, [part("Mast foot and lower standoff", win(mast_all + S("standoffs", "xplates", "ubolts", "wall_plates", "flanges"), L2 - 10, MX + 100, -300, 300, 2150, 2700), COL["mast"])],
           [part("Earth rod, conductor and clamp", S("earth"), COL["earth"], (0, -300, 0))],
           "earth the mast", "Rod driven 1.2 m into the ground 400 mm from the wall; 16 mm2 conductor; clamp on the mast foot",
           context=ctx_house(*ge, names=("walls",)), elev=12, azim=-55)
    cx = (6200, 6500, -4760, -4250, 2330, 2800)
    if not only or only == 14:
        st(14, [], [part("Verge cleat with its arm", S("cleat_f", "arm_f", "pod_fix_f"), COL["cleat"], (200, 0, 0)),
                    part("Pod with its plate", S(*[k for k in C() if k.endswith("_f") and k not in ("cleat_f", "arm_f", "pod_fix_f")]), COL["pod"], (0, 0, 220))],
           "cleat, arm and pod at each gutter corner (front shown)", "Two 8 mm coach screws into the verge; pod plate on the pivot bolt; aim 10 degrees in, then lock the slot bolt",
           context=ctx_house(*cx), elev=18, azim=-35)
    ux_ = (L2 - 200, L2 + 600, -2600, -1000, 0, 1600)
    if not only or only == 15:
        st(15, [], [part("Ground enclosure", S("box_body", "box_door", "box_lugs", "box_glands", "siren", "key", "gear_plate", "board", "relay", "battery", "strap"), COL["box"], (400, 0, 0)),
                    part("Valve board assembly", S("valve_board", "pipe_clips", "manifold", "valves", "xducer"), COL["valves"], (400, 0, 0)),
                    part("Lug screws into wall plugs", S("box_screws"), COL["bolt"], (150, 0, 0))],
           "enclosure and valve board on the gable wall", "Enclosure centre 1.15 m up; valve board below it; screws into wall plugs; level both",
           context=ctx_house(*ux_, names=("walls",)), elev=15, azim=-45)
    fz = (4500, L2 + 400, -4800, -1300, 0, 2700)
    if not only or only == 16:
        st(16, [part("Valve board assembly", S("valve_board", "manifold", "valves", "xducer", "pipe_clips"), COL["valves"])],
           [part("Front riser and eave line", win(S("lines"), 4500, L2 + 200, -4800, -1300, 0, 2700), COL["lines"], (0, -250, 0)),
            part("Wall clips and fascia clip", win(S("wall_clips", "fascia_clips"), 4500, L2 + 200, -4800, -1300, 0, 2700), COL["clips"], (0, -250, 0)),
            part("Lip clips and heads", win(S("lip_clips", "heads"), 4500, L2 + 200, -4800, -1300, 0, 2700), COL["heads"], (0, -250, 0))],
           "spray lines (front zone shown)", "Riser along the wall base and up the corner, out under the gutter, along the lip on clips; heads on tees",
           context=ctx_house(*fz), elev=18, azim=-40)
    if not only or only == 17:
        z = (L2 - 150, L2 + 800, -2300, 450, 300, 2700)
        st(17, [part("Mast, pods, enclosure, valves and lines", win(S("mast", "standoffs", "xplates", "wall_plates", "flanges", "box_body", "box_door",
                                                                       "valve_board", "valves", "manifold", "pod_body_f", "pod_body_b",
                                                                       "arm_f", "arm_b", "cleat_f", "cleat_b", "lines"), *z), COL["mast"])],
           [part("Mast cable", win(S("mast_cable"), *z), COL["cable"], (150, 0, 0)),
            part("Pod cables (2)", win(S("pod_cables"), *z), "#4B5563", (150, 0, 0)),
            part("Valve cable", win(S("valve_cable"), *z), "#374151", (150, 0, 0))],
           "cables into the enclosure", "Mast cable from the mast foot; pod cables arrive along the wall from both corners; each through its own gland, saddle clips every 500 mm",
           context=ctx_house(*z, names=("walls",)), elev=15, azim=-35)
    ux18 = (L2 - 200, L2 + 700, -2500, -1100, 800, 1700)
    if not only or only == 18:
        st(18, [part("Enclosure on the gable wall", S("box_body", "box_door", "box_lugs", "siren", "key"), COL["box"])],
           [part("Sun shade on its two arms", S("shade", "shade_arms"), COL["shade"], (0, 0, 220)),
            part("Wall screws (2)", S("shade_screws"), COL["bolt"], (150, 0, 0))],
           "sun shade over the enclosure", "Arms 120 mm either side of the enclosure's centre line; plate top 1.48 m up and level; clear of the siren and the door's swing",
           context=ctx_house(*ux18, names=("walls",)), elev=18, azim=-45)
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.4), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 74); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 72, "EmberGuard prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 68.6, "Bought modules wired at block level on the controller's protoboard; no circuit board is laid out. "
                     "Stranded copper; ferrules on every screw terminal.", fontsize=8.5, color=MUT, va="top")
    ax.text(2, 0.8, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 0.8, "github.com/BoujeeEnjinia1701/emberguard", fontsize=7, color="#0F766E", ha="right", family="monospace")
    ax.add_patch(FancyBboxPatch((28, 12), 62, 50, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(29.5, 61, "Inside the ground enclosure (gear plate)", fontsize=8, color=MUT, va="top")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.3, title, ha="center", va="top", fontsize=8.8, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.1, sub, ha="center", va="top", fontsize=7, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY = "#B91C1C", "#1D4ED8", "#6B7280"
    blk(3, 47, 17, 11, "Solar panel", "10 W, 12 V, on the mast;\nlead in the mast cable", "#1E3A8A")
    blk(3, 31, 17, 12, "Mast sensors", "anemometer (pulse),\nvane (resistor ladder),\nhumidity probe (I2C)", "#1F2937")
    blk(3, 13, 17, 12, "Two sensor pods", "thermal sensor and pod\nnode each; RS-485 and\n12 V on 4 pairs", "#0F766E")
    blk(31, 46, 17, 12, "Charge controller", "PWM, LiFePO4 profile;\nprobe on the battery\nstops charge above 45 C", "#16A34A")
    blk(31, 28, 17, 12, "Battery", "12.8 V 10 Ah LiFePO4,\nbuilt-in BMS; 10 A fuse\nat the terminal", "#7C3AED")
    blk(54, 32, 18, 26, "Controller board", "ESP32 module, 12 to\n3.3 V buck, input fuse,\nRS-485 transceiver,\ntwo MOSFET valve\ndrivers, siren driver,\nterminals", "#16A34A")
    blk(54, 14, 18, 11, "Pump-start relay", "isolated, dry contact\nonly", "#DB2777")
    blk(76, 48, 12, 10, "Siren, light,\nkey switch", "0.5 mm² leads", "#DC2626")
    blk(96, 44, 21, 14, "Zone valves A and B", "12 V normally closed,\nabout 6 W coils;\nflyback diode each", "#D4A017")
    blk(96, 24, 21, 13, "Pressure transducer", "0.5 to 4.5 V out,\n5 V supply", "#0EA5E9")
    blk(96, 5, 21, 11, "Pump (homeowner)", "its own supply and\ncertified controls", "#9CA3AF")
    wire([(20, 52), (31, 52)], RED); lab(25.5, 54, "1.0 mm²", RED, "center")
    wire([(39.5, 46), (39.5, 40)], RED); lab(40.2, 44, "1.5 mm²", RED)
    wire([(48, 38), (54, 38)], RED); lab(51, 36.3, "1.5\nmm²", RED, "center")
    wire([(20, 37), (25, 37), (25, 45.5), (54, 45.5)], BLU); lab(31.5, 43.9, "signals, 0.25 mm²", BLU, "center")
    wire([(20, 19), (51, 19), (51, 34), (54, 34)], BLU); lab(22, 22, "RS-485 pair and 12 V, 0.5 mm², 5 A fuse", BLU)
    wire([(72, 53), (76, 53)], GRY, 1.4)
    wire([(72, 45.5), (96, 45.5)], RED); lab(84, 43.6, "valve cable, 1.0 mm²", RED, "center")
    wire([(72, 36), (90, 36), (90, 30), (96, 30)], BLU); lab(81, 37.8, "0.25 mm², shielded", BLU, "center")
    wire([(63, 32), (63, 25)], GRY, 1.4); lab(63.6, 28.5, "coil, 0.5 mm²", GRY)
    wire([(72, 19), (84, 19), (84, 10.5), (96, 10.5)], GRY, 1.4); lab(84.6, 15, "dry contact only", GRY)
    ax.text(2, 9.6, "Safety: battery fuse out and the battery disconnected until the safety stops in section 6 of the plan are passed.",
            fontsize=7.4, color="#B45309", fontweight="bold")
    ax.text(2, 6.6, "12 V DC only; no mains wiring in EmberGuard. The relay contact signals the pump's own controls and never carries pump power.",
            fontsize=7.1, color=MUT)
    ax.text(2, 3.9, "Red: power. Blue: signal and RS-485. Grey: control.", fontsize=7.1, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    args = sys.argv[1:] or ["overview", "sheets", "joints", "steps", "wiring"]
    for a in args:
        if a.startswith("step-"):
            print(steps(int(a[5:])))
        elif a.startswith("joint-"):
            print(joints(int(a[6:])))
        elif a.startswith("EGD-DWG-"):
            print(sheets(a))
        else:
            print(a, "->", {"overview": overview, "sheets": sheets, "joints": joints, "steps": steps, "wiring": wiring}[a]())
