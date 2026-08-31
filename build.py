"""
Consolide les fichiers IPS open data (académie de Lille) en un fichier ips.json
avec, pour chaque établissement encore en activité, la série temporelle de son IPS.

Sources (data.education.gouv.fr, DEPP) :
  Écoles    : fr-en-ips_ecoles_v2.csv (2016-17 -> 2021-22)
              fr-en-ips-ecoles-ap2022.csv (2022-23 -> 2024-25)
  Collèges  : fr-en-ips_colleges.csv (2016-17 -> 2021-22)
              fr-en-ips-colleges-ap2022.csv (2022-23)
              fr-en-ips-colleges-ap2023.csv (2023-24 -> 2025-26)
  Lycées    : fr-en-ips_lycees.csv (2016-17 -> 2021-22)
              fr-en-ips-lycees-ap2022.csv (2022-23)
              fr-en-ips-lycees-ap2023.csv (2023-24 -> 2025-26)
  Métadonnées (libellés propres + coordonnées) : donnees-ips-*.csv (rentrée 2023-24)
"""
import pandas as pd, json, os, re

B = os.path.dirname(os.path.abspath(__file__))
YEARS = ["2016-2017", "2017-2018", "2018-2019", "2019-2020", "2020-2021",
         "2021-2022", "2022-2023", "2023-2024", "2024-2025", "2025-2026"]
LAST = {"École": "2024-2025", "Collège": "2025-2026", "Lycée": "2025-2026"}


def load(f):
    return pd.read_csv(os.path.join(B, f), sep=";", dtype=str, encoding="utf-8-sig")


def num(x):
    try:
        v = float(x)
    except (ValueError, TypeError):
        return None
    if v != v:  # NaN
        return None
    return round(v, 1)


def pos(p):
    if not isinstance(p, str) or "," not in p:
        return (None, None)
    a, b = p.split(",", 1)
    try:
        return (round(float(a), 6), round(float(b), 6))
    except ValueError:
        return (None, None)


def titlecase_fr(s):
    """Remet en casse lisible un libellé tout en majuscules."""
    if not s or s != s.upper():
        return s
    small = {"de", "du", "des", "la", "le", "les", "et", "à", "d", "l", "en", "sur", "sous", "lès", "les"}
    out = []
    for i, w in enumerate(re.split(r"([ \-']+)", s.lower())):
        if re.match(r"[ \-']+", w) or not w:
            out.append(w)
        elif w in small and i != 0:
            out.append(w)
        else:
            out.append(w[:1].upper() + w[1:])
    return "".join(out)


rec = {}   # uai -> dict


def entry(uai, typ):
    return rec.setdefault(uai, {"type": typ, "uai": uai, "hist": {}})


# ---------------------------------------------------------------- ÉCOLES
for f in ["fr-en-ips_ecoles_v2.csv", "fr-en-ips-ecoles-ap2022.csv"]:
    d = load(f)
    nom_c = "Nom de l'établissment" if "Nom de l'établissment" in d.columns else "Nom de l'établissement"
    for _, r in d.iterrows():
        e = entry(r["UAI"], "École")
        e["hist"][r["Rentrée scolaire"]] = {"ips": num(r["IPS"])}
        e.update(nom=r[nom_c], commune=r["Nom de la commune"], code_commune=r["Code INSEE de la commune"],
                 departement=r["Département"], secteur=r["Secteur"].lower())

# ---------------------------------------------------------------- COLLÈGES
for f in ["fr-en-ips_colleges.csv", "fr-en-ips-colleges-ap2022.csv"]:
    d = load(f)
    for _, r in d.iterrows():
        e = entry(r["UAI"], "Collège")
        e["hist"][r["Rentrée scolaire"]] = {"ips": num(r["IPS"])}
        e.update(nom=r["Nom de l'établissment"], commune=r["Nom de la commune"],
                 code_commune=r["Code INSEE de la commune"], departement=r["Département"],
                 secteur=r["Secteur"].lower())
d = load("fr-en-ips-colleges-ap2023.csv")
for _, r in d.iterrows():
    e = entry(r["UAI"], "Collège")
    e["hist"][r["Année scolaire"]] = {"ips": num(r["IPS"])}
    lat, lon = pos(r["Latitude et longitude WGS84"])
    e.update(nom=r["Nom de l'établissement"], commune=r["Libellé commune"],
             code_commune=r["Code commune Insee"], departement=r["Libellé département"],
             secteur=r["Secteur"].lower(), lat=lat, lon=lon)

# ---------------------------------------------------------------- LYCÉES
for f in ["fr-en-ips_lycees.csv", "fr-en-ips-lycees-ap2022.csv"]:
    d = load(f)
    for _, r in d.iterrows():
        e = entry(r["UAI"], "Lycée")
        gt, pro, ens = num(r["IPS voie GT"]), num(r["IPS voie PRO"]), num(r["IPS Ensemble GT-PRO"])
        e["hist"][r["Rentrée scolaire"]] = {"ips": ens if ens is not None else (gt if gt is not None else pro),
                                            "gt": gt, "pro": pro}
        e.update(nom=r["Nom de l'établissment"], commune=r["Nom de la commune"],
                 code_commune=r["Code INSEE de la commune"], departement=r["Département"],
                 secteur=r["Secteur"].lower())
