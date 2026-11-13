import datetime, requests
MAIN = "https://opendata.rdw.nl/resource/m9d7-ebf2.json"
FUEL = "https://opendata.rdw.nl/resource/8ys7-d773.json"

def _months(n=4):
    d = datetime.date.today().replace(day=1)
    for _ in range(n):
        d = (d - datetime.timedelta(days=1)).replace(day=1)
        yield d

def collect():
    out = {}
    for first in _months():
        nxt = (first + datetime.timedelta(days=32)).replace(day=1)
        where = (f"voertuigsoort='Personenauto' AND datum_eerste_toelating>='{first:%Y%m%d}' "
                 f"AND datum_eerste_toelating<'{nxt:%Y%m%d}'")
        plates, offset = [], 0
        while True:
            r = requests.get(MAIN, params={"$select": "kenteken", "$where": where,
                             "$limit": 50000, "$offset": offset}, timeout=120)
            r.raise_for_status(); rows = r.json()
            plates += [x["kenteken"] for x in rows]
            if len(rows) < 50000: break
            offset += 50000
        if not plates: continue
        fuels = {}
        for i in range(0, len(plates), 300):
            q = ",".join(f"'{p}'" for p in plates[i:i+300])
            r = requests.get(FUEL, params={"$select": "kenteken,brandstof_omschrijving",
                             "$where": f"kenteken in({q})", "$limit": 50000}, timeout=120)
            r.raise_for_status()
            for x in r.json():
                fuels.setdefault(x["kenteken"], set()).add(x.get("brandstof_omschrijving"))
        bev = sum(1 for f in fuels.values() if f in ({"Elektriciteit"}, {"Elettricità"}))
        out[f"{first:%Y-%m}"] = {"total": len(plates), "bev": bev}
    return out
