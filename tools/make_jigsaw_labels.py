#!/usr/bin/env python3
"""Overlay consequence labels on the 4x4 jigsaw image. Colour pieces = common, white pieces = rare."""
import sys, pathlib
from PIL import Image
IMG="assets/uterus-jigsaw.png"
W,H=Image.open(pathlib.Path(sys.argv[1]).parent.parent/IMG).size
cx=[W/8*(2*i+1) for i in range(4)]; cy=[H/8*(2*j+1) for j in range(4)]
COMMON=[  # (col,row,label)
 (0,0,"Painful periods"),(1,0,"Chronic pelvic pain"),(2,0,"Pain during sex"),(3,0,"Fatigue"),
 (0,1,"Ovarian reserve ↓"),(1,1,"Infertility"),(2,1,"Bowel problems"),(3,1,"Bladder symptoms"),
 (1,2,"Pregnancy risks"),(2,2,"Depression & anxiety"),
 (1,3,"Adhesions"),(2,3,"Autoimmune links"),
]
RARE=[(0,2,"Silent kidney damage"),(3,2,"Lung / diaphragm"),(0,3,"Cardiovascular risk"),(3,3,"Ovarian cancer, small ↑")]
o=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" class="jg-svg" role="img" aria-labelledby="jg-t jg-d">',
   '<title id="jg-t">Consequences of unrecognised endometriosis</title>',
   '<desc id="jg-d">A jigsaw of a uterus illustration. Coloured pieces carry common consequences; white pieces carry rarer ones.</desc>',
   f'<image href="{IMG}" x="0" y="0" width="{W}" height="{H}"/>']
i=0
def chip(x,y,label,cls,i):
    lw=int(len(label)*6.4)+22
    return (f'<g class="jg-chip {cls}" style="--i:{i}"><rect x="{x-lw/2:.0f}" y="{y-13:.0f}" width="{lw}" height="26" rx="13"/>'
            f'<text x="{x:.0f}" y="{y+4.5:.0f}" text-anchor="middle">{label}</text></g>')
for c,r,l in COMMON: o.append(chip(cx[c],cy[r],l,"common",i)); i+=1
for c,r,l in RARE: o.append(chip(cx[c],cy[r],l,"rare",i)); i+=1
o.append('</svg>')
pathlib.Path(sys.argv[1]).write_text("\n".join(o),encoding="utf-8"); print("ok",W,H)
