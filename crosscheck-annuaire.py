"""
Croise l'annuaire de l'Éducation nationale (écoles ouvertes du Nord et du
Pas-de-Calais) avec les UAI présents dans les fichiers IPS de la Depp, pour
lister les écoles de niveau élémentaire SANS IPS publié et comprendre pourquoi.

Entrée : annuaire-ecoles-npdc.csv (export API fr-en-annuaire-education) +
         fr-en-ips-ecoles-*.csv
Sortie : ecoles-elementaires-sans-ips.csv (252 écoles, catégorisées)

Rappel : les écoles maternelles ne sont jamais concernées par l'IPS.
"""
import pandas as pd

B = r"D:\IPS"

ips_uai = set()
def add(df, col):
    for _, r in df.iterrows():
        v = str(r[col]).strip()
        if v and v.upper() not in ("NS", "NAN", "NONE", ""):
            ips_uai.add(r["UAI"])

for f in ["fr-en-ips-ecoles-ap2022.csv", "fr-en-ips_ecoles_v2.csv"]:
    add(pd.read_csv(f"{B}/{f}", sep=";", dtype=str, encoding="utf-8-sig"), "IPS")

a = pd.read_csv(f"{B}/annuaire-ecoles-npdc.csv", sep=";", dtype=str, encoding="utf-8-sig")
a["nom_commune"] = a["nom_commune"].str.title()
a["a_elementaire"] = a["ecole_elementaire"].astype(str).str.strip() == "1"

elem = a[a["a_elementaire"]].copy()
elem["a_ips"] = elem["identifiant_de_l_etablissement"].isin(ips_uai)
miss = elem[~elem["a_ips"]].copy()

def categorie(r):
    nom = str(r["nom_etablissement"]).lower()
    if str(r["statut_public_prive"]) == "Privé" and "hors contrat" in nom:
        return "privé hors contrat (jamais dans l'IPS)"
    if str(r["date_ouverture"]) >= "2021-09-01":
        return "ouverte depuis 2021 (trop récente)"
    if "rpi" in nom or "niveau 1" in nom or "niveau 2" in nom or "niveau 3" in nom:
        return "site multi-niveaux / RPI (IPS souvent sous un autre UAI)"
    if str(r["statut_public_prive"]) == "Privé":
        return "privé sous contrat sans IPS publié"
    return "public sans IPS publié (effectifs faibles / NS)"

miss["categorie"] = miss.apply(categorie, axis=1)

print("=== Écoles avec niveau élémentaire, académie de Lille ===")
print(f"  annuaire (ouvertes)   : {len(elem)}")
print(f"  avec IPS Depp         : {elem['a_ips'].sum()}")
print(f"  SANS IPS Depp         : {len(miss)}")
print()
print("Par catégorie :")
print(miss["categorie"].value_counts().to_string())
print()
print("Par département :", miss["libelle_departement"].value_counts().to_dict())
print()

# cas urbains publics = les plus discutables
urb = miss[(miss["categorie"] == "public sans IPS publié (effectifs faibles / NS)")]
big = urb[urb["nom_commune"].isin(["Lille","Roubaix","Tourcoing","Dunkerque","Villeneuve-D'Ascq",
    "Douai","Valenciennes","Béthune","Calais","Boulogne-Sur-Mer","Arras","Lens","Denain",
    "Maubeuge","Wattrelos","Marcq-En-Baroeul","Armentières","Hazebrouck","Cambrai"])]
print(f"--- dont en commune urbaine (public, hors RPI/récent) : {len(big)} ---")
print(big[["identifiant_de_l_etablissement","nom_etablissement","nom_commune",
           "appartenance_education_prioritaire"]].sort_values("nom_commune").to_string(index=False))

cols = ["identifiant_de_l_etablissement","nom_etablissement","nom_commune","code_commune",
        "libelle_departement","statut_public_prive","appartenance_education_prioritaire",
        "date_ouverture","nom_circonscription","categorie"]
miss[cols].sort_values(["categorie","libelle_departement","nom_commune","nom_etablissement"]) \
    .to_csv(f"{B}/ecoles-elementaires-sans-ips.csv", index=False, encoding="utf-8-sig")
print(f"\n-> D:\\IPS\\ecoles-elementaires-sans-ips.csv ({len(miss)} lignes)")

for uai in ["0595217A"]:
    row = a[a["identifiant_de_l_etablissement"] == uai]
    if len(row):
        rr = row.iloc[0]
        print(f"\nHenri Carrette {uai} : {rr['nom_etablissement']} | {rr['nom_commune']} | "
              f"ouverte {rr['date_ouverture']} | élémentaire={rr['ecole_elementaire']} "
              f"maternelle={rr['ecole_maternelle']} | IPS Depp: {'oui' if uai in ips_uai else 'NON'}")
