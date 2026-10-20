#!/usr/bin/env python3
"""Gera os SVGs do perfil: banner, terminal, quote, painel de anime e divisor.

Sprites animados: PokeAPI/sprites (Gen 5 animated + Showdown GIFs), fan use, nao comercial.
Pokemon (c) Nintendo / Creatures / GAME FREAK.

Rode: python tools/make_assets.py
"""
import base64
import math
import os
import random
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
ASSETS = os.path.join(ROOT, "assets")
SPRITES = os.path.join(HERE, "sprites")
os.makedirs(ASSETS, exist_ok=True)

CYAN = "#00e5ff"
GREEN = "#3ddc97"
LIME = "#a3e635"
GOLD = "#ffd166"
VIOLET = "#a78bfa"
ORANGE = "#ff8a4c"
BLUE = "#38bdf8"
RED = "#ff5c5c"

MON = {
    "rayquaza": {"file": "rayquaza.png", "color": GREEN, "name": "MEGA RAYQUAZA", "type": "DRAGON / FLYING"},
    "deoxys": {"file": "deoxys.png", "color": ORANGE, "name": "DEOXYS", "type": "SPEED / PSYCHIC"},
    "greninja": {"file": "greninja.png", "color": BLUE, "name": "ASH-GRENINJA", "type": "WATER / DARK"},
    "sceptile": {"file": "sceptile.png", "color": LIME, "name": "MEGA SCEPTILE", "type": "GRASS / DRAGON"},
}

_cache = {}


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    return struct.unpack(">II", head[16:24])


def sprite(key):
    if key not in _cache:
        path = os.path.join(SPRITES, MON[key]["file"])
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("ascii")
        w, h = png_size(path)
        _cache[key] = (data, w, h)
    return _cache[key]


def rect(x, y, w, h, fill, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{extra}/>'


FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
}

FONT_BIG = {
    "A": ["0001000", "0011100", "0011100", "0110110", "0110110", "1100011", "1111111", "1100011", "1100011"],
    "D": ["1111100", "1111110", "1100011", "1100011", "1100011", "1100011", "1100011", "1111110", "1111100"],
    "E": ["1111111", "1111111", "1100000", "1100000", "1111110", "1111110", "1100000", "1111111", "1111111"],
    "I": ["1111111", "1111111", "0011100", "0011100", "0011100", "0011100", "0011100", "1111111", "1111111"],
    "L": ["1100000", "1100000", "1100000", "1100000", "1100000", "1100000", "1100000", "1111111", "1111111"],
    "R": ["1111100", "1111110", "1100011", "1100011", "1111110", "1111100", "1101100", "1100110", "1100011"],
    "S": ["0111111", "1111111", "1100000", "1100000", "0111110", "0011111", "0000011", "1111111", "1111110"],
    "V": ["1100011", "1100011", "1100011", "1100011", "0110110", "0110110", "0011100", "0011100", "0001000"],
    "Y": ["1100011", "1100011", "0110110", "0110110", "0011100", "0011100", "0011100", "0011100", "0011100"],
}


def ptext_width(text, s, gap=1, cols=5):
    return (len(text) * cols + (len(text) - 1) * gap) * s


def ptext(text, x, y, s, gap=1, fill=CYAN, cls=None, extra="", font=None, cols=5, raw=False):
    font = font or FONT
    parts = []
    for i, ch in enumerate(text.upper()):
        glyph = font.get(ch)
        if not glyph:
            continue
        gx = x + i * (cols + gap) * s
        for ry, row in enumerate(glyph):
            rx = 0
            while rx < cols:
                if row[rx] == "1":
                    rx2 = rx
                    while rx2 < cols and row[rx2] == "1":
                        rx2 += 1
                    parts.append(f'<rect x="{gx + rx * s}" y="{y + ry * s}" width="{(rx2 - rx) * s}" height="{s}"/>')
                    rx = rx2
                else:
                    rx += 1
    if raw:
        return "".join(parts)
    attrs = [f'fill="{fill}"']
    if cls:
        attrs.append(f'class="{cls}"')
    if extra:
        attrs.append(extra)
    return f'<g {" ".join(attrs)}>{"".join(parts)}</g>'


def mon(key, cx, cy, size, delay=0.0, dur=6.0):
    data, w0, h0 = sprite(key)
    scale = size / max(w0, h0)
    w, h = w0 * scale, h0 * scale
    x, y = cx - w / 2, cy - h / 2
    color = MON[key]["color"]
    r = size * 0.5
    return f'''<g class="mon" style="animation-delay:{delay}s;animation-duration:{dur}s">
<circle class="ring" cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="{color}" stroke-opacity=".22" stroke-width="1.5" stroke-dasharray="4 10"/>
<ellipse class="aura" cx="{cx:.1f}" cy="{cy:.1f}" rx="{size * 0.42:.1f}" ry="{size * 0.36:.1f}" fill="{color}" opacity=".16" filter="url(#blur24)"/>
<image href="data:image/png;base64,{data}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" style="image-rendering:pixelated"/>
</g>'''


ANIM = {
    "rayquaza": "rayquaza.gif",
    "deoxys": "deoxys.gif",
    "greninja": "greninja.gif",
    "sceptile": "sceptile.gif",
}

_anim_cache = {}


def gif_sprite(key):
    if key not in _anim_cache:
        path = os.path.join(HERE, "anim", ANIM[key])
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("ascii")
        with open(path, "rb") as f:
            head = f.read(10)
        w, h = struct.unpack("<HH", head[6:10])
        _anim_cache[key] = (data, w, h)
    return _anim_cache[key]


