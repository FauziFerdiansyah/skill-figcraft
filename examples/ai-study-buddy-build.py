#!/usr/bin/env python3
"""
AI Study Buddy - 3 Screen Mobile App
Reconstructed for FigCraft with:
- Google Fonts: Plus Jakarta Sans
- Iconify Icons: Lucide collection
- Native FigCraft commands (node.create, file.placeImage for photo avatars, auto-layout, vectors)
"""
import os
import sys
import json
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, "assets")
AVATAR_FEMALE = os.path.join(ASSETS_DIR, "avatar_female.png")
AVATAR_MALE   = os.path.join(ASSETS_DIR, "avatar_male.png")

CANVAS_BG   = "#EAEFEA"
SCREEN_BG   = "#F8FAF8"
WHITE       = "#FFFFFF"
INK_TITLE   = "#111827"
INK_BODY    = "#374151"
INK_MUTED   = "#6B7280"
INK_LIGHT   = "#9CA3AF"
BORDER_LT   = "#E5E7EB"

# Accents
LIME_HERO   = "#92DC36"
LIME_BRIGHT = "#A3E635"
LIME_DEEP   = "#365314"
LIME_GLOW   = "#A3E63540"

# Pastel chips
PURPLE_BG   = "#F3E8FF"
PURPLE_INK  = "#9333EA"
MINT_BG     = "#DCFCE7"
MINT_INK    = "#16A34A"
BLUE_BG     = "#E0F2FE"
BLUE_INK    = "#0284C7"
PEACH_BG    = "#FFEDD5"
PEACH_INK   = "#EA580C"

FONT_FAMILY = "Plus Jakarta Sans"

SHADOW_CARD = [{"type": "dropShadow", "color": "#0000000A", "offset": [0, 4], "radius": 16}]
SHADOW_NAV  = [{"type": "dropShadow", "color": "#00000014", "offset": [0, 6], "radius": 24}]
SHADOW_SOFT = [{"type": "dropShadow", "color": "#00000008", "offset": [0, 2], "radius": 8}]

