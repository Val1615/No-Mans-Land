# Steel-Megalopolis · Asia-Ground (fiche de quartier, rien n'est codé)

Légende : **[canon]** roman tome 1 (§ = ligne de l'extraction texte, mêmes numéros que `CANON_ARBITRAGES.md`) · **[décision]** Valentin · **[proposition]** à valider.
Jeu en 2175, roman en 2202 : aucun personnage du roman n'apparaît (CANON_ARBITRAGES §9).

## 1. Rôle et population
- Quartier lié au commerce de Lower-Town : un « quartier marchand de Lower-Town, près de Asia-Ground » où une famille tenait un stand chinois [canon Ch. IV §1038]. Le plan en fait le quartier marchand lui-même [décision, STEEL_MEGALOPOLIS_PLAN §1].
- Emplacements loués par des intermédiaires qui prennent un pourcentage et endettent les familles [canon §1038, l'exemple date de 2202 ; le principe est repris, pas le personnage].
- Population : petits commerçants, cuisiniers, porteurs, familles installées depuis plusieurs générations, clients montés de Lower-Town et descendus du centre [proposition].
- Voisin de China Lake, repaire de mafia [canon Ch. IX §2071] : la mafia y passe pour encaisser, elle n'y règne pas ouvertement [proposition].
- Monnaie : crédit [décision] ; prix affichés en crédits, marchandage autorisé [proposition].

## 2. Ambiance
- Palette : rouge laque et or terni sur fond noir, vapeur blanche ; un seul néon cyan, celui d'IO au-dessus du marché, pour rappeler le centre [proposition].
- Lumière : lanternes rouges sur câbles [canon pour China Lake §2104, reprise ici en plus modeste : proposition], lampes nues des stands, lueur des woks. Plus chaud que Lower-Town, moins que la Sous-Ville [proposition].
- Matériaux : bâtisses de plusieurs étages, devantures décorées [canon pour China Lake §2104 ; reprise = proposition], auvents en toile plastique, carrelage ancien, bois peint, caisses de poisson sur glace [proposition].
- Sons : marchandage dans plusieurs langues, huile qui crépite, hachoir, cloche d'un ascenseur de marchandises, haut-parleur IO qui répète les consignes [proposition].
- Odeurs : épices, gras et sucre de la restauration rapide [canon pour China Lake §2104 ; reprise = proposition].

## 3. Plan (zone `steel_asia`, 48 × 36 m) [proposition]
- **Le Marché couvert** (centre, x 12-36, z 10-26) : allées de stands sous un toit de tôle percé, trois allées est-ouest, deux transversales. Dense, on y circule mal, idéal pour semer une patrouille.
- **Rue des Lanternes** (nord, z 4-8) : rue de restaurants à étages, câbles et lanternes au-dessus. Arrivée depuis Center-Town.
- **Escalier des Mille Marches** (nord-est, x 40-46) : large escalier public qui descend de Center-Town, caméra en haut, aucune en bas. Jonction réciproque : `c_sud_est` (Center-Town, x 38, z 36) ↔ `a_escalier` (Asia-Ground, x 43, z 0). La grille `c_sud` (x 19,5) reste la sortie de la Sous-Ville.
- **Cour des Porteurs** (sud-est) : quai de chargement et monte-charge de marchandises, relié à l'Usine 7 de Lower-Town par l'arrière [proposition], hors caméras.
- **Bout de rue ouest** (x 0, z 18) : continue vers Lower-Town. Jonction `a_nord` ↔ `l_sud` (voir LOWER_TOWN.md). La rue vers China Lake (bord sud) reste fermée par un barrage de gang tant que China Lake n'existe pas.
- Pas d'accès direct à la Sous-Ville [proposition] : on y descend par Lower-Town.

## 4. Services (nom affiché seulement une fois découverts) [proposition]
| Avant découverte | Après | Ce qu'on y trouve |
|---|---|---|
| Stand fumant | **Les Nouilles de Mei** | repas (soin léger), 3 cr, rumeurs du marché |
| Boutique aux volets | **Pharmacie Lau** | soins, stimulants, pansements |
| Étal de pièces | **Électronique Okafor** | pièces, piles, réparation d'implant légère |
| Bureau à l'étage | **Bureau des Emplacements** | location de stand, dettes, travail de livraison |

## 5. PNJ [proposition]
| PNJ | Fonction | Envie | Peur | Secret | Voix |
|---|---|---|---|---|---|
| **Mei Tran** | tient le stand de nouilles | racheter son emplacement pour de bon | que son fils parte à China Lake | paie deux loyers, l'officiel et celui de la mafia | rapide, maternelle, mélange les langues |
| **Victor Seng** | loue les emplacements | devenir respectable, monter au centre | que les comptes soient lus | double les dettes avec de faux frais | poli, doucereux, cite des pourcentages |
| **Hana Lau** | pharmacienne | soigner sans poser de questions | la lampe des patrouilles qui « voit sous la peau » (écho v2 de Dusk-Town) | soigne des mutants la nuit, dans l'arrière-boutique | sèche, précise, jamais un mot de trop |
| **Okafor** | réparateur d'électronique | trouver une pièce d'avant-guerre | qu'IO lui retire sa licence | sait désactiver un lecteur d'implant quelques secondes | jovial, technique, explique trop |
| **Kim Tran** | fils de Mei, porteur, 17 ans | gagner vite et sortir sa mère de là | décevoir sa mère | fait déjà des courses pour un homme de China Lake | bravache, mais baisse la voix devant Mei |

## 6. Accroche de quête [proposition]
« Le loyer de Mei » : Victor Seng annonce à Mei une hausse soudaine de son emplacement. Le joueur peut trouver le faux registre de Seng (Bureau des Emplacements, la nuit), payer la dette en crédits, ou suivre Kim jusqu'au barrage de China Lake et découvrir qui touche vraiment l'argent.

## 7. Bâtiments et props pour Création [proposition]
Angle caméra v4, nuit, palette §2.
1. **Restaurant à étages** (8 × 6 m, 3 niveaux) : rez-de-chaussée ouvert sur la rue avec comptoir, étages à fenêtres étroites, enseigne en idéogrammes sans texte lisible.
2. **Halle du marché** (24 × 16 m, en trois modules) : toit de tôle sur poteaux, ouvert sur les côtés, pour qu'on voie les stands dessous.
3. **Boutique-atelier** (6 × 5 m) : rideau métallique à moitié levé, étagères visibles ; sert pour Pharmacie Lau et Électronique Okafor (deux variantes de façade).
4. **Escalier public** (Mille Marches) : volée large en béton, rampe, caméra et lampadaire en haut, d'un seul tenant pour le raccord avec Center-Town.
Props : stand (3 variantes : nouilles, poisson, pièces), lanterne rouge sur câble, auvent, caisses de légumes, glacière, wok sur brasero, chariot de porteur, haut-parleur IO sur poteau, monte-charge de quai.
