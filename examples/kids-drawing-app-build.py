#!/usr/bin/env python3
"""Build the complete 3-screen Kids Drawing App with 100% reference fidelity."""
import json

# ---------------------------------------------------------------- palette
CREAM       = "#FDF8EE"
CANVAS_DOT  = "#EFE5D0"
HERO        = "#FFC83B"
HERO_DEEP   = "#F5A623"
HERO_SOFT   = "#FFD966"
ORANGE      = "#F59324"
ORANGE_HOT  = "#FF7A3D"
WHITE       = "#FFFFFF"
CANVAS      = "#FBF8F2"
INK         = "#18181B"
INK_SOFT    = "#9E988F"
BORDER      = "#F0E8D8"
CHIP        = "#F4F1EA"
TRACK       = "#EFEAE0"
GREEN       = "#34C759"
GREEN_NAV   = "#32B753"
GREEN_BTN   = "#00B862"
GREEN_GLOW  = "#00B86255"
RED         = "#FF4B4B"
RED_SOFT    = "#E2574C"
BLUE_WHALE  = "#1976D2"
BLUE_DARK   = "#0D47A1"
BLUE_FIN2   = "#1A4452"
BLUE_DEEP   = "#063D78"
BLUE_LT     = "#38BDF8"
PINK        = "#FF7B98"
PINK_LT     = "#FFA8BE"
PINK_BODY   = "#FFA0B6"
PINK_SHIRT  = "#FF2A7A"
LILAC       = "#C4B5FD"
PURPLE      = "#A855F7"
GOLD        = "#FBBF24"
GOLD_DARK   = "#D97706"
GOLD_STRIPE = "#F5A623"
LIME_SPOT   = "#84CC16"
BLACK       = "#18181B"
WOOD        = "#E8D5B5"
GILL_GREEN  = "#4ADE80"
BELLY_CREAM = "#FFFDF5"

ROUND = "SF Pro Rounded"

SHADOW_CARD = [{"type": "dropShadow", "color": "#B8965826", "offset": [0, 8], "radius": 20}]
SHADOW_SOFT = [{"type": "dropShadow", "color": "#B896581F", "offset": [0, 4], "radius": 12}]
SHADOW_NAV  = [{"type": "dropShadow", "color": "#9E7A382A", "offset": [0, -2], "radius": 16}]
SHADOW_POLA = [{"type": "dropShadow", "color": "#0000002A", "offset": [0, 10], "radius": 22}]

steps = []

def node(kind, name=None, parent=None, x=None, y=None, w=None, h=None,
         props=None, text=None, path=None, ref=None, index=None):
    params = {"type": kind}
    if name is not None:
        params["name"] = name
    if parent is not None:
        params["parent"] = {"$ref": parent} if isinstance(parent, str) else parent
    for key, val in (("x", x), ("y", y), ("width", w), ("height", h), ("index", index)):
        if val is not None:
            params[key] = val
    if text is not None:
        params["text"] = text
    if path is not None:
        params["path"] = path
    if props:
        params["props"] = props
    step = {"command": "node.create", "params": params}
    if ref:
        step["as"] = ref
    steps.append(step)
    return ref

def label(parent, x, y, text, size=12, style="Bold", color=INK, w=None,
          align=None, family=ROUND, name=None, rotation=None):
    props = {"fontFamily": family, "fontStyle": style, "fontSize": size, "fill": color}
    if align:
        props["textAlign"] = align
    if rotation is not None:
        props["rotation"] = rotation
    node("text", name or f"Text/{text[:20]}", parent, x, y, w, None, props, text=text)

def box(name, parent, x, y, w, h, fill, radius=0, stroke=None, weight=None,
        effects=None, ref=None, clip=None, rotation=None, opacity=None, extra=None):
    props = {"fill": fill}
    if radius:
        props["cornerRadius"] = radius
    if stroke:
        props["stroke"] = stroke
        props["strokeWeight"] = weight or 1.5
    if effects:
        props["effects"] = effects
    if clip is not None:
        props["clip"] = clip
    if rotation is not None:
        props["rotation"] = rotation
    if opacity is not None:
        props["opacity"] = opacity
    if extra:
        props.update(extra)
    return node("frame", name, parent, x, y, w, h, props, ref=ref)

def rect(name, parent, x, y, w, h, fill, radius=0, rotation=None, opacity=None,
         stroke=None, weight=None):
    props = {"fill": fill}
    if radius:
        props["cornerRadius"] = radius
    if rotation is not None:
        props["rotation"] = rotation
    if opacity is not None:
        props["opacity"] = opacity
    if stroke:
        props["stroke"] = stroke
        props["strokeWeight"] = weight or 1.5
    node("rectangle", name, parent, x, y, w, h, props)

def oval(name, parent, x, y, w, h, fill, stroke=None, weight=None, opacity=None,
         rotation=None):
    props = {"fill": fill}
    if stroke:
        props["stroke"] = stroke
        props["strokeWeight"] = weight or 2
    if opacity is not None:
        props["opacity"] = opacity
    if rotation is not None:
        props["rotation"] = rotation
    node("ellipse", name, parent, x, y, w, h, props)

def ring(name, parent, x, y, size, color, weight=3.5):
    node("ellipse", name, parent, x, y, size, size,
         {"fill": "none", "stroke": color, "strokeWeight": weight})

def vec(name, parent, path, x, y, w, h, fill, stroke=None, weight=None, strokeCap=None, rotation=None, opacity=None):
    props = {"fill": fill}
    if stroke:
        props["stroke"] = stroke
        props["strokeWeight"] = weight or 2
    if strokeCap:
        props["strokeCap"] = strokeCap
    if rotation is not None:
        props["rotation"] = rotation
    if opacity is not None:
        props["opacity"] = opacity
    node("vector", name, parent, x, y, w, h, props, path=path)

def star(name, parent, x, y, size, fill, points=5, inner=0.45, rotation=None,
         stroke=None, weight=None):
    props = {"fill": fill, "pointCount": points, "innerRadius": inner}
    if rotation is not None:
        props["rotation"] = rotation
    if stroke:
        props["stroke"] = stroke
        props["strokeWeight"] = weight or 2
    node("star", name, parent, x, y, size, size, props)