d = load("fr-en-ips-lycees-ap2023.csv")
for _, r in d.iterrows():
    e = entry(r["uai"], "Lycée")
    gt, pro, ens = num(r["ips_voie_gt"]), num(r["ips_voie_pro"]), num(r["ips_etab"])
    e["hist"][r["rentree_scolaire"]] = {"ips": ens if ens is not None else (gt if gt is not None else pro),
                                        "gt": gt, "pro": pro}
    e.update(nom=r["nom_de_l_etablissement"], commune=r["nom_de_la_commune"],
             code_commune=r["code_insee_de_la_commune"], departement=r["departement"],
             secteur=r["secteur"].lower())

# ---------------------------------------------------- MÉTADONNÉES (libellés + coords 2023-24)
meta = {}
for f, cols in [
    ("donnees-ips-ecoles.csv", ("uai", "appellation_officielle", "libelle_commune", "libelle_departement", "position")),
    ("donnees-ips-colleges.csv", ("uai", "appellation_officielle", "libelle_commune", "libelle_departement", "position")),
    ("donnees-ips-lycees.csv", ("uai", "appellation_officielle", "libelle_commune", "libelle_departement", "position")),
]:
    d = load(f)
    for _, r in d.iterrows():
        lat, lon = pos(r[cols[4]])
        meta[r[cols[0]]] = {"nom": r[cols[1]], "commune": r[cols[2]], "departement": r[cols[3]], "lat": lat, "lon": lon}

# ---------------------------------------------------------------- ASSEMBLAGE
out = []
for uai, e in rec.items():
    typ = e["type"]
    m = meta.get(uai)
    if m:
        e["nom"] = m["nom"]
        e["commune"] = m["commune"]
        e["departement"] = m["departement"]
        if e.get("lat") is None:
            e["lat"], e["lon"] = m["lat"], m["lon"]
    e["nom"] = titlecase_fr(e["nom"])
    e["commune"] = titlecase_fr(e["commune"])
    e["departement"] = {"NORD": "Nord", "PAS-DE-CALAIS": "Pas-de-Calais"}.get(
        e["departement"], e["departement"])
    e.setdefault("lat", None)
    e.setdefault("lon", None)

    hist_raw = e.pop("hist")
    hist = []
    for y in YEARS:
        if y in hist_raw and hist_raw[y]["ips"] is not None:
            item = {"annee": y, "ips": hist_raw[y]["ips"]}
            if typ == "Lycée":
                if hist_raw[y].get("gt") is not None:
                    item["gt"] = hist_raw[y]["gt"]
                if hist_raw[y].get("pro") is not None:
                    item["pro"] = hist_raw[y]["pro"]
            hist.append(item)

    # on ne garde que les établissements encore en activité :
    # un IPS publié sur le dernier millésime disponible pour leur niveau
    if not hist or hist[-1]["annee"] != LAST[typ]:
        continue

    cur = hist[-1]
    e["ips"] = cur["ips"]
    e["annee"] = cur["annee"]
    if typ == "Lycée":
        e["ips_gt"] = cur.get("gt")
        e["ips_pro"] = cur.get("pro")
    first = hist[0]
    e["evolution"] = round(cur["ips"] - first["ips"], 1) if len(hist) >= 2 else None
    e["historique"] = hist
    out.append(e)

order = {"École": 0, "Collège": 1, "Lycée": 2}
out.sort(key=lambda d: (order[d["type"]], -(d["ips"] or 0)))

# ---------------------------------------------------------------- CONTRÔLES
import collections
print("Établissements retenus :", len(out), dict(collections.Counter(d["type"] for d in out)))
for t in ["École", "Collège", "Lycée"]:
    sub = [d for d in out if d["type"] == t]
    multi = sum(1 for d in sub if len(d["historique"]) >= 2)
    nocoord = sum(1 for d in sub if d["lat"] is None)
    span = collections.Counter(len(d["historique"]) for d in sub)
    print(f"  {t}: {len(sub)} | courbe >=2pts: {multi} | sans coord: {nocoord} | "
          f"IPS {min(d['ips'] for d in sub)}–{max(d['ips'] for d in sub)} | millésime réf: {LAST[t]}")
print("Départements :", dict(collections.Counter(d["departement"] for d in out)))
print("Secteurs :", dict(collections.Counter(d["secteur"] for d in out)))

with open(os.path.join(B, "ips.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, separators=(",", ":"))

flat = []
for d in out:
    row = {k: d[k] for k in ["type", "uai", "nom", "commune", "code_commune", "departement",
                             "secteur", "ips", "annee", "evolution", "lat", "lon"]}
    row["ips_gt"] = d.get("ips_gt")
    row["ips_pro"] = d.get("ips_pro")
    for y in YEARS:
        row[y] = next((h["ips"] for h in d["historique"] if h["annee"] == y), None)
    flat.append(row)
pd.DataFrame(flat).to_csv(os.path.join(B, "ips.csv"), index=False, encoding="utf-8-sig")

print("\nips.json :", round(os.path.getsize(os.path.join(B, "ips.json")) / 1024), "Ko")
print("Exemple :", json.dumps(out[0], ensure_ascii=False)[:400])
