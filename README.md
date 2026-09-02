# IPS des établissements de l'académie de Lille (Nord–Pas-de-Calais)

Moteur de recherche public de l'**indice de position sociale (IPS)** des écoles,
collèges et lycées de l'académie de Lille, avec l'**évolution année par année
depuis 2016**.

## Qu'est-ce que l'IPS ?

Indicateur construit par la **Depp** (service statistique du ministère de
l'Éducation nationale). Il résume la situation sociale des familles des élèves d'un
établissement à partir de la profession et catégorie socioprofessionnelle (PCS)
des parents.

- Plus l'IPS est **élevé**, plus le public de l'établissement est **favorisé**.
- Ce n'est **pas** une note de qualité : c'est une photographie du recrutement social.
- Repères du dernier millésime :

| Niveau | IPS moyen national | IPS moyen académie de Lille |
|---|---|---|
| Écoles (2024-2025) | 105,8 | 98,5 |
| Collèges (2025-2026) | 106,2 | 99,8 |
| Lycées – voie GT (2025-2026) | 120,2 | 114,2 |

L'académie de Lille se situe donc **en dessous de la moyenne nationale** à tous les niveaux.

## Sources

Fichiers open data publiés par le ministère de l'Éducation nationale (Depp) sur
[data.education.gouv.fr](https://data.education.gouv.fr), tous filtrés sur
`académie = LILLE` (départements du Nord et du Pas-de-Calais).

| Niveau | Jeux de données | Millésimes |
|---|---|---|
| Écoles | `fr-en-ips_ecoles_v2` + `fr-en-ips-ecoles-ap2022` | 2016-2017 → **2024-2025** |
| Collèges | `fr-en-ips_colleges` + `fr-en-ips-colleges-ap2022` + `fr-en-ips-colleges-ap2023` | 2016-2017 → **2025-2026** |
| Lycées | `fr-en-ips_lycees` + `fr-en-ips-lycees-ap2022` + `fr-en-ips-lycees-ap2023` | 2016-2017 → **2025-2026** |

Le fichier lycées `ap2023` a été récupéré via l'API Opendatasoft (subset académie de
Lille). Les libellés propres et les coordonnées géographiques proviennent des
exports `donnees-ips-*.csv` (rentrée 2023-2024).

## Périmètre du fichier consolidé

**2 642 établissements** encore en activité : 1 980 écoles, 437 collèges, 225 lycées.

Sont **exclus** : les établissements fermés ou fusionnés (pas d'IPS sur le dernier
millésime disponible) et les ~100 petites écoles rurales sans IPS publié.

## Pourquoi tel établissement n'apparaît pas ?

La couverture est celle des **fichiers open data de la Depp**, pas celle de
l'annuaire de l'Éducation nationale. Trois cas d'absence, tous côté source :

1. **Les écoles maternelles ne sont jamais concernées.** La Depp ne calcule l'IPS
   qu'à partir du niveau élémentaire. Les ~775 maternelles du Nord et du
   Pas-de-Calais n'ont pas d'IPS (ex. à Roubaix : maternelles Albert Samain,
   Alphonse Daudet, Jacques Prévert, Paul Valéry).
2. **Environ 260 écoles élémentaires** de l'académie n'ont pas d'IPS publié
   (effectifs trop faibles, taux de réponse PCS insuffisant, ouverture récente →
   valeur « NS », non significative). Sur ~2 250 écoles élémentaires de l'annuaire,
   la Depp en couvre ~1 990. Ex. : école primaire Henri Carrette à Roubaix.
3. **Établissements fermés ou fusionnés** depuis 2016 : écartés car sans IPS sur le
   dernier millésime.

Vérifier un cas signalé : chercher l'UAI dans l'[annuaire de l'éducation](https://data.education.gouv.fr/explore/dataset/fr-en-annuaire-education/)
(nature de l'établissement = maternelle ou élémentaire ?) puis dans le jeu
`fr-en-ips-ecoles-ap2022` (l'IPS y est-il présent, ou absent / « NS » ?).

## Points de vigilance (à rappeler dans la méthodo publiée)

- **Comparabilité 2022-2023 pour le privé sous contrat** : la Depp signale une
  rupture de série pour les établissements privés à cette date (meilleure remontée
  des PCS des deux parents). L'évolution avant / après 2022-2023 d'un établissement
  privé est donc à interpréter avec prudence.
- **Le dernier millésime diffère selon le niveau** : écoles arrêtées à 2024-2025,
  collèges et lycées à 2025-2026.
- **14 écoles** sans coordonnées géographiques (non retrouvées dans les fichiers
  géolocalisés) : pas de point sur la carte, mais présentes dans la recherche.
- L'IPS d'un lycée « d'ensemble » combine voie générale et technologique (GT) et
  voie professionnelle (PRO) ; `ips_gt` et `ips_pro` sont fournis séparément.

## Fichiers du dépôt

| Fichier | Rôle |
|---|---|
| `ips.json` | **Fichier consommé par l'app** (2 642 établissements + historique) |
| `ips.csv` | Même contenu, une colonne par millésime |
| `build.py` | Script de consolidation (reproductible depuis les CSV du dépôt) |
| `PROMPT-LOVABLE.md` | Brief à coller dans Lovable |
| `donnees-ips-*.csv` | Exports source rentrée 2023-2024 (libellés + géoloc) |
| `fr-en-ips*.csv` | Séries historiques source |

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
  "ips": 76.2,                 // dernier millésime disponible
  "annee": "2025-2026",
  "ips_gt": 130.4,             // lycées : voie générale et technologique
  "ips_pro": 117.0,            // lycées : voie professionnelle
  "evolution": 4.3,            // IPS dernier millésime − IPS premier millésime connu
  "lat": 50.641243,
  "lon": 3.011502,
  "historique": [
    { "annee": "2016-2017", "ips": 71.9 },
    { "annee": "2017-2018", "ips": 72.4 },
    ...
    // pour les lycées, chaque point porte aussi "gt" et "pro" quand ils existent
  ]
}
```

## Régénérer les données

```bash
python build.py
```
