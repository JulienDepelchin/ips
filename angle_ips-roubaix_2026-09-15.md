# Note d'angle — L'IPS des établissements de Roubaix

*Préparé le 2026-09-15 pour un sujet sur l'IPS à Roubaix. Données : Depp, académie de Lille, millésimes 2016-2017 à 2025-2026 (écoles jusqu'à 2024-2025). Script source : `analyse_roubaix.py`.*

---

## 1. Contexte

**[ctx_01]** Roubaix est la grande ville la plus pauvre de France : 46 % de ses habitants vivent sous le seuil de pauvreté (60 % du niveau de vie médian), un record partagé avec Saint-Benoît (La Réunion) parmi les communes de plus de 20 000 habitants. Source : Insee, données Filosofi 2021-2022 ; relayé notamment par *Opinion Internationale* (août 2025).

**[ctx_02]** Cette pauvreté est un héritage direct de l'effondrement de l'industrie textile roubaisienne, qui employait des dizaines de milliers d'ouvriers. Source : Insee, dossier complet commune de Roubaix (INSEE COM-59512).

**[ctx_03]** Au niveau national, la publication des IPS par établissement a mis en évidence l'ampleur de la ségrégation scolaire : le chercheur Julien Grenet (École d'économie de Paris) estime que les « stratégies d'évitement » des familles expliquent près d'un tiers de la ségrégation sociale observée à l'école, le privé sous contrat jouant un rôle documenté dans ce mécanisme. Source : synthèse France Info / La Vie des idées, débat public sur carte scolaire et mixité sociale.

**[ctx_04]** La Depp signale elle-même une rupture de série en 2022-2023 : la comparabilité des IPS avant/après cette date « n'est pas assurée » pour le secteur privé sous contrat, en raison d'une meilleure remontée des professions des deux parents. Source : Depp, *Indice de position sociale (IPS) : actualisation 2022*, Thierry Rocher (education.gouv.fr).

---

## 2. Analyse quantitative

### ana_01 — Composition du corpus roubaisien
65 établissements avec IPS publié à Roubaix : **41 écoles** (32 publiques, 9 privées sous contrat), **12 collèges** (7 publics, 5 privés), **12 lycées** (8 publics, 4 privés). Calcul : `analyse_roubaix.py`, section ana_01.

### ana_02 — Données manquantes (à mentionner, sourcé)
- **14 écoles maternelles** à Roubaix n'ont et n'auront jamais d'IPS : la Depp ne le calcule qu'à partir du niveau élémentaire (Georges Sand, Jean Macé, Charles Perrault, Albert Camus, Linné, Alphonse Daudet, Paul Valéry, Lavoisier, Albert Samain, Jules Verne, Édouard Vaillant, Jacques Prévert, Pierre de Ronsard, Ernest Renan).
- **École primaire Henri Carrette** (publique, REP+) : niveau élémentaire réel, mais aucun IPS publié par la Depp sur aucun millésime (effectifs/taux de réponse insuffisants).
- **École élémentaire Pierre de Ronsard niveau 1** : probablement comptée sous un autre UAI (site à plusieurs niveaux).
- **2 écoles privées hors contrat** (Le Cours La Cordée, Main dans la Main) : hors du périmètre Depp par construction (public + privé sous contrat uniquement).

→ Utile pour couper court à d'éventuelles remarques de lecteurs sur des établissements « absents ».

