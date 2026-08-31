# Brief à coller dans Lovable

> Nouveau projet Lovable. **Glisser `ips.json` dans la zone de chat** avant d'envoyer
> le message (ou le déposer dans `public/ips.json` via GitHub après connexion du dépôt).

---

Crée une application web d'une seule page : un **moteur de recherche de l'indice de
position sociale (IPS) des établissements scolaires de l'académie de Lille**
(Nord et Pas-de-Calais), avec l'**évolution de l'IPS année par année depuis 2016**.

Inspiration à égaler côté lisibilité : `https://ips-etablissements.forge.apps.education.fr/ips-ecole/`
(recherche instantanée, grande valeur d'IPS mise en avant, graphiques sobres).
Notre plus : la **courbe d'évolution dans le temps** de chaque établissement.

## Données

Charge `ips.json` au démarrage (place-le dans `public/ips.json`, `fetch('/ips.json')`).
2 642 établissements. Schéma d'un objet :

- `type` : `"École"`, `"Collège"` ou `"Lycée"`
- `nom`, `commune`, `departement` (`"Nord"` / `"Pas-de-Calais"`), `secteur` (`"public"` / `"privé sous contrat"`)
- `uai` : identifiant officiel
- `ips` : nombre — IPS du dernier millésime disponible
- `annee` : millésime de `ips` (écoles → `"2024-2025"`, collèges et lycées → `"2025-2026"`)
- `ips_gt`, `ips_pro` : lycées uniquement (voie générale et technologique / voie pro), parfois absents
- `evolution` : écart entre l'IPS le plus récent et le plus ancien connu (ex. `+4.3`)
- `lat`, `lon` : coordonnées (parfois `null` pour quelques écoles)
- `historique` : tableau `[{ "annee": "2016-2017", "ips": 71.9 }, …]` trié par année.
  Pour les lycées, chaque point porte aussi `gt` et `pro` quand ils existent.

## Fonctionnalités

### 1. Recherche
- Barre de recherche en haut, **autofocus**, filtrage en temps réel (pas de bouton).
- Cherche dans le **nom de l'établissement** ET le **nom de la commune**.
- Insensible à la casse ET aux accents. Normalise aussi « Saint / St » et les tirets
  (« st-omer », « saint omer », « Saint-Omer » doivent tous matcher).

### 2. Filtres (boutons / segments cliquables, pas des menus déroulants)
- Type : Tous / École / Collège / Lycée
- Département : Tous / Nord / Pas-de-Calais
- Secteur : Tous / Public / Privé sous contrat
- Tri : IPS décroissant (défaut) / IPS croissant / A→Z

### 3. Liste de résultats — cartes compactes
Chaque carte affiche :
- **Nom** en gras ; sous-titre `commune (département)`.
- Deux petits badges : type, secteur.
- **IPS en gros à droite**, avec une **pastille de couleur** (voir échelle plus bas)
  et, dessous, l'année (`2025-2026`) en petit.
- **Mini-courbe (sparkline)** de `historique` : ~60 × 22 px, sans axes, juste la ligne.
- La variation `evolution` avec flèche et signe : `▲ +4,3` en vert si positif,
  `▼ −2,1` en rouge si négatif, gris si ~0.
- Pour un lycée : sous l'IPS, `voie GT : 130,4 · voie pro : 117,0` en petit
  (masquer une voie absente).
- Nombres à la française : une décimale, virgule (`76,2`).
- Toute la carte est **cliquable** → ouvre le détail (accordéon qui se déplie
  sous la carte, ou panneau latéral). Une seule fiche ouverte à la fois.

### 4. Fiche détail (au clic sur une carte)
- **Grande courbe d'évolution de l'IPS** (2016-2017 → dernier millésime) :
  - axe X = années, axe Y = IPS, valeurs au survol (tooltip : année + IPS).
  - points marqués, ligne lissée légère.
  - une **ligne horizontale de référence** = IPS moyen national du niveau :
    écoles 105,8 · collèges 106,2 · lycées (voie GT) 120,2. Légende : « moyenne nationale ».
  - pour un **lycée**, proposer un petit sélecteur : Ensemble / Voie GT / Voie pro
    (utilise `gt` / `pro` de `historique`).
  - pour un établissement **privé sous contrat**, afficher sous la courbe une note :
    « Rupture de série en 2022-2023 pour le privé : l'évolution avant / après cette
    date est à interpréter avec prudence (source : Depp). »
- Rappel : commune, secteur, IPS du dernier millésime. **Ne pas afficher l'UAI**
  (ne parle à personne).
- **Positionnement** : une petite barre / jauge situant l'établissement entre le
  minimum et le maximum observés dans l'académie pour son niveau (calcule les bornes
  à partir des données chargées). Optionnel : son rang (« 128ᵉ IPS sur 437 collèges
  de l'académie »).
- **Pas de carte** dans la fiche (n'apporte rien) — ne pas charger Leaflet.

### 5. Échelle de couleur de l'IPS
Dégradé sobre, continu si possible, sinon 3 paliers :
- IPS < 90 : rouge / orangé
- 90 – 115 : neutre (gris-bleu)
- > 115 : vert
Couleurs douces, pas saturées. Même code couleur pour la pastille et la sparkline.
Cette échelle rouge/neutre/vert reste indépendante du bleu de marque (voir ci-dessous).

### Identité visuelle — charte La Voix du Nord
- **Bleu VDN `#0854e8`** : couleur d'accent principale (titre, liens, focus, et
  surtout les **filtres actifs**).
- Gris anthracite `#23242D` pour le texte principal, blanc / gris très clair pour les fonds.
- **Bloc filtres mis en avant** : conteneur avec un léger fond bleuté
  (`#0854e8` à ~6 % d'opacité) ou une bordure, un peu d'air autour. Labels
  `TYPE / DÉPARTEMENT / SECTEUR / TRI` en bleu VDN.
- Chip de filtre **actif** : fond `#0854e8`, texte blanc. **Inactif** : fond blanc,
  bordure gris clair, texte anthracite ; au survol, fond bleu très pâle.
- Barre de recherche : bordure qui passe au bleu VDN au focus.

### 6. Cadre et contexte
- **Header minimal** : titre « IPS des écoles, collèges et lycées du Nord et du
  Pas-de-Calais » + une ligne : « Indice de position sociale — évolution depuis 2016.
  Académie de Lille. »
- **Compteur** de résultats qui se met à jour : « 2 642 établissements » →
  « 214 résultats ».
- **N'afficher que les 10 premiers résultats**, jamais plus, pas de bouton
  « Afficher plus » ni de défilement infini. Si le filtre renvoie plus de 10
  résultats, message sous la liste : « Seuls les 10 premiers sont affichés
  (triés par IPS décroissant). Affinez votre recherche ou utilisez les filtres. »
  La frappe dans la recherche doit rester fluide (mémoïser le filtrage).
- **Bloc dépliable « Comprendre l'IPS »** (fermé par défaut) :
  « L'indice de position sociale (IPS) résume le milieu social des familles des
  élèves d'un établissement, d'après la profession des parents. Plus il est élevé,
  plus le public est favorisé. Moyenne nationale : environ 106 (105,8 pour les
  écoles, 106,2 pour les collèges) ; l'académie de Lille est en dessous à tous les
  niveaux. L'IPS ne mesure pas la qualité d'un établissement.
  Pour le privé sous contrat, les valeurs d'avant et d'après 2022-2023 ne sont pas
  strictement comparables.
  Source : ministère de l'Éducation nationale (Depp), data.education.gouv.fr.
  Millésimes : écoles jusqu'à 2024-2025, collèges et lycées jusqu'à 2025-2026. »
- **Pied de page** sur une ligne : source + « Données 2016 à 2026 · Depp ».

## Contraintes d'affichage — l'app sera embarquée en iframe dans un article

- **Conçois d'abord pour une colonne étroite (≈ 360–800 px de large)** : l'app sera
  quasiment toujours en mode « mobile », quel que soit l'appareil du lecteur.
  Tout doit rester **utilisable à la souris** (clic, molette), pas seulement au doigt.
- Responsive via `window.matchMedia` ou media queries CSS — **jamais** une lecture
  unique de `window.innerWidth`.
- Pas de hauteur fixe imposée en dur ; laisse le contenu déterminer la hauteur,
  garde l'ensemble compact (accordéons repliés par défaut, pas de grands vides).
- Design sobre et journalistique : typographie lisible, beaucoup de blanc, palette
  neutre + une couleur d'accent, pas d'animations superflues.
- Interface **100 % en français**.

## Pour plus tard (pas dans cette version)

Comparateur multi-établissements, export, carte plein écran de tous les
établissements, partage d'une fiche par URL.