def mon_anim(key, cx, cy, size, flip=False, sway=None, delay=0.0, dur=5.5):
    data, w0, h0 = gif_sprite(key)
    scale = size / max(w0, h0)
    w, h = w0 * scale, h0 * scale
    x, y = cx - w / 2, cy - h / 2
    color = MON[key]["color"]
    img = (f'<image href="data:image/gif;base64,{data}" x="{x:.1f}" y="{y:.1f}" '
           f'width="{w:.1f}" height="{h:.1f}" style="image-rendering:pixelated"/>')
    if flip:
        img = f'<g transform="translate({2 * cx:.1f},0) scale(-1,1)">{img}</g>'
    cls = "mon" + (f" sway-{sway}" if sway else "")
    r = size * 0.5
    return f'''<g class="{cls}" style="animation-delay:{delay}s;animation-duration:{dur}s">
<circle class="ring" cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="{color}" stroke-opacity=".22" stroke-width="1.5" stroke-dasharray="4 10"/>
<ellipse class="aura" cx="{cx:.1f}" cy="{cy:.1f}" rx="{size * 0.42:.1f}" ry="{size * 0.36:.1f}" fill="{color}" opacity=".16" filter="url(#blur24)"/>
{img}
</g>'''


HERO_CSS = """
@keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-9px); } }
@keyframes aura { 0%,100% { opacity: .12; } 50% { opacity: .28; } }
@keyframes nameFloat {
  0%,100% { transform: translate(0,6px) rotate(0deg); }
  25% { transform: translate(12px,-6px) rotate(.5deg); }
  50% { transform: translate(0,-14px) rotate(0deg); }
  75% { transform: translate(-12px,-6px) rotate(-.5deg); }
}
@keyframes ticker { from { transform: translateX(0); } to { transform: translateX(-780px); } }
@keyframes twinkle { 0%,100% { opacity: .12; } 50% { opacity: .85; } }
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes rain { from { transform: translateY(-90px); } to { transform: translateY(520px); } }
@keyframes flicker {
  0%, 6%, 8%, 43%, 45%, 100% { opacity: 0; }
  7% { opacity: .8; }
  44% { opacity: .55; }
}
@keyframes scanpass { from { transform: translateY(0); } to { transform: translateY(480px); } }
@keyframes swayL { 0%,100% { transform: translate(0,0) rotate(0deg); } 50% { transform: translate(8px,-10px) rotate(2deg); } }
@keyframes swayR { 0%,100% { transform: translate(0,0) rotate(0deg); } 50% { transform: translate(-8px,-10px) rotate(-2deg); } }
@keyframes shine { 0% { transform: translateX(0); } 58%,100% { transform: translateX(820px); } }
@keyframes nameGlow { 0%,100% { opacity: .35; } 50% { opacity: .62; } }
@keyframes leafpulse { 0%,100% { opacity: .25; } 50% { opacity: .72; } }
@keyframes speedline { 0%,100% { opacity: .12; transform: translateX(0); } 50% { opacity: .55; transform: translateX(-7px); } }
.mon { animation: float 6s ease-in-out infinite; will-change: transform; }
.sway-l { animation: swayL 5.4s ease-in-out infinite; }
.sway-r { animation: swayR 5.8s ease-in-out infinite; }
.aura { animation: aura 4.5s ease-in-out infinite; will-change: opacity; }
.ring { animation: spin 80s linear infinite; transform-box: fill-box; transform-origin: center; }
.name-float { animation: nameFloat 7s ease-in-out infinite; transform-box: fill-box; transform-origin: center; will-change: transform; }
.name-glow { animation: nameGlow 4s ease-in-out infinite; will-change: opacity; }
.name-shine { animation: shine 5.8s ease-in-out infinite; will-change: transform; }
.ticker-track { animation: ticker 24s linear infinite 1s; will-change: transform; }
.leaf { animation: leafpulse 3.2s ease-in-out infinite; }
.speedline { animation: speedline 1.9s ease-in-out infinite; }
.bit { animation: twinkle 4s ease-in-out infinite; }
.rain { animation: rain 16s linear infinite; }
.bolt { animation: flicker 7s steps(1,end) infinite; }
.shuriken { animation: spin 12s linear infinite; transform-box: fill-box; transform-origin: center; }
.scanpass { animation: scanpass 9s linear infinite; }
"""


def bits(n=30, seed=9):
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x = rnd.randrange(18, 1182)
        y = rnd.randrange(18, 462)
        s = rnd.choice([2, 2, 3, 4])
        col = rnd.choice([CYAN, GREEN, GOLD, VIOLET])
        delay = -round(rnd.uniform(0, 4), 2)
        dur = round(rnd.uniform(3, 7), 2)
        out.append(rect(x, y, s, s, col,
                        f' class="bit" style="animation-delay:{delay}s;animation-duration:{dur}s" opacity=".75"'))
    return "".join(out)


def rain_columns(seed=21):
    rnd = random.Random(seed)
    out = []
    for i in range(7):
        x = 80 + i * 168 + rnd.randrange(-18, 18)
        dur = round(rnd.uniform(13, 22), 2)
        delay = -round(rnd.uniform(0, 20), 2)
        parts = []
        for j in range(5):
            parts.append(rect(x, 16 + j * 28, 2, 11, CYAN, ' opacity=".55"'))
            parts.append(rect(x + 7, 30 + j * 28, 2, 6, GREEN, ' opacity=".3"'))
        out.append(f'<g class="rain" style="animation-delay:{delay}s;animation-duration:{dur}s">{"".join(parts)}</g>')
    return "".join(out)


def bolt(x, y, scale=1.0, delay=0.0):
    pts = [(0, 0), (7, 30), (-1, 32), (9, 64), (1, 66), (15, 100)]
    path = " ".join(f"{x + px * scale:.1f},{y + py * scale:.1f}" for px, py in pts)
    return (f'<g class="bolt" style="animation-delay:{delay}s">'
            f'<polyline points="{path}" fill="none" stroke="{GOLD}" stroke-width="{3 * scale:.1f}" '
            f'stroke-linejoin="miter" opacity=".85" filter="url(#glow)"/></g>')


def leaf(cx, cy, s, rot, delay=0.0, color=LIME):
    d = (f"M0,{-s:.1f} C{s * .8:.1f},{-s * .35:.1f} {s * .8:.1f},{s * .35:.1f} 0,{s:.1f} "
         f"C{-s * .8:.1f},{s * .35:.1f} {-s * .8:.1f},{-s * .35:.1f} 0,{-s:.1f} Z")
    vein = f'<line x1="0" y1="{-s * .72:.1f}" x2="0" y2="{s * .72:.1f}" stroke="#0b2a1a" stroke-width="1" opacity=".55"/>'
    return (f'<g class="leaf" transform="translate({cx},{cy}) rotate({rot})" opacity=".55" '
            f'style="animation-delay:{delay}s">'
            f'<path d="{d}" fill="{color}"/>{vein}</g>')


