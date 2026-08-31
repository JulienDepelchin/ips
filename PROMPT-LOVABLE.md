# Brief à coller dans Lovable

> Copier-coller le bloc ci-dessous dans un nouveau projet Lovable.
> **Avant d'envoyer le message, glisser le fichier `ips.json` dans la zone de chat**
> (ou le déposer dans `public/ips.json` via GitHub après connexion du dépôt).

---

Crée une application web d'une seule page : un **moteur de recherche de l'indice de
position sociale (IPS) des établissements scolaires de l'académie de Lille**
(Nord et Pas-de-Calais), rentrée 2023-2024.

## Données

Utilise le fichier `ips.json` que je te fournis (2 766 établissements). Charge-le au
démarrage (place-le dans `public/ips.json` et `fetch('/ips.json')`). Schéma d'un objet :

- `type` : "École", "Collège" ou "Lycée"
- `nom`, `commune`, `departement` ("Nord" / "Pas-de-Calais"), `secteur` ("public" / "privé sous contrat")
- `uai` : identifiant officiel de l'établissement
- `ips` : nombre (ex. 76.0) ou `null` si non communiqué
- `ips_gt`, `ips_pro` : pour les lycées uniquement (voie générale et technologique / voie professionnelle)
- `lat`, `lon` : coordonnées

## Fonctionnalités

1. **Barre de recherche** en haut, avec autofocus. Filtre en temps réel (sans bouton)
   sur le **nom de l'établissement** ET le **nom de la commune**, insensible à la
   casse et aux accents.
2. **Filtres** (boutons/segments cliquables, pas des menus déroulants si possible) :
   - Type : Tous / École / Collège / Lycée
   - Département : Tous / Nord / Pas-de-Calais
   - Secteur : Tous / Public / Privé sous contrat
3. **Tri** : par IPS décroissant (défaut), IPS croissant, ordre alphabétique.
4. **Liste de résultats** en cartes compactes. Chaque carte affiche :
   - Nom de l'établissement (en gras)
   - Commune + département en sous-titre
   - Deux petits badges : type, secteur
   - **L'IPS en gros à droite**. Si `ips` est `null`, afficher « non communiqué »
     en gris (jamais « 0 »).
   - Pour un lycée, afficher sous l'IPS d'ensemble deux mentions discrètes :
     « voie GT : 130,4 · voie pro : 117,0 » (masquer une voie si sa valeur est `null`).
   - Nombres formatés à la française : une décimale, séparateur virgule (`76,0`).
5. **Pastille de couleur** sur la valeur d'IPS selon un dégradé sobre :
   rouge/orangé sous 90, neutre autour de 100-110, vert au-dessus de 120.
   Utilise une échelle continue lisible, pas des couleurs criardes.
6. **Compteur** : « 2 766 établissements » qui se met à jour selon les filtres
   (« 214 résultats »).
7. Si plus de 100 résultats, n'affiche que les 100 premiers avec un bouton
   « Afficher plus » (ou un défilement infini). La recherche doit rester fluide.
8. **Bloc d'aide dépliable** (fermé par défaut) : « Qu'est-ce que l'IPS ? » →
   « L'indice de position sociale résume le milieu social des familles des élèves
   d'un établissement. Plus il est élevé, plus le public est favorisé (moyenne
   nationale autour de 100 ; 105,5 pour les écoles). Il ne mesure pas la qualité
   d'un établissement. Source : ministère de l'Éducation nationale (Depp),
   data.education.gouv.fr, rentrée 2023-2024. »

## Contraintes d'affichage (l'app sera embarquée en iframe dans un article)

- **Conçois d'abord pour une colonne étroite (≈ 360–800 px de large)** : l'app sera
  presque toujours affichée en mode "mobile" quel que soit l'appareil du lecteur.
  Tout doit rester pleinement utilisable **à la souris** (clic, molette, pas
  seulement au tactile).
- Utilise `window.matchMedia` ou des media queries CSS pour le responsive,
  **jamais** une lecture unique de `window.innerWidth`.
- Pas de dépendance à des services payants (pas de Mapbox, pas de Google Maps).
- Design sobre et journalistique : typographie lisible, beaucoup de blanc, pas
  d'animations superflues. Palette neutre + une couleur d'accent.
- Interface **100 % en français**.
- Header minimal : titre « IPS des collèges, écoles et lycées du Nord et du
  Pas-de-Calais » + une ligne de contexte. Pas de pied de page volumineux :
  juste la mention de source sur une ligne.

## Pas besoin pour cette première version

Carte interactive, page de détail par établissement, export, comparateur.
On garde ça pour plus tard. L'objectif : **trouver vite l'IPS d'un établissement
qu'on cherche par son nom.**
