#!/usr/bin/env python3
"""Generate pixel-perfect FigCraft batch script matching the reference image."""
import json

# ---------------------------------------------------------------- palette
CREAM       = "#FDF8EE"
CANVAS_DOT  = "#F2E8D5"
HERO        = "#FFC83B"
HERO_DEEP   = "#F5B82E"
HERO_SOFT   = "#FFD966"
ORANGE      = "#F59324"
ORANGE_HOT  = "#FF7A3D"
WHITE       = "#FFFFFF"
CANVAS      = "#FDFBF7"
INK         = "#2D2A26"
INK_SOFT    = "#9E988F"
BORDER      = "#F0E8D8"
CHIP        = "#F4F1EA"
TRACK       = "#EFEAE0"
GREEN       = "#34C759"
GREEN_NAV   = "#32B753"
RED         = "#F6453D"
RED_SOFT    = "#E2574C"
BLUE        = "#1E88E5"
BLUE_DARK   = "#0D47A1"
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
BLACK       = "#18181B"
WOOD        = "#E8D5B5"
GILL_GREEN  = "#4ADE80"

ROUND = "SF Pro Rounded"
CHALK = "Chalkboard SE"

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
P_TRASH  = "M9.2 2.6h5.6l.9 1.9h4.1v2.2H4.2V4.5h4.1zM6 8.6h12l-1 12.8H7z"
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
P_BRISTLE   = "M0 0h18l-2 13c-5 5-9 5-14 0z"
P_TRI       = "M0 0h14l-7 16z"

# ---------------------------------------------------------------- complex assets
def trophy(parent, x, y, scale=1.0, name="Trophy"):
    g = box(name, parent, x, y, 24 * scale, 24 * scale, "none", ref=f"{name}-{int(x)}-{int(y)}")
    s = scale
    # blue ribbon
    vec("RibbonL", g, "M0 0 L5 12 L10 0 Z", 3 * s, 11 * s, 7 * s, 12 * s, "#1E88E5", rotation=-14)
    vec("RibbonR", g, "M0 0 L5 12 L10 0 Z", 14 * s, 11 * s, 7 * s, 12 * s, "#1E88E5", rotation=14)
    # cup base
    rect("Base", g, 7 * s, 18 * s, 10 * s, 4 * s, GOLD_DARK, radius=1)
    rect("Stem", g, 10.5 * s, 13 * s, 3 * s, 6 * s, GOLD)
    # cup body
    vec("Cup", g, "M0 0 C0 8, 4 12, 10 12 C16 12, 20 8, 20 0 Z", 2 * s, 3 * s, 20 * s, 12 * s, GOLD)
    # handles
    ring("HandleL", g, 0 * s, 4 * s, 6 * s, GOLD, weight=1.6 * s)
    ring("HandleR", g, 18 * s, 4 * s, 6 * s, GOLD, weight=1.6 * s)
    return g

def pencil_giant(parent, x, y, length=200, rotation=22, name="GiantPencil"):
    g = box(name, parent, x, y, length, 36, "none", rotation=rotation, ref=f"{name}-{int(x)}")
    # eraser
    rect("Eraser", g, 0, 4, 22, 28, "#FF8DA1", radius=[6, 0, 0, 6])
    # ferrule
    rect("Ferrule", g, 22, 4, 12, 28, "#B0BEC5")
    # body stripes
    rect("ShaftTop", g, 34, 4, length - 74, 9, "#FDD835")
    rect("ShaftMid", g, 34, 13, length - 74, 10, "#FBC02D")
    rect("ShaftBot", g, 34, 23, length - 74, 9, "#F57F17")
    # wooden tip
    vec("Wood", g, "M0 0 L26 14 L0 28 Z", length - 40, 4, 26, 28, WOOD)
    # lead
    vec("Lead", g, "M0 0 L10 5 L0 10 Z", length - 14, 13, 10, 10, BLACK)
    return g

