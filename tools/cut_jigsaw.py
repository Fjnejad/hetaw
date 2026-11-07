#!/usr/bin/env python3
"""Cut the jigsaw image into its pieces along the drawn black borders; write RGBA piece PNGs + a manifest."""
import cv2, numpy as np, json, sys, pathlib
SRC = "assets/uterus-jigsaw.png"; OUT = pathlib.Path("assets/pieces")
im = cv2.imread(SRC, cv2.IMREAD_COLOR); H, W = im.shape[:2]
g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
b,gg,r = cv2.split(im.astype(int)); sat = np.max(im,axis=2).astype(int)-np.min(im,axis=2).astype(int)
lines = ((g < 110) & (sat < 45)).astype(np.uint8)   # black/grey lines only, not dark red tissue
lines = cv2.dilate(lines, np.ones((3, 3), np.uint8))          # close anti-aliased gaps
# frame the image so edge pieces are closed off
lines[0:2, :] = 1; lines[-2:, :] = 1; lines[:, 0:2] = 1; lines[:, -2:] = 1
n, lab, stats, cent = cv2.connectedComponentsWithStats((1 - lines).astype(np.uint8), connectivity=4)
pieces = []
for i in range(1, n):
    x, y, w, h, area = stats[i]
    if area < 0.006 * W * H:  # noise
        continue
    pieces.append((i, x, y, w, h, area, cent[i]))
print("regions:", len(pieces))
# Each piece: region mask dilated to include its share of the border line
rgba = cv2.cvtColor(im, cv2.COLOR_BGR2BGRA)
manifest = []
for k, (i, x, y, w, h, area, (cx, cy)) in enumerate(sorted(pieces, key=lambda p: (round(p[6][1] / (H / 4)), p[6][0]))):
    m = (lab == i).astype(np.uint8) * 255
    m = cv2.dilate(m, np.ones((5, 5), np.uint8))
    ys, xs = np.where(m > 0); x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    piece = rgba[y0:y1, x0:x1].copy(); piece[:, :, 3] = m[y0:y1, x0:x1]
    name = f"piece-{k:02d}.png"; cv2.imwrite(str(OUT / name), piece)
    col = min(3, int(cx / (W / 4))); row = min(3, int(cy / (H / 4)))
    # is the piece mostly white (no picture)?
    reg = im[lab == i]; white = float((reg.min(axis=1) > 235).mean())
    manifest.append({"file": name, "x": int(x0), "y": int(y0), "w": int(x1 - x0), "h": int(y1 - y0), "cx": float(cx), "cy": float(cy), "col": col, "row": row, "white": white > 0.85})
json.dump({"W": W, "H": H, "pieces": manifest}, open(OUT / "manifest.json", "w"), indent=1)
print(json.dumps([(p["col"], p["row"], p["white"]) for p in manifest]))
