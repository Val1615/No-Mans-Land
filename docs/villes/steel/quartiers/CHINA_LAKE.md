# Steel-Megalopolis · China Lake (fiche de quartier)

Légende : **[canon]** roman tome 1 (§ = numéro de paragraphe de l'extraction texte, mêmes numéros que `CANON_ARBITRAGES.md`) · **[décision]** Valentin · **[proposition]** à valider.
Jeu en 2175, roman en 2202 : aucun personnage du roman n'apparaît (CANON_ARBITRAGES §9).
Fiche réécrite le 2026-10-28 après perte de la version précédente. Elle s'aligne sur l'implémentation de Rivet (lot 3, `src/data/china_lake.js`, `CHINA_LAKE_POSITIONS.md`, commit 984c9b2 de la branche `dev/volonte`), sur la DA d'Ocre (`DA_QUARTIERS.md` §4 bis, branche `creation/quartiers`) et sur les emprises du manifeste Ocre a301df7. En cas d'écart, les positions de Rivet font foi pour le code ; cette fiche fait foi pour l'intention.

## 1. Rôle et population
- Quartier de Lower-Town : « Vous aurez besoin de vous rendre dans un quartier de Lower-Town. China Lake pour être plus précis. » [canon Ch. IX §2069].
- « China Lake… un repaire pour la mafia la plus connue de la ville. » [canon Ch. IX §2071]. Le roman parle aussi du « lac de Lower Street » [canon Ch. III §806] ; le rapprochement des deux lacs reste une [proposition].
- Au bord d'un lac conséquent et pollué, couvert de déchets ; bâtisses de plusieurs étages, rues peuplées, stands sauvages, décoration chinoise [canon Ch. IX §2104].
- Avant tout un énorme marché de contrefaçons et de produits illégaux [décision]. On y vend ce qu'IO interdit ou trace : implants, puces, armes, papiers, médicaments [décision].
- Les passants dévisagent l'étranger, la mafia sait déjà qui entre [canon §2104]. Hommes de main en costume, armés de poignards [canon §2108].
- Population : marchands à la sauvette, receleurs, faussaires, mafieux, clients venus de tout Lower-Town et quelques gens du centre qui ne veulent pas être vus [proposition].
- Monnaie : crédit [décision]. Prix affichés à la craie, marchandage de règle [proposition].

## 2. Ambiance [proposition, d'après DA_QUARTIERS §4 bis]
- Palette : noir pétrole `#0B0D0A`, tôle verdie `#4F5A2A`, bois gorgé d'eau `#4A3523`, papier ivoire `#E6DCC0`. Lumière dominante : ampoules nues ambre `#E8A13A` [décision]. Rouge `#C8322A` seulement pour les lanternes et leurs reflets.
- Interdits : aucun rose [décision], aucun néon cyan, violet ou or. Le seul néon toléré est le rouge du kiosque à implants (sprite `cl_stand_implants`, retouche Ocre du 2026-10-28) [proposition, à confirmer].
- Lumière : lanternes rouges sur câbles au-dessus du lac [canon §2104] ; ballons et figures de papier en forme d'animaux mythologiques [canon §2104], éclairés de l'intérieur [proposition] ; reflets sur l'eau noire, brume basse.
- Toits : **pas de pagode** [décision]. La maison de thé est le seul bâtiment au toit légèrement recourbé, un seul toit, sans étages en gradins [proposition]. Tout le reste : tôle et bois, toits plats ou pentes simples.
- Enseignes bilingues français et chinois, lisibles et simples, ou vierges [décision, DA].
- Sons : marchandage à voix basse, huile de friture, clapot, générateurs, tuiles de mah-jong [proposition].
- Odeurs : épices, gras et sucre de la restauration rapide [canon §2104], puis l'âcreté du lac pollué [canon §2104].
- Différence avec Asia-Ground : Asia-Ground est sec, béton, rouge laque et or, vapeur blanche, un néon IO. China Lake s'organise autour d'un vide d'eau noire, tôle et bois mouillés, ambre [proposition].

## 3. Plan (zone `steel_china`, 48 × 36 m)
Une seule zone [décision]. Coordonnées en mètres, x vers l'est, z vers le sud ; le nord (z petit) est le haut du cadre caméra v4.
- **Le lac** (x 14-34, z 12-26) [décision : lac au centre, non marchable] : sol `g_cl_eau`, bloqué pour la navigation. Câbles à lanternes, ballons, déchets flottants. Il agrandit la vue sans demander de contenu.
- **Les quais** : une ceinture de stands tout autour du lac [décision], regroupés par rive [proposition, reprise par Rivet] :
  - nord : implants et puces ;
  - est : armes ;
  - sud : faux papiers, et l'établi du technicien au bord de l'eau (table couverte d'appareils et de pièces, écho de §2104) ;
  - ouest : médicaments et stimulants, ponton de Shen.
  Le tour complet du lac par les quais doit rester possible sans passer dans l'eau.
- **Les bâtiments en fond** [décision] : sur le bord nord, haut du cadre, pour ne jamais masquer le lac. Pavillon du Dragon (nord-ouest), façades muettes, maison de thé (nord-est, x 30-40), pilotis dans les angles.
- **Le Barrage** (trouée nord, x 21,5-29,5) : barrière de caisses, entrée depuis Asia-Ground.
- **Les ruelles** [décision : quelques petites ruelles] : entre les pilotis et les façades (angle nord-ouest, angle sud-ouest), et la **ruelle de l'angle est** vers Lower-Town, qui passe derrière Les Filets.
- La maison de thé n'est pas sur l'axe x 24 comme prévu au plan : cet axe est la trouée du Barrage. Elle reste visible depuis le Barrage, par-dessus les stands [proposition, écart déjà posé par Rivet].

## 4. Entrées
| Id ici | Position | Vers | Id en face | Condition |
|---|---|---|---|---|
| `k_est` | x 48, z 32 (ruelle de l'angle) | Lower-Town | `l_sud_est` (x 30, z 36) | ruelle **gratuite**, libre dans les deux sens [décision]. C'est la route sans argent. |
| `k_nord` | x 24, z 0 (Le Barrage) | Asia-Ground | `a_sud` (x 24, z 36) | **barrage de gang : 20 cr** à payer à Ah-Lam, côté Asia-Ground (drapeau `cl_barrage`) [proposition] ; sortie libre |
- Le plan prévoyait « `l_sud_est` ouvert seulement après une première visite ». La décision de deux entrées dont une gratuite rend cette règle caduque [décision].
- Les autres conditions du barrage (quête de Mei active, laissez-passer) restent des [propositions] pour le lot 4.

## 5. Marchandises (5, canon du projet) [décision]
| Marchandise | Rive | Stand (sprite) | Vendeur | Exemples [proposition] | Prix indicatif [proposition] |
|---|---|---|---|---|---|
| **Implants** | nord | `cl_stand_implants` | Marchande d'implants | implants contrefaits « garantis », implant d'immatriculation de seconde main | 40 à 120 cr |
| **Puces** | nord | `cl_stand_puces` | figurant, et le technicien pour la lecture | puces piratées, lecteurs, clés de crédit vidées | 10 à 30 cr |
| **Armes** | est | `cl_stand_armes` | Armurier | armes sans numéro, munitions au détail, poignards | 25 à 90 cr |
| **Papiers** | sud | `cl_stand_papiers` | Faussaire | faux permis de transit, faux registres, tampons | 30 à 80 cr |
| **Médocs** | ouest | `cl_stand_medocs` | Apothicaire | stimulants, antidouleurs, antiradiations coupés | 5 à 25 cr |
Les achats des stands ne sont pas encore branchés (lot 4). Les prix devront être relus avec `docs/ARGENT_DUSKTOWN.md` et le change (20 $ = 11 cr).

## 6. Services (nom affiché une fois découverts) [proposition]
| Avant découverte | Après | Ce qu'on y trouve |
|---|---|---|
| Façade aux lanternes | **Pavillon du Dragon** | restaurant, bol du jour 5 cr, salle de jeu à l'étage (décor) |
| Toit recourbé | **Maison de thé** | siège de Madame Zhou ; on n'y entre que si l'on a affaire à elle |
| Cabane humide | **Les Filets** | objets repêchés dans le lac, cache sous le plancher (lot 4) |
| Ponton | **Ponton de Shen** | lecture de puces, rachat d'objets |
| Établi | **Établi du technicien** | réparation légère, lecture de puces |
- Le Pavillon du Dragon est à China Lake [décision]. Le restaurant d'Asia-Ground s'appelle **Chez Lin 林记** [décision] : ne pas confondre les deux.

## 7. Bâtiments et emprises réelles (manifeste Ocre a301df7)
| Bâtiment | Sprite | Emprise w × d (m) | Hauteur (m) | Position Rivet (coin min x, z) |
|---|---|---|---|---|
| Pavillon du Dragon | `cl_immeuble_fond` | 7 × 8 | 9 | 8 ; 0,5 |
| Façades muettes × 2 | `cl_immeuble_fond_b` | 6 × 8 | 8 | 15,5 ; 0,5 et 41 ; 0,5 |
| Maison de thé | `cl_maison_the` | 10 × 5,5 | 8,5 | 30 ; 0,5 |
| Pilotis × 2 | `cl_pilotis` | 6 × 6 | 4,5 | 0,5 ; 0,5 et 0,5 ; 29,5 |
| Les Filets | `cl_cabane` | 8 × 2 | 3,5 | 40 ; 24 |
| Ponton de Shen | `cl_ponton` | 5 × 3 (non plein) | 3,5 | 9 ; 17 |
| Stands implants, puces, papiers | `cl_stand_*` | 2,5 × 1 | 2,4 à 2,6 | voir POSITIONS |
| Stand armes | `cl_stand_armes` | 2,5 × 2 | 2,6 | voir POSITIONS |
| Stand médocs | `cl_stand_medocs` | 2,5 × 1,5 | 2,6 | voir POSITIONS |
- Les emprises du manifeste diffèrent du plan (maison de thé 10 × 5,5 au lieu de 10 × 8 ; immeuble 7 × 8 au lieu de 8 × 6 ; stands 2,5 × 1 à 2,5 × 2 au lieu de 2 × 2). Les emprises du manifeste comptent, la collision suit le dessin [proposition].
- Props : `cl_cable_lanternes` (14 m), 4 ballons (dragon, carpe, tigre, phénix), `cl_bache`, `cl_treteaux`, `cl_caisse_armes`, `cl_bac_puces`, `cl_presse_papiers`, `cl_bocaux`, `cl_friture`, `cl_mahjong`, `cl_barriere_caisses`, `cl_pieux` et `cl_pieux_b`, 3 déchets.

## 8. Intérieurs (3, chacun ≥ 10 × 8 m) [décision pour le nombre et la taille]
| Intérieur | Taille | Contenu [proposition] | PNJ |
|---|---|---|---|
| `the_in` (Maison de thé) | 12 × 9 m | salle à paravents, tables basses, estrade au fond, porte gardée vers un bureau (décor seul) | Madame Zhou (6, 2), deux hommes de main (2, 4) et (10, 4) |
| `dragon_in` (Pavillon du Dragon) | 12 × 9 m | salle de restaurant, cuisine ouverte, escalier vers la salle de jeu (décor) | serveur (2,4 ; 3,2), Vieux Lo (9, 6) |
| `filets_in` (Les Filets) | 10 × 8 m | cabane humide, filets, objets repêchés, trappe sous le plancher | Yu (4, 3) |
Sortie au sud, au milieu, seuil à 1 m dans la pièce. Le style reprend l'extérieur (`CHINA_IN`) : bois mouillé, ambre, rouge en points.

## 9. PNJ [proposition pour les traits ; liste = décision]
| PNJ | Lieu | Fonction | Envie | Peur | Secret | Voix |
|---|---|---|---|---|---|---|
| **Shen** | ponton, rive ouest | receleuse, lit les puces | garder son ponton hors des comptes de Zhou | qu'une puce lue chez elle remonte jusqu'à IO | garde une copie de tout ce qu'elle lit | lente, ironique, ne dit jamais un prix en premier |
| **Marchande d'implants** | stand nord | vend des implants contrefaits | passer de la table à la clinique | une pose ratée qui tue un client | une partie de son stock vient des morgues | bonimenteuse, rassurante, trop |
| **Armurier** | stands est | armes sans numéro | être le seul fournisseur du marché | les gardes d'IO déguisés en clients | prête des armes aux deux camps | sec, chiffres et calibres |
| **Faussaire** | stand sud | faux papiers, faux registres | un dernier gros contrat et partir | que Zhou le juge trop bavard | a fabriqué le faux registre de Victor Seng (lien avec « Le loyer de Mei ») | précieux, parle bas |
| **Apothicaire** | stand ouest | médicaments, stimulants | soigner ceux qu'Asia-Ground refuse | les coupes qu'on lui impose | coupe ses produits sur ordre de la mafia | douce, fatiguée |
| **Technicien** | établi au bord du lac | réparations, lecture de puces | réparer ce que personne ne sait réparer | ses propres implants, qui vieillissent | travaille aussi pour Zhou | précis, poli, s'incline avant de parler (écho de §2110, sans être le personnage du roman) |
| **Madame Zhou** | maison de thé | tient le quartier pour la mafia | l'ordre, et que l'argent remonte | une guerre ouverte avec IO | sait que Seng la vole sur Asia-Ground | calme, polie, jamais pressée |
| **Hommes de main × 2** | maison de thé | gardes de Zhou | à écrire | à écrire | à écrire | costume, poignards [canon §2108] ; peu de mots |
| **Serveur** | Pavillon du Dragon | sert le bol du jour | à écrire | à écrire | à écrire | figurant ; « En haut, c'est privé. » |
| **Vieux Lo** | Pavillon du Dragon le soir | ancien du quartier, joueur de mah-jong | qu'on se souvienne de China Lake avant la mafia | mourir sans héritier pour sa table | connaît chaque passage autour du lac | conteur, digressions, proverbes inventés |
| **Yu** | Les Filets | réparatrice de filets, repêche ce que le lac rejette | quitter le quartier un jour | ce qui remonte parfois dans les filets | cache sous le plancher | brève, ne lève pas les yeux de ses mains |
- **Ah-Lam** n'est pas dans la liste de Valentin. Il est repris du plan et de l'implémentation de Rivet comme garde du Barrage, côté Asia-Ground, qui encaisse les 20 cr [proposition, à confirmer ou à remplacer par un des hommes de main].
- Les noms Lin (Chez Lin 林记) et la ressemblance avec Lin Qiao des documents précédents ne lient aucun PNJ de China Lake [proposition].

## 10. Règle de placement des PNJ [décision]
- Un PNJ reste à **≥ 1,5 m** d'une étiquette (porte, jonction, stand ou objet à libellé), mesuré du centre du PNJ au centre de l'emprise ou au point d'ouverture, et jamais au sud de l'étiquette sur la ligne vers la caméra.
- Contrôle sur les positions de Rivet (984c9b2), distance au centre de l'emprise du stand :
  | PNJ | Position | Étiquette proche | Distance | Verdict |
  |---|---|---|---|---|
  | Marchande d'implants | 17,25 ; 9,9 | stand « Implants garantis » (centre 17,25 ; 11,1) | 1,2 m | **à corriger** : z 9,5 (1,6 m) [proposition] |
  | Apothicaire | 11,75 ; 12,9 | stand médocs (centre 11,75 ; 14,35) | 1,45 m | **à corriger** : z 12,8 (1,55 m) [proposition] |
  | Technicien | 24 ; 25,9 | « Établi du technicien » (centre 24 ; 27,1) | 1,2 m, et z 25,9 est dans le rectangle du lac | **à corriger** : à l'est de l'établi, (25,7 ; 27,1), sur le quai [proposition] |
  | Armurier | 38,25 ; 12,3 | stand armes (centre 38,25 ; 14) | 1,7 m | conforme |
  | Faussaire | 19,1 ; 28,6 | stand papiers (centre 17,25 ; 29) | 1,9 m | conforme |
  | Shen | 7,6 ; 18,6 | ponton (centre 11,5 ; 18,5) | 3,9 m | conforme |
  | Zhou, hommes de main, serveur, Vieux Lo, Yu | intérieurs | seuil de sortie | ≥ 3 m | conformes |
- Si le libellé d'un stand est ancré ailleurs qu'au centre, refaire la mesure sur capture.

## 11. Accroches de quête [proposition]
- « Le loyer de Mei », partie 2 : remonter l'argent de Kim (Ah-Lam, puis Zhou) et découvrir la fraude de Seng. Trois issues sans combat : preuve à Zhou (faux registre et lecture de puce chez Shen ou chez le technicien), rachat de Kim, ou prise de la place de Seng.
- Accroches de combat : `hook_hommes_de_main` (menacer Zhou) et `hook_ah_lam` (forcer le barrage). Drapeaux et répliques seulement tant que le lot C du combat ne les branche pas (voir `docs/design/COMBAT.md`).

## 12. Vérifications du lot 3
- Tour complet du lac par les quais, sans passage dans l'eau (test de connexité).
- La maison de thé est le seul toit recourbé, aucune pagode, aucun rose ; elle se voit depuis le Barrage.
- Les deux entrées fonctionnent : `k_est` ↔ `l_sud_est` gratuite, `k_nord` ↔ `a_sud` à 20 cr.
- Trois intérieurs d'au moins 10 × 8 m, sans grande zone noire à l'écran.
- Aucun PNJ à moins de 1,5 m d'une étiquette (§10).
- Palette distincte d'Asia-Ground sur captures côte à côte.

## 13. Points ouverts
1. Ah-Lam : garder, renommer, ou confier le barrage à un homme de main de Zhou.
2. Néon rouge du kiosque à implants : toléré ou à retirer (la DA dit « aucun néon »).
3. Prix des 5 marchandises, à équilibrer avec l'argent de Dusk-Town et le change.
4. Trois PNJ à déplacer (§10), dans `src/data/china_lake.js` (chez Rivet, pas en Régie).