def axolotl_cute(parent, x, y, scale=1.0, pose="sitting", with_pencil=False, name="Mascot"):
    """
    Accurate cute axolotl character with hot-pink shirt, lavender shorts,
    smiling open mouth with tooth/tongue, and lime green-tipped gills.
    """
    w_box = 150 * scale
    h_box = 145 * scale
    g = box(name, parent, x, y, w_box, h_box, "none", ref=f"{name}-{int(x)}-{int(y)}")
    s = scale

    # Gills (3 pairs with lime green tips)
    for i, (gx, gy, rot) in enumerate(((6, 22, -22), (0, 40, -6), (8, 58, 16))):
        oval(f"GillL_Base_{i}", g, gx * s, gy * s, 26 * s, 14 * s, PINK, rotation=rot)
        oval(f"GillL_Tip_{i}", g, (gx - 2) * s, (gy + 2) * s, 12 * s, 10 * s, GILL_GREEN, rotation=rot)
    for i, (gx, gy, rot) in enumerate(((112, 22, 22), (118, 40, 6), (110, 58, -16))):
        oval(f"GillR_Base_{i}", g, gx * s, gy * s, 26 * s, 14 * s, PINK, rotation=rot)
        oval(f"GillR_Tip_{i}", g, (gx + 16) * s, (gy + 2) * s, 12 * s, 10 * s, GILL_GREEN, rotation=rot)

    # Body & Clothes
    # Chubby Pink Legs & Feet
    oval("FootL", g, 38 * s, 114 * s, 24 * s, 16 * s, PINK_LT)
    oval("FootR", g, 84 * s, 114 * s, 24 * s, 16 * s, PINK_LT)
    
    # Lavender Shorts
    rect("ShortsL", g, 40 * s, 100 * s, 32 * s, 20 * s, LILAC, radius=[4, 4, 10, 10])
    rect("ShortsR", g, 74 * s, 100 * s, 32 * s, 20 * s, LILAC, radius=[4, 4, 10, 10])
    
    # Hot Pink Shirt / Torso
    rect("Shirt", g, 38 * s, 70 * s, 70 * s, 38 * s, PINK_SHIRT, radius=[18, 18, 8, 8])

    # Arms
    if pose == "waving_left":
        # Left arm stretched wide waving towards Screen 1 Home
        vec("ArmL", g, "M 28 20 C 14 18, 0 8, 2 0 C 4 -6, 18 2, 34 10 Z", 6 * s, 70 * s, 36 * s, 26 * s, PINK_LT, rotation=15)
        oval("HandL", g, 2 * s, 68 * s, 18 * s, 18 * s, PINK_LT)
        # Right arm resting down
        oval("ArmR", g, 104 * s, 78 * s, 20 * s, 24 * s, PINK_LT, rotation=-15)
    elif with_pencil:
        # Hands resting on pencil
        oval("HandL", g, 34 * s, 86 * s, 18 * s, 16 * s, PINK_LT)
        oval("HandR", g, 94 * s, 86 * s, 18 * s, 16 * s, PINK_LT)
    else:
        # Normal cute arms
        oval("ArmL", g, 26 * s, 74 * s, 18 * s, 22 * s, PINK_LT, rotation=20)
        oval("ArmR", g, 102 * s, 74 * s, 18 * s, 22 * s, PINK_LT, rotation=-20)

    # Head
    oval("Head", g, 30 * s, 14 * s, 86 * s, 68 * s, PINK_LT)
    
    # Blushing Cheeks
    oval("CheekL", g, 36 * s, 52 * s, 18 * s, 12 * s, PINK, opacity=0.85)
    oval("CheekR", g, 92 * s, 52 * s, 18 * s, 12 * s, PINK, opacity=0.85)
    
    # Eyes
    oval("EyeL", g, 50 * s, 34 * s, 11 * s, 13 * s, BLACK)
    oval("EyeR", g, 84 * s, 34 * s, 11 * s, 13 * s, BLACK)
    oval("GlintL", g, 53 * s, 36 * s, 4.5 * s, 4.5 * s, WHITE)
    oval("GlintR", g, 87 * s, 36 * s, 4.5 * s, 4.5 * s, WHITE)

    # Joyful Open Mouth with Tooth & Tongue
    m = box("MouthFrame", g, 58 * s, 48 * s, 30 * s, 22 * s, "#881337", radius=[4, 4, 15, 15], clip=True, ref=f"mouth-{int(x)}-{int(y)}")
    rect("Tooth", m, 11 * s, 0, 8 * s, 5 * s, WHITE, radius=2)
    oval("Tongue", m, 5 * s, 11 * s, 20 * s, 14 * s, "#FF7B98")

    return g

