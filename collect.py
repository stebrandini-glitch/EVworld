"""Lancia tutti i collector in collectors/ e aggiorna data/data.json."""
import importlib, json, pathlib, traceback
from registry import COUNTRIES
DATA = pathlib.Path("data/data.json")
data = json.loads(DATA.read_text()) if DATA.exists() else {}
report = {}
for code, *_ in COUNTRIES:
    try:
        mod = importlib.import_module(f"collectors.{code.lower()}")
    except ModuleNotFoundError:
        report[code] = "nessun collector"; continue
    try:
        new = mod.collect()
        data.setdefault(code, {}).update(new)
        report[code] = f"ok ({', '.join(sorted(new)) or 'nessun dato nuovo'})"
    except Exception:
        report[code] = "ERRORE"; traceback.print_exc()
DATA.parent.mkdir(exist_ok=True)
DATA.write_text(json.dumps(data, indent=1, sort_keys=True))
for c, r in report.items(): print(c, r)