def row(name, parent, x, y, w, h=None, gap=10, pad=0, main="spaceBetween",
        cross="center", fill="none", radius=0, ref=None, vertical=False,
        sizing_h="fixed", sizing_v="fixed", stroke=None, effects=None):
    props = {
        "fill": fill,
        "layout": "vertical" if vertical else "horizontal",
        "gap": gap,
        "padding": pad,
        "mainAlign": main,
        "crossAlign": cross,
        "sizingH": sizing_h,
        "sizingV": sizing_v,
    }
    if radius:
        props["cornerRadius"] = radius
    if stroke:
        props["stroke"] = stroke
        props["strokeWeight"] = 1.5
    if effects:
        props["effects"] = effects
    return node("frame", name, parent, x, y, w, h, props, ref=ref)

# ---------------------------------------------------------------- glyph paths
P_BELL   = "M12 2a6 6 0 0 0-6 6v4.2L3.8 15.6h16.4L18 12.2V8a6 6 0 0 0-6-6zm0 19.5a3.1 3.1 0 0 0 3-2.4H9a3.1 3.1 0 0 0 3 2.4z"
P_BACK   = "M15.2 3.4L6.1 12l9.1 8.6 2.3-2.4L10.8 12l6.7-6.2z"
P_CHECK  = "M3.6 11.8l2.4-2.4 3.2 3.2 8.8-8.8 2.4 2.4-11.2 11.2z"
P_PLUS   = "M10.8 3.6h2.4v7.2h7.2v2.4h-7.2v7.2h-2.4v-7.2H3.6v-2.4h7.2z"
P_HOUSE  = "M12 2.6l9.4 8.4h-3.1v10.4h-4.6v-6.4h-3.4v6.4H5.7V11H2.6z"
P_SPARK  = "M12 1.8l2.4 6.6 6.6 2.4-6.6 2.4L12 19.8l-2.4-6.6L3 10.8l6.6-2.4z"
P_CAR    = "M2.6 12.2l2.6-5.4h13.6l2.6 5.4v4H2.6z"
P_BARS   = "M3.4 13h4v8h-4zm6.6-5h4v13h-4zm6.6-4h4v17h-4z"
P_PLANE  = "M2.4 11.4L21.6 3.2l-6.4 18.4-3.6-6.4-6.4-1.6z"
P_FLAME  = "M12 1.8c3.2 3.6 1.4 5.8.4 7.4-1.2 1.9 0 4 2 4 1.9 0 3-1.5 3-3.4 2.4 2.6 2.6 5.4 1.4 7.6-1.6 3-5 4.8-6.8 4.8s-5.2-1.4-6.8-4.4C3.4 14.6 4.6 9.4 8 7.4c-.6 2.6.6 3.8 1.6 3.8 1.4 0 2.4-1.2 1.8-3.2-.6-2 .2-4.4.6-6.2z"
P_BOLT   = "M13.6 1.8L4.4 13.6h5.2l-1.6 8.6 9.6-12.4h-5.4z"
P_REDO   = "M12 4.2V1.4l5.4 4.2-5.4 4.2V7a5.4 5.4 0 1 0 5.2 6.8h2.6A8 8 0 1 1 12 4.2z"
P_CLIP   = "M14.6 3.4a3.4 3.4 0 0 1 4.8 4.8l-9 9a5.6 5.6 0 0 1-7.9-7.9l8-8 1.8 1.8-8 8a3 3 0 0 0 4.3 4.3l9-9a.9.9 0 0 0-1.2-1.2l-8.4 8.4-1.8-1.8z"
P_RAINBOW_1 = "M0 30A30 30 0 0 1 60 30h-9A21 21 0 0 0 9 30z"
P_RAINBOW_2 = "M11 30A19 19 0 0 1 49 30h-9A10 10 0 0 0 20 30z"
P_CORAL     = "M10 40c0-8-6-10-6-16 0-4 3-6 6-6s6 2 6 6c0 6-6 8-6 16z"
P_SOLID_ARROW = "M 18 8 L 18 14 L 10 14 L 14 18 L 10 21 L 2 11 L 10 1 L 14 4 L 10 8 Z"

# ---------------------------------------------------------------- complex assets
def trophy(parent, x, y, scale=1.0, name="Trophy"):
    g = box(name, parent, x, y, 24 * scale, 24 * scale, "none", ref=f"{name}-{int(x)}-{int(y)}")
    s = scale
    vec("RibbonL", g, "M0 0 L5 12 L10 0 Z", 3 * s, 11 * s, 7 * s, 12 * s, "#1E88E5", rotation=-14)
    vec("RibbonR", g, "M0 0 L5 12 L10 0 Z", 14 * s, 11 * s, 7 * s, 12 * s, "#1E88E5", rotation=14)
    rect("Base", g, 7 * s, 18 * s, 10 * s, 4 * s, GOLD_DARK, radius=1)
    rect("Stem", g, 10.5 * s, 13 * s, 3 * s, 6 * s, GOLD)
    vec("Cup", g, "M0 0 C0 8, 4 12, 10 12 C16 12, 20 8, 20 0 Z", 2 * s, 3 * s, 20 * s, 12 * s, GOLD)
    ring("HandleL", g, 0 * s, 4 * s, 6 * s, GOLD, weight=1.6 * s)
    ring("HandleR", g, 18 * s, 4 * s, 6 * s, GOLD, weight=1.6 * s)
    return g

def pencil_giant(parent, x, y, length=200, rotation=22, name="GiantPencil"):
    g = box(name, parent, x, y, length, 36, "none", rotation=rotation, ref=f"{name}-{int(x)}")
    rect("Eraser", g, 0, 4, 22, 28, "#FF8DA1", radius=[6, 0, 0, 6])
    rect("Ferrule", g, 22, 4, 12, 28, "#B0BEC5")
    rect("ShaftTop", g, 34, 4, length - 74, 9, "#FDD835")
    rect("ShaftMid", g, 34, 13, length - 74, 10, "#FBC02D")
    rect("ShaftBot", g, 34, 23, length - 74, 9, "#F57F17")
    vec("Wood", g, "M0 0 L26 14 L0 28 Z", length - 40, 4, 26, 28, WOOD)
    vec("Lead", g, "M0 0 L10 5 L0 10 Z", length - 14, 13, 10, 10, BLACK)
    return g