def whale_drawing_accurate(parent, x, y, scale=1.0, name="Drawing/Whale"):
    """
    Pixel-accurate cartoon whale matching the reference image.
    Features:
    - Bulbous dome head facing right
    - Cream underbelly with 3 dark blue groove lines
    - Black smiling mouth with dimple tick at top-left
    - Glossy black eye with white glint
    - Cute curved tail flukes
    - Pectoral fin pointing down
    - 3 golden blowhole droplets
    - Purple, cyan, and coral doodle rings
    """
    g = box(name, parent, x, y, 220 * scale, 150 * scale, "none", ref=f"{name}-{int(x)}")
    s = scale

    # Surrounding Doodle Rings (behind whale)
    ring("RingPurple", g, 172 * s, 10 * s, 24 * s, PURPLE, weight=3.5 * s)
    ring("RingCyan", g, 204 * s, 32 * s, 16 * s, BLUE_LT, weight=3 * s)
    ring("RingCoral", g, 26 * s, 104 * s, 26 * s, ORANGE_HOT, weight=4 * s)

    # 3 Golden Water Spout Droplets
    P_DROP = "M 5 0 C 9 6, 9 13, 5 15 C 1 13, 1 6, 5 0 Z"
    vec("SpoutL", g, P_DROP, 126 * s, 4 * s, 10 * s, 15 * s, GOLD, rotation=-22)
    vec("SpoutM", g, P_DROP, 140 * s, 0 * s, 10 * s, 16 * s, GOLD, rotation=0)
    vec("SpoutR", g, P_DROP, 154 * s, 4 * s, 10 * s, 15 * s, GOLD, rotation=22)

    # Whale Body Vector (curved back, tail flukes on left, round forehead on right)
    P_WHALE_BODY = (
        "M 206 62 "
        "C 206 32, 170 18, 130 18 "
        "C 90 18, 62 36, 42 34 "
        "C 28 32, 16 18, 6 6 "
        "C 4 18, 10 32, 22 42 "
        "C 10 44, 4 56, 8 68 "
        "C 18 64, 28 54, 38 48 "
        "C 46 72, 72 96, 108 100 "
        "C 146 104, 184 94, 202 80 "
        "C 206 74, 206 68, 206 62 Z"
    )
    vec("Body", g, P_WHALE_BODY, 4 * s, 16 * s, 206 * s, 100 * s, BLUE, stroke=BLUE_DARK, weight=2.5 * s)

    # Cream Underbelly (clean standalone path)
    P_BELLY_CLEAN = "M 0 18 C 28 25, 60 17, 84 2 C 74 -6, 42 -8, 8 0 C 0 6, -2 12, 0 18 Z"
    vec("Belly", g, P_BELLY_CLEAN, 122 * s, 88 * s, 84 * s, 26 * s, "#FFF9D2", stroke=BLUE_DARK, weight=2 * s)

    # 3 Belly Grooves
    vec("Groove1", g, "M -0.5 0 L 0.5 14", 152 * s, 90 * s, 1 * s, 14 * s, "none", stroke=BLUE_DARK, weight=2 * s, strokeCap="round")
    vec("Groove2", g, "M -0.5 0 L 0.5 14", 166 * s, 86 * s, 1 * s, 14 * s, "none", stroke=BLUE_DARK, weight=2 * s, strokeCap="round")
    vec("Groove3", g, "M -0.5 0 L 0.5 12", 180 * s, 82 * s, 1 * s, 12 * s, "none", stroke=BLUE_DARK, weight=2 * s, strokeCap="round")

    # Pectoral Fin
    P_FIN = "M 0 0 C 12 12, 18 30, 12 38 C 2 36, -4 20, 0 0 Z"
    vec("Fin", g, P_FIN, 104 * s, 88 * s, 18 * s, 38 * s, BLUE, stroke=BLUE_DARK, weight=2.5 * s)

    # Smiling Mouth with Dimple Tick (bold black line)
    P_SMILE = "M 56 8 C 40 10, 14 6, 2 6 C 0 4, 2 0, 4 0"
    vec("MouthSmile", g, P_SMILE, 144 * s, 72 * s, 56 * s, 10 * s, "none", stroke=BLACK, weight=3.5 * s, strokeCap="round")

    # Single Glossy Eye
    oval("Eye", g, (4 + 158) * s, (16 + 50) * s, 9 * s, 10 * s, BLACK)
    oval("EyeGlint", g, (4 + 160) * s, (16 + 51) * s, 3.5 * s, 3.5 * s, WHITE)

    return g