# Authentic Iconify Lucide SVGs (flattened path definitions)
ICONS = {
  "arrow_left": "m12 19l-7-7l7-7m7 7H5",
  "chevron_down": "m6 9l6 6l6-6",
  "chevron_right": "m9 18l6-6l-6-6",
  "chevrons_right": "m6 17l5-5l-5-5m7 10l5-5l-5-5",
  "menu": "M21 12H9m12 6H7M21 6H3",
  "sparkles": "M11.017 2.814a1 1 0 0 1 1.966 0l1.051 5.558a2 2 0 0 0 1.594 1.594l5.558 1.051a1 1 0 0 1 0 1.966l-5.558 1.051a2 2 0 0 0-1.594 1.594l-1.051 5.558a1 1 0 0 1-1.966 0l-1.051-5.558a2 2 0 0 0-1.594-1.594l-5.558-1.051a1 1 0 0 1 0-1.966l5.558-1.051a2 2 0 0 0 1.594-1.594zM20 2v4m2-2h-4 M 2.0 20.0 A 2.0 2.0 0 1 0 6.0 20.0 A 2.0 2.0 0 1 0 2.0 20.0",
  "settings": "M9.671 4.136a2.34 2.34 0 0 1 4.659 0a2.34 2.34 0 0 0 3.319 1.915a2.34 2.34 0 0 1 2.33 4.033a2.34 2.34 0 0 0 0 3.831a2.34 2.34 0 0 1-2.33 4.033a2.34 2.34 0 0 0-3.319 1.915a2.34 2.34 0 0 1-4.659 0a2.34 2.34 0 0 0-3.32-1.915a2.34 2.34 0 0 1-2.33-4.033a2.34 2.34 0 0 0 0-3.831A2.34 2.34 0 0 1 6.35 6.051a2.34 2.34 0 0 0 3.319-1.915 M 9.0 12.0 A 3.0 3.0 0 1 0 15.0 12.0 A 3.0 3.0 0 1 0 9.0 12.0",
  "tv": "m17 2l-5 5l-5-5 M 2.0 7.0 H 22.0 V 22.0 H 2.0 Z",
  "camera": "M13.997 4a2 2 0 0 1 1.76 1.05l.486.9A2 2 0 0 0 18.003 7H20a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h1.997a2 2 0 0 0 1.759-1.048l.489-.904A2 2 0 0 1 10.004 4z M 9.0 13.0 A 3.0 3.0 0 1 0 15.0 13.0 A 3.0 3.0 0 1 0 9.0 13.0",
  "mic": "M12 19v3m7-12v2a7 7 0 0 1-14 0v-2 M 9.0 2.0 H 15.0 V 15.0 H 9.0 Z",
  "crown": "M11.562 3.266a.5.5 0 0 1 .876 0L15.39 8.87a1 1 0 0 0 1.516.294L21.183 5.5a.5.5 0 0 1 .798.519l-2.834 10.246a1 1 0 0 1-.956.734H5.81a1 1 0 0 1-.957-.734L2.02 6.02a.5.5 0 0 1 .798-.519l4.276 3.664a1 1 0 0 0 1.516-.294zM5 21h14",
  "plus": "M5 12h14m-7-7v14",
  "scan_face": "M3 7V5a2 2 0 0 1 2-2h2m10 0h2a2 2 0 0 1 2 2v2m0 10v2a2 2 0 0 1-2 2h-2M7 21H5a2 2 0 0 1-2-2v-2m5-3s1.5 2 4 2s4-2 4-2M9 9h.01M15 9h.01",
  "message_square": "M22 17a2 2 0 0 1-2 2H6.828a2 2 0 0 0-1.414.586l-2.202 2.202A.71.71 0 0 1 2 21.286V5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2z",
  "message_check": "M22 17a2 2 0 0 1-2 2H6.828a2 2 0 0 0-1.414.586l-2.202 2.202A.7.7 0 0 1 2 21.286V5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2z m9 11l2 2l4-4",
  "book_open": "M12 5v16m8.001-2A2 2 0 0 0 22 17V5a2 2 0 0 0-1.999-2L16 3.002A5 5 0 0 0 12 5a5 5 0 0 0-4-2H4a2 2 0 0 0-2 2v12a2 2 0 0 0 1.999 2H8a5 5 0 0 1 4 2a5 5 0 0 1 4-2z",
  "play": "M5 5a2 2 0 0 1 3.008-1.728l11.997 6.998a2 2 0 0 1 .003 3.458l-12 7A2 2 0 0 1 5 19z",
  "arrow_up_right": "M7 7h10v10M7 17L17 7",
  "home": "M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8 M3 10a2 2 0 0 1 .709-1.528l7-6a2 2 0 0 1 2.582 0l7 6A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z",
  "clock": "M12 6v6l4 2 M 2.0 12.0 A 10.0 10.0 0 1 0 22.0 12.0 A 10.0 10.0 0 1 0 2.0 12.0",
  "trophy": "M10 14.66V17a1 1 0 0 1-1 1a2 2 0 0 0-2 2v2m7-7.34V17a1 1 0 0 0 1 1a2 2 0 0 1 2 2v2m.916-12H19.5A2.5 2.5 0 0 0 22 7.5V5a1 1 0 0 0-1-1h-3M4 22h16 M6 9a6 6 0 0 0 12 0V3a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1z M6.084 10H4.5A2.5 2.5 0 0 1 2 7.5V5a1 1 0 0 1 1-1h3",
  "flame": "M12 3q1 4 4 6.5t3 5.5a1 1 0 0 1-14 0a5 5 0 0 1 1-3a1 1 0 0 0 5 0c0-2-1.5-3-1.5-5q0-2 2.5-4",
  "flask": "M14 2v6a2 2 0 0 0 .245.96l5.51 10.08A2 2 0 0 1 18 22H6a2 2 0 0 1-1.755-2.96l5.51-10.08A2 2 0 0 0 10 8V2M6.453 15h11.094M8.5 2h7",
  "globe": "M12 2a14.5 14.5 0 0 0 0 20a14.5 14.5 0 0 0 0-20M2 12h20 M 2.0 12.0 A 10.0 10.0 0 1 0 22.0 12.0 A 10.0 10.0 0 1 0 2.0 12.0",
  "calculator": "M8 6h8m0 8v4m0-8h.01M12 10h.01M8 10h.01M12 14h.01M8 14h.01M12 18h.01M8 18h.01 M 4.0 2.0 H 20.0 V 22.0 H 4.0 Z",
  "send": "M14.536 21.686a.5.5 0 0 0 .937-.024l6.5-19a.496.496 0 0 0-.635-.635l-19 6.5a.5.5 0 0 0-.024.937l7.93 3.18a2 2 0 0 1 1.112 1.11zm7.318-19.539l-10.94 10.939",
  "bookmark": "M17 3a2 2 0 0 1 2 2v15a1 1 0 0 1-1.496.868l-4.512-2.578a2 2 0 0 0-1.984 0l-4.512 2.578A1 1 0 0 1 5 20V5a2 2 0 0 1 2-2z",
  "clipboard_check": "M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2 m9 14l2 2l4-4 M 8.0 2.0 H 16.0 V 6.0 H 8.0 Z",
  "star": "M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.12 2.12 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.12 2.12 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.12 2.12 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.12 2.12 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.12 2.12 0 0 0 1.597-1.16z",
  "hexagon": "M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16"
}

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

