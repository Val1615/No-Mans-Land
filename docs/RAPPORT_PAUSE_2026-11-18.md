# Rapport d'avancement : pause du 18/11/2026 (Régie)

Ce rapport fait le point au moment où Valentin met No Man's Land en pause. Il sert à reprendre sans relire les conversations, pour un agent de l'équipe, pour ChatGPT ou pour Valentin. Le jeu publié est sur https://val1615.github.io/No-Mans-Land/ et le dernier commit de main au moment du rapport est `7768653`.

## 1. Ce qui est en jeu

### Chargement
- Le monogramme NML est en jeu (`f3429cc`) : un hexagone, un anneau qui porte le vrai pourcentage, et la légende « SECTEUR n % ».
- Reste à faire : le correctif du chargement, mis de côté jusqu'à ce que le visuel soit validé.

### Mega-Line et terminus
La refonte de la ligne et du terminus de fret est faite à partir des artworks d'Ocre, et elle est close de notre côté (`67d923e`). Côté terminus :
- la halle a ses nervures, son éclairage au sodium et ses alarmes ;
- le mât de fin de voie est en place ;
- le portique et les conteneurs deviennent transparents quand ils cachent le joueur ;
- en 390, le cadrage ne laisse plus de bande noire.

Valentin doit encore juger le résultat sur Pages.

### Rencontres aléatoires
La consigne complète est dans `docs/rencontres/CONSIGNE.md`, et le suivi détaillé dans `docs/rencontres/README.md`, qui est le point d'entrée du chantier.

Ce que fait le système :
- **Tirage** : une rencontre est tirée à l'entrée de chaque case, aux taux de base de `src/data/nml.js`, sans les gonfler. Un réglage central, `RENCONTRES_FREQUENCE = 1`, permet de changer la fréquence globale.
- **Répétitions** : le jeu garde en mémoire les 3 dernières rencontres, sans jamais tirer la même deux fois de suite. Les événements uniques sont marqués par un drapeau de monde.
- **Arrêt et reprise** : le marqueur s'arrête et le temps se met en pause. Le jeu charge une vraie scène isométrique. À la sortie, il revient sur la carte, en halte ou en reprenant le trajet.
- **Sauvegarde** : elle fonctionne dans la scène hors combat. Une sauvegarde automatique est faite juste avant chaque combat.
- **Lumière** : elle suit l'heure du voyage (jour, ou nuit avec une seule source visible). La nuit, les personnages ont un liseré de lune.
- **Mode DEV** : une section Rencontres, ou `?rencontre=<id>` dans l'adresse, permet de forcer une scène.

## 2. Les huit rencontres de la consigne

| N° | Rencontre | État | Fiche ou scène |
|---|---|---|---|
| 01 | Convoi ensablé | fiche écrite, pas en jeu | `CONVOI.md` (4 cargaisons en variantes) |
| 02 | Caravane marchande | **en jeu** | « La citerne qui respire » (`?rencontre=caravane_relais`) |
| 03 | Voyageur blessé | **en jeu** | « Le témoin sous les pins » (`1c73446`, `b8e1de4`) |
| 04 | Péage des pillards | **en jeu**, à compléter : intimider, contourner | « L'appât de la piste » (`?rencontre=embuscade_piste`) |
| 05 | Mutants errants (hostiles) | fiche écrite, pas en jeu | `ERRANTS.md`, « Les Brûlés » |
| 06 | Patrouille du Service (IO) | fiche écrite, pas en jeu | `PATROUILLE.md`, poste routier |
| 07 | Tempête de poussière | fiche écrite, pas en jeu | `TEMPETE.md` |
| 08 | Faune mutante | **en jeu** | « L'écluse des Verriers » (`?rencontre=ecluse_verriers`), harde de pécaris |

Quatre rencontres sont jouables et les quatre autres sont prêtes à être produites. Les fiches restantes réutilisent les modules du désert et du verre, avec peu de nouvelles clés.

## 3. Travail en cours, non publié
- Rivet a commencé deux corrections du témoin : le soin doit vraiment rendre des points de vie, et frapper Roque doit lancer un vrai combat. Elles sont commitées sur la branche locale `wip/convoi` de Rivet (`f521c8f`), non testées et pas encore sur GitHub. Il les reprendra avec le convoi.

Le volet DA (sprites manquants par rencontre) est tenu par Ocre dans `rencontres/ETAT_DA.md`.

## 4. Ordre de reprise
1. Le convoi ensablé (01), avec les deux corrections du témoin. Ce sont les premières variantes déclarées.
2. La patrouille du Service (IO) (06) au poste routier, avec un poids par région et par faction.
3. La tempête de poussière (07), avec le voile de poussière.
4. Les mutants errants (05), avec l'action « bruit » pour détourner l'attention.
5. Le péage (04) : ajouter « intimider » et « contourner ».
6. Ensuite seulement, la phase D : la finition, les variantes et la liste « À reprendre en phase D » du README.

## 5. Règles de travail en vigueur
- Production d'abord, finition ensuite : aucune retouche visuelle tant que les huit rencontres ne sont pas jouables.
- Par lot, on fait les cinq tests de la consigne (§15) et une seule passe de captures en 1280 et en 390. Les grosses suites de tests seulement aux jalons.
- Aucune action proposée au joueur ne doit rester sans effet (§17).
- On ne déforme jamais un sprite. Les décors racontent quelque chose, et chaque lumière a une source visible.
- Les drapeaux `monde_*` (filière, Mateo, Lena) ne servent qu'à des répliques et à des indices, sans aucune conséquence de quête, tant que Valentin n'a pas validé le lore.

## 6. En attente de Valentin
- Le lore introduit, détaillé dans les §13 de `MUTANTS.md` et `SURVIVANT.md` :
  - le verre comme territoire mutant ;
  - la filière de Remedios ;
  - Ines ;
  - les pécaris ;
  - la forêt occidentale ;
  - Mateo, emmené par le Service (IO).
- Le jugement sur Pages de la Mega-Line, du terminus et du monogramme.