def tool_slot(slot, kind):
    """Accurate drawing tool illustrations."""
    if kind == "brush":
        rect("Brush/Handle", slot, 26, 6, 14, 24, "#6B6B6B", radius=7)
        rect("Brush/Ferrule", slot, 25, 28, 16, 7, "#B9B9B9", radius=2)
        vec("Brush/Bristle", slot, P_BRISTLE, 24, 34, 18, 18, INK)
    elif kind == "pencil":
        rect("Pencil/Body", slot, 26, 6, 14, 26, GOLD, radius=[7, 7, 0, 0])
        rect("Pencil/Band", slot, 26, 20, 14, 5, "#E08B2C")
        vec("Pencil/Wood", slot, P_TRI, 26, 31, 14, 15, WOOD)
        vec("Pencil/Lead", slot, P_TRI, 29.5, 40, 7, 7, INK)
    elif kind == "crayon":
        rect("Crayon/Body", slot, 26, 8, 14, 26, BLACK, radius=[6, 6, 0, 0])
        rect("Crayon/Band", slot, 26, 18, 14, 6, "#4A4A4A")
        vec("Crayon/Tip", slot, P_TRI, 26, 33, 14, 14, "#111111")
    else:
        # Angled eraser with blue top, white stripe, pink base
        box("EraserBlock", slot, 18, 12, 30, 40, "#38BDF8", radius=4, rotation=24, ref=f"eraser-{slot}")
        rect("Eraser/Stripe", f"eraser-{slot}", 0, 16, 30, 8, WHITE)
        rect("Eraser/Pink", f"eraser-{slot}", 0, 24, 30, 16, "#FF7B98", radius=[0, 0, 4, 4])

# ================================================================ screen 1 (Home)
S1 = "S1"
box("Screen/1 - Home", None, 0, 0, 390, 844, WHITE, radius=40, clip=True, ref=S1)

box("Hero", S1, 0, 0, 390, 305, HERO, radius=[40, 40, 36, 36], clip=True, ref="hero")
# Cheese-like organic cutout bubbles on top-left
oval("Hero/Cheese1", "hero", 10, 110, 60, 60, HERO_DEEP, opacity=0.45)
oval("Hero/Cheese2", "hero", 44, 165, 42, 42, HERO_DEEP, opacity=0.4)
oval("Hero/Cheese3", "hero", 6, 195, 48, 48, HERO_DEEP, opacity=0.35)
rect("Hero/Paper1", "hero", 300, 186, 42, 48, "#FDE7B4", radius=6, rotation=-14, opacity=0.9)
rect("Hero/Paper2", "hero", 326, 212, 32, 36, "#FFF2CF", radius=5, rotation=12, opacity=0.9)