def label(parent, x, y, text, size=12, style="Bold", color=INK_TITLE, w=None,
          align=None, family=FONT_FAMILY, name=None, rotation=None):
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

def vec(name, parent, path, x, y, w, h, fill="none", stroke=None, weight=None, strokeCap=None, rotation=None, opacity=None):
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

def iconify(name, parent, icon_name, x, y, size=24, color="#111827", stroke_width=2.0, fill="none"):
    """Draw authentic icon vector from Iconify."""
    path = ICONS.get(icon_name)
    if not path:
        return
    props = {
        "fill": fill,
        "stroke": color,
        "strokeWeight": stroke_width,
        "strokeCap": "round"
    }
    node("vector", name or f"Icon/{icon_name}", parent, x, y, size, size, props, path=path)

def place_avatar(parent, img_path, x, y, size=32, ref=None):
    """Place real masked circular photo avatar."""
    f = box("AvatarMask", parent, x, y, size, size, "none", radius=size/2, clip=True, ref=ref)
    if os.path.exists(img_path):
        step = {
            "command": "file.placeImage",
            "params": {
                "parent": {"$ref": ref} if ref else f,
                "path": img_path,
                "x": 0,
                "y": 0,
                "width": size,
                "height": size
            }
        }
        steps.append(step)
    return f

def status_bar(parent, w=375):
    """Clean iOS status bar."""
    bar = box("StatusBar", parent, 0, 0, w, 44, "none", ref=f"status-{parent}")
    label(bar, 24, 14, "9:41", size=14, style="Bold", color=INK_TITLE)
    rect("Cell1", bar, w - 68, 22, 3, 5, INK_TITLE, radius=1)
    rect("Cell2", bar, w - 63, 19, 3, 8, INK_TITLE, radius=1)
    rect("Cell3", bar, w - 58, 16, 3, 11, INK_TITLE, radius=1)
    rect("Cell4", bar, w - 53, 13, 3, 14, INK_TITLE, radius=1)
    iconify("Icon/Wifi", bar, "sparkles", w - 44, 14, size=15, color=INK_TITLE, stroke_width=2)
    rect("BatteryBody", bar, w - 26, 15, 20, 11, "none", radius=3, stroke=INK_TITLE, weight=1.5)
    rect("BatteryFill", bar, w - 24, 17, 14, 7, INK_TITLE, radius=1.5)
    rect("BatteryTip", bar, w - 5, 18, 1.5, 5, INK_TITLE, radius=0.5)

def bottom_nav(parent, active_tab="home", w=375, y=730):
    """Floating capsule bottom navigation bar."""
    nav = box("NavBar", parent, 20, y, w - 40, 64, WHITE, radius=32, effects=SHADOW_NAV, ref=f"nav-{parent}")
    tabs = [
        ("home", "Home", "home"),
        ("chat", "Chat", "message_square"),
        ("books", "Library", "book_open"),
        ("profile", "Profile", "settings"),
    ]
    tab_x = 8
    for tab_id, tab_title, tab_icon in tabs:
        if tab_id == active_tab:
            btn = box(f"Nav/{tab_title}/Active", nav, tab_x, 8, 108, 48, "#18181B", radius=24, ref=f"act-{parent}-{tab_id}")
            iconify("ActIcon", btn, tab_icon, 14, 13, size=22, color=WHITE, stroke_width=2.2)
            label(btn, 44, 15, tab_title, size=13.5, style="Bold", color=WHITE)
            tab_x += 114
        else:
            btn = box(f"Nav/{tab_title}", nav, tab_x, 8, 48, 48, "none", radius=24, ref=f"inact-{parent}-{tab_id}")
            iconify("InactIcon", btn, tab_icon, 13, 13, size=22, color=INK_MUTED, stroke_width=1.8)
            tab_x += 54
    rect("HomeIndicator", parent, (w - 134) / 2, 796, 134, 5, "#18181B", radius=2.5)

