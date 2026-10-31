# 🎨 FigCraft MCP Skill Suite

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![FigCraft Engine](https://img.shields.io/badge/FigCraft-v0.12.1+-orange.svg)](https://github.com/storytold/figcraft)
[![Compatibility](https://img.shields.io/badge/Compatible%20With-Antigravity%20%7C%20Claude%20Code%20%7C%20Kiro-green.svg)](#installation)

A production-grade, battle-tested **Model Context Protocol (MCP) Skill Suite** that empowers AI coding assistants (Google Antigravity, Claude Code, Kiro, Cursor) to design, construct, prototype, and audit native **[FigCraft](https://github.com/storytold/figcraft)** interface files (`.figcraft`).

---\n\n## 📸 Example Showcase\n\nHere is an example mobile homescreen design reconstructed directly from a reference image using this skill suite via FigCraft MCP:\n\n<p align=\"center\">\n  <img src=\"examples/preview.png\" width=\"320\" alt=\"FigCraft Generated Preview\">\n</p>\n\n*The native design file with 100+ vector and frame layers is available at [`examples/ui.figcraft`](examples/ui.figcraft).*\n\n---

FigCraft is an open-source, high-performance, offline-first interface design tool written in Rust (a Figma-class desktop app). Its built-in MCP server (`figcraft-cli mcp`) allows AI agents to directly create nodes, manipulate vectors, and wire interactive prototypes.

However, raw MCP tools alone lack domain workflows and often lead to hallucinated behaviors. **This Skill Suite provides the expert operating procedures (SOP)**:
* **Anti-Overengineering (YAGNI):** Forbids unrequested screens and assumes nothing without user confirmation.
* **Figma-Standard Prototyping:** Proper `overflow: "horizontal"` content sliders and Smart Animate screen-to-screen transitions.
* **Engine Grounded & Anti-Hallucination:** Hardened against real FigCraft engine quirks (no false headless preview claims, safe `changeTo` wiring, and deterministic overflow verification).

---

## 🧩 The 4 Modular Skills

```
skill-figcraft/
└── skills/
    ├── figcraft/              # 1. Master Coordinator (Single point of entry & intake)
    ├── figcraft-builder/      # 2. Native Screen & Vector Construction
    ├── figcraft-prototyper/   # 3. Sliders, Navigation, Overlays & State Wiring
    └── figcraft-review/       # 4. Design Scoring (100 Pts) & Prototype Pass/Fail Gate
```

### 1. `figcraft` (Master Coordinator)
* **Path:** [`skills/figcraft/SKILL.md`](skills/figcraft/SKILL.md)
* **Role:** Single point of entry. Routes tasks sequentially: `builder` $\rightarrow$ `prototyper` $\rightarrow$ `review`.
* **Key Features:**
  * **Reference Manifest:** Maps multi-image inputs to screen frames, responsive sizes, and overlays before creating any layers.
  * **Scope Gate:** Enforces strict intake rules for text-only prompts.
  * **Definition of Done:** Verifies structure, persistence, and hand-off before claiming completion.

### 2. `figcraft-builder` (Screen & Vector Builder)
* **Path:** [`skills/figcraft-builder/SKILL.md`](skills/figcraft-builder/SKILL.md)
* **Role:** Constructs production-ready design hierarchies from image references or specifications.
* **Key Features:**
  * **Hybrid Auto-Layout:** Auto-layout (`layout: "horizontal"` | `"vertical"`) for cards, lists, tags, and date strips; absolute positioning for status chrome, FABs, and decorative vectors.
  * **Strict Non-Presumptive Sizing:** Never forces arbitrary device sizes or fonts unless indicated by the source.
  * **Native Asset Handling:** Leverages `file.import` for SVGs/PNGs rather than wasting tokens redrawing existing assets.

### 3. `figcraft-prototyper` (Interactive Prototyping)
* **Path:** [`skills/figcraft-prototyper/SKILL.md`](skills/figcraft-prototyper/SKILL.md)
* **Role:** Wires living prototypes into static screens using Figma conventions.
* **Key Features:**
  * **Horizontal Content Sliders:** Bounded viewport + auto-layout track with `overflow: "horizontal"`.
  * **Smart Animate Navigation:** Uses `proto.interaction.add` (`trigger: onClick`, `transition: smartAnimate`, `durationMs: 300`, `easing: easeInOut`).
  * **Overlays & Modals:** Bottom-sheets with outside-click dismiss and dim backdrops (`openOverlay`).
  * **Typing Boundary:** Transparently acknowledges runtime text input limits in FigCraft rather than falsely claiming arbitrary input typing.

### 4. `figcraft-review` (Quality & Accessibility Audit)
* **Path:** [`skills/figcraft-review/SKILL.md`](skills/figcraft-review/SKILL.md)
* **Role:** Automated audit for design tokens, auto-layout, and accessibility.
* **Key Features:**
  * **Design Quality Score (100 Points):**
    * Structure & Auto-Layout (40 pts)
    * Tokens & Visual Consistency (30 pts)
    * Accessibility & Usability (30 pts — validates touch targets $\ge 44\text{px}$ Apple / $24\text{px}$ WCAG 2.2 AA).
  * **Separate Pass/Fail Gates:** Reference Coverage Gate and Prototype Correctness Gate (a broken navigation flow fails the prototype gate regardless of visual aesthetics).

---

## 🛠️ Prerequisites & Setup

### 1. Install `figcraft-cli`
Download precompiled binaries from the official [FigCraft Releases](https://github.com/storytold/figcraft/releases) (or build from source via Cargo):

```bash
# Example for macOS (Universal Binary):
curl -L -o figcraft-cli.zip https://github.com/storytold/figcraft/releases/download/v0.12.1/figcraft-cli-0.12.1-macos-universal.zip
unzip figcraft-cli.zip
mv figcraft-cli-*-macos-universal/figcraft-cli ~/.local/bin/figcraft-cli
chmod +x ~/.local/bin/figcraft-cli
```

### 2. Configure MCP Server
Add FigCraft to your agent's MCP configuration (`mcp_config.json`, `~/.kiro/settings/mcp.json`, or Claude Desktop config):

```json
{
  "mcpServers": {
    "figcraft": {
      "command": "/absolute/path/to/figcraft-cli",
      "args": ["mcp"]
    },
    "figcraft-app": {
      "command": "/absolute/path/to/figcraft-cli",
      "args": ["mcp", "--attach", "7979"]
    }
  }
}
```

* **`figcraft` (Headless):** Starts an in-process headless session. Ideal for automated, high-speed background generation.
* **`figcraft-app` (Attached):** Connects to your running desktop FigCraft app started with `figcraft --control 7979` so you can watch live canvas updates!

---

## 🚀 Installing the Skills

### Option A: Global Installation (Recommended)
Copy the skills to your global agent skills directory:

* **Antigravity / Gemini CLI:**
  ```bash
  cp -r skills/* ~/.gemini/config/skills/
  ```
* **Claude Code:**
  ```bash
  cp -r skills/* ~/.claude/skills/
  ```
* **Kiro IDE:**
  ```bash
  cp -r skills/* ~/.kiro/skills/
  ```

### Option B: Project-Level Installation
Copy the skills into your project's local agent folder:
```bash
mkdir -p .agents/skills
cp -r skills/* .agents/skills/
```

---

## 🛡️ Battle-Tested Engine Discoveries

During rigorous empirical stress-testing against the live `figcraft-cli` binary, this skill suite uncovered and patched several critical edge-case behaviors:

1. **Write-Only `overflow` Property:**
   FigCraft saves `"overflow": "horizontal"` into `.figcraft` correctly, but `inspect_document` and `get_node` do not return this field. This suite teaches the AI to verify sliders through three deterministic methods (call status, track vs. viewport bounding boxes, and `.figcraft` zip inspection) rather than hallucinating.
2. **Headless `proto.preview` Reality:**
   In headless mode, `proto.preview` returns success without a window and cannot simulate interactive click-throughs. The suite prohibits false "runtime verified" claims and generates explicit manual verification checklists for the human designer.
3. **`changeTo` Variant Validation:**
   The FigCraft engine accepts `changeTo` interactions pointing to regular frames without throwing an error, but the wire fails silently during playback. The suite enforces pre-wiring checks ensuring the destination is an authentic component variant.

---

## 🤝 Contributors & Community

* **Fauzi Ferdiansyah** ([@FauziFerdiansyah](https://github.com/FauziFerdiansyah)) — Creator, Architect & Maintainer
* **Akhmad Sugiannoor** — Early MCP bridge inspiration
* **GPT-5.6-sol** — Architectural decomposition & Master Coordinator design
* **Claude** — Empirical stress-testing, engine grounding & anti-hallucination hardening
* **[storytold/figcraft](https://github.com/storytold/figcraft)** — The open-source Rust design engine

See [CONTRIBUTORS.md](CONTRIBUTORS.md) for detailed acknowledgments.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