# Cookie Avatar
oval("Avatar/Ring", S1, 24, 44, 48, 48, "#FFF3DA")
oval("Avatar/Cookie", S1, 31, 51, 34, 34, "#E3A765")
for i, (ax, ay) in enumerate(((38, 60), (48, 56), (52, 68), (41, 71))):
    oval(f"Avatar/Chip{i}", S1, ax, ay, 6, 6, "#7A4A22")
label(S1, 84, 46, "Hi,", size=12, style="Medium", color="#A8792B")
label(S1, 84, 62, "Tiffany", size=19, style="Bold", color="#3A2D14")

# Notification Bell with orange top badge
box("Button/Bell", S1, 318, 44, 48, 48, WHITE, radius=18, effects=SHADOW_SOFT, ref="bell")
vec("Icon/Bell", "bell", P_BELL, 13, 12, 22, 24, HERO_DEEP)
oval("Bell/OrangeDot", "bell", 30, 8, 10, 10, ORANGE_HOT)

# Giant Diagonal Pencil in Hero
pencil_giant(S1, 70, 220, length=210, rotation=22, name="HeroPencil")

# Axolotl Mascot sitting on pencil
axolotl_cute(S1, 76, 134, scale=1.05, pose="sitting", with_pencil=True, name="Character/Axolotl-Hero")

# Speech Bubble
box("Bubble", S1, 224, 130, 136, 64, WHITE, radius=20, effects=SHADOW_SOFT, ref="bubble")
label("bubble", 18, 12, "Let's start", size=14, style="Bold", color="#3A2D14")
label("bubble", 18, 32, "Drawing!", size=14, style="Bold", color="#3A2D14")
vec("Bubble/Tail", S1, "M0 0 L16 4 L4 14 Z", 212, 168, 16, 14, WHITE)

# Little Artist Card with Trophy
box("Card/Progress", S1, 24, 260, 342, 96, WHITE, radius=24, effects=SHADOW_CARD, ref="prog")
label("prog", 20, 20, "Little Artist", size=15, style="Bold")
trophy("prog", 112, 16, scale=1.0, name="ProgTrophy")
label("prog", 240, 22, "History  ›", size=12, style="Medium", color=INK_SOFT)
rect("Progress/Track", "prog", 20, 52, 228, 14, TRACK, radius=7)
rect("Progress/Fill", "prog", 20, 52, 116, 14, GREEN, radius=7)
label("prog", 254, 53, "13/40", size=11, style="Medium", color=INK_SOFT)
box("Pill/Lv1", "prog", 294, 48, 46, 24, BLACK, radius=12, ref="lv1")
label("lv1", 10, 6, "Lv 1", size=11, style="Bold", color=WHITE)

# Category Icons
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

# Daily Challenges Section
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
        vec("Icon/MiniWhale", disc, "M4 14 C4 6, 14 2, 26 2 C36 2, 42 6, 44 12 C36 14, 30 18, 22 18 C14 18, 4 16, 4 14 Z", 6, 14, 32, 16, BLUE)
        oval("Icon/WhaleEye", disc, 30, 18, 3, 3, WHITE)
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

# Card 3 (Flying car)
box("Card/FlyingCar", S1, 24, 662, 342, 70, WHITE, radius=20, stroke=BORDER, ref="card3")
box("Icon/Disc3", "card3", 14, 13, 44, 44, "#FBC9A4", radius=22, ref="cd3")
rect("Mini/CarCabin", "cd3", 15, 12, 15, 11, "#F7A07A", radius=[6, 6, 0, 0])
rect("Mini/CarWindow", "cd3", 18, 15, 10, 6, WHITE, radius=2, opacity=0.85)
rect("Mini/CarBody", "cd3", 7, 21, 30, 11, "#E8743F", radius=5)
oval("Mini/CarWheelL", "cd3", 11, 28, 8, 8, "#A84B22")
oval("Mini/CarWheelR", "cd3", 25, 28, 8, 8, "#A84B22")
label("card3", 70, 22, "Invent a Flying Car!", size=13.5, style="Bold")

