import pandas as pd, json

base = r"D:\IPS"

def split_pos(p):
    if not isinstance(p, str) or "," not in p:
        return (None, None)
    a, b = p.split(",", 1)
    try:
        return (round(float(a), 6), round(float(b), 6))
    except ValueError:
        return (None, None)

def num(x):
    if x is None or pd.isna(x):
        return None
    try:
        return round(float(x), 1)
    except (ValueError, TypeError):
        return None

rows = []

e = pd.read_csv(f"{base}/donnees-ips-ecoles.csv", sep=";", dtype=str)
for _, r in e.iterrows():
    lat, lon = split_pos(r["position"])
    rows.append({"type": "École", "uai": r["uai"], "nom": r["appellation_officielle"],
                 "commune": r["libelle_commune"], "code_commune": r["code_commune"],
                 "departement": r["libelle_departement"], "secteur": r["secteur"],
                 "ips": num(r["ips"]), "lat": lat, "lon": lon})

c = pd.read_csv(f"{base}/donnees-ips-colleges.csv", sep=";", dtype=str)
for _, r in c.iterrows():
    lat, lon = split_pos(r["position"])
    rows.append({"type": "Collège", "uai": r["uai"], "nom": r["appellation_officielle"],
                 "commune": r["libelle_commune"], "code_commune": r["code_commune"],
                 "departement": r["libelle_departement"], "secteur": r["secteur"],
                 "ips": num(r["ips"]), "lat": lat, "lon": lon})

l = pd.read_csv(f"{base}/donnees-ips-lycees.csv", sep=";", dtype=str)
for _, r in l.iterrows():
    lat, lon = split_pos(r["position"])
    gt, pro, ens = num(r["ips_voie_gt"]), num(r["ips_voie_pro"]), num(r["ips_ensemble_gt_pro"])
    main = ens if ens is not None else (gt if gt is not None else pro)
    rows.append({"type": "Lycée", "uai": r["uai"], "nom": r["appellation_officielle"],
                 "commune": r["libelle_commune"], "code_commune": r["code_commune"],
                 "departement": r["libelle_departement"], "secteur": r["secteur"],
                 "ips": main, "ips_gt": gt, "ips_pro": pro, "lat": lat, "lon": lon})

df = pd.DataFrame(rows)
print("Total:", len(df))
print(df.groupby("type").size().to_dict())
print("Départements:", df.groupby("departement").size().to_dict())
print("Secteurs:", df.groupby("secteur").size().to_dict())
print("IPS manquants:", df["ips"].isna().sum(), "(petites écoles rurales / RPI, non publié dans la source)")
print("Positions manquantes:", df["lat"].isna().sum())
print("IPS min/max:", df["ips"].min(), df["ips"].max())

with open(f"{base}/ips.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, separators=(",", ":"))
df.to_csv(f"{base}/ips.csv", index=False, encoding="utf-8-sig")
print("OK -> ips.json / ips.csv")