def axolotl_cute(parent, x, y, scale=1.0, pose="sitting", with_pencil=False, name="Mascot"):
    w_box = 150 * scale
    h_box = 145 * scale
    g = box(name, parent, x, y, w_box, h_box, "none", ref=f"{name}-{int(x)}-{int(y)}")
    s = scale

    for i, (gx, gy, rot) in enumerate(((6, 22, -22), (0, 40, -6), (8, 58, 16))):
        oval(f"GillL_Base_{i}", g, gx * s, gy * s, 26 * s, 14 * s, PINK, rotation=rot)
        oval(f"GillL_Tip_{i}", g, (gx - 2) * s, (gy + 2) * s, 12 * s, 10 * s, GILL_GREEN, rotation=rot)
    for i, (gx, gy, rot) in enumerate(((112, 22, 22), (118, 40, 6), (110, 58, -16))):
        oval(f"GillR_Base_{i}", g, gx * s, gy * s, 26 * s, 14 * s, PINK, rotation=rot)
        oval(f"GillR_Tip_{i}", g, (gx + 16) * s, (gy + 2) * s, 12 * s, 10 * s, GILL_GREEN, rotation=rot)

    oval("FootL", g, 38 * s, 114 * s, 24 * s, 16 * s, PINK_LT)
    oval("FootR", g, 84 * s, 114 * s, 24 * s, 16 * s, PINK_LT)
    
    rect("ShortsL", g, 40 * s, 100 * s, 32 * s, 20 * s, LILAC, radius=[4, 4, 10, 10])
    rect("ShortsR", g, 74 * s, 100 * s, 32 * s, 20 * s, LILAC, radius=[4, 4, 10, 10])
    rect("Shirt", g, 38 * s, 70 * s, 70 * s, 38 * s, PINK_SHIRT, radius=[18, 18, 8, 8])

    if pose == "waving_left":
        vec("ArmL", g, "M 28 20 C 14 18, 0 8, 2 0 C 4 -6, 18 2, 34 10 Z", 6 * s, 70 * s, 36 * s, 26 * s, PINK_LT, rotation=15)
        oval("HandL", g, 2 * s, 68 * s, 18 * s, 18 * s, PINK_LT)
        oval("ArmR", g, 104 * s, 78 * s, 20 * s, 24 * s, PINK_LT, rotation=-15)
    elif with_pencil:
        oval("HandL", g, 34 * s, 86 * s, 18 * s, 16 * s, PINK_LT)
        oval("HandR", g, 94 * s, 86 * s, 18 * s, 16 * s, PINK_LT)
    else:
        oval("ArmL", g, 26 * s, 74 * s, 18 * s, 22 * s, PINK_LT, rotation=20)
        oval("ArmR", g, 102 * s, 74 * s, 18 * s, 22 * s, PINK_LT, rotation=-20)

    oval("Head", g, 30 * s, 14 * s, 86 * s, 68 * s, PINK_LT)
    oval("CheekL", g, 36 * s, 52 * s, 18 * s, 12 * s, PINK, opacity=0.85)
    oval("CheekR", g, 92 * s, 52 * s, 18 * s, 12 * s, PINK, opacity=0.85)
    
    oval("EyeL", g, 50 * s, 34 * s, 11 * s, 13 * s, BLACK)
    oval("EyeR", g, 84 * s, 34 * s, 11 * s, 13 * s, BLACK)
    oval("GlintL", g, 53 * s, 36 * s, 4.5 * s, 4.5 * s, WHITE)
    oval("GlintR", g, 87 * s, 36 * s, 4.5 * s, 4.5 * s, WHITE)

    m = box("MouthFrame", g, 58 * s, 48 * s, 30 * s, 22 * s, "#881337", radius=[4, 4, 15, 15], clip=True, ref=f"mouth-{int(x)}-{int(y)}")
    rect("Tooth", m, 11 * s, 0, 8 * s, 5 * s, WHITE, radius=2)
    oval("Tongue", m, 5 * s, 11 * s, 20 * s, 14 * s, "#FF7B98")

    return g