# Bottom Navigation
row("Nav/Bar", S1, 16, 752, 358, 70, gap=0, pad=[10, 26, 10, 26], main="spaceBetween", cross="center", fill=WHITE, radius=28, effects=SHADOW_NAV, ref="nav")
for nname, glyph, active in (("Home", P_HOUSE, True), ("Stars", None, False), ("Ranks", P_BARS, False)):
    tint = GREEN_NAV if active else "#C9C3B8"
    cell = row(f"Nav/{nname}", "nav", None, None, None, None, gap=5, vertical=True, main="min", cross="center", sizing_h="hug", sizing_v="hug", ref=f"nav-{nname}")
    if glyph:
        vec(f"Nav/{nname}/Icon", cell, glyph, None, None, 25, 25, tint)
    else:
        star(f"Nav/{nname}/Icon", cell, None, None, 25, tint, inner=0.45)
    label(cell, None, None, nname, size=11, style="Bold", color=GREEN_NAV if active else "#A8A29A")

# ================================================================ screen 2 (Draw Screen)
S2 = "S2"
box("Screen/2 - Draw", None, 470, 0, 390, 844, CANVAS, radius=40, clip=True, ref=S2)

box("Canvas/DotGrid", S2, 0, 0, 390, 844, "none", ref="dotgrid")
for gx in range(0, 10):
    for gy in range(0, 16):
        oval(f"Dot/{gx}-{gy}", "dotgrid", 22 + gx * 39, 110 + gy * 36, 3.4, 3.4, "#E8DEC8", opacity=0.75)

box("Button/Back2", S2, 24, 44, 48, 48, HERO_DEEP, radius=24, ref="back2")
vec("Icon/Back2", "back2", P_BACK, 15, 12, 20, 24, WHITE)

row("Pill/Title", S2, 88, 44, 214, 48, gap=10, pad=[6, 14, 6, 10], main="min", cross="center", fill=WHITE, radius=24, effects=SHADOW_SOFT, ref="title2")
# Mini axolotl face in title pill
m_axo = box("MiniAxo", "title2", None, None, 34, 34, "none", ref="mini-axo-title")
oval("Mini/Gill1", m_axo, 0, 10, 11, 7, PINK)
oval("Mini/Gill2", m_axo, 23, 10, 11, 7, PINK)
oval("Mini/Head", m_axo, 6, 6, 22, 20, PINK_LT)
oval("Mini/EyeL", m_axo, 12, 13, 3.4, 4, INK)
oval("Mini/EyeR", m_axo, 20, 13, 3.4, 4, INK)
label("title2", None, None, "Draw a Whale", size=14.5, style="Bold")

box("Button/Trash", S2, 318, 44, 48, 48, RED, radius=24, ref="trash2")
vec("Icon/Trash", "trash2", P_TRASH, 13, 12, 22, 24, WHITE)

# Accurate Whale Drawing in Screen 2
whale_drawing_accurate(S2, 85, 290, scale=1.0)
label(S2, 122, 455, "WHALE", size=40, style="Bold", color=BLACK, family=CHALK)

box("Button/Transform", S2, 118, 570, 154, 48, GREEN, radius=24, effects=SHADOW_SOFT, ref="transform")
label("transform", 22, 14, "Transform!", size=15, style="Bold", color=WHITE)
vec("Icon/Spark", "transform", P_SPARK, 116, 15, 18, 18, "#FFF4C2")

