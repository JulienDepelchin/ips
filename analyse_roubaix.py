"""
Analyse IPS des établissements de Roubaix pour angle éditorial.
Sources : ips.json (consolidé, voir build.py), fr-en-ips-*.csv (références
France/académie/département), ecoles-elementaires-sans-ips.csv, annuaire-ecoles-npdc.csv.

Sortie : impressions console reprises dans angle_ips-roubaix_2026-09-15.md (ana_01 à ana_09).
"""
import json, statistics, collections
import pandas as pd

B = r"D:\IPS"
d = json.load(open(f"{B}/ips.json", encoding="utf-8"))
rbx = [x for x in d if x["commune"] == "Roubaix"]


def avg(items, key="ips"):
    v = [x[key] for x in items if x.get(key) is not None]
    return round(statistics.mean(v), 1) if v else None


# ana_01 — vue d'ensemble
print("=== ana_01 : composition Roubaix ===")
for t in ["École", "Collège", "Lycée"]:
    sub = [x for x in rbx if x["type"] == t]
    print(t, len(sub), collections.Counter(x["secteur"] for x in sub))

# ana_03/04/05 — classements
print("\n=== ana_03-05 : classements par type ===")
for t in ["École", "Collège", "Lycée"]:
    sub = sorted([x for x in rbx if x["type"] == t and x["ips"] is not None], key=lambda x: -x["ips"])
    print(f"--- {t} ---")
    for x in sub:
        print(f"  {x['ips']:6.1f}  {x['secteur']:20s} {x['nom']}")

# ana_06 — écart public/privé
print("\n=== ana_06 : écart public/privé (Roubaix) ===")
for t in ["École", "Collège", "Lycée"]:
    sub = [x for x in rbx if x["type"] == t]
    pub, priv = avg([x for x in sub if x["secteur"] == "public"]), avg([x for x in sub if x["secteur"] == "privé sous contrat"])
    print(t, "public =", pub, "| privé =", priv, "| écart =", round((priv or 0) - (pub or 0), 1))

# ana_08 — écart interne Roubaix vs académie
print("\n=== ana_08 : écart interne (max-min) ===")
for t in ["École", "Collège", "Lycée"]:
    allv = [x["ips"] for x in d if x["type"] == t and x["ips"] is not None]
    rv = [x["ips"] for x in d if x["type"] == t and x["commune"] == "Roubaix" and x["ips"] is not None]
    print(t, "académie:", round(max(allv) - min(allv), 1), "| Roubaix:", round(max(rv) - min(rv), 1))

# ana_09 — rupture méthodologique 2022-2023, académie vs Roubaix
print("\n=== ana_09 : saut 2021-22 -> 2022-23 (médiane), académie vs Roubaix ===")
def deltas(items, y1, y2, secteur):
    out = []
    for x in items:
        if x["secteur"] != secteur:
            continue
        h = {p["annee"]: p["ips"] for p in x["historique"]}
        if y1 in h and y2 in h:
            out.append(h[y2] - h[y1])
    return out

ecoles = [x for x in d if x["type"] == "École"]
rbx_ecoles = [x for x in ecoles if x["commune"] == "Roubaix"]
for label, items in [("Académie", ecoles), ("Roubaix", rbx_ecoles)]:
    for sect in ["public", "privé sous contrat"]:
        witness = deltas(items, "2020-2021", "2021-2022", sect)
        jump = deltas(items, "2021-2022", "2022-2023", sect)
        print(f"{label:10s} {sect:20s} témoin(20-21->21-22)={statistics.median(witness):+.1f}  "
              f"saut(21-22->22-23)={statistics.median(jump):+.1f}  (n={len(jump)})")

# Cas Jean Rostand — contamination post-bac
print("\n=== Cas particulier : Lycée Jean Rostand (post-bac) ===")
lyap = pd.read_csv(f"{B}/fr-en-ips-lycees-ap2023.csv", sep=";", dtype=str, encoding="utf-8-sig")
sub = lyap[lyap["uai"] == "0590184E"][["rentree_scolaire", "ips_voie_gt", "ips_post_bac", "ips_etab"]]
print(sub.to_string(index=False))

# Données manquantes
print("\n=== Données manquantes Roubaix ===")
miss = pd.read_csv(f"{B}/ecoles-elementaires-sans-ips.csv", encoding="utf-8-sig")
print(miss[miss["nom_commune"] == "Roubaix"][["nom_etablissement", "categorie"]].to_string(index=False))
ann = pd.read_csv(f"{B}/annuaire-ecoles-npdc.csv", sep=";", dtype=str, encoding="utf-8-sig")
ann["nom_commune"] = ann["nom_commune"].str.title()
mat = ann[(ann["nom_commune"] == "Roubaix") & (ann["ecole_maternelle"].astype(str).str.strip() == "1")
          & (ann["ecole_elementaire"].astype(str).str.strip() != "1")]
print("Maternelles pures Roubaix (jamais d'IPS) :", len(mat))