def build_whale_drawing(parent, x, y, scale=1.0, name="WhaleArt"):
    """Accurate Cartoon Blue Whale from reference."""
    s = scale
    g = box(name, parent, x, y, 270 * s, 240 * s, "none", ref=f"{name}-{int(x)}")

    # Doodle rings
    ring("Doodle/Purple", g, 150 * s, 10 * s, 24 * s, "#C084FC", weight=3.8 * s)
    ring("Doodle/Cyan", g, 212 * s, 38 * s, 14 * s, "#06B6D4", weight=3.0 * s)
    ring("Doodle/Coral", g, 16 * s, 165 * s, 26 * s, "#FB7185", weight=4.5 * s)

    # Rear Fin
    P_REAR_FIN = "M 0 0 C 14 10, 26 24, 22 40 C 10 40, -2 24, 0 0 Z"
    vec("RearFin", g, P_REAR_FIN, 174 * s, 134 * s, 26 * s, 40 * s, BLUE_FIN2)

    # Whale Body
    P_WHALE = (
        "M 226 72 "
        "C 226 36, 188 16, 144 16 "
        "C 102 16, 74 38, 50 36 "
        "C 34 34, 22 18, 10 6 "
        "C 8 20, 16 38, 28 48 "
        "C 16 52, 10 68, 14 82 "
        "C 24 76, 36 64, 48 56 "
        "C 56 86, 88 120, 134 124 "
        "C 174 128, 208 114, 224 96 "
        "C 226 88, 226 80, 226 72 Z"
    )
    vec("WhaleBody", g, P_WHALE, 14 * s, 14 * s, 226 * s, 124 * s, BLUE_WHALE)

    # Lime Green Highlights on Tail Flukes
    vec("TailMark1", g, "M 0 0 L 2 10", 34 * s, 34 * s, 3 * s, 10 * s, "none", stroke=LIME_SPOT, weight=2.8 * s, strokeCap="round")
    vec("TailMark2", g, "M 0 0 L 2 10", 42 * s, 38 * s, 3 * s, 10 * s, "none", stroke=LIME_SPOT, weight=2.8 * s, strokeCap="round")
    vec("TailMark3", g, "M 0 0 L 2 10", 78 * s, 46 * s, 3 * s, 10 * s, "none", stroke=LIME_SPOT, weight=2.8 * s, strokeCap="round")
    vec("TailMark4", g, "M 0 0 L 2 10", 88 * s, 44 * s, 3 * s, 10 * s, "none", stroke=LIME_SPOT, weight=2.8 * s, strokeCap="round")

    # Cream Underbelly with Golden Radiating Stripes
    P_BELLY_SHAPE = "M 4 0 C 30 10, 52 26, 54 44 C 44 52, 22 52, 0 40 C 2 26, 4 12, 4 0 Z"
    vec("BellyBase", g, P_BELLY_SHAPE, 168 * s, 78 * s, 54 * s, 52 * s, BELLY_CREAM, stroke=BLUE_DARK, weight=2.2 * s)
    vec("BellyStripe1", g, "M 0 18 L 22 0", 176 * s, 88 * s, 22 * s, 18 * s, "none", stroke=GOLD_STRIPE, weight=3.5 * s, strokeCap="round")
    vec("BellyStripe2", g, "M 0 24 L 28 0", 182 * s, 90 * s, 28 * s, 24 * s, "none", stroke=GOLD_STRIPE, weight=4.5 * s, strokeCap="round")
    vec("BellyStripe3", g, "M 0 16 L 20 0", 196 * s, 100 * s, 20 * s, 16 * s, "none", stroke=GOLD_STRIPE, weight=3.5 * s, strokeCap="round")

    # Front Pectoral Fin
    P_FRONT_FIN = "M 2 0 C 8 18, 12 40, 14 56 C 6 58, -2 42, 0 0 Z"
    vec("FrontFin", g, P_FRONT_FIN, 134 * s, 94 * s, 16 * s, 58 * s, BLUE_WHALE, stroke=BLUE_DARK, weight=2.5 * s)

    # Two Cute Bead Eyes
    oval("EyeL", g, 172 * s, 54 * s, 6.5 * s, 9.5 * s, INK, rotation=10)
    oval("EyeR", g, 189 * s, 52 * s, 6.5 * s, 9.5 * s, INK)

    # Smile with dimple tick
    P_SMILE = "M 88 12 C 64 22, 22 16, 4 8 C 0 5, 2 0, 5 0"
    vec("Smile", g, P_SMILE, 142 * s, 64 * s, 88 * s, 18 * s, "none", stroke=INK, weight=4.2 * s, strokeCap="round")

    # Hand-drawn "WHALE" Text (Vector glyphs)
    whale_text = box("WhaleLetters", g, 65 * s, 180 * s, 140 * s, 30 * s, "none", ref=f"whale_letters-{int(x)}")
    P_W = "M 4 2 L 7 22 L 12 10 L 16 22 L 19 2 L 24 2 L 19 26 L 14 26 L 11 14 L 8 26 L 3 26 L 0 2 Z"
    P_H = "M 0 2 L 5.5 2 L 5.5 11 L 13.5 11 L 13.5 2 L 19 2 L 19 26 L 13.5 26 L 13.5 16.5 L 5.5 16.5 L 5.5 26 L 0 26 Z"
    P_A = "M 8 2 L 14 2 L 22 26 L 16.5 26 L 14.5 19.5 L 6.5 19.5 L 5 26 L 0 26 Z M 8.5 14 L 13 14 L 11 7 Z"
    P_L = "M 0 2 L 5.5 2 L 5.5 20.5 L 17 20.5 L 17 26 L 0 26 Z"
    P_E = "M 0 2 L 20 2 L 20 7.5 L 5.5 7.5 L 5.5 11.5 L 17 11.5 L 17 16.5 L 5.5 16.5 L 5.5 20.5 L 21 20.5 L 21 26 L 0 26 Z"

    vec("Letter_W", whale_text, P_W, 0 * s, 0, 24 * s, 26 * s, INK)
    vec("Letter_H", whale_text, P_H, 29 * s, 0, 19 * s, 26 * s, INK)
    vec("Letter_A", whale_text, P_A, 53 * s, 0, 22 * s, 26 * s, INK)
    vec("Letter_L", whale_text, P_L, 80 * s, 0, 17 * s, 26 * s, INK)
    vec("Letter_E", whale_text, P_E, 102 * s, 0, 21 * s, 26 * s, INK)
    return g

# ================================================================ screen 1 (Home)
S1 = "S1"
box("Screen/1 - Home", None, 0, 0, 390, 844, WHITE, radius=40, clip=True, ref=S1)

box("Hero", S1, 0, 0, 390, 305, HERO, radius=[40, 40, 36, 36], clip=True, ref="hero")
oval("Hero/Cheese1", "hero", 10, 110, 60, 60, HERO_DEEP, opacity=0.45)
oval("Hero/Cheese2", "hero", 44, 165, 42, 42, HERO_DEEP, opacity=0.4)
oval("Hero/Cheese3", "hero", 6, 195, 48, 48, HERO_DEEP, opacity=0.35)
rect("Hero/Paper1", "hero", 300, 186, 42, 48, "#FDE7B4", radius=6, rotation=-14, opacity=0.9)
rect("Hero/Paper2", "hero", 326, 212, 32, 36, "#FFF2CF", radius=5, rotation=12, opacity=0.9)

oval("Avatar/Ring", S1, 24, 44, 48, 48, "#FFF3DA")
oval("Avatar/Cookie", S1, 31, 51, 34, 34, "#E3A765")
for i, (ax, ay) in enumerate(((38, 60), (48, 56), (52, 68), (41, 71))):
    oval(f"Avatar/Chip{i}", S1, ax, ay, 6, 6, "#7A4A22")
label(S1, 84, 46, "Hi,", size=12, style="Medium", color="#A8792B")
label(S1, 84, 62, "Tiffany", size=19, style="Bold", color="#3A2D14")

box("Button/Bell", S1, 318, 44, 48, 48, WHITE, radius=18, effects=SHADOW_SOFT, ref="bell")
vec("Icon/Bell", "bell", P_BELL, 13, 12, 22, 24, HERO_DEEP)
oval("Bell/OrangeDot", "bell", 30, 8, 10, 10, ORANGE_HOT)

pencil_giant(S1, 70, 220, length=210, rotation=22, name="HeroPencil")
axolotl_cute(S1, 76, 134, scale=1.05, pose="sitting", with_pencil=True, name="Character/Axolotl-Hero")

box("Bubble", S1, 224, 130, 136, 64, WHITE, radius=20, effects=SHADOW_SOFT, ref="bubble")
label("bubble", 18, 12, "Let's start", size=14, style="Bold", color="#3A2D14")
label("bubble", 18, 32, "Drawing!", size=14, style="Bold", color="#3A2D14")
vec("Bubble/Tail", S1, "M0 0 L16 4 L4 14 Z", 212, 168, 16, 14, WHITE)

