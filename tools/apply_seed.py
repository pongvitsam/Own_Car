"""Apply seed_data.py state block to index.html."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from seed_data import build_seed_state, render_state_js  # noqa: E402

INDEX = ROOT / "index.html"


def patch_index() -> None:
    text = INDEX.read_text(encoding="utf-8")
    state_js = render_state_js()
    new_text, n = re.subn(
        r"let state = \{[\s\S]*?\n        \};",
        state_js,
        text,
        count=1,
    )
    if n != 1:
        raise SystemExit("Could not find state block in index.html")
    new_text = new_text.replace(
        "myhome_carcare_state_v2.0",
        "myhome_carcare_state_v2.1",
    )
    INDEX.write_text(new_text, encoding="utf-8")
    state = build_seed_state()
    counts = {}
    for entry in state["maintenanceLogs"]:
        vid = entry["vehicleId"]
        if entry["type"] == "Maintenance":
            counts[vid] = counts.get(vid, 0) + 1
    print(f"Patched {INDEX}")
    print(f"Vehicles: {len(state['vehicles'])}")
    for v in state["vehicles"]:
        print(f"  {v['id']} {v['name']}: {counts.get(v['id'], 0)} maintenance logs")


if __name__ == "__main__":
    patch_index()