def shuriken(cx, cy, r):
    p = (f"0,{-r} {r * .18:.1f},{-r * .18:.1f} {r},0 {r * .18:.1f},{r * .18:.1f} "
         f"0,{r} {-r * .18:.1f},{r * .18:.1f} {-r},0 {-r * .18:.1f},{-r * .18:.1f}")
    inner = r * .28
    return (f'<g transform="translate({cx},{cy})"><g class="shuriken">'
            f'<polygon points="{p}" fill="{BLUE}" opacity=".8" filter="url(#glow)"/>'
            f'<polygon points="0,{-inner} {inner},0 0,{inner} {-inner},0" fill="#d8fbff"/></g></g>')


def banner():
    w, h = 1200, 480
    name_s, name_gap = 9, 1
    name_text = "ADRIARLEY"
    name_w = ptext_width(name_text, name_s, name_gap, cols=7)
    nx = (w - name_w) // 2
    ny = 176
    name_shape = ptext(name_text, nx, ny, name_s, name_gap, font=FONT_BIG, cols=7, raw=True)

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
                 f'role="img" aria-label="Banner pixel art com Mega Rayquaza, Deoxys Speed, Mega Sceptile e Ash-Greninja ao redor do nome Adriarley, com ticker da frase de Stan Lee">')
    parts.append(f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#04060d"/>
  <stop offset=".55" stop-color="#07111f"/>
  <stop offset="1" stop-color="#03080e"/>
</linearGradient>
<linearGradient id="nameGrad" gradientUnits="userSpaceOnUse" x1="0" y1="{ny}" x2="0" y2="{ny + 9 * name_s}">
  <stop offset="0" stop-color="#ffffff"/>
  <stop offset=".42" stop-color="#bdfaff"/>
  <stop offset="1" stop-color="{GREEN}"/>
</linearGradient>
<linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#ffffff" stop-opacity="0"/>
  <stop offset=".5" stop-color="#ffffff" stop-opacity=".9"/>
  <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
</linearGradient>
<clipPath id="nameClip">{name_shape}</clipPath>
<radialGradient id="vig" cx=".5" cy=".46" r=".78">
  <stop offset=".55" stop-color="#000" stop-opacity="0"/>
  <stop offset="1" stop-color="#000" stop-opacity=".48"/>
</radialGradient>
<pattern id="grid" width="44" height="44" patternUnits="userSpaceOnUse">
  <path d="M44 0H0V44" fill="none" stroke="#143245" stroke-width="1"/>
</pattern>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
  <rect width="4" height="1" fill="#000" opacity=".55"/>
</pattern>
<filter id="blur24" x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="24"/></filter>
<filter id="blur40" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="40"/></filter>
<filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="7"/></filter>
<clipPath id="tickerClip"><rect x="358" y="308" width="576" height="30"/></clipPath>
<linearGradient id="tickerFadeR" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#02070c" stop-opacity="0"/>
  <stop offset="1" stop-color="#02070c" stop-opacity="1"/>
</linearGradient>
<linearGradient id="tickerFadeL" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#02070c" stop-opacity="1"/>
  <stop offset="1" stop-color="#02070c" stop-opacity="0"/>
</linearGradient>
</defs>''')
    parts.append(f'<style>{HERO_CSS}</style>')
    parts.append(f'<rect width="{w}" height="{h}" fill="url(#bg)"/>')
    parts.append(rain_columns())
    parts.append(f'<g filter="url(#blur40)">'
                 f'<ellipse cx="150" cy="70" rx="270" ry="150" fill="{GREEN}" opacity=".16"/>'
                 f'<ellipse cx="1040" cy="60" rx="250" ry="150" fill="{ORANGE}" opacity=".13"/>'
                 f'<ellipse cx="1080" cy="340" rx="230" ry="130" fill="{BLUE}" opacity=".12"/>'
                 f'<ellipse cx="120" cy="350" rx="230" ry="130" fill="{LIME}" opacity=".10"/>'
                 f'</g>')
    parts.append(f'<rect width="{w}" height="{h}" fill="url(#grid)" opacity=".55"/>')

    floor = []
    for i in range(-9, 10):
        x = 600 + i * 100
        floor.append(f'<line x1="600" y1="300" x2="{x}" y2="{h}" stroke="{CYAN}" stroke-opacity=".10"/>')
    for yy, op in [(312, .10), (328, .09), (348, .08), (374, .07), (406, .06), (444, .05)]:
        floor.append(f'<line x1="0" y1="{yy}" x2="{w}" y2="{yy}" stroke="{CYAN}" stroke-opacity="{op}"/>')
    parts.append(f'<g>{"".join(floor)}</g>')

    parts.append(f'<polygon points="600,4 934,216 600,428 266,216" fill="none" stroke="{CYAN}" '
                 f'stroke-opacity=".13" stroke-width="1.5" stroke-dasharray="7 12"/>')
    parts.append(f'<g class="ring"><polygon points="600,40 900,216 600,392 300,216" fill="none" '
                 f'stroke="{GREEN}" stroke-opacity=".11" stroke-width="1.5" stroke-dasharray="3 16"/></g>')
    for (dx, dy, col) in [(600, 4, GOLD), (934, 216, CYAN), (600, 428, GOLD), (266, 216, CYAN)]:
        parts.append(f'<polygon points="{dx},{dy - 5} {dx + 5},{dy} {dx},{dy + 5} {dx - 5},{dy}" fill="{col}" opacity=".5"/>')
    parts.append(bits())

    parts.append(mon_anim("rayquaza", 150, 160, 200, flip=True, sway="l", delay=-0.5, dur=5.4))
    parts.append(mon_anim("deoxys", 1072, 128, 185, sway="r", delay=-2.4, dur=5.8))
    parts.append(mon_anim("sceptile", 132, 340, 195, flip=True, sway="l", delay=-1.4, dur=4.8))
    parts.append(mon_anim("greninja", 1065, 340, 200, sway="r", delay=-3.1, dur=5.2))

    parts.append(leaf(216, 276, 11, 35, -0.4))
    parts.append(leaf(233, 318, 9, -25, -1.6))
    parts.append(leaf(204, 380, 12, 65, -2.8))
    parts.append(leaf(226, 250, 7, 10, -1.1))
    parts.append(shuriken(960, 278, 17))
    for i, (yy, ln) in enumerate([(88, 46), (124, 30), (160, 40)]):
        parts.append(f'<line class="speedline" x1="{980 - ln}" y1="{yy}" x2="980" y2="{yy}" '
                     f'stroke="{ORANGE}" stroke-width="2" opacity=".35" style="animation-delay:{-i * 0.6}s"/>')

    def tag(text, x, y, color, anchor="start"):
        return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="ui-monospace, Consolas, monospace" '
                f'font-size="9" letter-spacing="2.5" fill="{color}" opacity=".72">{text}</text>')

    parts.append(tag("MEGA RAYQUAZA // DRAGON / FLYING", 36, 26, GREEN))
    parts.append(tag("DEOXYS // SPEED / PSYCHIC", 1164, 26, ORANGE, "end"))
    parts.append(tag("MEGA SCEPTILE // GRASS / DRAGON", 36, 452, LIME))
    parts.append(tag("ASH-GRENINJA // WATER / DARK", 1164, 452, BLUE, "end"))

    layers = [(12, "#0a3a2e"), (8, "#0d4d3a"), (4, "#116347")]
    name_parts = [f'<g class="name-glow" filter="url(#glow)">{ptext(name_text, nx, ny, name_s, name_gap, CYAN, font=FONT_BIG, cols=7)}</g>']
    for dx, col in layers:
        name_parts.append(ptext(name_text, nx + dx, ny + dx, name_s, name_gap, col, font=FONT_BIG, cols=7))
    name_parts.append(ptext(name_text, nx, ny, name_s, name_gap, "url(#nameGrad)", font=FONT_BIG, cols=7))
    name_parts.append(f'<g clip-path="url(#nameClip)"><rect class="name-shine" x="{nx - 110}" y="{ny - 14}" '
                      f'width="90" height="{9 * name_s + 28}" fill="url(#shine)" opacity=".8"/></g>')
    parts.append(f'<g class="name-float">{"".join(name_parts)}</g>')

    parts.append(f'<text x="600" y="154" text-anchor="middle" font-family="ui-monospace, Consolas, monospace" '
                 f'font-size="11" letter-spacing="5" fill="#7dd3fc" opacity=".85">PLAYER 01 // @EuSouEu223</text>')
    parts.append(f'<text x="600" y="292" text-anchor="middle" font-family="ui-monospace, Consolas, monospace" '
                 f'font-size="11" letter-spacing="5" fill="{GREEN}" opacity=".8">PYTHON DEV · APRENDENDO · PIXEL ART</text>')

    # Ticker: duas copias da frase. O avanco (780px) tem que bater com
    # @keyframes ticker e com o x da segunda copia (376 + 780 = 1156).
    def ticker_copy(x):
        return (f'<text x="{x}" y="330" font-family="Georgia, Times New Roman, serif" font-style="italic" '
                f'font-size="13" fill="#eafcff">Se você tem uma '
                f'<tspan font-family="Impact, Arial Black, sans-serif" font-style="normal" font-weight="700" '
                f'font-size="14.5" fill="{GOLD}">ideia</tspan>, que você '
                f'<tspan font-family="ui-monospace, Consolas, monospace" font-style="normal" font-weight="700" '
                f'font-size="12.5" fill="{CYAN}">genuinamente</tspan> acha '
                f'<tspan font-family="Trebuchet MS, Verdana, sans-serif" font-style="normal" font-weight="700" '
                f'font-size="14.5" fill="{LIME}">boa</tspan>, não deixe '
                f'<tspan font-family="Trebuchet MS, Verdana, sans-serif" font-style="normal" font-weight="700" '
                f'font-size="13.5" fill="{ORANGE}">ninguém</tspan> te convencer do '
                f'<tspan font-family="Georgia, Times New Roman, serif" font-style="italic" font-weight="700" '
                f'font-size="14" fill="#ffffff">contrário.</tspan>'
                f'<tspan dx="14" font-family="ui-monospace, Consolas, monospace" font-style="normal" '
                f'font-size="10.5" fill="{GOLD}">— STAN LEE</tspan>'
                f'<tspan dx="14" font-family="ui-monospace, Consolas, monospace" font-style="normal" '
                f'font-size="10.5" fill="{GOLD}">✦</tspan></text>')

    parts.append(
        '<g>'
        f'<rect x="260" y="306" width="680" height="36" rx="2" fill="#02070c" fill-opacity=".94" '
        f'stroke="{GOLD}" stroke-opacity=".42"/>'
        f'<rect x="260" y="306" width="3" height="36" fill="{GOLD}" opacity=".55"/>'
        f'<line x1="264" y1="307.5" x2="938" y2="307.5" stroke="{GOLD}" stroke-opacity=".18"/>'
        f'<line x1="264" y1="340.5" x2="938" y2="340.5" stroke="{GOLD}" stroke-opacity=".14"/>'
        f'<circle cx="268" cy="324" r="2.5" fill="{GOLD}"/>'
        f'<text x="274" y="329" font-family="ui-monospace, Consolas, monospace" font-size="9.5" '
        f'letter-spacing="1.1" fill="{GOLD}" opacity=".95">// STAN LEE</text>'
        f'<line x1="354" y1="312" x2="354" y2="336" stroke="{GOLD}" stroke-opacity=".26"/>'
        '<g clip-path="url(#tickerClip)"><g class="ticker-track">'
        f'{ticker_copy(376)}{ticker_copy(1156)}'
        '</g></g>'
        '<rect x="356" y="306" width="28" height="36" fill="url(#tickerFadeL)"/>'
        '<rect x="884" y="306" width="56" height="36" fill="url(#tickerFadeR)"/>'
        '</g>'
    )
    parts.append(f'<text x="600" y="466" text-anchor="middle" font-family="ui-monospace, Consolas, monospace" '
                 f'font-size="9" letter-spacing="6" fill="#5a7a8a" opacity=".7">INSERT COIN</text>')

    parts.append(f'<rect class="scanpass" x="0" y="0" width="{w}" height="2" fill="{CYAN}" opacity=".16"/>')
    parts.append(f'<rect width="{w}" height="{h}" fill="url(#scan)" opacity=".16"/>')
    parts.append(f'<rect width="{w}" height="{h}" fill="url(#vig)"/>')
    parts.append(f'<rect x="1.5" y="1.5" width="{w - 3}" height="{h - 3}" rx="6" fill="none" '
                 f'stroke="{CYAN}" stroke-opacity=".28" stroke-width="3"/>')
    parts.append(f'<path d="M16 44V16h28M1156 16h28v28M1184 436v28h-28M44 464H16v-28" fill="none" '
                 f'stroke="{CYAN}" stroke-opacity=".65" stroke-width="2"/>')
    parts.append('</svg>')
    return "\n".join(parts)


ANIME_CSS = """
@keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-6px); } }
@keyframes aura { 0%,100% { opacity: .12; } 50% { opacity: .26; } }
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes flick {
  0%, 5%, 7%, 41%, 43%, 100% { opacity: 0; }
  6% { opacity: .10; }
  42% { opacity: .07; }
}
@keyframes rec { 0%,100% { opacity: 1; } 50% { opacity: .15; } }
@keyframes play { 0%,100% { opacity: .45; } 50% { opacity: 1; } }
@keyframes vs { 0%,100% { transform: scale(1); opacity: .8; } 50% { transform: scale(1.08); opacity: 1; } }
.mon { animation: float 5.5s ease-in-out infinite; will-change: transform; }
.aura { animation: aura 4s ease-in-out infinite; will-change: opacity; }
.ring { animation: spin 70s linear infinite; transform-box: fill-box; transform-origin: center; }
.flick { animation: flick 7s steps(1,end) infinite; }
.rec { animation: rec 1.5s steps(1,end) infinite; }
.play { animation: play 2.2s ease-in-out infinite; }
.vs { animation: vs 2.4s ease-in-out infinite; transform-box: fill-box; transform-origin: center; will-change: transform, opacity; }
"""


def anime_shelf():
    w, h = 700, 240
    scene = []
    scene.append('<rect x="38" y="46" width="298" height="148" fill="url(#screenSky)"/>')
    for (x, y, s) in [(58, 62, 2), (86, 74, 2), (126, 58, 3), (168, 70, 2), (206, 54, 2),
                      (246, 66, 3), (292, 56, 2), (318, 90, 2), (64, 104, 2), (150, 96, 2)]:
        scene.append(rect(x, y, s, s, "#dff6ff", ' opacity=".45"'))
    scene.append(f'<circle cx="310" cy="66" r="24" fill="{GOLD}" opacity=".12" filter="url(#blur24)"/>')
    scene.append(f'<circle cx="310" cy="66" r="12" fill="{GOLD}" opacity=".9"/>')
    scene.append(f'<polygon points="38,194 92,138 132,164 178,118 228,170 274,136 336,194" fill="#0a1826"/>')
    scene.append(f'<polygon points="38,194 76,162 122,184 168,148 218,186 270,160 336,194" fill="#07111d"/>')
    scene.append('<rect x="38" y="176" width="298" height="18" fill="#040a11"/>')
    for i in range(-6, 7):
        x = 187 + i * 30
        scene.append(f'<line x1="187" y1="176" x2="{x}" y2="194" stroke="{CYAN}" stroke-opacity=".12"/>')
    scene.append(f'<line x1="38" y1="176" x2="336" y2="176" stroke="{CYAN}" stroke-opacity=".25"/>')
    scene.append(mon_anim("rayquaza", 108, 124, 100, flip=True, delay=-0.5, dur=5.8))
    scene.append(mon_anim("deoxys", 286, 124, 90, delay=-1.8, dur=6.6))
    scene.append(ptext("VS", 178, 112, 4, 1, GOLD, cls="vs"))
    scene.append(f'<text x="108" y="186" text-anchor="middle" font-family="ui-monospace, Consolas, monospace" '
                 f'font-size="6.5" letter-spacing="1" fill="{GREEN}" opacity=".85">MEGA RAYQUAZA</text>')
    scene.append(f'<text x="286" y="186" text-anchor="middle" font-family="ui-monospace, Consolas, monospace" '
                 f'font-size="7" letter-spacing="2" fill="{ORANGE}" opacity=".85">DEOXYS</text>')
    scene.append(f'<rect x="46" y="56" width="4" height="4" fill="{RED}"/>')
    scene.append(f'<text x="54" y="61" font-family="ui-monospace, Consolas, monospace" font-size="7" '
                 f'letter-spacing="2" fill="#ffd9d9" opacity=".8">LIVE</text>')
    scene.append(f'<text x="326" y="61" text-anchor="end" font-family="ui-monospace, Consolas, monospace" '
                 f'font-size="7" letter-spacing="2" fill="#7dd3fc" opacity=".75">EP.01</text>')
    scene.append('<rect x="38" y="46" width="298" height="148" fill="url(#scan2)" opacity=".4"/>')
    scene.append('<rect class="flick" x="38" y="46" width="298" height="148" fill="#7df9ff" opacity="0"/>')
    scene.append('<polygon points="38,46 150,46 38,120" fill="#ffffff" opacity=".04"/>')

    chips = []
    for i, (label, col) in enumerate([("ON REPEAT", CYAN), ("SUB", GOLD), ("3D", GREEN)]):
        x = 390 + i * 92
        chips.append(f'<rect x="{x}" y="168" width="82" height="22" rx="2" fill="#0a1521" stroke="{col}" stroke-opacity=".6"/>')
        chips.append(f'<text x="{x + 41}" y="183" text-anchor="middle" font-family="ui-monospace, Consolas, monospace" '
                     f'font-size="9" letter-spacing="1.5" fill="{col}">{label}</text>')

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
                 f'role="img" aria-label="Painel anime mode com uma batalha pixel entre Mega Rayquaza e Deoxys Speed">')
    parts.append('''<defs>
<linearGradient id="panel" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#050b14"/>
  <stop offset="1" stop-color="#081624"/>
</linearGradient>
<linearGradient id="screenSky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#060c1c"/>
  <stop offset="1" stop-color="#0a2030"/>
</linearGradient>
<linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#00e5ff" stop-opacity="0"/>
  <stop offset=".5" stop-color="#00e5ff" stop-opacity=".45"/>
  <stop offset="1" stop-color="#00e5ff" stop-opacity="0"/>
</linearGradient>
<pattern id="scan2" width="4" height="4" patternUnits="userSpaceOnUse">
  <rect width="4" height="1" fill="#000" opacity=".55"/>
</pattern>
<clipPath id="scr"><rect x="38" y="46" width="298" height="148"/></clipPath>
<filter id="blur24" x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="24"/></filter>
<filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="5"/></filter>
</defs>''')
    parts.append(f'<style>{ANIME_CSS}</style>')
    parts.append(f'<polygon points="0,14 14,0 686,0 700,14 700,226 686,240 14,240 0,226" fill="url(#panel)" '
                 f'stroke="{CYAN}" stroke-opacity=".32" stroke-width="2.5"/>')
    parts.append(f'<path d="M16 46V18h28M656 18h28v28M684 194v28h-28M44 222H16v-28" fill="none" '
                 f'stroke="{CYAN}" stroke-opacity=".4" stroke-width="2"/>')
    parts.append('<rect x="22" y="30" width="330" height="180" rx="8" fill="#0a1420" stroke="#1b3a4a" stroke-width="2"/>')
    parts.append('<rect x="34" y="42" width="306" height="156" rx="4" fill="#03070d"/>')
    parts.append(f'<g clip-path="url(#scr)">{"".join(scene)}</g>')
    parts.append(f'<circle cx="334" cy="196" r="3" fill="{GREEN}"/>')
    parts.append(f'<text x="390" y="36" font-family="ui-monospace, Consolas, monospace" font-size="9" '
                 f'letter-spacing="2" fill="#5a7a8a">// BATTLE_ARCHIVE</text>')
    parts.append(f'<text x="390" y="90" font-family="ui-monospace, Consolas, monospace" font-size="36" '
                 f'font-weight="700" letter-spacing="8" fill="#eafcff">ANIME</text>')
    parts.append(f'<text x="390" y="128" font-family="ui-monospace, Consolas, monospace" font-size="36" '
                 f'font-weight="700" letter-spacing="8" fill="{CYAN}">MODE</text>')
    parts.append(f'<text x="390" y="150" font-family="ui-monospace, Consolas, monospace" font-size="10" '
                 f'letter-spacing="2" fill="#7dd3fc" opacity=".8">SHONEN // PIXEL // 3D</text>')
    parts.append("".join(chips))
    parts.append(f'<text x="390" y="214" font-family="ui-monospace, Consolas, monospace" font-size="8" '
                 f'letter-spacing="2" fill="#5a7a8a" opacity=".7">SRC: PIXEL VAULT // 60 FPS</text>')
    parts.append(f'<rect x="390" y="222" width="270" height="3" fill="url(#fade)" opacity=".7"/>')
    parts.append(f'<circle class="play" cx="662" cy="60" r="14" fill="none" stroke="{CYAN}" stroke-opacity=".55"/>')
    parts.append(f'<polygon points="657,52 657,68 671,60" fill="{CYAN}" opacity=".85"/>')
    parts.append(f'<circle class="rec" cx="648" cy="20" r="3" fill="{RED}"/>')
    parts.append(f'<text x="656" y="23" font-family="ui-monospace, Consolas, monospace" font-size="8" '
                 f'letter-spacing="2" fill="{RED}" opacity=".85">REC</text>')
    parts.append('</svg>')
    return "\n".join(parts)


TERM_CSS = """
@keyframes msg {
  0% { opacity: 0; transform: translateY(6px); }
  3% { opacity: 1; transform: translateY(0); }
  86% { opacity: 1; }
  92%, 100% { opacity: 0; transform: translateY(0); }
}
@keyframes blink { 0%,49% { opacity: 1; } 50%,100% { opacity: 0; } }
@keyframes bar { from { transform: scaleX(0); } to { transform: scaleX(1); } }
@keyframes scanpass { from { transform: translateY(0); } to { transform: translateY(300px); } }
.msg { animation: msg 26s linear infinite; animation-fill-mode: both; will-change: opacity, transform; }
.cursor { animation: blink 1s steps(1,end) infinite; }
.bar { transform-box: fill-box; transform-origin: left; animation: bar 3.6s ease-out infinite; will-change: transform; }
.scanpass { animation: scanpass 10s linear infinite; }
"""


def terminal():
    w, h = 1200, 300
    lines = [
        ("$ whoami", "Adriarley — dev em aprendizado · Python · pixel art", "#eafcff"),
        ("$ ls repos/", "python/  estudos/  projetos/  pixel-lab/", GREEN),
        ("$ cat mission.txt", "aprender Python na prática e transformar ideia em projeto real", "#eafcff"),
        ("$ git log -1", "feat: mais um boss derrotado", GOLD),
        ("$ echo $MOTIVACAO", "todo bug é um boss. respawn e tenta de novo.", GREEN),
        ("$ ./next.sh", "consistência > motivação. próximo commit.", CYAN),
    ]
    body = []
    for i, (cmd, out, col) in enumerate(lines):
        y = 84 + i * 30
        cursor = ""
        if i == len(lines) - 1:
            cx = 250 + int(len(out) * 7.8) + 6
            cursor = f'<rect class="cursor" x="{cx}" y="{y - 12}" width="8" height="14" fill="{GREEN}"/>'
        body.append(f'''<g class="msg" style="animation-delay:{i * 2.2}s">
<text x="40" y="{y}" font-family="ui-monospace, Consolas, monospace" font-size="13" fill="{CYAN}" opacity=".9">{cmd}</text>
<text x="250" y="{y}" font-family="ui-monospace, Consolas, monospace" font-size="13" fill="{col}" style="white-space:pre">{out}</text>
{cursor}
</g>''')

    bars = []
    for i, (label, val, col) in enumerate([("FOCO", 88, CYAN), ("PYTHON", 76, GREEN), ("SHIPS", 64, GOLD)]):
        y = 124 + i * 38
        fillw = 280 * val / 100
        bars.append(f'<text x="886" y="{y}" font-family="ui-monospace, Consolas, monospace" font-size="10" '
                    f'letter-spacing="2" fill="#7dd3fc" opacity=".8">{label}</text>')
        bars.append(f'<text x="1150" y="{y}" text-anchor="end" font-family="ui-monospace, Consolas, monospace" '
                    f'font-size="10" fill="{col}" opacity=".9">{val}%</text>')
        bars.append(f'<rect x="886" y="{y + 8}" width="264" height="6" fill="#0b2230"/>')
        bars.append(f'<rect class="bar" x="886" y="{y + 8}" width="{fillw * 264 / 280:.1f}" height="6" fill="{col}" '
                    f'style="animation-delay:{i * 0.35}s"/>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Terminal animado com mensagens sobre Adriarley, seus repositórios e frases motivacionais">
<defs>
<linearGradient id="tbg" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#040a12"/>
  <stop offset="1" stop-color="#071824"/>
</linearGradient>
<radialGradient id="tvg" cx=".5" cy=".45" r=".8">
  <stop offset=".55" stop-color="#000" stop-opacity="0"/>
  <stop offset="1" stop-color="#000" stop-opacity=".35"/>
</radialGradient>
<pattern id="tscan" width="4" height="4" patternUnits="userSpaceOnUse">
  <rect width="4" height="1" fill="#000" opacity=".55"/>
</pattern>
</defs>
<style>{TERM_CSS}</style>
<polygon points="0,16 16,0 1184,0 1200,16 1200,284 1184,300 16,300 0,284" fill="url(#tbg)" stroke="{CYAN}" stroke-opacity=".3" stroke-width="2.5"/>
<ellipse cx="140" cy="10" rx="320" ry="120" fill="{GREEN}" opacity=".055"/>
<circle cx="36" cy="22" r="4" fill="{RED}"/>
<circle cx="50" cy="22" r="4" fill="{GOLD}"/>
<circle cx="64" cy="22" r="4" fill="{GREEN}"/>
<text x="82" y="27" font-family="ui-monospace, Consolas, monospace" font-size="12" letter-spacing="1" fill="#7dd3fc">EuSouEu223@github: ~/profile</text>
<text x="1166" y="27" text-anchor="end" font-family="ui-monospace, Consolas, monospace" font-size="9" fill="#5a7a8a" opacity=".7">bash — 80x24</text>
<line x1="0" y1="42" x2="1200" y2="42" stroke="{CYAN}" stroke-opacity=".14"/>
{''.join(body)}
<line x1="846" y1="64" x2="846" y2="252" stroke="{CYAN}" stroke-opacity=".14"/>
<rect x="866" y="64" width="306" height="188" rx="2" fill="#07121c" stroke="#1b3a4a" stroke-opacity=".8"/>
<text x="886" y="90" font-family="ui-monospace, Consolas, monospace" font-size="10" letter-spacing="2" fill="{CYAN}" opacity=".85">// STATUS</text>
<circle class="cursor" cx="1150" cy="86" r="3" fill="{GREEN}"/>
{''.join(bars)}
<text x="886" y="238" font-family="ui-monospace, Consolas, monospace" font-size="10" letter-spacing="2" fill="{GOLD}" opacity=".85">LV. 99 // CONTINUE</text>
<line x1="40" y1="264" x2="1160" y2="264" stroke="{CYAN}" stroke-opacity=".1"/>
<circle cx="40" cy="278" r="3" fill="{GREEN}"/>
<text x="54" y="282" font-family="ui-monospace, Consolas, monospace" font-size="9" letter-spacing="2" fill="{GREEN}" opacity=".85">READY // KEEP SHIPPING</text>
<text x="1166" y="282" text-anchor="end" font-family="ui-monospace, Consolas, monospace" font-size="9" letter-spacing="1" fill="#5a7a8a" opacity=".55">UTF-8 · 60 FPS</text>
<rect class="scanpass" x="0" y="0" width="1200" height="2" fill="{CYAN}" opacity=".12"/>
<rect width="1200" height="300" fill="url(#tscan)" opacity=".12"/>
<rect width="1200" height="300" fill="url(#tvg)"/>
<path d="M16 44V16h28M1156 16h28v28M1184 256v28h-28M44 284H16v-28" fill="none" stroke="{CYAN}" stroke-opacity=".4" stroke-width="2"/>
</svg>'''


QUOTE_CSS = """
@keyframes qlineIn {
  0% { opacity: 0; transform: translateY(14px); }
  5%, 80% { opacity: 1; transform: translateY(0); }
  88%, 100% { opacity: 0; transform: translateY(0); }
}
@keyframes qkey { 0%,100% { opacity: .72; } 50% { opacity: 1; } }
@keyframes qbar { from { transform: scaleX(0); } to { transform: scaleX(1); } }
@keyframes qfloat { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-5px); } }
@keyframes qscan { from { transform: translateY(0); } to { transform: translateY(230px); } }
.qline { animation: qlineIn 18s ease-out infinite; animation-fill-mode: both; will-change: opacity, transform; }
.qkey { animation: qkey 2.6s ease-in-out infinite; }
.qbar { transform-box: fill-box; transform-origin: left; animation: qbar 1.4s ease-out 3.6s both; will-change: transform; }
.qfloat { animation: qfloat 6s ease-in-out infinite; will-change: transform; }
.qscan { animation: qscan 9s linear infinite; }
"""


def quote():
    w, h = 1200, 230
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Frase de Stan Lee sobre ideias, animada com diferentes fontes">
<defs>
<linearGradient id="qbg" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#04080f"/>
  <stop offset=".55" stop-color="#07121d"/>
  <stop offset="1" stop-color="#03070d"/>
</linearGradient>
<linearGradient id="qlineGrad" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{GOLD}" stop-opacity="0"/>
  <stop offset=".5" stop-color="{GOLD}" stop-opacity=".9"/>
  <stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
</linearGradient>
<radialGradient id="qvig" cx=".5" cy=".45" r=".8">
  <stop offset=".55" stop-color="#000" stop-opacity="0"/>
  <stop offset="1" stop-color="#000" stop-opacity=".4"/>
</radialGradient>
<pattern id="qscan" width="4" height="4" patternUnits="userSpaceOnUse">
  <rect width="4" height="1" fill="#000" opacity=".55"/>
</pattern>
<filter id="qblur" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="30"/></filter>
</defs>
<style>{QUOTE_CSS}</style>
<polygon points="0,16 16,0 1184,0 1200,16 1200,214 1184,230 16,230 0,214" fill="url(#qbg)" stroke="{GOLD}" stroke-opacity=".28" stroke-width="2.5"/>
<ellipse cx="600" cy="120" rx="430" ry="82" fill="{GOLD}" opacity=".05" filter="url(#qblur)"/>
<line x1="40" y1="42" x2="1160" y2="42" stroke="{GOLD}" stroke-opacity=".12"/>
<circle cx="40" cy="27" r="3.5" fill="{GOLD}"/>
<text x="54" y="31" font-family="ui-monospace, Consolas, monospace" font-size="10" letter-spacing="2.5" fill="{GOLD}" opacity=".85">// MINDSET</text>
<text x="1160" y="31" text-anchor="end" font-family="ui-monospace, Consolas, monospace" font-size="9" letter-spacing="2" fill="#7dd3fc" opacity=".6">KEEP CREATING</text>
<g class="qfloat" opacity=".12">
  <text x="48" y="118" font-family="Georgia, serif" font-size="140" fill="{GOLD}">“</text>
  <text x="1152" y="224" text-anchor="end" font-family="Georgia, serif" font-size="140" fill="{GOLD}">”</text>
</g>
<g class="qline" style="animation-delay:.2s">
  <text x="600" y="82" text-anchor="middle" font-family="Georgia, Times New Roman, serif" font-style="italic" font-size="31" fill="#eafcff">Se você tem uma ideia,</text>
</g>
<g class="qline" style="animation-delay:1.4s">
  <text x="600" y="128" text-anchor="middle" font-family="Trebuchet MS, Verdana, sans-serif" font-size="27" fill="#cfefff">que você<tspan dx="8" class="qkey" font-family="ui-monospace, Consolas, monospace" font-weight="700" fill="{CYAN}">genuinamente</tspan><tspan dx="8">acha boa,</tspan></text>
</g>
<g class="qline" style="animation-delay:2.6s">
  <text x="600" y="178" text-anchor="middle" font-family="Impact, Arial Black, sans-serif" font-weight="700" font-size="30" fill="{GOLD}" letter-spacing="1">não deixe ninguém<tspan dx="10" font-family="Georgia, serif" font-style="italic" font-weight="400" font-size="26" letter-spacing="0" fill="#eafcff">te convencer do contrário.</tspan></text>
  <rect class="qbar" x="360" y="190" width="480" height="2" fill="url(#qlineGrad)"/>
</g>
<g class="qline" style="animation-delay:3.4s">
  <text x="600" y="212" text-anchor="middle" font-family="ui-monospace, Consolas, monospace" font-size="10" letter-spacing="3" fill="{GOLD}" opacity=".8">— STAN LEE</text>
</g>
<rect class="qscan" x="0" y="0" width="1200" height="2" fill="{CYAN}" opacity=".1"/>
<rect width="1200" height="230" fill="url(#qscan)" opacity=".12"/>
<rect width="1200" height="230" fill="url(#qvig)"/>
<path d="M16 42V16h28M1156 16h28v26M1184 188v26h-28M44 214H16v-26" fill="none" stroke="{CYAN}" stroke-opacity=".38" stroke-width="2"/>
</svg>'''


def divider():
    w, h = 1200, 40
    ticks = "".join(rect(x, 19, 2, 2, CYAN, ' opacity=".22"') for x in range(80, 520, 56))
    ticks += "".join(rect(x, 19, 2, 2, CYAN, ' opacity=".22"') for x in range(680, 1120, 56))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="divisor">
<defs>
<linearGradient id="dl" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{CYAN}" stop-opacity="0"/>
  <stop offset="1" stop-color="{CYAN}" stop-opacity=".55"/>
</linearGradient>
<linearGradient id="dr" x1="1" y1="0" x2="0" y2="0">
  <stop offset="0" stop-color="{CYAN}" stop-opacity="0"/>
  <stop offset="1" stop-color="{CYAN}" stop-opacity=".55"/>
</linearGradient>
<filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="4"/></filter>
</defs>
<line x1="0" y1="20" x2="532" y2="20" stroke="url(#dl)" stroke-width="1.5"/>
<line x1="668" y1="20" x2="1200" y2="20" stroke="url(#dr)" stroke-width="1.5"/>
{ticks}
<polygon points="558,16 566,20 558,24 550,20" fill="{CYAN}" opacity=".6"/>
<polygon points="642,16 650,20 642,24 634,20" fill="{CYAN}" opacity=".6"/>
<polygon points="594,2 606,2 600,12 612,12 586,37 594,20 582,20" fill="{GOLD}" opacity=".95" filter="url(#glow)"/>
<polygon points="594,2 606,2 600,12 612,12 586,37 594,20 582,20" fill="{GOLD}"/>
<rect x="600" y="30" width="0" height="0" fill="none"/>
</svg>'''


def write(name, text, root=False):
    path = os.path.join(ROOT if root else ASSETS, name)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("wrote", name, len(text), "bytes")


if __name__ == "__main__":
    write("banner.svg", banner(), root=True)
    write("terminal.svg", terminal())
    write("quote.svg", quote())
    write("anime-shelf.svg", anime_shelf())
    write("divider.svg", divider())
    for old in ["creature.svg", "squad.svg", "hero.svg", "banner.svg"]:
        old_path = os.path.join(ASSETS, old)
        if os.path.exists(old_path):
            os.remove(old_path)
            print("removed assets/" + old)
    old_root = os.path.join(ROOT, "hero.svg")
    if os.path.exists(old_root):
        os.remove(old_root)
        print("removed hero.svg")


