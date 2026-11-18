# État DA, assets et lore — pause du 18 novembre 2026 (heure de Paris)

Volet DA du rapport d'avancement, pour reprendre le chantier sans relire les conversations. Sources : les fiches de `docs/rencontres/`, le [README de suivi](README.md), `MUTANTS.md`, `CANON_ARBITRAGES.md`, et le manifeste `assets/rencontres/manifest.json` (168 clés, quatre groupes). Rien n'est produit dans ce lot.

Les maquettes (étiquetées MAQUETTE, hors dépôt) sont sur la machine de travail, dans `/workspace/nml-shots/rencontres/`.

## 1. Les huit rencontres

| N° | Fiche | Titre en jeu | État | Sprites livrés | Sprites à produire |
|---|---|---|---|---|---|
| 01 | [CONVOI.md](CONVOI.md) | Le convoi ensablé | fiche seule | aucun groupe propre ; réutilise le désert de `rc_pilote_appat` et quelques clés de `rc_caravane` (`g_rc_sable` `_b` `_c`, `g_rc_piste` `_b` `_c`, `rc_ds_talus_*`, `rc_ds_rochers_*`, `rc_ds_panneau_ufsa_3q`, `rc_car_ferraille_3q`, `rc_car_traces_3q`) | `rc_cv_camion_3q` (lampe de travail `_neon` au battant, nuit seulement), `rc_cv_cric_3q`, `rc_cv_planches_3q`, `rc_cv_langue_3q`, les quatre caisses de variante (`_med`, `_eau`, `_pieces`, `_contre`), `rc_cv_panneau_tombe_3q` seulement si le panneau UFSA ne peut pas être posé couché ; `gen_rc_nando` et `gen_rc_sola` (face, dos, portrait 192 px). Ne pas réutiliser le tracteur, la citerne, le pick-up ni l'épave du Service. |
| 02 | [CARAVANE.md](CARAVANE.md) | La citerne qui respire | en jeu | groupe `rc_caravane`, **27 clés** (décors, calques `_neon` et `_texte`, PNJ, portraits, icônes `lame_ressort`). Sols, talus, rochers et panneau UFSA viennent de `rc_pilote_appat`. | Rien de nouveau. |
| 03 | [SURVIVANT.md](SURVIVANT.md) | Le témoin sous les pins | en jeu | groupe `rc_survivant_pins`, **41 clés** (sols, forêt v1.1, ombres de couronne, props, Roque et Paca). | Rien de nouveau. Les retouches de finition vont en phase D (§4). |
| 04 | [PILOTE.md](PILOTE.md) | L'appât de la piste | en jeu, à compléter côté jeu (options « intimider » et « contourner ») | groupe `rc_pilote_appat`, **43 clés**, dont 17 modules de bibliothèque désert (`g_rc_*`, `rc_ds_*`) réutilisés par la caravane, le convoi, la patrouille et la tempête. | Rien de nouveau côté DA. Les options manquantes sont du câblage, pas des sprites. |
| 05 | [ERRANTS.md](ERRANTS.md) | Les Brûlés | fiche seule | aucun groupe propre ; réutilise les modules de verre de `rc_ecluse_verriers` (`g_rc_verre` `_b` `_c`, `g_rc_cendre` `_b`, `rc_vr_dalles_*`, éclats / plaques / arêtes / aiguilles / coulures et leurs `_reflet`). | `rc_err_carcasse_3q`, `rc_err_croute_3q`, `rc_err_ferraille_3q` ; `gen_rc_brule_a`, `_b` et `_c` (face et dos seulement, pas de portrait parlant). Ne pas réutiliser le four, la cabane, la péniche, les portes, les parapets, le quai, le limon, le blindé, les Verriers ni les chanchos. |
| 06 | [PATROUILLE.md](PATROUILLE.md) | La patrouille du Service (IO) | fiche seule | aucun groupe propre ; réutilise le désert du pilote et de la caravane (mêmes sols, talus, rochers, panneau, ferraille, traces). | Bibliothèque E, préfixe `rc_pr_` : `rc_pr_guerite_3q` (lampe `_neon`, nuit seulement), `rc_pr_barriere_3q`, `rc_pr_sacs_3q` (`_b` si besoin), `rc_pr_vehicule_3q`, `rc_pr_container_3q` `_b`, `rc_pr_local_3q`, `rc_pr_caisse_3q` ; `gen_rc_prato`, `gen_rc_kenn`, `gen_rc_orel` (face, dos, portrait). Ne pas réutiliser l'épave du Service, le pick-up, le blindé vitrifié ni le tracteur de Remedios. |
| 07 | [TEMPETE.md](TEMPETE.md) | La tempête de poussière | fiche seule | aucun groupe propre ; même route désertique que le convoi, mêmes modules réutilisés. | `rc_tp_carcasse_3q`, `rc_tp_tole_3q`, `rc_tp_caisse_3q`, `rc_tp_gourde_3q`. Pas de PNJ. Le voile de poussière n'est pas un sprite : c'est un effet décrit pour Rivet (TEMPETE.md §10), à brancher plus tard, sans remplacer la courbe `desert`. Ne pas réutiliser l'épave du Service, le relais UFSA ni le pick-up. |
| 08 | [MUTANTS.md](MUTANTS.md) | L'écluse des Verriers (harde de pécaris) | en jeu | groupe `rc_ecluse_verriers`, **57 clés** (sols de verre, quai, écluse, four et flaque, Verriers, chanchos, éclats et calques `_reflet`). | Rien de nouveau. Les retouches de l'escalier et des éclats vont en phase D (§4). |