box("Card/Progress", S1, 24, 260, 342, 96, WHITE, radius=24, effects=SHADOW_CARD, ref="prog")
label("prog", 20, 20, "Little Artist", size=15, style="Bold")
trophy("prog", 112, 16, scale=1.0, name="ProgTrophy")
label("prog", 240, 22, "History  ›", size=12, style="Medium", color=INK_SOFT)
rect("Progress/Track", "prog", 20, 52, 228, 14, TRACK, radius=7)
rect("Progress/Fill", "prog", 20, 52, 116, 14, GREEN, radius=7)
label("prog", 254, 53, "13/40", size=11, style="Medium", color=INK_SOFT)
box("Pill/Lv1", "prog", 294, 48, 46, 24, BLACK, radius=12, ref="lv1")
label("lv1", 10, 6, "Lv 1", size=11, style="Bold", color=WHITE)

CATS = [
    ("Animals", "#FDE3C7", "cat"),
    ("Cars", "#D9ECFA", "car"),
    ("Flowers", "#FBE8CF", "flower"),
    ("Magic", "#EDE3FB", "magic"),
    ("More", "#F1EFE8", "more"),
]
row("Row/Categories", S1, 24, 372, 342, 78, gap=12, main="spaceBetween", cross="min", ref="cats")
for cname, tint, glyph in CATS:
    cell = row(f"Cat/{cname}", "cats", None, None, None, gap=8, main="min", cross="center", vertical=True, sizing_h="hug", sizing_v="hug", ref=f"cat-{cname}")
    disc = box(f"Cat/{cname}/Disc", cell, None, None, 56, 56, tint, radius=28, ref=f"disc-{cname}")
    if glyph == "cat":
        vec("Cat/EarL", disc, "M0 13L5 0l10 8z", 13, 11, 14, 13, "#F0A64E")
        vec("Cat/EarR", disc, "M15 13L10 0 0 8z", 29, 11, 14, 13, "#F0A64E")
        oval("Cat/Face", disc, 14, 18, 28, 25, "#F7B968")
        oval("Cat/EyeL", disc, 21, 26, 4, 5, INK)
        oval("Cat/EyeR", disc, 31, 26, 4, 5, INK)
        oval("Cat/Nose", disc, 26, 33, 4, 3, "#D97F3C")
    elif glyph == "car":
        rect("Car/Roof", disc, 20, 15, 17, 10, "#7FC0EC", radius=[5, 5, 0, 0])
        vec("Car/Body", disc, P_CAR, 12, 23, 32, 14, "#4A95D9")
        oval("Car/WheelL", disc, 17, 33, 9, 9, "#23527D")
        oval("Car/WheelR", disc, 30, 33, 9, 9, "#23527D")
    elif glyph == "flower":
        for i, (px, py) in enumerate(((23, 11), (33, 20), (23, 29), (13, 20))):
            oval(f"Flower/Petal{i}", disc, px, py, 12, 12, "#F7C948")
        oval("Flower/Core", disc, 23, 20, 11, 11, "#E58A2E")
        rect("Flower/Stem", disc, 27, 30, 3, 14, "#5BA85C", radius=2)
    elif glyph == "magic":
        vec("Magic/Spark", disc, P_SPARK, 13, 14, 28, 28, PURPLE)
        oval("Magic/Dot", disc, 36, 16, 7, 7, "#C9B2F2")
    else:
        vec("More/Spark", disc, P_SPARK, 15, 15, 26, 26, "#B5AFA3")
    label(cell, None, None, cname, size=11, style="Medium", color="#6E6A63")

label(S1, 24, 464, "Daily challenges", size=15, style="Bold")
for i, (dx, dy) in enumerate(((306, 468), (314, 468), (306, 476), (314, 476))):
    rect(f"Grid/Dot{i}", S1, dx, dy, 6, 6, "#C9C3B8", radius=2)
box("Button/AddChallenge", S1, 332, 460, 30, 30, GREEN, radius=15, ref="addbtn")
vec("Icon/Plus", "addbtn", P_PLUS, 7, 7, 16, 16, WHITE)

CHALLENGES = [
    ("Imagine a Whale!", "Magic animal", "7", "#FBD96B", "whale"),
    ("Let's Draw a Rainbow!", "Nature", "10", "#BFE3F5", "rainbow"),
]
row("List/Challenges", S1, 24, 498, 342, None, gap=12, vertical=True, main="min", cross="min", sizing_v="hug", ref="list")
for title, sub, energy, tint, glyph in CHALLENGES:
    card = row(f"Card/{title[:12]}", "list", None, None, 342, 70, gap=12, pad=[12, 14, 12, 14], main="min", cross="center", fill=WHITE, radius=20, stroke=BORDER, ref=f"card-{glyph}")
    disc = box("Icon/Disc", card, None, None, 44, 44, tint, radius=22, ref=f"cd-{glyph}")
    if glyph == "whale":
        # Mini cartoon whale matching the main whale
        vec("MiniWhaleBody", disc, "M 2 12 C 2 4, 14 0, 26 0 C 34 0, 38 4, 40 8 C 32 10, 26 14, 20 14 C 12 14, 2 13, 2 12 Z", 4, 15, 36, 14, BLUE_WHALE)
        oval("MiniWhaleBelly", disc, 24, 21, 10, 7, BELLY_CREAM)
        oval("MiniWhaleEye", disc, 32, 18, 2.5, 3, INK)
    else:
        vec("Mini/Arc1", disc, P_RAINBOW_1, 7, 14, 30, 16, "#F2705B")
        vec("Mini/Arc2", disc, P_RAINBOW_2, 12, 19, 20, 11, "#5BBCE4")
    txt = row("Text", card, None, None, None, None, gap=3, vertical=True, main="min", cross="min", sizing_h="fill", sizing_v="hug", ref=f"tx-{glyph}")
    label(txt, None, None, title, size=13.5, style="Bold")
    label(txt, None, None, sub, size=11, style="Medium", color=INK_SOFT)
    meta = row("Meta", card, None, None, None, None, gap=8, main="min", cross="center", sizing_h="hug", sizing_v="hug", ref=f"mt-{glyph}")
    label(meta, None, None, energy, size=12, style="Bold", color=ORANGE_HOT)
    vec("Icon/Bolt", meta, P_BOLT, None, None, 12, 15, GOLD)
    chk = box("Check", meta, None, None, 36, 36, "#FFF6E0", radius=13, stroke="#F5C95C", ref=f"ck-{glyph}")
    vec("Icon/Check", chk, P_CHECK, 9, 10, 18, 16, "#F0A32B")

