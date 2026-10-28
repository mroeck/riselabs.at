"""Generate the two CollaborativeCarbon figures as SVG.

Values are taken verbatim from the project's final-results write-up
(riseregenerate.substack.com). Only the six projects the post names with a
value are plotted; the caption says so.

Drawn on a white card, like the other figures on the site (see .fig img in
style.css), so it reads the same in the dark and light themes.
"""
import pathlib

OUT = pathlib.Path("/home/claude/rise-site/assets/img/figures")
OUT.mkdir(parents=True, exist_ok=True)

NAVY      = "#001730"
INK_SOFT  = "#5a6b7f"
MAGENTA   = "#f92d84"
MAG_TINT  = "#f78fb8"
SLATE     = "#6b7f96"
RULE      = "#d8dee6"

# name, sub-label, kg CO2e/m2 (net, A1-A3), colour key
ROWS = [
    ("La Chalmeta",    "Spain · concrete + aluminium",      326, "concrete"),
    ("TRIO inklusiv",  "Vienna · concrete · reference",     306, "concrete"),
    ("OASE inklusiv",  "Vienna · concrete · reference",     267, "concrete"),
    ("Gleis 21",       "Vienna · CLT–concrete hybrid",      171, "hybrid"),
    ("Cirerers",       "Barcelona · CLT + bio-based",       -63, "timber"),
    ("KooWo",          "rural · timber + bio-based",       -115, "timber"),
]
FILL = {"concrete": SLATE, "hybrid": MAG_TINT, "timber": MAGENTA}

# ---------------------------------------------------------------- figure 1
LABEL_W, PAD_L, PAD_R = 196, 16, 18
W = 760
PLOT_X0, PLOT_X1 = LABEL_W + PAD_L, W - PAD_R
DOMAIN = (-150, 360)
ROW_H, BAR_H, TOP = 54, 26, 80

def x(v):
    lo, hi = DOMAIN
    return PLOT_X0 + (v - lo) / (hi - lo) * (PLOT_X1 - PLOT_X0)

H = TOP + len(ROWS) * ROW_H + 46
zero = x(0)
s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
     f'role="img" aria-label="Net embodied carbon, modules A1 to A3, for six '
     f'of the twelve modelled projects, in kilograms CO2 equivalent per square '
     f'metre. La Chalmeta 326, TRIO inklusiv 306, OASE inklusiv 267, Gleis 21 '
     f'171, Cirerers minus 63, KooWo minus 115.">',
     f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
     f'<style>text{{font-family:Figtree,system-ui,sans-serif}}</style>']

# gridlines + ticks
for v in (-100, 0, 100, 200, 300):
    gx = round(x(v), 1)
    is_zero = v == 0
    s.append(f'<line x1="{gx}" y1="{TOP - 16}" x2="{gx}" y2="{TOP + len(ROWS)*ROW_H - 12}" '
             f'stroke="{NAVY if is_zero else RULE}" stroke-width="{1.4 if is_zero else 1}"/>')
    s.append(f'<text x="{gx}" y="{TOP - 24}" text-anchor="middle" font-size="12.5" '
             f'fill="{INK_SOFT}">{v:+d}</text>'.replace("+0", "0"))

s.append(f'<text x="16" y="26" font-size="13" font-weight="600" fill="{NAVY}">'
         f'Net embodied carbon, A1–A3 &#8212; kg CO<tspan baseline-shift="sub" '
         f'font-size="9.5">2</tspan>e/m<tspan baseline-shift="super" '
         f'font-size="9.5">2</tspan></text>')

for i, (name, sub, val, key) in enumerate(ROWS):
    cy = TOP + i * ROW_H + ROW_H / 2 - 6
    s.append(f'<text x="{LABEL_W}" y="{cy - 2}" text-anchor="end" font-size="14.5" '
             f'font-weight="600" fill="{NAVY}">{name}</text>')
    s.append(f'<text x="{LABEL_W}" y="{cy + 14}" text-anchor="end" font-size="11.5" '
             f'fill="{INK_SOFT}">{sub}</text>')
    bx0, bx1 = (zero, x(val)) if val >= 0 else (x(val), zero)
    s.append(f'<rect x="{round(bx0,1)}" y="{round(cy - BAR_H/2 + 2,1)}" '
             f'width="{round(bx1-bx0,1)}" height="{BAR_H}" rx="2" fill="{FILL[key]}"/>')
    if val >= 0:
        s.append(f'<text x="{round(bx1+8,1)}" y="{cy + 7}" font-size="13.5" '
                 f'font-weight="600" fill="{NAVY}">+{val}</text>')
    else:
        s.append(f'<text x="{round(bx0-8,1)}" y="{cy + 7}" text-anchor="end" '
                 f'font-size="13.5" font-weight="600" fill="{NAVY}">{val}</text>')

ly = TOP + len(ROWS) * ROW_H + 16
lx = PLOT_X0
for key, lab in (("concrete", "concrete"), ("hybrid", "hybrid"), ("timber", "timber / bio-based")):
    s.append(f'<rect x="{lx}" y="{ly - 9}" width="11" height="11" rx="2" fill="{FILL[key]}"/>')
    s.append(f'<text x="{lx + 17}" y="{ly}" font-size="12" fill="{INK_SOFT}">{lab}</text>')
    lx += 26 + len(lab) * 6.6
s.append("</svg>")
(OUT / "collabcarbon-embodied-carbon.svg").write_text("\n".join(s))

# ---------------------------------------------------------------- figure 2
FW, FH = 760, 206
# Widths are indicative of the narrowing, not a measured axis - the labels
# carry the counts. Numbers sit inside the bars, labels clear of them, so
# nothing clips however long the text gets.
STAGES = [
    ("329", "projects on the European longlist",            300, SLATE),
    ("60",  "screened for whole life carbon",               186, "#e05a9b"),
    ("12",  "modelled in detail - 10 collaborative, 2 Vienna references", 90, MAGENTA),
]
LABEL_X = 346
f = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {FW} {FH}" role="img" '
     f'aria-label="The study funnel: 329 projects on the European longlist, 60 '
     f'screened for whole life carbon, 12 modelled in detail - 10 collaborative '
     f'projects and 2 Vienna reference blocks.">',
     f'<rect width="{FW}" height="{FH}" fill="#ffffff"/>',
     f'<style>text{{font-family:Figtree,system-ui,sans-serif}}</style>']
by, bh, gap, x0 = 20, 48, 14, 20
for num, lab, w, col in STAGES:
    f.append(f'<rect x="{x0}" y="{by}" width="{w}" height="{bh}" rx="3" fill="{col}"/>')
    f.append(f'<text x="{x0 + 16}" y="{by + 33}" font-size="23" font-weight="700" '
             f'fill="#ffffff">{num}</text>')
    f.append(f'<text x="{LABEL_X}" y="{by + 32}" font-size="13.5" fill="{NAVY}">{lab}</text>')
    by += bh + gap
f.append("</svg>")
(OUT / "collabcarbon-funnel.svg").write_text("\n".join(f))

for p in ("collabcarbon-embodied-carbon.svg", "collabcarbon-funnel.svg"):
    print(f"{p}  {(OUT / p).stat().st_size:,} bytes")