box("Toolbar", S2, 24, 672, 342, 150, WHITE, radius=30, effects=SHADOW_CARD, ref="toolbar")
SWATCHES = [BLACK, BLUE_LT, PINK, PURPLE, "#F3EAD7", "#2E7D4F", "#8DD98D", RED, ORANGE_HOT, GOLD]
row("Row/Swatches", "toolbar", 18, 18, 306, 26, gap=6, main="spaceBetween", cross="center", ref="swatches")
for i, color in enumerate(SWATCHES):
    oval(f"Swatch/{i}", "swatches", None, None, 24, 24, color, stroke="#E2DACB" if color == "#F3EAD7" else None, weight=1.5)

row("Tray/Tools", "toolbar", 16, 56, 310, 80, gap=8, pad=8, main="spaceBetween", cross="center", fill=HERO_DEEP, radius=24, ref="tray")
for kind in ("brush", "pencil", "crayon", "eraser"):
    slot = box(f"Tool/{kind}", "tray", None, None, 66, 64, WHITE, radius=18, ref=f"tool-{kind}")
    tool_slot(slot, kind)
oval("Tool/ActiveDot", "toolbar", 168, 140, 6, 6, BLACK)

# ================================================================ screen 3 (Completed)
S3 = "S3"
box("Screen/3 - Completed", None, 940, 0, 390, 844, HERO, radius=40, clip=True, ref=S3)

# Golden Sunburst Rays
for i in range(13):
    vec(f"Ray/{i}", S3, "M16 0L32 440H0z", 170 + (i - 6) * 10, -70, 64, 560, HERO_SOFT, rotation=(i - 6) * 12, opacity=0.6)

# Confetti Rectangles
CONFETTI = [("#F2705B", 30, 120, 10, 14, 20), ("#5BBCE4", 320, 150, 12, 12, -14),
            ("#8DD98D", 60, 210, 9, 13, 36), ("#A98BE8", 300, 236, 11, 11, 22),
            ("#F6453D", 96, 128, 8, 12, -28), ("#4CC764", 268, 112, 10, 10, 14),
            ("#F2982A", 40, 300, 9, 9, 8), ("#E0439B", 330, 330, 8, 12, -20),
            ("#FFFFFF", 150, 108, 9, 9, 18), ("#5BBCE4", 212, 96, 8, 11, -32),
            ("#F7C948", 352, 206, 9, 12, 30), ("#F2705B", 14, 392, 8, 11, -16)]
for i, (color, cx, cy, cw, ch, rot) in enumerate(CONFETTI):
    rect(f"Confetti/{i}", S3, cx, cy, cw, ch, color, radius=3, rotation=rot, opacity=0.95)

# Pencil tip peeking out behind card at bottom-left
box("Deco/Pencil", S3, -10, 560, 36, 110, "none", rotation=35, ref="deco-pencil")
rect("Deco/PencilShaft", "deco-pencil", 0, 0, 24, 80, GOLD, radius=[4, 4, 0, 0])
vec("Deco/PencilWood", "deco-pencil", "M0 0 L12 24 L24 0 Z", 0, 80, 24, 24, WOOD)
vec("Deco/PencilLead", "deco-pencil", "M4 0 L12 16 L20 0 Z", 0, 88, 24, 16, BLACK)

# Marker pen tip peeking out on right
box("Deco/Marker", S3, 350, 330, 30, 90, "none", rotation=-35, ref="deco-marker")
rect("Deco/MarkerBody", "deco-marker", 4, 26, 22, 64, BLACK, radius=[0, 0, 4, 4])
vec("Deco/MarkerTip", "deco-marker", "M0 26 L11 0 L22 26 Z", 4, 0, 22, 26, "#333333")

box("Button/Back3", S3, 24, 44, 48, 48, ORANGE, radius=24, ref="back3")
vec("Icon/Back3", "back3", P_BACK, 15, 12, 20, 24, INK)
label(S3, 88, 56, "Challenge Completed!", size=17, style="Bold", color=INK)
box("Button/Retry", S3, 318, 44, 48, 48, WHITE, radius=24, effects=SHADOW_SOFT, ref="retry")
vec("Icon/Retry", "retry", P_REDO, 13, 12, 22, 24, ORANGE)