box("Card/FlyingCar", S1, 24, 662, 342, 70, WHITE, radius=20, stroke=BORDER, ref="card3")
box("Icon/Disc3", "card3", 14, 13, 44, 44, "#FBC9A4", radius=22, ref="cd3")
rect("Mini/CarCabin", "cd3", 15, 12, 15, 11, "#F7A07A", radius=[6, 6, 0, 0])
rect("Mini/CarWindow", "cd3", 18, 15, 10, 6, WHITE, radius=2, opacity=0.85)
rect("Mini/CarBody", "cd3", 7, 21, 30, 11, "#E8743F", radius=5)
oval("Mini/CarWheelL", "cd3", 11, 28, 8, 8, "#A84B22")
oval("Mini/CarWheelR", "cd3", 25, 28, 8, 8, "#A84B22")
label("card3", 70, 22, "Invent a Flying Car!", size=13.5, style="Bold")

row("Nav/Bar", S1, 16, 752, 358, 70, gap=0, pad=[10, 26, 10, 26], main="spaceBetween", cross="center", fill=WHITE, radius=28, effects=SHADOW_NAV, ref="nav")
for nname, glyph, active in (("Home", P_HOUSE, True), ("Stars", None, False), ("Ranks", P_BARS, False)):
    tint = GREEN_NAV if active else "#C9C3B8"
    cell = row(f"Nav/{nname}", "nav", None, None, None, None, gap=5, vertical=True, main="min", cross="center", sizing_h="hug", sizing_v="hug", ref=f"nav-{nname}")
    if glyph:
        vec(f"Nav/{nname}/Icon", cell, glyph, None, None, 25, 25, tint)
    else:
        star(f"Nav/{nname}/Icon", cell, None, None, 25, tint, inner=0.45)
    label(cell, None, None, nname, size=11, style="Bold", color=GREEN_NAV if active else "#A8A29A")

# ================================================================ screen 2 (Draw Screen - NEW & EXACT)
S2 = "S2"
box("Screen/2 - Draw", None, 470, 0, 390, 844, CANVAS, radius=40, clip=True, ref=S2)

box("Canvas/DotGrid", S2, 0, 0, 390, 844, "none", ref="dotgrid2")
for gx in range(0, 11):
    for gy in range(0, 18):
        oval(f"Dot2/{gx}-{gy}", "dotgrid2", 20 + gx * 35, 100 + gy * 35, 3.2, 3.2, "#E8DFD0", opacity=0.8)

# Header
box("Button/Back2", S2, 24, 44, 48, 48, HERO_DEEP, radius=18, ref="back2")
vec("Icon/BackArrow2", "back2", P_SOLID_ARROW, 14, 13, 20, 22, "#4A3200")

row("Pill/Title2", S2, 86, 44, 218, 48, gap=8, pad=[4, 14, 4, 10], main="min", cross="center", fill=WHITE, radius=24,
    effects=[{"type": "dropShadow", "color": "#00000012", "offset": [0, 4], "radius": 12}], ref="title2")

m2 = box("MiniMascot2", "title2", None, None, 44, 38, "none", ref="minimascot2")
vec("MiniWand2", m2, "M 2 16 L 16 2", 2, 8, 14, 14, "none", stroke="#F59E0B", weight=2.2)
star("MiniStar2", m2, 12, 4, 11, "#FBBF24", points=4, inner=0.42)
oval("MGillL1_2", m2, 10, 14, 8, 5, "#FF7B98", rotation=-20)
oval("MGillL2_2", m2, 8, 20, 8, 5, "#FF7B98", rotation=0)
oval("MGillR1_2", m2, 34, 14, 8, 5, "#FF7B98", rotation=20)
oval("MGillR2_2", m2, 36, 20, 8, 5, "#FF7B98", rotation=0)
rect("MBody2", m2, 19, 24, 16, 12, "#FF2A7A", radius=[4, 4, 2, 2])
oval("MHead2", m2, 15, 10, 24, 19, "#FFA8BE")
oval("MEyeL2", m2, 20, 15, 2.5, 3.2, INK)
oval("MEyeR2", m2, 28, 15, 2.5, 3.2, INK)
vec("MMouth2", m2, "M 21 22 C 23 25, 27 25, 29 22", 19, 21, 10, 5, "#881337", stroke="#881337", weight=1.5)
label("title2", None, None, "Draw a Whale", size=15, style="Bold", color=INK)

box("Button/Trash2", S2, 318, 44, 48, 48, RED, radius=18, ref="trash2")
rect("TrashLid2", "trash2", 14, 14, 20, 4, WHITE, radius=2)
rect("TrashHandle2", "trash2", 21, 11, 6, 4, WHITE, radius=[2, 2, 0, 0])
rect("TrashBody2", "trash2", 16, 19, 16, 17, WHITE, radius=[0, 0, 4, 4])
rect("TrashRib1_2", "trash2", 19, 23, 2, 9, RED, radius=1)
rect("TrashRib2_2", "trash2", 23, 23, 2, 9, RED, radius=1)
rect("TrashRib3_2", "trash2", 27, 23, 2, 9, RED, radius=1)

# Exact Whale Drawing
build_whale_drawing(S2, 60, 270, scale=1.0, name="WhaleArt2")

# Transform button
btn2 = box("Button/Transform2", S2, 115, 565, 160, 48, GREEN_BTN, radius=24,
           effects=[{"type": "dropShadow", "color": GREEN_GLOW, "offset": [0, 6], "radius": 16}], ref="transform_btn2")
label("transform_btn2", 22, 14, "Transform!", size=15, style="Bold", color=WHITE)
star("TransformSpark1_2", "transform_btn2", 118, 16, 14, WHITE, points=4, inner=0.45)
star("TransformSpark2_2", "transform_btn2", 134, 24, 9, WHITE, points=4, inner=0.45)

# Toolbar
tb2 = box("Toolbar2", S2, 20, 650, 350, 170, WHITE, radius=36,
          effects=[{"type": "dropShadow", "color": "#00000014", "offset": [0, 8], "radius": 24}], ref="toolbar2")

