#!/usr/bin/env python3
"""Jigsaw built from a photo/illustration: 3x2 pieces of assets/uterus-pieces.jpg, each labelled with a consequence."""
import sys, pathlib
W, H = 600, 400
X = [0, 200, 400, 600]; Y = [0, 200, 400]; R = 30
IMG = "assets/uterus-pieces.jpg"
PIECES = [  # id, col, row, label, dx, dy, rot
    ("p1", 0, 0, "Chronic pain & fatigue",     -250, -150, -16),
    ("p2", 1, 0, "Depression & anxiety",          0, -230,   7),
    ("p3", 2, 0, "Autoimmune conditions",       250, -140,  15),
    ("p4", 0, 1, "Bowel problems",             -260,  150, -11),
    ("p5", 1, 1, "Infertility",                   0,  240,  -6),
    ("p6", 2, 1, "Silent kidney damage",        260,  150,  13),
]
TABS = {  # (owner, neighbour, centre)
    "a": ("p1", "p2", (200, 100)), "b": ("p3", "p2", (400, 100)),
    "c": ("p5", "p4", (200, 300)), "d": ("p5", "p6", (400, 300)),
    "e": ("p4", "p1", (100, 200)), "f": ("p2", "p5", (300, 200)), "g": ("p6", "p3", (500, 200)),
}
SUB = {"p3": "e.g. Hashimoto’s thyroiditis", "p6": "from ureteral endometriosis", "p4": "often labelled IBS"}
def rect(c, r): return X[c], Y[r], X[c+1]-X[c], Y[r+1]-Y[r]
def mask(pid, c, r):
    x, y, w, h = rect(c, r)
    parts = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="black"/>', f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="white"/>']
    for o, n, (cx, cy) in TABS.values():
        if o == pid: parts.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="white"/>')
        elif n == pid: parts.append(f'<circle cx="{cx}" cy="{cy}" r="{R+1.5}" fill="black"/>')
    return f'<mask id="mi-{pid}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">{"".join(parts)}</mask>'
def seams(pid, c, r):
    x, y, w, h = rect(c, r)
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}"/>']
    for o, n, (cx, cy) in TABS.values():
        if o == pid or n == pid: out.append(f'<circle cx="{cx}" cy="{cy}" r="{R}"/>')
    return "".join(out)
o = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H+70}" class="pz-svg" role="img" aria-labelledby="pzi-t pzi-d">',
     '<title id="pzi-t">Consequences of unrecognised endometriosis</title>',
     '<desc id="pzi-d">A medical illustration of the uterus cut into six jigsaw pieces, each labelled with a consequence of late diagnosis: chronic pain and fatigue, depression and anxiety, autoimmune conditions, bowel problems, infertility, silent kidney damage.</desc>',
     '<defs>',
     '<filter id="pzi-shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#0B1A33" flood-opacity=".28"/></filter>']
for pid, c, r, *_ in PIECES: o.append(mask(pid, c, r))
o.append('</defs>')
o.append(f'<rect class="pzi-ghost" x="0" y="0" width="{W}" height="{H}" rx="10"/>')
for pid, c, r, label, dx, dy, rot in PIECES:
    x, y, w, h = rect(c, r); lx, ly = x + w/2, y + h/2
    o.append(f'<g class="pz pz-{pid}" style="--dx:{dx}px;--dy:{dy}px;--rot:{rot}deg" filter="url(#pzi-shadow)">')
    o.append(f'  <g mask="url(#mi-{pid})"><image href="{IMG}" x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice"/>'
             f'<rect x="0" y="0" width="{W}" height="{H}" class="pzi-tint"/><g class="pz-seam">{seams(pid, c, r)}</g></g>')
    sub = SUB.get(pid)
    lw = max(120, int(len(label) * 7.2) + 26); lh = 46 if sub else 30
    o.append(f'  <g class="pzi-label"><rect x="{lx-lw/2:.0f}" y="{ly-lh/2:.0f}" width="{lw}" height="{lh}" rx="8"/>'
             f'<text x="{lx:.0f}" y="{ly+(-3 if sub else 5):.0f}" text-anchor="middle">{label}</text>'
             + (f'<text class="sub" x="{lx:.0f}" y="{ly+14:.0f}" text-anchor="middle">{sub}</text>' if sub else '') + '</g>')
    o.append('</g>')
o.append(f'<g class="pz-final"><rect x="120" y="{H+22}" width="360" height="34" rx="17"/><text x="300" y="{H+45}" text-anchor="middle">Left unrecognised, it does not stay in the pelvis.</text></g>')
o.append('</svg>')
pathlib.Path(sys.argv[1]).write_text("\n".join(o), encoding="utf-8"); print("ok")
