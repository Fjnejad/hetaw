#!/usr/bin/env python3
"""Build the animated jigsaw SVG from assets/pieces/manifest.json: pieces fly in along their real cut outlines."""
import json, sys, pathlib, math
man = json.load(open("assets/pieces/manifest.json")); W, H = man["W"], man["H"]
LABELS = {
 (0,0):"Painful periods",(1,0):"Chronic pelvic pain",(2,0):"Pain during sex",(3,0):"Fatigue",
 (0,1):"Ovarian reserve ↓",(1,1):"Infertility",(2,1):"Bowel problems",(3,1):"Bladder symptoms",
 (1,2):"Pregnancy risks",(2,2):"Depression & anxiety",(1,3):"Adhesions",(2,3):"Autoimmune links",
 (0,2):"Silent kidney damage",(3,2):"Lung / diaphragm",(0,3):"Cardiovascular risk",(3,3):"Ovarian cancer, small ↑",
}
o=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" class="jg-svg" role="img" aria-labelledby="jg-t jg-d">',
   '<title id="jg-t">Consequences of unrecognised endometriosis</title>',
   '<desc id="jg-d">Jigsaw pieces of a uterus illustration assemble; coloured pieces carry common consequences, white pieces rarer ones.</desc>',
   '<defs><filter id="jg-sh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="5" stdDeviation="5" flood-color="#0B1A33" flood-opacity=".28"/></filter></defs>',
   f'<rect class="jg-ghost" x="1" y="1" width="{W-2}" height="{H-2}" rx="8"/>']
order = sorted(man["pieces"], key=lambda p: (abs(p["cx"]-W/2)+abs(p["cy"]-H/2)))  # centre pieces first
for k, p in enumerate(order):
    dx = (p["cx"] - W/2); dy = (p["cy"] - H/2); d = math.hypot(dx, dy) or 1
    fx, fy = dx/d*260 + (dx*0.35), dy/d*200 + (dy*0.35)   # fly in from outside, radially
    rot = (k % 2 * 2 - 1) * (8 + k % 5 * 3)
    label = LABELS[(p["col"], p["row"])]; cls = "rare" if p["white"] else "common"
    lw = int(len(label) * 6.4) + 22; lx, ly = p["cx"], p["cy"]
    o.append(f'<g class="jp" style="--dx:{fx:.0f}px;--dy:{fy:.0f}px;--rot:{rot}deg;--i:{k}" filter="url(#jg-sh)">'
             f'<image href="assets/pieces/{p["file"]}" x="{p["x"]}" y="{p["y"]}" width="{p["w"]}" height="{p["h"]}"/>'
             f'<g class="jg-chip {cls}"><rect x="{lx-lw/2:.0f}" y="{ly-13:.0f}" width="{lw}" height="26" rx="13"/>'
             f'<text x="{lx:.0f}" y="{ly+4.5:.0f}" text-anchor="middle">{label}</text></g></g>')
o.append('</svg>')
pathlib.Path(sys.argv[1]).write_text("\n".join(o), encoding="utf-8"); print("ok", len(order))