swatches_row2 = row("Row/Swatches2", "toolbar2", 16, 18, 318, 32, gap=6, main="spaceBetween", cross="center", ref="swatches2")
PALETTE2 = [
    ("#18181B", False),
    ("#38BDF8", True),
    ("#FF8DA1", False),
    ("#A855F7", False),
    ("#F5EBE1", False),
    ("#0D6832", False),
    ("#A7F3D0", False),
    ("#EF4444", False),
    ("#F97316", False),
    ("#FBBF24", False),
]
for i, (color, is_selected) in enumerate(PALETTE2):
    sw_box = box(f"SwatchBox2/{i}", "swatches2", None, None, 26, 26, "none", ref=f"swbox2-{i}")
    if is_selected:
        ring("RingSelected2", sw_box, 0, 0, 26, "#BAE6FD", weight=2)
        oval("SwatchCircle2", sw_box, 3, 3, 20, 20, color)
    else:
        oval("SwatchCircle2", sw_box, 1, 1, 24, 24, color, stroke="#E7E5E4" if color == "#F5EBE1" else None, weight=1)

tray2 = box("Tray/Tools2", "toolbar2", 14, 58, 322, 94, HERO_DEEP, radius=28, ref="tray2")
slots_row2 = row("Slots2", "tray2", 10, 8, 302, 78, gap=8, main="spaceBetween", cross="center", ref="slots2")

# Slot 1: Paintbrush
s1_2 = box("Slot/Brush2", "slots2", None, None, 68, 76, WHITE, radius=22, ref="slot_brush2")
rect("BrushHandle2", s1_2, 30, 42, 8, 22, "#D97706", radius=[2, 2, 4, 4])
rect("BrushFerrule2", s1_2, 28, 36, 12, 6, "#94A3B8", radius=1)
vec("BrushBristle2", s1_2, "M 0 20 C -4 14, -6 6, 0 0 C 6 6, 4 14, 0 20 Z", 34, 16, 16, 20, "#334155")

# Slot 2: Pencil
s2_2 = box("Slot/Pencil2", "slots2", None, None, 68, 76, WHITE, radius=22, ref="slot_pencil2")
rect("PencilBody2", s2_2, 27, 36, 14, 28, "#F59E0B", radius=[2, 2, 4, 4])
rect("PencilStripe2", s2_2, 32, 36, 4, 28, "#FCD34D")
vec("PencilWood2", s2_2, "M 0 16 L 7 0 L 14 16 Z", 27, 20, 14, 16, "#FDE68A")
vec("PencilLead2", s2_2, "M 0 6 L 4 0 L 8 6 Z", 30, 20, 8, 6, "#1E293B")

# Slot 3: Crayon/Marker (ACTIVE)
s3_2 = box("Slot/Marker2", "slots2", None, None, 68, 76, "#FEF3C7", radius=22, ref="slot_marker2")
rect("MarkerBody2", s3_2, 27, 34, 14, 34, "#1E293B", radius=[2, 2, 4, 4])
rect("MarkerCapBand2", s3_2, 26, 30, 16, 5, "#334155", radius=1)
vec("MarkerTip2", s3_2, "M 0 14 L 6 0 L 12 14 Z", 28, 16, 12, 14, "#0F172A")

# Slot 4: Eraser
s4_2 = box("Slot/Eraser2", "slots2", None, None, 68, 76, WHITE, radius=22, ref="slot_eraser2")
er2 = box("EraserTilted2", s4_2, 18, 18, 32, 42, "none", rotation=30, ref="er_tilted2")
rect("EraserBlue2", er2, 0, 0, 30, 16, "#0284C7", radius=[4, 4, 0, 0])
rect("EraserWhite2", er2, 0, 16, 30, 8, WHITE)
rect("EraserPink2", er2, 0, 24, 30, 18, "#F43F5E", radius=[0, 0, 4, 4])

oval("Dot/ActiveIndicator2", "toolbar2", 172, 156, 6, 6, INK)

# ================================================================ screen 3 (Completed)
S3 = "S3"
box("Screen/3 - Completed", None, 940, 0, 390, 844, HERO, radius=40, clip=True, ref=S3)

for i in range(13):
    vec(f"Ray/{i}", S3, "M16 0L32 440H0z", 170 + (i - 6) * 10, -70, 64, 560, HERO_SOFT, rotation=(i - 6) * 12, opacity=0.6)

CONFETTI = [("#F2705B", 30, 120, 10, 14, 20), ("#5BBCE4", 320, 150, 12, 12, -14),
            ("#8DD98D", 60, 210, 9, 13, 36), ("#A98BE8", 300, 236, 11, 11, 22),
            ("#F6453D", 96, 128, 8, 12, -28), ("#4CC764", 268, 112, 10, 10, 14),
            ("#F2982A", 40, 300, 9, 9, 8), ("#E0439B", 330, 330, 8, 12, -20),
            ("#FFFFFF", 150, 108, 9, 9, 18), ("#5BBCE4", 212, 96, 8, 11, -32),
            ("#F7C948", 352, 206, 9, 12, 30), ("#F2705B", 14, 392, 8, 11, -16)]
for i, (color, cx, cy, cw, ch, rot) in enumerate(CONFETTI):
    rect(f"Confetti/{i}", S3, cx, cy, cw, ch, color, radius=3, rotation=rot, opacity=0.95)

box("Deco/Pencil", S3, -10, 560, 36, 110, "none", rotation=35, ref="deco-pencil")
rect("Deco/PencilShaft", "deco-pencil", 0, 0, 24, 80, GOLD, radius=[4, 4, 0, 0])
vec("Deco/PencilWood", "deco-pencil", "M0 0 L12 24 L24 0 Z", 0, 80, 24, 24, WOOD)
vec("Deco/PencilLead", "deco-pencil", "M4 0 L12 16 L20 0 Z", 0, 88, 24, 16, BLACK)

box("Deco/Marker", S3, 350, 330, 30, 90, "none", rotation=-35, ref="deco-marker")
rect("Deco/MarkerBody", "deco-marker", 4, 26, 22, 64, BLACK, radius=[0, 0, 4, 4])
vec("Deco/MarkerTip", "deco-marker", "M0 26 L11 0 L22 26 Z", 4, 0, 22, 26, "#333333")

box("Button/Back3", S3, 24, 44, 48, 48, ORANGE, radius=24, ref="back3")
vec("Icon/Back3", "back3", P_BACK, 15, 12, 20, 24, INK)
label(S3, 88, 56, "Challenge Completed!", size=17, style="Bold", color=INK)
box("Button/Retry", S3, 318, 44, 48, 48, WHITE, radius=24, effects=SHADOW_SOFT, ref="retry")
vec("Icon/Retry", "retry", P_REDO, 13, 12, 22, 24, ORANGE)

