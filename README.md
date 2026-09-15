# StopSlopAMO

AI-writing slop detection for **DesarrollAMO**.

## Principle
**No templates.** The tool exists to make decisions specific to each client, audience, domain and project.

## v0.1
- portable agent skill in `SKILL.md`
- deterministic local core in `src/tool.py`
- smoke tests
- runnable example
- explicit provenance

## Run
```powershell
python src/tool.py examples/input.json
python -m unittest discover -s tests -v
```

## Agent compatibility
Designed to be readable by Codex/ChatGPT workflows, Claude Code, Cursor and other agents with filesystem access.

## Provenance
Original DesarrollAMO implementation. Conceptually inspired by https://github.com/hardikpandya/stop-slop. No upstream source code is vendored in v0.1.

## License
MIT for original DesarrollAMO code.