def study_pro_banner(parent, x=20, y=240, w=335, h=136):
    """Lime green Unlock Study Pro promotional banner."""
    card = box("Banner/StudyPro", parent, x, y, w, h, LIME_HERO, radius=24, ref=f"banner-{parent}")
    oval("CrownDisc", card, 16, 16, 44, 44, LIME_DEEP)
    iconify("CrownIcon", card, "crown", 26, 26, size=24, color=WHITE, stroke_width=2.0)
    label(card, 68, 16, "Unlock Study Pro", size=16, style="Bold", color=INK_TITLE)
    label(card, 68, 38, "Upgrade your learning with unlimited\naccess to premium perks.", size=11.5, style="Medium", color=INK_BODY)
    btn = box("Button/Upgrade", card, 16, 80, w - 32, 42, WHITE, radius=21, ref=f"btn-up-{parent}")
    label(btn, 0, 12, "+ Upgrade to Pro", size=13.5, style="Bold", color=INK_TITLE, align="center", w=w - 32)

def build_app():
    # ================================================================ SCREEN 1: HOME
    S1 = "Screen1"
    box("Screen/1 - Home", None, 50, 40, 375, 812, SCREEN_BG, radius=44, clip=True, ref=S1)
    status_bar(S1, w=375)

    # Profile name pill
    p_pill = box("Header/UserPill", S1, 20, 56, 154, 42, WHITE, radius=21, stroke=BORDER_LT, weight=1, ref="user_pill")
    place_avatar(p_pill, AVATAR_FEMALE, 5, 5, size=32, ref="av_female")
    label(p_pill, 42, 13, "Hello, ", size=13, style="Regular", color=INK_MUTED)
    label(p_pill, 82, 13, "Tommy!", size=13, style="Bold", color=INK_TITLE)
    iconify("ChevronDown", p_pill, "chevron_down", 132, 15, size=14, color=INK_MUTED, stroke_width=2)

    # Action button 1: Lime circle with sparkles
    btn_spark = box("Button/Magic", S1, 265, 56, 42, 42, LIME_BRIGHT, radius=21, ref="btn_spark")
    iconify("Icon/Sparkles", btn_spark, "sparkles", 11, 11, size=20, color=INK_TITLE, stroke_width=2.2)

    # Action button 2: White circle with menu icon
    btn_menu = box("Button/Menu", S1, 313, 56, 42, 42, WHITE, radius=21, stroke=BORDER_LT, weight=1, ref="btn_menu")
    iconify("Icon/Menu", btn_menu, "menu", 11, 11, size=20, color=INK_TITLE, stroke_width=2.2)

    # Hero Headings
    label(S1, 20, 118, "Need help", size=32, style="Bold", color=INK_TITLE)
    label(S1, 20, 156, "studying today?", size=32, style="Medium", color=INK_MUTED)

    # "Ask a Question" Bar
    ask_bar = box("Bar/AskQuestion", S1, 20, 206, 335, 54, WHITE, radius=27, stroke=BORDER_LT, weight=1, effects=SHADOW_SOFT, ref="ask_bar")
    ask_pill = box("Pill/Ask", ask_bar, 6, 6, 140, 42, "none", radius=21, stroke=BORDER_LT, weight=1.2, ref="ask_pill")
    label(ask_pill, 22, 13, "Ask a Question", size=13, style="SemiBold", color=INK_TITLE)

    icon_actions = [("tv", 168), ("camera", 224), ("mic", 280)]
    for ic_name, ic_x in icon_actions:
        c_btn = box(f"Btn/{ic_name}", ask_bar, ic_x, 8, 38, 38, "none", radius=19, ref=f"btn-{ic_name}")
        iconify(f"Icon/{ic_name}", c_btn, ic_name, 9, 9, size=20, color=INK_TITLE, stroke_width=1.8)

    # Unlock Study Pro Banner
    study_pro_banner(S1, x=20, y=276, w=335, h=136)

    # 3 Quick Tools Row: Math Solver, Give Answer, Textbooks
    tools_y = 428
    card_m = box("Card/MathSolver", S1, 20, tools_y, 104, 108, WHITE, radius=22, stroke=BORDER_LT, weight=1, effects=SHADOW_CARD, ref="c_math")
    oval("Disc/Math", card_m, 32, 16, 40, 40, PURPLE_BG)
    iconify("Icon/Math", card_m, "scan_face", 42, 26, size=20, color=PURPLE_INK, stroke_width=2.0)
    label(card_m, 12, 68, "Math Solver", size=12.5, style="Bold", color=INK_TITLE)

    card_g = box("Card/GiveAnswer", S1, 135, tools_y, 105, 108, MINT_BG, radius=22, ref="c_give")
    oval("Disc/Give", card_g, 32, 16, 40, 40, WHITE)
    iconify("Icon/Give", card_g, "message_check", 42, 26, size=20, color=MINT_INK, stroke_width=2.0)
    label(card_g, 14, 68, "Give Answer", size=12.5, style="Bold", color=INK_TITLE)

    card_t = box("Card/Textbooks", S1, 251, tools_y, 104, 108, WHITE, radius=22, stroke=BORDER_LT, weight=1, effects=SHADOW_CARD, ref="c_text")
    oval("Disc/Text", card_t, 32, 16, 40, 40, BLUE_BG)
    iconify("Icon/Text", card_t, "book_open", 42, 26, size=20, color=BLUE_INK, stroke_width=2.0)
    label(card_t, 18, 68, "Textbooks", size=12.5, style="Bold", color=INK_TITLE)

    # "Today's Tasks" Section
    label(S1, 20, 554, "Today's Tasks", size=16, style="Bold", color=INK_TITLE)
    label(S1, 305, 556, "View All", size=12, style="SemiBold", color=INK_MUTED)

    task1 = box("Card/Task1", S1, 20, 584, 335, 68, WHITE, radius=20, stroke=BORDER_LT, weight=1, effects=SHADOW_SOFT, ref="task1")
    oval("Disc/Task1", task1, 14, 14, 40, 40, MINT_BG)
    iconify("Icon/Play", task1, "play", 25, 25, size=18, color=MINT_INK, stroke_width=2.0)
    label(task1, 64, 15, "Video Lessons", size=14, style="Bold", color=INK_TITLE)
    label(task1, 64, 37, "Learn with expert-guided tutorials", size=11, style="Medium", color=INK_MUTED)
    iconify("Icon/Arrow1", task1, "arrow_up_right", 298, 25, size=18, color=INK_MUTED, stroke_width=2.0)

    task2 = box("Card/Task2", S1, 20, 662, 335, 60, WHITE, radius=20, stroke=BORDER_LT, weight=1, opacity=0.7, ref="task2")
    oval("Disc/Task2", task2, 14, 10, 40, 40, "#F3F4F6")
    iconify("Icon/Spark2", task2, "sparkles", 25, 21, size=18, color=INK_MUTED, stroke_width=2.0)
    label(task2, 64, 14, "AI Study Tips", size=14, style="Bold", color=INK_TITLE)

    bottom_nav(S1, active_tab="home")

    # ================================================================ SCREEN 2: AI STUDY BUDDY
    S2 = "Screen2"
    box("Screen/2 - AI Study Buddy", None, 465, 40, 375, 812, SCREEN_BG, radius=44, clip=True, ref=S2)
    status_bar(S2, w=375)

    btn_back2 = box("Button/Back2", S2, 20, 56, 42, 42, WHITE, radius=21, stroke=BORDER_LT, weight=1, ref="btn_back2")
    iconify("Icon/Back2", btn_back2, "arrow_left", 11, 11, size=20, color=INK_TITLE, stroke_width=2.2)

    title_pill = box("Pill/BuddyTitle", S2, 105, 56, 165, 42, WHITE, radius=21, stroke=BORDER_LT, weight=1, ref="title_pill")
    iconify("Icon/SparkTitle", title_pill, "sparkles", 14, 12, size=18, color=INK_TITLE, stroke_width=2.0)
    label(title_pill, 38, 13, "AI Study Buddy", size=13.5, style="Bold", color=INK_TITLE)

    btn_menu2 = box("Button/Menu2", S2, 313, 56, 42, 42, WHITE, radius=21, stroke=BORDER_LT, weight=1, ref="btn_menu2")
    iconify("Icon/Menu2", btn_menu2, "menu", 11, 11, size=20, color=INK_TITLE, stroke_width=2.2)

    # Central Glowing Robot Mascot
    robot_center_x = 375 / 2
    robot_center_y = 230

    oval("HaloRing1", S2, robot_center_x - 70, robot_center_y - 70, 140, 140, MINT_BG, opacity=0.6)
    oval("HaloRing2", S2, robot_center_x - 50, robot_center_y - 50, 100, 100, "#BEF264")
    oval("HaloDisc3", S2, robot_center_x - 35, robot_center_y - 35, 70, 70, LIME_BRIGHT)
    vec("OrbitArc", S2, "M 20 60 C 10 30, 30 10, 60 4", robot_center_x - 68, robot_center_y - 68, 60, 60, "none", stroke="#65A30D", weight=1.5, strokeCap="round")

    robot_g = box("Mascot/Robot", S2, robot_center_x - 22, robot_center_y - 18, 44, 36, "none", ref="robot_mascot")
    rect("AntennaStem", robot_g, 20, 0, 3, 6, INK_TITLE, radius=1)
    oval("AntennaBall", robot_g, 19, -3, 5, 5, INK_TITLE)
    rect("RobotHead", robot_g, 2, 6, 40, 30, INK_TITLE, radius=12)
    rect("EarL", robot_g, 0, 14, 3, 14, INK_TITLE, radius=1.5)
    rect("EarR", robot_g, 41, 14, 3, 14, INK_TITLE, radius=1.5)
    oval("RobotEyeL", robot_g, 11, 16, 6, 7, LIME_BRIGHT)
    oval("RobotEyeR", robot_g, 27, 16, 6, 7, LIME_BRIGHT)
    oval("RobotPupilL", robot_g, 13, 17, 3, 4, INK_TITLE)
    oval("RobotPupilR", robot_g, 29, 17, 3, 4, INK_TITLE)
    vec("RobotSmile", robot_g, "M 17 26 C 20 29, 24 29, 27 26", 17, 25, 10, 4, "none", stroke=LIME_BRIGHT, weight=2, strokeCap="round")

    # Large Display Headline
    label(S2, 20, 340, "How Can I Help\nYou Today?", size=32, style="SemiBold", color=INK_TITLE, align="center", w=335)

    # Subject Pill Tags Row
    subj_y = 574
    row_subj = row("Row/Subjects", S2, 16, subj_y, 343, 38, gap=8, main="min", cross="center", ref="row_subj")

    SUBJECTS = [
        ("Math", "calculator", PURPLE_BG, PURPLE_INK),
        ("Science", "flask", MINT_BG, MINT_INK),
        ("English", "book_open", BLUE_BG, BLUE_INK),
        ("History", "globe", MINT_BG, MINT_INK),
    ]
    for sname, sicon, sbg, sink in SUBJECTS:
        spill = box(f"Pill/{sname}", "row_subj", None, None, 82, 38, WHITE, radius=19, stroke=BORDER_LT, weight=1, ref=f"spill-{sname}")
        iconify(f"Icon/{sname}", spill, sicon, 10, 10, size=18, color=sink, stroke_width=2.0)
        label(spill, 32, 11, sname, size=12.5, style="Bold", color=INK_TITLE)

    # Interactive Chat Input Box
    chat_box = box("Card/ChatInput", S2, 16, 626, 343, 134, WHITE, radius=28, stroke=BORDER_LT, weight=1, effects=SHADOW_CARD, ref="chat_input")
    iconify("Icon/SparkInput", chat_box, "sparkles", 18, 18, size=18, color=INK_MUTED, stroke_width=1.8)
    label(chat_box, 44, 18, "Ask a question...", size=14, style="Medium", color=INK_LIGHT)

    btn_plus = box("Button/Plus", chat_box, 14, 76, 38, 38, WHITE, radius=19, stroke=BORDER_LT, weight=1.2, ref="btn_plus")
    iconify("Icon/Plus", btn_plus, "plus", 11, 11, size=16, color=INK_TITLE, stroke_width=2.2)

    pill_deep = box("Pill/DeepThink", chat_box, 60, 76, 126, 38, WHITE, radius=19, stroke=BORDER_LT, weight=1.2, ref="pill_deep")
    label(pill_deep, 16, 11, "Deep Think", size=13, style="Bold", color=INK_TITLE)
    iconify("Icon/ChevronDeep", pill_deep, "chevron_down", 96, 12, size=14, color=INK_TITLE, stroke_width=2.0)

    btn_mic = box("Button/Mic", chat_box, 240, 76, 38, 38, "none", radius=19, ref="btn_mic")
    iconify("Icon/Mic", btn_mic, "mic", 9, 9, size=20, color=INK_BODY, stroke_width=1.8)

    btn_send = box("Button/Send", chat_box, 286, 74, 42, 42, LIME_BRIGHT, radius=21, effects=SHADOW_SOFT, ref="btn_send")
    iconify("Icon/Send", btn_send, "send", 11, 11, size=20, color=INK_TITLE, stroke_width=2.2)

    rect("HomeIndicator2", S2, (375 - 134) / 2, 796, 134, 5, "#18181B", radius=2.5)

    # ================================================================ SCREEN 3: PROFILE
    S3 = "Screen3"
    box("Screen/3 - Profile", None, 880, 40, 375, 812, SCREEN_BG, radius=44, clip=True, ref=S3)
    status_bar(S3, w=375)

    # Header Row
    btn_back3 = box("Button/Back3", S3, 20, 56, 42, 42, WHITE, radius=21, stroke=BORDER_LT, weight=1, ref="btn_back3")
    iconify("Icon/Back3", btn_back3, "arrow_left", 11, 11, size=20, color=INK_TITLE, stroke_width=2.2)

    label(S3, 156, 66, "Profile", size=17, style="Bold", color=INK_TITLE)

    btn_gear = box("Button/Settings", S3, 313, 56, 42, 42, WHITE, radius=21, stroke=BORDER_LT, weight=1, ref="btn_gear")
    iconify("Icon/Gear", btn_gear, "settings", 11, 11, size=20, color=INK_TITLE, stroke_width=2.0)

    # Profile Card with User & Stats
    p_card = box("Card/UserProfile", S3, 20, 118, 335, 172, WHITE, radius=24, stroke=BORDER_LT, weight=1, effects=SHADOW_CARD, ref="prof_card")
    place_avatar(p_card, AVATAR_MALE, 16, 16, size=64, ref="av_male")

    label(p_card, 16, 92, "Helping Hand", size=18, style="Bold", color=INK_TITLE)
    lvl_pill = box("Badge/Level", p_card, 16, 120, 116, 24, MINT_BG, radius=12, ref="lvl_pill")
    iconify("Icon/StarLvl", lvl_pill, "star", 8, 4, size=14, color=MINT_INK, stroke_width=2.0)
    label(lvl_pill, 26, 5, "Level 5 Learner", size=11, style="Bold", color=MINT_INK)
    label(p_card, 16, 148, "Keep learning, keep growing!", size=10.5, style="Medium", color=INK_MUTED)

    # Right: 2 Stat Blocks
    stat1 = box("Box/StudyHours", p_card, 172, 16, 147, 66, WHITE, radius=16, stroke="#F3F4F6", weight=1, ref="st1")
    oval("Disc/Clock", stat1, 10, 14, 30, 30, PURPLE_BG)
    iconify("Icon/Clock", stat1, "clock", 16, 20, size=18, color=PURPLE_INK, stroke_width=2.0)
    label(stat1, 48, 14, "187h", size=18, style="Bold", color=INK_TITLE)
    label(stat1, 48, 38, "Study Hours", size=10.5, style="Medium", color=INK_MUTED)

    stat2 = box("Box/QuizCount", p_card, 172, 90, 147, 66, WHITE, radius=16, stroke="#F3F4F6", weight=1, ref="st2")
    oval("Disc/Trophy", stat2, 10, 14, 30, 30, MINT_BG)
    iconify("Icon/Trophy", stat2, "trophy", 16, 20, size=18, color=MINT_INK, stroke_width=2.0)
    label(stat2, 48, 14, "670", size=18, style="Bold", color=INK_TITLE)
    label(stat2, 48, 38, "Quiz Count", size=10.5, style="Medium", color=INK_MUTED)

    # Metrics Bar (3 Columns: XP, Quizzes, Streak)
    met_card = box("Card/MetricsBar", S3, 20, 304, 335, 86, WHITE, radius=20, stroke=BORDER_LT, weight=1, effects=SHADOW_CARD, ref="met_bar")

    oval("Disc/XP", met_card, 36, 12, 28, 28, PURPLE_BG)
    iconify("Icon/Hex", met_card, "hexagon", 41, 17, size=18, color=PURPLE_INK, stroke_width=2.0)
    label(met_card, 22, 44, "XP Points", size=10.5, style="Medium", color=INK_MUTED)
    label(met_card, 32, 60, "175", size=18, style="Bold", color=INK_TITLE)

    rect("Div1", met_card, 110, 18, 1, 50, BORDER_LT)

    oval("Disc/Quiz", met_card, 154, 12, 28, 28, BLUE_BG)
    iconify("Icon/BookQ", met_card, "book_open", 159, 17, size=18, color=BLUE_INK, stroke_width=2.0)
    label(met_card, 144, 44, "Quizzes", size=10.5, style="Medium", color=INK_MUTED)
    label(met_card, 154, 60, "99", size=18, style="Bold", color=INK_TITLE)

    rect("Div2", met_card, 222, 18, 1, 50, BORDER_LT)

    oval("Disc/Streak", met_card, 268, 12, 28, 28, PEACH_BG)
    iconify("Icon/Flame", met_card, "flame", 273, 17, size=18, color=PEACH_INK, stroke_width=2.0)
    label(met_card, 262, 44, "Streak", size=10.5, style="Medium", color=INK_MUTED)
    label(met_card, 252, 60, "05", size=18, style="Bold", color=INK_TITLE)
    label(met_card, 276, 62, "Days", size=11, style="Medium", color=INK_MUTED)

    # Unlock Study Pro Banner on Profile
    study_pro_banner(S3, x=20, y=404, w=335, h=136)

    # Action List Items
    item1 = box("Item/Saved", S3, 20, 554, 335, 68, WHITE, radius=20, stroke=BORDER_LT, weight=1, effects=SHADOW_SOFT, ref="it1")
    oval("Disc/Save", item1, 14, 14, 40, 40, PURPLE_BG)
    iconify("Icon/Bookmark", item1, "bookmark", 24, 24, size=20, color=PURPLE_INK, stroke_width=2.0)
    label(item1, 64, 15, "Saved Resources", size=14, style="Bold", color=INK_TITLE)
    label(item1, 64, 37, "Your bookmarked notes & lessons", size=11, style="Medium", color=INK_MUTED)
    iconify("Icon/Chev1", item1, "chevrons_right", 298, 25, size=18, color=INK_MUTED, stroke_width=2.0)

    item2 = box("Item/History", S3, 20, 632, 335, 68, WHITE, radius=20, stroke=BORDER_LT, weight=1, effects=SHADOW_SOFT, ref="it2")
    oval("Disc/Hist", item2, 14, 14, 40, 40, MINT_BG)
    iconify("Icon/Clip", item2, "clipboard_check", 24, 24, size=20, color=MINT_INK, stroke_width=2.0)
    label(item2, 64, 15, "Practice History", size=14, style="Bold", color=INK_TITLE)
    label(item2, 64, 37, "Track your completed exercises", size=11, style="Medium", color=INK_MUTED)
    iconify("Icon/Chev2", item2, "chevrons_right", 298, 25, size=18, color=INK_MUTED, stroke_width=2.0)

    bottom_nav(S3, active_tab="profile")

