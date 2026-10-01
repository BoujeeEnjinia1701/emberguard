"""EmberGuard general arrangement sheet EGD-DWG-001, Rev P4 (TRL 3, constructable design).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/EGD-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Dimensions are taken from PARAMS and derived(), so
they follow any parameter change. The concept sheet in media/ is EGD-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, assembly, build_parts, derived, house_parts, MAST_KEYS, GROUND_KEYS  # noqa: E402

DATE = "2026-09-25"
DATE_P4 = "2026-10-01"


def safe_project_views(part, workdir, line_weight=0.35, names=("front", "top", "right", "iso")):
    """Same views as drawing.project_views, edge by edge, so a degenerate edge is skipped."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out, skipped = {}, 0
    for name in names:
        origin, up = setups[name]
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    skipped += 1
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    if skipped:
        print(f"projected views; skipped {skipped} degenerate edges")
    return out


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    ax += (aw - (k * (max(fw, tw) + rw) + gap)) / 2
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab)) / 2
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text, side=-1):
    a = 1.4
    cx, cy = x + side * 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def leader(x1, y1, x2, y2, text, anchor="start"):
    return [f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.15"/>',
            f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="{INK}"/>',
            _t(x2 + (1 if anchor == "start" else -1), y2 + 0.8, text, 2.1, 400, INK, anchor)]