### ana_03/04/05 — Meilleurs et pires établissements
**Écoles** (41, IPS 2024-2025) : de **62,9** (école publique Buffon) à **148,1** (école privée Jeanne d'Arc). Le podium : Jeanne d'Arc (privé, 148,1), École primaire Anatole France (**publique**, 115,6 — la seule école publique au-dessus de 100), Sainte Bernadette (privé, 102,6). Le bas de tableau est exclusivement public : Buffon (62,9), Condorcet (64,7), Lakanal (64,9), Elsa Triolet (65,3), Edgard Quinet-Paul Bert (65,5) — toutes en dessous de 66.

**Collèges** (12, IPS 2025-2026) : de **63,3** (Rosa Parks, public) à **149,2** (Jeanne d'Arc, privé). Écart de 85,9 points sur 12 établissements seulement.

**Lycées** (12, IPS 2025-2026) : de **69,4** (LP Turgot, public) à **127,7** (lycée technologique Arts Appliqués Textile, **public**). Voir caveat ana_05bis ci-dessous sur le lycée Jean Rostand.

### ana_05bis — ⚠️ Un piège méthodologique à ne pas publier tel quel : le lycée Jean Rostand
Le lycée général public Jean Rostand affiche un IPS « ensemble » de 101,5 en 2025-2026, en apparente hausse de +23 points depuis 2016 (78,5). **Cette hausse est trompeuse.** Le fichier Depp distingue depuis 2023-2024 l'IPS de la voie GT (lycée) de l'IPS post-bac (BTS) :

| Rentrée | Voie GT | Post-bac (BTS) | Ensemble |
|---|---|---|---|
| 2023-2024 | 85,9 | 97,1 | 92,3 |
| 2024-2025 | 84,9 | 119,2 | 102,1 |
| 2025-2026 | 80,7 | 123,2 | 101,5 |

La voie GT (les vrais lycéens) est stable, voire en léger recul (85,9 → 80,7). C'est la section BTS, socialement plus favorisée et en forte hausse (97,1 → 123,2), qui tire l'« ensemble » vers le haut. Avant 2023, l'IPS publié ne portait que sur la voie GT — la hausse affichée sur la longue période mélange donc deux populations différentes selon les années. **À ne présenter qu'en distinguant explicitement GT et post-bac, jamais avec le chiffre « ensemble » seul sur une longue période.**

### ana_06 — Écart public/privé, par niveau (Roubaix)
| Niveau | IPS moyen public | IPS moyen privé sous contrat | Écart |
|---|---|---|---|
| Écoles | 74,6 | 97,4 | **+22,8** |
| Collèges | 69,6 | 95,9 | **+26,3** |
| Lycées | 88,7 | 93,3 | +4,6 |

**Contre-intuitif [angle fort] :** l'écart public/privé, massif à l'école et au collège (23 à 26 points), **s'effondre au lycée** (4,6 points). Explication visible dans les données : à Roubaix, le privé sous contrat au lycée est en réalité dominé par des filières professionnelles (Saint-François d'Assise, Léonard de Vinci, 89-90 de moyenne), tandis que le public compte deux établissements nettement au-dessus de la moyenne roubaisienne (lycée technologique Arts Appliqués Textile, 127,7 ; Maxence Van Der Meersch GT, 101,3). Le clivage social à Roubaix n'est donc pas simplement « privé contre public » mais aussi une question de filière (générale/techno vs professionnelle).

### ana_07 — Roubaix face à l'académie (Nord-Pas-de-Calais) et à la France
| Niveau | Roubaix (moy.) | Académie de Lille | France |
|---|---|---|---|
| Écoles | **79,6** | 98,5 | 105,8 |
| Collèges | **80,6** | 99,8 | 106,2 |
| Lycées (voie GT, réf. officielle) | — | 114,2 | 120,2 |

Sources références académie/France : Depp, `fr-en-ips-ecoles-ap2022` (2024-2025), `fr-en-ips-colleges-ap2023` (2025-2026), `fr-en-ips-lycees-ap2023` (2025-2026) — colonnes IPS académique/national officielles.

Roubaix est donc **18 à 19 points sous la moyenne académique** (école et collège), elle-même déjà 7 à 8 points sous la moyenne nationale. Cumulé : les écoles et collèges roubaisiens affichent un IPS moyen inférieur d'environ **26 points à la moyenne nationale** — l'équivalent, sur l'échelle IPS, de l'écart entre un établissement REP+ typique et un établissement de centre-ville favorisé.

### ana_08 — Roubaix, un raccourci de l'académie entière
Écart interne (établissement le plus favorisé − le moins favorisé) :
| Niveau | Écart dans l'académie entière (2 642 étab.) | Écart à Roubaix seul (65 étab.) |
|---|---|---|
| Écoles | 99,3 points | **85,2 points** |
| Collèges | 94,9 points | **85,9 points** |
| Lycées | 87,2 points | 58,3 points |

**[Angle fort, contre-intuitif]** À l'école et au collège, l'écart social interne à Roubaix représente à lui seul **86 à 91 % de l'écart observé sur l'ensemble de l'académie de Lille** (2 642 établissements, Nord et Pas-de-Calais réunis). Autrement dit : il n'est pas nécessaire de quitter Roubaix pour trouver, en miniature, quasiment toute l'étendue des inégalités sociales scolaires du Nord–Pas-de-Calais. La fracture n'est pas seulement entre Roubaix et le reste de la région — elle traverse la ville elle-même, rue par rue, entre écoles Jeanne d'Arc (148) et Buffon (63).

### ana_09 — Une remontée en trompe-l'œil depuis 2022-2023 ?
En comparant l'évolution médiane d'une année « témoin » normale (2020-2021 → 2021-2022) à celle de l'année où la Depp signale une rupture méthodologique (2021-2022 → 2022-2023) :

| | Année témoin (normale) | Année de rupture (2022-2023) |
|---|---|---|
| Écoles publiques, académie | +0,3 | +1,0 |
| Écoles privées, académie | +0,4 | +1,4 |
| **Écoles publiques, Roubaix** | +0,8 | **+4,9** |
| **Écoles privées, Roubaix** | +0,7 | **+7,1** |

**[Angle fort, à traiter avec prudence — verif-data]** Le saut de 2022-2023 est environ **5 fois plus marqué à Roubaix que sur l'ensemble de l'académie**, et il touche identiquement le public et le privé. La Depp ne documente explicitement cette rupture que pour le privé sous contrat (meilleure remontée des PCS des deux parents). Mais le même schéma — plat ou en légère baisse de 2016 à 2021, puis bond net en 2022-2023, puis reprise d'une hausse plus modérée — s'observe systématiquement sur les écoles publiques les plus concernées (Pierre de Roubaix +9,7 en un an, Littré +6,3, Léo Lagrange +5,4).

**Hypothèse à formuler avec prudence, pas comme un fait établi :** un ajustement méthodologique nationalement documenté pour le privé pourrait avoir eu un effet mécanique plus fort à Roubaix parce que le taux de non-réponse ou de déclaration imprécise des PCS parentales y était structurellement plus élevé (chômage, emploi informel) — sa correction gonflerait alors l'IPS sans traduire une évolution sociale réelle des familles. **Cette hypothèse mériterait une question directe à la Depp ou à un chercheur (ex. Julien Grenet) avant publication** — ne pas présenter la hausse récente des IPS roubaisiens comme une amélioration sociale démontrée.

---

## 3. Angle éditorial proposé

### Affirmation centrale
Roubaix concentre, à elle seule, la quasi-totalité de l'écart social scolaire de tout le Nord–Pas-de-Calais — et la légère amélioration apparente de ses IPS depuis 2022 doit beaucoup à un artefact statistique plus qu'à un vrai progrès social.

### La tension
Le lecteur s'attend à lire « Roubaix, la plus pauvre, a les pires écoles ». C'est vrai en moyenne — mais l'histoire plus intéressante est que **la ville abrite en son sein presque tout l'éventail social de la région**, du 148 au 63, et que les chiffres récents « en hausse » sont à manier avec des pincettes.

### Ce que le lecteur doit comprendre différemment après lecture
Ce n'est pas Roubaix contre le reste de la région : c'est une fracture qui recoupe la ville elle-même, quartier par quartier, et un instrument de mesure (l'IPS) dont la précision a changé de calibre en 2022, ce qui complique toute lecture de tendance.

### Structure proposée

**§1 — Accroche [ana_08, ctx_01]**
Ouvrir directement sur le chiffre le plus fort : l'écart entre l'école Jeanne d'Arc (148) et l'école Buffon (63), toutes deux à Roubaix, à moins de 3 km l'une de l'autre — un écart presque aussi large que celui qui sépare, à l'échelle de toute l'académie de Lille, l'établissement le plus favorisé du moins favorisé.
`[SUGGESTION VISUELLE : carte de Roubaix avec les établissements positionnés et colorés par IPS — montre l'écart géographique en un coup d'œil]`

**§2 — Contexte [ctx_01, ctx_02]**
Rappeler en une phrase le statut de Roubaix, ville la plus pauvre de France (Insee), et son passé industriel textile. Ne pas s'attarder : le lecteur VDN connaît déjà Roubaix, l'angle n'est pas là.
`[éditorial]`

**§3 — Preuve : le classement complet [ana_03, ana_04, ana_05]**
Présenter les meilleurs et les pires établissements par niveau (écoles, collèges, lycées), avec le podium et le bas de tableau. Insister sur le fait que le haut du classement est presque toujours privé, le bas presque toujours public — sauf exception notable (Arts Appliqués Textile, lycée public à 127,7).
`[SUGGESTION VISUELLE : classement en barres horizontales, trié, coloré par secteur public/privé]`

**§4 — Bascule contre-intuitive : le privé n'explique pas tout [ana_06]**
Montrer que l'écart public/privé, énorme à l'école (+23) et au collège (+26), s'effondre au lycée (+4,6) — parce qu'à Roubaix le privé lycéen est surtout professionnel. Le vrai clivage lycéen est filière générale/techno vs professionnelle, pas secteur.
`[SUGGESTION VISUELLE : petit graphique à 3 paires de barres (école/collège/lycée, public vs privé)]`

**§5 — Roubaix dans la région [ana_07]**
Chiffrer l'écart avec la moyenne académique et nationale : ~19 points sous l'académie, ~26 sous la France, à l'école et au collège.
`[éditorial + ana_07]`

**§6 — Prudence sur les chiffres récents [ana_09, ctx_04]**
Section la plus délicate à rédiger : expliquer que les IPS roubaisiens progressent depuis 2022-2023, mais que ce bond est cinq fois plus fort qu'ailleurs dans l'académie, coïncide avec une révision méthodologique nationale documentée par la Depp (pour l'instant seulement pour le privé), et ne doit donc pas être présenté comme une preuve d'amélioration sociale sans vérification complémentaire. Recommandation : contacter la Depp ou un chercheur (Julien Grenet, École d'économie de Paris) avant de trancher.
`[éditorial + ana_09 + ctx_03, ctx_04]`

**§7 — Ce qui manque aux données [ana_02]**
Un encadré court : les maternelles n'ont jamais d'IPS, une poignée d'écoles élémentaires (dont Henri Carrette, REP+) n'ont pas de valeur publiée. Utile en anticipation des réactions de lecteurs.
`[SUGGESTION VISUELLE : encadré factuel, pas de graphique]`

---

## Sources
- Depp, jeux de données `fr-en-ips-ecoles-ap2022`, `fr-en-ips-ecoles_v2`, `fr-en-ips-colleges-ap2022/ap2023`, `fr-en-ips-lycees-ap2022/ap2023` (data.education.gouv.fr)
- Depp, *Indice de position sociale (IPS) : actualisation 2022*, Thierry Rocher — education.gouv.fr/depp
- Insee, dossier complet commune de Roubaix (COM-59512) ; données Filosofi 2021-2022
- Annuaire de l'éducation (`fr-en-annuaire-education`), data.education.gouv.fr
- Fichier consolidé du projet : `ips.json`, `ecoles-elementaires-sans-ips.csv`, `annuaire-ecoles-npdc.csv`