def main():
    build_app()
    script = [
        {"command": "page.setBackground", "params": {"color": CANVAS_BG}},
        {"command": "page.rename", "params": {"name": "AI Study Buddy"}},
        {"command": "command.batch", "params": {"label": "Build AI Study Buddy v2", "commands": steps}},
    ]
    
    script_path = os.path.join(SCRIPT_DIR, "ai-study-buddy-script.json")
    figcraft_path = os.path.join(SCRIPT_DIR, "ai-study-buddy.figcraft")
    preview_path = os.path.join(SCRIPT_DIR, "ai-study-buddy-preview.png")
    
    with open(script_path, "w") as f:
        json.dump(script, f, indent=1)
    print(f"Emitted script with {len(steps)} steps to {script_path}")

    print("Running figcraft-cli to generate .figcraft...")
    subprocess.run(["figcraft-cli", "run", script_path, "--out", figcraft_path], check=True)
    
    print("Rendering 2x preview png...")
    subprocess.run(["figcraft-cli", "render", "--out", preview_path, "--scale", "2", figcraft_path], check=True)
    
    # Cleanup temporary json script
    if os.path.exists(script_path):
        os.remove(script_path)
        
    print(f"Success! Generated:\n- {figcraft_path}\n- {preview_path}")

if __name__ == "__main__":
    main()
