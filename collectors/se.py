import requests

URLS = [
    "https://api.scb.se/OV0104/v1/doris/en/ssd/TK/TK1001/TK1001A/PersBilarDrivMedel",
    "https://api.scb.se/OV0104/v1/doris/en/ssd/START/TK/TK1001/TK1001A/PersBilarDrivMedel",
]

def _meta():
    last = None
    for u in URLS:
        try:
            r = requests.get(u, timeout=60)
            r.raise_for_status()
            return u, r.json()
        except Exception as e:
            last = e
    raise last

def collect():
    url, meta = _meta()
    vars_ = {v["code"]: v for v in meta["variables"]}
    fuel_var = next(c for c in vars_ if c.lower().startswith("drivmedel") or "fuel" in vars_[c]["text"].lower())
    fuel = dict(zip(vars_[fuel_var]["values"], vars_[fuel_var]["valueTexts"]))
    print("SE carburanti:", fuel)

    tot = [k for k, t in fuel.items() if t.lower() in ("total", "all fuels", "all types of fuel", "totalt")]
    ele = [k for k, t in fuel.items() if t.lower().startswith("electricity") and "hybrid" not in t.lower()]
    if not ele:
        raise RuntimeError("Carburante elettrico non trovato, vedi elenco sopra")

    region_var = next(c for c in vars_ if c.lower() == "region")
    reg = "00" if "00" in vars_[region_var]["values"] else vars_[region_var]["values"][0]
    months = vars_["Tid"]["values"][-4:]

    query = [
        {"code": region_var, "selection": {"filter": "item", "values": [reg]}},
        {"code": fuel_var, "selection": {"filter": "all", "values": ["*"]}},
        {"code": "Tid", "selection": {"filter": "item", "values": months}},
    ]
    if "ContentsCode" in vars_:
        query.append({"code": "ContentsCode", "selection": {"filter": "all", "values": ["*"]}})
    r = requests.post(url, json={"query": query, "response": {"format": "json"}}, timeout=60)
    r.raise_for_status()

    order = [q["code"] for q in query if q["code"] != "ContentsCode"]
    fi, ti = order.index(fuel_var), order.index("Tid")
    by = {}
    for row in r.json()["data"]:
        try:
            v = int(row["values"][0])
        except ValueError:
            continue
        by.setdefault(row["key"][ti], {})[row["key"][fi]] = v

    out = {}
    for m, d in by.items():
        total = sum(d[k] for k in tot if k in d) if tot else sum(d.values())
        bev = sum(d.get(k, 0) for k in ele)
        if total > 0:
            out[m.replace("M", "-")] = {"total": total, "bev": bev}
    return out
