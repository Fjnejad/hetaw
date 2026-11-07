#!/usr/bin/env python3
"""Generate the puzzle SVG (six jigsaw pieces forming a stylised uterus) with per-piece masks and symptom labels."""
import sys, pathlib

W, H = 600, 585
# cell grid: cols x 0-200-400-600, rows y 80-310-540
X = [0, 200, 400, 600]
Y = [80, 310, 540]
R = 27  # tab radius

# stylised uterus silhouette (symbolic, not anatomical): body, two tubes, two ovaries, cervix
UTERUS = (
    " M300,150 C230,150 180,185 180,250 C180,330 250,400 300,470 C350,400 420,330 420,250 C420,185 370,150 300,150 Z"  # body
    " M200,190 C150,165 110,195 92,240 C84,262 86,286 96,304 L118,296 C110,282 110,262 118,248 C130,222 160,206 208,218 Z"  # left tube
    " M400,190 C450,165 490,195 508,240 C516,262 514,286 504,304 L482,296 C490,282 490,262 482,248 C470,222 440,206 392,218 Z"  # right tube
    " M71,318 a34,44 0 1,0 68,0 a34,44 0 1,0 -68,0 Z"  # left ovary
    " M461,318 a34,44 0 1,0 68,0 a34,44 0 1,0 -68,0 Z"  # right ovary
    " M268,440 L332,440 L324,500 C318,520 282,520 276,500 Z"  # cervix
)

# pieces: (id, col, row, label, start dx, dy, rot)
PIECES = [
    ("p1", 0, 0, "Irritable bowel",        -260, -140, -18, "#C4574D"),
    ("p2", 1, 0, "\u201cNormal\u201d period pain", 0, -220,   8, "#B3463D"),
    ("p3", 2, 0, "Cystitis / UTI",          260, -150,  16, "#CF665B"),
    ("p4", 0, 1, "Pelvic inflammatory disease", -270, 150, -12, "#A93F37"),
    ("p5", 1, 1, "Stress / psychosomatic",    0,  230,  -6, "#BE5047"),
    ("p6", 2, 1, "Appendicitis",            260,  160,  14, "#D4756A"),
]
# tabs: (edge, owner) — vertical edges at x=200/400 per row, horizontal edges at y=310 per col
# owner gets a white circle (tab), neighbour gets black (notch)
TABS = {
    # vertical edge between (col0,row0) and (col1,row0) at (200,195): owner p1
    ("v", 0, 0): ("p1", "p2", (200, 195)),
    ("v", 1, 0): ("p3", "p2", (400, 195)),
    ("v", 0, 1): ("p5", "p4", (200, 425)),
    ("v", 1, 1): ("p5", "p6", (400, 425)),
    # horizontal edges at y=310: col0 owner p4, col1 owner p2, col2 owner p6
    ("h", 0, 0): ("p4", "p1", (100, 310)),
    ("h", 1, 0): ("p2", "p5", (300, 310)),
    ("h", 2, 0): ("p6", "p3", (500, 310)),
}

def cell_rect(c, r):
    return X[c], Y[r], X[c+1]-X[c], Y[r+1]-Y[r]

def mask(pid, c, r):
    x, y, w, h = cell_rect(c, r)
    parts = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="black"/>',
             f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="white"/>']
    for key, (owner, nb, (cx, cy)) in TABS.items():
        if owner == pid:
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="white"/>')
        elif nb == pid:
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="{R+1.5}" fill="black"/>')
    return f'<mask id="m-{pid}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">{"".join(parts)}</mask>'

def seam_paths(pid, c, r):
    """Outline of the piece region (cell edges with tab bumps) for a light seam stroke."""
    x, y, w, h = cell_rect(c, r)
    segs = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" />']
    for key, (owner, nb, (cx, cy)) in TABS.items():
        if owner == pid or nb == pid:
            segs.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" />')
    return "".join(segs)

label_pos = {
    "p1": (122, 212), "p2": (300, 236), "p3": (478, 212),
    "p4": (105, 352), "p5": (300, 396), "p6": (495, 352),
}

out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" class="pz-svg" role="img" aria-labelledby="pz-t pz-d">',
       '<title id="pz-t">Scattered symptoms assembling into one picture</title>',
       '<desc id="pz-d">Six puzzle pieces, each labelled with an endometriosis symptom, come together to form a stylised uterus.</desc>',
       '<defs>',
       '<linearGradient id="pz-sheen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".22"/><stop offset=".55" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="1" stop-color="#000000" stop-opacity=".12"/></linearGradient>',
       '<filter id="pz-shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#5A1F1A" flood-opacity=".28"/></filter>',
       '<clipPath id="pz-shape">' + "".join(f'<path d="M{seg.strip()}"/>' for seg in UTERUS.split(" M") if seg.strip()) + '</clipPath>']
for pid, c, r, *_ in PIECES:
    out.append(mask(pid, c, r))
out.append('</defs>')
# faint ghost of the final shape so the destination is readable before assembly
out.append('<g class="pz-ghost">' + "".join(f'<path d="M{seg.strip()}"/>' for seg in UTERUS.split(" M") if seg.strip()) + '</g>')
for pid, c, r, label, dx, dy, rot, col in PIECES:
    lx, ly = label_pos[pid]
    out.append(f'<g class="pz pz-{pid}" style="--dx:{dx}px;--dy:{dy}px;--rot:{rot}deg" filter="url(#pz-shadow)">')
    out.append(f'  <g mask="url(#m-{pid})">')
    out.append(f'    <g clip-path="url(#pz-shape)"><rect x="0" y="0" width="{W}" height="{H}" class="pz-fill" style="fill:{col}"/>'
               f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#pz-sheen)"/>'
               f'<g class="pz-seam">{seam_paths(pid, c, r)}</g></g>')
    out.append('  </g>')
    lw = max(96, int(len(label) * 6.6) + 22)
    out.append(f'  <g class="pz-label"><rect x="{lx-lw//2}" y="{ly-14}" width="{lw}" height="28" rx="14"/>'
               f'<text x="{lx}" y="{ly+4.5}" text-anchor="middle">{label}</text></g>')
    out.append('</g>')
out.append('<g class="pz-final"><rect x="186" y="540" width="228" height="34" rx="17"/><text x="300" y="563" text-anchor="middle">\u2026 the real one: Endometriosis</text></g>')
out.append('</svg>')
pathlib.Path(sys.argv[1]).write_text("\n".join(out), encoding="utf-8")
print("ok", sum(len(l) for l in out))
