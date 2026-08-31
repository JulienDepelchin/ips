# IPS des établissements de l'académie de Lille (Nord–Pas-de-Calais)

Moteur de recherche permettant au public de retrouver l'indice de position sociale (IPS)
des écoles, collèges et lycées de l'académie de Lille.

## Qu'est-ce que l'IPS ?

L'**indice de position sociale** est un indicateur construit par la Depp (service
statistique du ministère de l'Éducation nationale). Il résume la situation sociale
des familles des élèves d'un établissement à partir de la profession des parents.

- Plus l'IPS est **élevé**, plus le milieu social des élèves est **favorisé**.
- L'IPS moyen est calé autour de **100** au niveau national ; pour les écoles, la
  référence nationale de ce millésime est de **105,5** (colonne `ips_national` du
  fichier source).
- Il permet de comparer des établissements et de neutraliser en partie l'effet du
  recrutement social quand on analyse d'autres résultats (brevet, bac…).

## Source des données

Fichiers publiés en open data par le ministère de l'Éducation nationale sur
[data.education.gouv.fr](https://data.education.gouv.fr) :

| Niveau    | Jeu de données |
|-----------|----------------|
| Écoles    | « IPS des écoles » |
| Collèges  | « IPS des collèges » |
| Lycées    | « IPS des lycées » (IPS voie GT / voie pro) |

- **Millésime : rentrée scolaire 2023-2024.**
- Périmètre : `libelle_academie = "Lille"` (départements du Nord et du Pas-de-Calais).
- Producteur : Depp (Direction de l'évaluation, de la prospective et de la performance).

## Contenu du dépôt

| Fichier | Description |
|---|---|
| `donnees-ips-ecoles.csv` | Source brute écoles (séparateur `;`) |
| `donnees-ips-colleges.csv` | Source brute collèges |
| `donnees-ips-lycees.csv` | Source brute lycées |
| `build.py` | Script de consolidation des trois fichiers |
| `ips.json` | **Fichier consolidé consommé par l'app** (2 766 établissements) |
| `ips.csv` | Même contenu au format CSV |
| `PROMPT-LOVABLE.md` | Brief à coller dans Lovable |

## Schéma de `ips.json`

```json
{
  "type": "École | Collège | Lycée",
  "uai": "0590131X",
  "nom": "Collège Jean Jaurès",
  "commune": "Lille",
  "code_commune": "59350",
  "departement": "Nord | Pas-de-Calais",
  "secteur": "public | privé sous contrat",
  "ips": 76.0,
  "ips_gt": 130.4,   // lycées uniquement (voie générale et technologique)
  "ips_pro": 117.0,  // lycées uniquement (voie professionnelle)
  "lat": 50.641243,
  "lon": 3.011502
}
```

Pour les lycées, `ips` reprend l'IPS d'ensemble (voie GT + voie pro) quand il existe,
sinon l'IPS de la seule voie renseignée.

## Points de vigilance

- **134 écoles** (petites structures rurales, regroupements pédagogiques
  intercommunaux) n'ont **pas d'IPS publié** dans la source : `ips` y est `null`.
  L'app doit afficher « non communiqué » et non « 0 ».
- Les coordonnées `lat`/`lon` proviennent de la colonne `position` des fichiers
  source (présente pour 100 % des établissements).
- L'IPS n'est pas une note de qualité d'un établissement : c'est une photographie
  de son recrutement social.

## Régénérer `ips.json`

```bash
python build.py
```