def main():
    from build123d import Compound
    D = derived(P)
    work = ROOT / "cad" / "drawings" / "_views"
    from build123d import Box, Pos
    above = Pos(0, 0, 10000) * Box(40000, 40000, 20000)       # the earth rod below ground is left off the views
    asm = Compound(children=[v[1] & above if k == "earth" else v[1] for k, v in build_parts().items()]
                   + list(house_parts().values()))
    views = safe_project_views(asm, work / "ga")
    bb = asm.bounding_box()
    s = Sheet(project="EmberGuard", title="General arrangement", dwg_no="EGD-DWG-001", rev="P4",
              author="Amish Chadha", date=DATE_P4, scale=None, theme="technical",
              material="House, roof, fascia and gutters are the reference house (context only); kit parts per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
                         ("P2", "Sensor pods at gutter corners, 10 Ah battery (EGD-DDR-002)", DATE, "AC"),
                         ("P3", "Layout and labels tidied", "2026-09-30", "AC"),
                         ("P4", "Design for construction (EGD-DDR-003)", DATE_P4, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    L = []
    mx = D["mast_x"]

    # front view (from -Y): X to the right, Z up
    x, y, w, h = c["front"]
    X = lambda mx_: x + (mx_ - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    zt = Z(bb.max.Z) - 5
    L += [ext(X(-D["roof_len"] / 2), Z(D["lip_z"]), X(-D["roof_len"] / 2), zt - 1),
          ext(X(D["roof_len"] / 2), Z(D["lip_z"]), X(D["roof_len"] / 2), zt - 1)]
    L += dim_h(X(-D["roof_len"] / 2), X(D["roof_len"] / 2), zt, f"{D['roof_len']:,.0f} gutter")
    xr = X(bb.max.X) + 5
    L += [ext(X(mx) + 1, Z(P["arm_z"]), xr + 1, Z(P["arm_z"])), ext(X(D["pod_x"]), Z(D["pod_z"]), xr + 7, Z(D["pod_z"])),
          ext(X(D["roof_len"] / 2), Z(D["lip_z"]), xr + 13, Z(D["lip_z"]))]
    L += dim_v(xr, Z(P["arm_z"]), Z(0), f"{P['arm_z']:,.0f} anemometer", side=3)
    L += dim_v(xr + 6, Z(D["pod_z"]), Z(0), f"{D['pod_z']:,.0f} pod", side=1)
    L += dim_v(xr + 12, Z(D["lip_z"]), Z(0), f"{D['lip_z']:,.0f} lip", side=1)
    L += leader(X(D["pod_x"]), Z(D["pod_z"]), X(D["pod_x"]) - 14, Z(D["pod_z"]) - 14, "2, 3  sensor pod", "end")
    L += leader(X(mx), Z(P["arm_z"]), X(mx) - 14, Z(P["arm_z"]) - 4, "4  wind sensors", "end")
    L += leader(X(-2000), Z(D["line_z"]), X(-2000) - 6, Z(D["line_z"]) - 10, "14  spray line on gutter lip", "end")

    # top view (from +Z): X to the right, Y up the sheet
    x, y, w, h = c["top"]
    Xt = lambda px: x + (px - bb.min.X) * k
    Yt = lambda py: y + h - (py - bb.min.Y) * k
    L += leader(Xt(mx), Yt(0), Xt(mx) - 20, Yt(0) - 3, f"1  mast, {P['mast_off']:.0f} off gable", "end")
    L += leader(Xt(D["box_c"][0]), Yt(D["box_c"][1]), Xt(D["box_c"][0]) - 18, Yt(D["box_c"][1]) + 5, "7, 10  ground unit and valves", "end")
    for sgn in (-1, 1):
        L += leader(Xt(0), Yt(sgn * D["lip_y"]), Xt(-1200), Yt(sgn * D["lip_y"]) + sgn * 17,
                    "zone A (front)" if sgn < 0 else "zone B (back)", "end")

    s._layers += L

    KA = 30
    # detail A: mast assembly seen from the front (-Y), 1:25
    parts = build_parts()
    mast = Compound(children=[parts[kk][1] for kk in MAST_KEYS if kk != "cable"])
    mv = safe_project_views(mast, work / "mast", names=("front",))
    s.add_svg(mv["front"], 276, 37, 70, 106, scale=1 / KA, label="Detail A: mast assembly", sublabel=f"Scale 1:{KA}, from the front")
    mb = mast.bounding_box()
    vx, vy, vw, vh = _viewbox(Path(mv["front"]).read_text())
    dw, dh = vw / KA, vh / KA
    bx0, by0 = 276 + (70 - dw) / 2, 37 + (106 - dh) / 2
    Za = lambda mz: by0 + dh - (mz - mb.min.Z) / KA
    Xa = lambda mx_: bx0 + (mx_ - mb.min.X) / KA
    xd = Xa(mb.min.X) - 3
    A = []
    A += [ext(Xa(mx), Za(P["mast_z1"]), xd - 1, Za(P["mast_z1"])), ext(Xa(mx), Za(P["mast_z0"]), xd - 1, Za(P["mast_z0"]))]
    A += dim_v(xd, Za(P["mast_z1"]), Za(P["mast_z0"]), f"{D['mast_len']:,.0f}")
    A += leader(Xa(mx + 90), Za(P["trh_z"] + 40), Xa(mx + 90) + 10, Za(P["trh_z"] + 40), "5")
    A += leader(Xa(mx), Za(P["arm_z"]), Xa(mx) + 12, Za(P["arm_z"]) - 2, "4")
    A += leader(Xa(mx), Za(P["panel_z"]), Xa(mx) + 12, Za(P["panel_z"]) + 3, "9")
    A += leader(Xa(P["house_l"] / 2 + 300), Za(P["standoff_z"][1]), Xa(P["house_l"] / 2 + 300) - 3, Za(P["standoff_z"][1]) - 6, "1", "end")
    s._layers += A

    # detail B: ground unit and valves seen from the east (+X), 1:25
    gu = Compound(children=[parts[kk][1] for kk in GROUND_KEYS])
    gv = safe_project_views(gu, work / "ground", names=("right",))
    s.add_svg(gv["right"], 352, 60, 66, 70, scale=1 / 25, label="Detail B: ground unit", sublabel="Scale 1:25, from the east")
    gb = gu.bounding_box()
    _, _, gw, gh = _viewbox(Path(gv["right"]).read_text())
    gx0, gy0 = 352 + (66 - gw / 25) / 2, 60 + (70 - gh / 25) / 2
    Yb = lambda py: gx0 + (py - gb.min.Y) / 25          # from the east, +Y is to the right
    Zb = lambda pz: gy0 + gh / 25 - (pz - gb.min.Z) / 25
    bc = D["box_c"]
    B = []
    B += leader(Yb(bc[1] + P["box"][1] / 2), Zb(bc[2]), Yb(bc[1] + P["box"][1] / 2) + 10, Zb(bc[2]) - 4, "7")
    B += leader(Yb(bc[1] - 80), Zb(bc[2] + P["box"][2] / 2 + 40), Yb(bc[1] - 80) - 8, Zb(bc[2] + P["box"][2] / 2 + 40) - 4, "15", "end")
    for vy in P["valve_y"]:
        B += leader(Yb(vy), Zb(P["manifold_z"]), Yb(vy) + 3, Zb(P["manifold_z"]) + 8, "10")
    yc = sum(P["valve_y"]) / 2
    B += leader(Yb(yc), Zb(P["manifold_z"] + 100), Yb(yc) + 6, Zb(P["manifold_z"] + 100) - 8, "11")
    s._layers += B

    bx, by, bh = P["box"]
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Reference house {P['house_l']:,.0f} x {P['house_d']:,.0f}, walls {P['wall_h']:,.0f}, roof {P['pitch']:.0f} deg, eaves {P['overhang']:.0f}",
        f"Mast {P['mast_od']:.0f} x {P['mast_wall']:.0f} Al, {D['mast_len']:,.0f} long, {P['mast_off']:.0f} off the gable; DN25 standoffs, crossover plates",
        f"Pods {P['pod_out']:.0f} past each gutter end, {P['pod_above_lip']:.0f} above the lip, on arms from verge cleats",
        f"Pod aim along the gutter, {P['aim_yaw']:.0f} deg in, {P['aim_down']:.0f} deg down",
        f"Gutter lip at {D['lip_z']:,.0f}; line {P['line_od']:.0f} OD on lip clips, {P['heads_per_eave']} heads at {P['head_pitch']:,.0f}",
        f"Zone lines {D['zone_len'][0] / 1000:.1f} m (A) and {D['zone_len'][1] / 1000:.1f} m (B) incl. risers",
        f"Ground box {bh:.0f} x {by:.0f} x {bx:.0f} steel IP65 at {P['box_z']:,.0f}; valve board, manifold at {P['manifold_z']:.0f}",
        "No roof penetrations; 12 V DC only; mast earthed (item 17)",
        "Hanger straps shadow deep gutter debris beyond 7.8 m (EGD-CAL-001 v0.2, A4)",
    ], x=276, y=158, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "EGD-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