Les quatre groupes du manifeste couvrent seulement les rencontres déjà en jeu. Les clés `rc_cv_*`, `rc_err_*`, `rc_pr_*`, `rc_tp_*`, `gen_rc_nando` / `sola` / `brule_*` / `prato` / `kenn` / `orel` n'y figurent pas encore.

## 2. Règles de DA en vigueur

- **Caméra iso** : yaw ~35°, pitch 28,8°, pentes cibles 0,33 (axe x) et 0,70 (axe z), 50 px/m. Les sols font 512 px pour 4 m, avec des variantes `_b` et `_c`. On n'étire aucun sprite.
- **Calques** : `_neon` (source visible, enseigne + flaque la nuit seulement), `_texte` (calque normal, jamais retourné, typiquement le lettrage d'un véhicule), `_avant`, et `_reflet` (additif, jour seulement, opacité `1 − lune`, jamais une émission). Les ombres de couronne sont des décalques `fond`, aussi à `1 − lune`.
- **PNJ** : pivot 0 (milieu des pieds), vraie vue de dos (`_dos`), portrait 192 px. Les créatures sans dialogue (chanchos, Brûlés) n'ont pas de portrait parlant.
- **Véhicules** : deux vues, le reste au miroir ; le texte va sur un calque `_texte` qui ne se retourne pas.
- **Interdits** : pas de violet, pas de cyan, pas de halo sans source, pas d'écran holographique. On ne change jamais la clé d'un autre lot dans le manifeste.
- **Accent IO** (décision DA, PATROUILLE.md §11 et §13) : graphite, laiton et ambre sale, bande au pochoir d'un rouge-oxyde foncé. Même pour le Service (IO), pas de cyan ni de violet, pas de gyrophare bleu.
- **Liseré de lune** : 50 % d'opacité, tête et épaules seulement, coupé net à 25 % de la silhouette (tranché pour toutes les scènes, MUTANTS.md §13).
- **Ambiance** : elle suit l'heure du voyage (`desert`, `glass`, `forest` proposée). Une seule lumière artificielle par scène, avec une source visible.

## 3. Décisions de lore en attente de l'avis de Valentin

Elles sont déjà appliquées dans les fiches et, pour les rencontres en jeu, dans les répliques. Elles restent sauf refus de Valentin. Les drapeaux `monde_*` servent seulement aux répliques et aux indices, tant que Valentin n'a pas validé une quête de la filière (garde-fou de Régie, 18/11).

**Les quatre points des Verriers** (MUTANTS.md §13, modifications importantes, à valider ou refuser une par une) :

1. **Le verre de Big Larry comme refuge des mutants.** La plaine vitrifiée est trop irradiée pour les « gens de bonne peau », supportable pour les mutants (`radResist`). Le Service n'y entre pas ; un blindé abandonné le prouve. Cela fait du verre un territoire mutant, ce qui est nouveau.
2. **Les Verriers, étape de la filière de Remedios.** Communauté de mutants sans faction, chassés de Dusk-Town par les rafles. Les passagers attendent ici avant d'entrer à Dusk-Town « par en dessous », avec l'aide de Sol. Cela étend le réseau proposé dans CARAVANE.md §13.1. Si la filière est refusée, les Verriers restent une simple communauté : il suffit de couper les répliques `filiere`, `perles` et la porte aux perles.
3. **Ines**, femme de Balta, prise dans une rafle et jetée dans la Sous-Ville. Accroche `monde_message_ines`, pas une quête.
4. **Première faune hostile** : les **chanchos de ceniza**, pécaris du verre. Ce sont des bêtes, jamais des mutants humains. Ils ont soif ; le combat n'est qu'une des issues, et personne ne meurt.

**Autres points encore ouverts** (SURVIVANT, CONVOI, ERRANTS, PATROUILLE) :

- **La forêt de pins secs** est un vrai lieu (cases F08, G08, F09, et G09 pour le Temple), première rencontre du biome `forest`.
- **Le Temple du couchant** n'est, dans cette scène, qu'un **repère** (borne, flèche, mot effacé). Pas un culte, pas un sanctuaire, pas une étape de la filière.
- **Roque, Mateo et Paca** : noms nouveaux. Mateo, treize ans, mutant (plaques des avant-bras), a été emmené par le Service. Accroche `monde_mateo_pris`, pas une quête. Pas de cadavre d'enfant dans la scène. Le Service peut entrer dans la forêt, contrairement au verre.
- **Le contact à la Station**, pour faire passer Mateo, s'appuie sur **la filière de Remedios** sans nouveau nœud. Si la filière est refusée, Roque dit seulement « quelqu'un qui les emmène plus au nord ».
- **Nando et Sola**, transporteurs civils indépendants, sans faction. Les quatre variantes de cargaison (dont la contrebande de lampes de radio pour un atelier de la Sous-Ville) n'étendent pas la filière, ni Mateo, ni les Verriers.
- Objets nouveaux **`bandage`** (« Bande de toile ») et **`tubes_radio`** (« Lampes de radio ») : pas des objets de quête.
- **Les Brûlés** : nom que leur donnent les Verriers. Mutants humains malades (type « mutants déments » de la maquette v0.13), pas une horde, pas les Féraux écartés au §13 de MUTANTS. Cause proposée : les poches de croûte chaude du verre de Big Larry, supportable pour un mutant mais qui brûle l'esprit si l'on s'y tient. Les Verriers restent pacifiques, campent au bord, et les redoutent.
- **Adjudant Prato, soldat Kenn, soldat Orel** : patrouille du Service (IO) dans une guérite à plusieurs kilomètres du dôme. Implants d'immatriculation ; humain sans implant = 10 $ ou un jet de parole ; mutant abattu à vue. Pas de laissez-passer papier nouveau. La plaque de camion n'en est pas un.

La filière elle-même (CARAVANE.md §13.1 : passeurs pour mutants dans le double fond de la citerne, circuit Novo Córdoba → Station → douane ouest → Dusk-Town, Lena qui cherche son père) reste aussi en attente d'avis. C'est le socle des points 2, Ines, et du contact pour Mateo.

## 4. Défauts connus côté DA (phase D)

Pas de retouche de finition tant que les huit rencontres ne sont pas jouables. Les défauts non bloquants attendent la phase D.

**Verriers (MUTANTS.md §15.5 et §15.6), pas encore recopiés dans la liste du README :**

- Escalier du quai (`rc_vr_escalier_quai_3q`, v1.1) : la descente se lit, mais l'emprise n'a que 0,5 m de profondeur ; les cinq marches sont minces à la taille du jeu, et le liseré de sable du bas touche le bord gauche de la toile.
- Grands décalques `rc_vr_eclats_*` : le contour est encore un peu lobé (la mosaïque interne est anguleuse, le pourtour l'est moins).

**Témoin, déjà dans « À reprendre en phase D » du README (volet DA seulement) :**

- Quelques ombres de couronne débordent hors du plateau (taches sur la marge, au sud et à l'est) ; à recadrer ou rogner.
- La flaque de la lanterne reste timide à 23 h.
- Roque paraît petit à 1280 sous les pins de 10–14 m.
- Aucune couronne ne passe devant le mulet au cadrage actuel (le fondu n'a été vérifié que sur Roque) ; à revoir si les pins bougent.

Le README liste aussi, pour le témoin, des écarts de fiche (soin sans gain de `pv:`, « frapper Roque » en dialogue, drapeau `monde_roque_escorte` sans accent). Ce n'est pas de la DA : Rivet les a commencés dans le clone, non publiés, à reprendre avec le convoi.

**Autres défauts de finition déjà notés dans les fiches, à verser en phase D :**

- Témoin (SURVIVANT.md §15.4) : motte d'aiguilles trop carrée au pied de `rc_fo_pin_3q` ; pentes mesurées de `pin_c`, du bouquet et du pin mort encore loin de 0,33 / 0,70 ; `pin` et `pin_c` se ressemblent ; `rc_fo_genet_3q` se lit encore un peu trop de dessus.
- Verriers (MUTANTS.md §15.5) : porte nord de la cabane sur une face cachée (déjà signalée par des planches au coin NE) ; oreille fendue de « le gris » illisible à la taille du jeu ; plaques de Rufina un peu « écailles » ; motif de `g_rc_verre` répétitif à 4 m (l'identité passe désormais par les décalques).
- Tempête : le polissage du voile (grain, direction du vent, variants) est déjà renvoyé en phase D (TEMPETE.md §10).
- Patrouille : les phares du véhicule de contrôle, s'ils deviennent une source, attendent aussi la phase D (PATROUILLE.md §10).

## 5. Reprise

Ordre convenu (Régie, 18/11) : **convoi (01)**, puis **patrouille (06)**, puis **tempête (07)**, puis **errants (05)**. Ocre produit les sprites quand Rivet en a besoin, dans cet ordre. Pas de finition avant que les huit soient jouables.

| Ordre | Rencontre | Ce qu'Ocre doit produire |
|---|---|---|
| 1 | Convoi ensablé (01) | Camion civil distinct (rouille-rouge délavé, pas le pick-up, pas le tracteur, pas l'épave), cric, planches, langue de sable, quatre caisses de variante, Nando et Sola (face, dos, portrait), lampe `_neon` au battant. Groupe nouveau à déclarer au manifeste, sans toucher aux clés des autres lots. |
| 2 | Patrouille du Service (IO) (06) | Gros œuvre de la bibliothèque E (`rc_pr_*`) et les trois soldats. Accent IO : graphite, laiton / ambre sale, rouge-oxyde au pochoir. Containers en rouille et graphite, pas de bleu (les containers un peu bleutés de la maquette ne sont pas canoniques). |
| 3 | Tempête de poussière (07) | Carcasse civile à demi ensevelie, tôle, caisse, gourde. Le voile est un effet moteur (Rivet, plus tard) ; Ocre n'a pas de sprite de voile à livrer dans ce lot. Gabarits gris acceptables en attendant. |
| 4 | Mutants errants (05) | Carcasse prise dans le verre, décalque de croûte (pas d'émission), ferraille lançable, trois Brûlés lisibles comme des gens (écouteur, osseux, marcheur), face et dos. Réutiliser les dalles et les éclats déjà publiés ; les touffes pâles de la maquette ne sont pas canoniques. |

Maquettes déjà prêtes, hors dépôt, sur la machine de travail : `/workspace/nml-shots/rencontres/convoi_concept.png`, `patrouille_concept.png`, `tempete_concept.png`, `errants_concept.png` (et les planches déjà utilisées pour les lots en jeu).