# The White Stats Card
box("Card/Result", S3, 24, 250, 342, 420, WHITE, radius=32, effects=SHADOW_CARD, ref="result")

# ---------------------------------------------------------------- POLAROID PHOTO
# True Polaroid frame overlapping the top of the card
pola = box("Frame/Polaroid", S3, 105, 80, 180, 205, WHITE, radius=16, effects=SHADOW_POLA, rotation=3, ref="polaroid")
# Photo insert
photo = box("Photo", pola, 12, 12, 156, 152, BLUE_DEEP, radius=8, clip=True, ref="photo-inner")
oval("Photo/Glow", photo, 20, 20, 116, 90, "#1976D2")
vec("CoralL", photo, P_CORAL, 10, 96, 24, 56, "#FF6584")
vec("CoralR", photo, P_CORAL, 122, 92, 22, 60, "#4DD0E1")
vec("CoralM", photo, P_CORAL, 68, 116, 18, 36, "#81D4FA")
whale_drawing_accurate(photo, 14, 38, scale=0.62, name="PhotoWhale")
for i, (bx, by, br) in enumerate(((26, 28, 5), (120, 36, 7), (140, 78, 4), (46, 70, 4))):
    oval(f"Bubble{i}", photo, bx, by, br, br, WHITE, opacity=0.6)
vec("Photo/CornerFold", photo, "M 0 0 L 26 0 L 26 26 Z", 130, 0, 26, 26, "#E1F5FE")
vec("Polaroid/Clip", pola, P_CLIP, 142, -8, 28, 36, "#E5A93C", rotation=16)

# 3 Golden 3D Stars (overlapping bottom of polaroid and top of white card)
star("Star/Left", S3, 110, 256, 48, GOLD, inner=0.44, rotation=-14, stroke=GOLD_DARK, weight=2.5)
star("Star/Right", S3, 232, 256, 48, GOLD, inner=0.44, rotation=14, stroke=GOLD_DARK, weight=2.5)
star("Star/Mid", S3, 165, 236, 60, GOLD, inner=0.44, stroke=GOLD_DARK, weight=2.5)

# Contents inside Card/Result (relative to result frame at y=250)
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

# Axolotl Winner with magic star wand
ax_win = axolotl_cute(S3, 264, 550, scale=0.88, pose="normal", with_pencil=False, name="Character/Axolotl-Win")
# Magic wand in hand
vec("Wand", S3, "M0 0 L16 16", 260, 584, 16, 16, "none", stroke="#FFD54F", weight=3.5)
star("WandStar", S3, 272, 594, 16, GOLD, points=4, inner=0.35)

box("Button/KeepDrawing", S3, 24, 692, 342, 60, BLACK, radius=22, effects=SHADOW_SOFT, ref="cta")
label("cta", 108, 20, "Keep Drawing", size=16, style="Bold", color=WHITE)

# ================================================================ THE BIG OVERLAPPING MASCOT
# Positioned between Screen 1 and Screen 2 on the canvas (top level)
# Waving arm towards Screen 1 Home button, hot pink shirt, lavender shorts
axolotl_cute(None, 245, 630, scale=1.55, pose="waving_left", with_pencil=False, name="Showcase/Mascot-Big")

# ---------------------------------------------------------------- emit script
script = [
    {"command": "page.setBackground", "params": {"color": CREAM}},
    {"command": "page.rename", "params": {"name": "Kids Drawing App"}},
    {"command": "command.batch", "params": {"label": "Build kids drawing app v3", "commands": steps}},
]
with open("/tmp/figcraft_build/ui_script_v3.json", "w") as fh:
    json.dump(script, fh, indent=1)
print("v3 steps:", len(steps))