box("Card/Result", S3, 24, 250, 342, 420, WHITE, radius=32, effects=SHADOW_CARD, ref="result")

# Polaroid Photo
pola = box("Frame/Polaroid", S3, 105, 80, 180, 205, WHITE, radius=16, effects=SHADOW_POLA, rotation=3, ref="polaroid")
photo = box("Photo", pola, 12, 12, 156, 152, BLUE_DEEP, radius=8, clip=True, ref="photo-inner")
oval("Photo/Glow", photo, 20, 20, 116, 90, "#1976D2")
vec("CoralL", photo, P_CORAL, 10, 96, 24, 56, "#FF6584")
vec("CoralR", photo, P_CORAL, 122, 92, 22, 60, "#4DD0E1")
vec("CoralM", photo, P_CORAL, 68, 116, 18, 36, "#81D4FA")
# Scaled down cartoon whale in underwater photo
build_whale_drawing(photo, -15, 15, scale=0.68, name="PhotoWhale")
for i, (bx, by, br) in enumerate(((26, 28, 5), (120, 36, 7), (140, 78, 4), (46, 70, 4))):
    oval(f"Bubble{i}", photo, bx, by, br, br, WHITE, opacity=0.6)
vec("Photo/CornerFold", photo, "M 0 0 L 26 0 L 26 26 Z", 130, 0, 26, 26, "#E1F5FE")
vec("Polaroid/Clip", pola, P_CLIP, 142, -8, 28, 36, "#E5A93C", rotation=16)

# 3 Golden 3D Stars
star("Star/Left", S3, 110, 256, 48, GOLD, inner=0.44, rotation=-14, stroke=GOLD_DARK, weight=2.5)
star("Star/Right", S3, 232, 256, 48, GOLD, inner=0.44, rotation=14, stroke=GOLD_DARK, weight=2.5)
star("Star/Mid", S3, 165, 236, 60, GOLD, inner=0.44, stroke=GOLD_DARK, weight=2.5)

label("result", 112, 62, "Little Artist", size=15, style="Bold")
trophy("result", 192, 56, scale=1.05, name="ResultTrophy")

rect("Progress2/Track", "result", 20, 88, 302, 14, TRACK, radius=7)
rect("Progress2/Fill", "result", 20, 88, 196, 14, GREEN, radius=7)
box("Pill/Lv1b", "result", 20, 110, 46, 24, BLACK, radius=12, ref="lv1b")
label("lv1b", 10, 6, "Lv 1", size=11, style="Bold", color=WHITE)
label("result", 132, 114, "18/40", size=12, style="Bold")
label("result", 176, 114, "+5", size=12, style="Bold", color=GREEN)
box("Pill/Lv2", "result", 276, 110, 46, 24, CHIP, radius=12, ref="lv2")
label("lv2", 10, 6, "Lv 2", size=11, style="Bold", color="#6E6A63")
rect("Divider", "result", 20, 144, 302, 1.5, "#F2EDE3")

box("Stat/Speed", "result", 20, 156, 146, 66, WHITE, radius=20, stroke=BORDER, ref="speed")
oval("Speed/Disc", "speed", 12, 20, 30, 30, "#FFF3D6")
vec("Speed/Bolt", "speed", P_BOLT, 21, 26, 13, 17, GOLD)
label("speed", 50, 18, "5 mins", size=14, style="Bold")
label("speed", 50, 38, "Speed", size=10.5, style="Medium", color=INK_SOFT)
box("Badge/Top", "result", 14, 144, 56, 22, ORANGE_HOT, radius=11, ref="top1")
label("top1", 9, 5, "Top 1%", size=10, style="Bold", color=WHITE)

box("Stat/Creativity", "result", 176, 156, 146, 66, WHITE, radius=20, stroke=BORDER, ref="crea")
oval("Crea/Disc", "crea", 12, 20, 30, 30, "#E8F6FD")
vec("Crea/Arc1", "crea", P_RAINBOW_1, 17, 26, 20, 11, "#F2705B")
vec("Crea/Arc2", "crea", P_RAINBOW_2, 21, 30, 13, 7, "#5BBCE4")
label("crea", 50, 18, "100%", size=14, style="Bold")
label("crea", 50, 38, "Creativity", size=10.5, style="Medium", color=INK_SOFT)

box("Stat/Streak", "result", 20, 230, 302, 66, WHITE, radius=20, stroke=BORDER, ref="streak")
oval("Streak/Disc", "streak", 14, 18, 32, 32, "#FFE9E0")
vec("Streak/Flame", "streak", P_FLAME, 23, 24, 15, 20, RED)
label("streak", 56, 18, "3 days streak", size=14, style="Bold", color=RED_SOFT)
label("streak", 56, 38, "Longest: 8 days", size=10.5, style="Medium", color=INK_SOFT)
oval("Coin", "streak", 236, 24, 22, 22, GOLD, stroke=GOLD_DARK, weight=2)
label("streak", 264, 24, "×5", size=13, style="Bold")

label("result", 22, 312, "Amazing creativity!", size=12, style="Bold")
vec("Icon/Share", "result", P_PLANE, 22, 342, 18, 18, INK)
label("result", 46, 342, "Share", size=13.5, style="Bold")

ax_win = axolotl_cute(S3, 264, 550, scale=0.88, pose="normal", with_pencil=False, name="Character/Axolotl-Win")
vec("Wand", S3, "M0 0 L16 16", 260, 584, 16, 16, "none", stroke="#FFD54F", weight=3.5)
star("WandStar", S3, 272, 594, 16, GOLD, points=4, inner=0.35)

box("Button/KeepDrawing", S3, 24, 692, 342, 60, BLACK, radius=22, effects=SHADOW_SOFT, ref="cta")
label("cta", 108, 20, "Keep Drawing", size=16, style="Bold", color=WHITE)

# ================================================================ THE BIG OVERLAPPING MASCOT
axolotl_cute(None, 245, 630, scale=1.55, pose="waving_left", with_pencil=False, name="Showcase/Mascot-Big")

# ---------------------------------------------------------------- emit script
script = [
    {"command": "page.setBackground", "params": {"color": CREAM}},
    {"command": "page.rename", "params": {"name": "Kids Drawing App"}},
    {"command": "command.batch", "params": {"label": "Build kids drawing app complete", "commands": steps}},
]
with open("/tmp/figcraft_build/ui_script_complete.json", "w") as fh:
    json.dump(script, fh, indent=1)
print("Complete app steps:", len(steps))
