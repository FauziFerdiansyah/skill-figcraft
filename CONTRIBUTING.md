# Contributing to FigCraft Skill Suite

Thank you for your interest in improving the **FigCraft Skill Suite**!

We welcome contributions of all kinds: adding new specialized skills (e.g. design tokens export, component variant generators), refining existing skills, fixing engine-compatibility quirks, and expanding documentation.

---

## Guiding Principles

1. **Empirical Engine Grounding:**
   * Never write a skill rule based on theoretical assumptions or standard Figma behavior without verifying it against the actual FigCraft engine (`figcraft-cli mcp`).
   * Test commands using `list_commands` and real executions to confirm exact parameter schemas and return types.
2. **Anti-Hallucination Guardrails:**
   * Do not instruct the AI agent to claim runtime verification that cannot be genuinely executed in a headless environment.
   * If an engine field is write-only (like `overflow`), provide deterministic fallback verification paths.
3. **Anti-Overengineering & YAGNI:**
   * Always enforce strict scope boundaries: never fabricate unrequested secondary screens, mock data, or unsolicited features without explicit user confirmation.

---

## Development & Testing Workflow

1. Clone this repository:
   ```bash
   git clone https://github.com/FauziFerdiansyah/skill-figcraft.git
   cd skill-figcraft
   ```
2. Ensure you have `figcraft-cli` installed and accessible in your `$PATH`.
3. Test your commands with the headless MCP session:
   ```bash
   figcraft-cli mcp
   ```
4. Verify schema definitions using:
   ```bash
   figcraft-cli commands --json --filter "<keyword>"
   ```
5. Submit your improvements via a Pull Request with a clear description of the engine behavior tested.

---

## License

By contributing to this repository, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
