# Steel-Megalopolis : dossier de conception (pour validation, **rien n'est codé**)

Légende : **[canon]** roman tome 1 (§ = ligne de l'extraction texte, mêmes numéros que `CANON_ARBITRAGES.md`) · **[décision]** décision de Valentin · **[proposition]** à valider · **[leçon]** tirée de la maquette `src/a` ou du dossier de conception `src/b`, jamais repris tel quel.
Jeu : **2175**. Roman : **5 octobre 2202** (Ch. I §288). Un fait du roman décrit 2202.

## 0. Décisions de Valentin (21/10/2026)
- **[décision] L'entrée dépend de la race choisie** : humain = **refusé** à la douane ; mutant = **attaqué à vue** ; augmenté ou cyborg = **possède l'implant**, passe la douane.
- **[décision]** Humain ou mutant : un villageois de Dusk-Town conseille de passer **par la Sous-Ville** et oriente vers un contact.
- **[décision]** La quête **s'arrête une fois entré dans la ville**. D'abord la carte, la quête ensuite.
- **[décision]** Premier quartier après la douane : **Center-Town**.
Cohérent avec le canon : contrôle par implants d'immatriculation (Ch. VII §1652), mutants abattus sans sommation (Ch. I §105, Ch. VII §1716), routes de sortie de la Sous-Ville (§1716).

## 1. Canon et décisions retenus
| Fait | Source |
|---|---|
| Capitale d'**IO** (Intelligent Organism) ; la phrase « capitale de l'Ex UFSA » (Ch. I §250) est à corriger dans le tome | [décision] CANON_ARBITRAGES §8 |
| Sous un **sarcophage** / « dôme » : « une masse noire d'une taille titanesque se voyant aisément à plusieurs kilomètres » | [canon] Ch. I §481 |
| Entrée : « grandes portes… une entrée gigantesque avec un énorme passage ouvert laissant une route pénétrer… deux énormes morceaux de métal rétractés servent de portes » | [canon] Ch. I §507 |
| **Guérite de sécurité** devant l'entrée, gardes | [canon] Ch. I §535 ; guérite « à plusieurs kilomètres du dôme » Ch. VII §1652 |
| Contrôle = lecture des **implants d'immatriculation** : « Laissez-moi le temps d'inspecter vos implants d'immatriculation » | [canon] Ch. VII §1652 |
| Sans implant = inconnu d'IO : « n'est pas référencé dans la base de données d'IO et ne possède pas d'implant » | [canon] Ch. I §157 ; « un chien est déclaré auprès d'Intelligent Organism… un implant » §302 |
| **Lower-Town** : « plongée dans une nuit permanente », « centre de la population et donc de la criminalité » | [canon] Ch. II §696, §720 |
| **Upper-Town** : « ciel radieux, purement synthétique », bâtiments neufs, végétation jamais vue ailleurs ; plafond séparant les niveaux | [canon] Ch. II §696 ; Ch. XII §3366 |
| **Center-Town** : tours, Arcadius Center (gestion d'IO) | [canon] Ch. III §854 |
| **Asia-Ground** quartier marchand ; **China Lake** repaire de mafia ; lac de Lower Street | [canon] Ch. IV §1038 ; Ch. IX §2067-2069 ; Ch. III §806 |
| **Sous-Ville** : « zone de non droit où les mutants sont jetés… condamnés à travailler dans les machineries alimentant la ville » ; « beaucoup ont leurs propres routes pour sortir » ; obscurité, « quelques feux dans les ruelles » ; entrées secrètes | [canon] Ch. VII §1701, §1716 ; Ch. IX §2031 ; Ch. VIII §1914 |
| Politique **anti-mutants** d'IO ; mutants abattus « sans sommation » hors Sous-Ville ; Service Militarisé | [canon] Ch. I §105 ; Ch. IV §1087 ; Ch. VI §1348 ; Ch. VII §1716 |
| SMPD (police de la ville), Service Militarisé, Interception Troupers | [canon] Ch. II §665, §718 ; Ch. I §353 |
| Quartiers distincts : centraux néons/surveillance, Upper marbre/or/ciel artificiel, Lower industrie, Sous-Ville précarité/lumières chaudes ; extérieur désertique ; **crédit** (dollar ailleurs) | [décision] |
| **Ambiguïtés 2175** : le sarcophage est intact (il chute en 2202, Ch. XII) ; Sine Vincula non datée ; Lysandre (≈14 ans en 2202), Klay, Clofford ne sont pas encore en place → **aucun personnage du roman utilisé** | CANON_ARBITRAGES §9 |

**Leçons de la maquette / conception** [leçon] : 18 secteurs dont 11 protégés = trop, identité et raccords insuffisants (`02_Etat-reel-et-ecarts` l.41) ; les cartes de niveaux étaient des schémas, pas une géométrie ; les transitions doivent être des ascenseurs, escaliers, contrôles **réciproques** ; « plus de 100 km² » non couvert par le roman ; valider un quartier avant d'étendre (`04_Reconstruction` l.32).

## 2. Y arriver depuis Dusk-Town
1. **Route** [proposition] : le bord est du Transit (« Route des patrouilles ») devient praticable quand l'objectif Steel est actif. À pied, une journée (Ch. I §61 [canon]) : eau et rations consommées. La caravane d'Ileana est gardée pour plus tard.
2. **Guérite puis douane** [canon guérite §535, §1652] :
   - **augmenté / cyborg** [décision] : l'implant est lu, passage. Le change dollar → crédit se fait au comptoir de la douane, à un taux mauvais [proposition] ;
   - **humain** [décision] : refusé (« pas d'implant, pas de ville »), renvoyé sur la route. Aucun combat ;
   - **mutant** [décision] : attaqué à vue. Sans système de combat, voir Q2.
3. **Conseil à Dusk-Town** [décision : un villageois ; choix du villageois = proposition] : **Sol** (la citerne, Les Sables). Elle cache déjà quelque chose sous son foulard (v7 : « ils regardent les mains, le cou, les yeux ») et vit au bord du désert : elle sait par où sortent ceux qu'on a jetés en dessous.
   - Elle parle si le joueur est mutant (elle reconnaît les siens), ou s'il a gardé son secret (`sol_vue`) ; sinon il faut revenir après le refus de la douane (« Tu as vu leur porte. Maintenant écoute-moi. »).
   - **Contact** [proposition] : le **frère de Bruno**, emmené par une patrouille « avec des lampes qui voient sous la peau » (v2). Le roman dit que les mutants capturés peuvent être « balancés dans la Sous Ville » (Ch. IV §1087 [canon]) : il est vivant, en bas, et fait passer des gens. Bruno donne son nom et un signe que lui seul connaît. Lien Sol ↔ Bruno : il porte l'eau la nuit (v2), elle tient l'eau des Sables.
   - Route : une sortie de service dans le désert, loin de la guérite, qui descend dans la Sous-Ville [canon : routes propres §1716 ; emplacement = proposition].
4. **Sous-Ville → Center-Town** [proposition] : le contact fait monter le joueur par un escalier ou monte-charge de service jusqu'à Center-Town, sans papiers. **Fin de la quête à l'arrivée en ville** [décision].
## 3. Ordre de production révisé [proposition]
Même règle que Dusk-Town : zones de 48×36 m, jonctions par bouts de rue, transitions verticales réciproques (escalier, monte-charge, contrôle).

| Lot | Contenu | Remarque |
|---|---|---|
| **L0 Race** | choix de race au début de partie (voir §3 bis) ; Dusk-Town réagit au minimum (2-3 répliques) | prérequis de tout le reste |
| **L1 Premier lot** | **S0 Extérieur** (route, guérite, douane, porte) + **S1 Center-Town** (première zone sous le dôme : néons, écrans, portiques, tours en fond) ; voyage depuis le bord est du Transit | chemin augmenté / cyborg complet ; humain refusé ; mutant : Q2 |
| **L2 Entrée alternative** | **S4 Sous-Ville** (une zone) reliée à S0 par la sortie de service et à S1 par l'escalier de service ; Sol + Bruno à Dusk-Town | chemin humain / mutant complet |
| L3+ | Lower-Town (industrie), Asia-Ground, Upper-Town, China Lake ; puis la quête « quelqu'un répond encore » | après validation de la carte |

### 3 bis. Introduire la race, impact minimal [proposition]
- **Où** : un écran unique avant la première scène de Dusk-Town, dans le style UI v8 : 4 cartes (Humain, Mutant, Augmenté, Cyborg), une phrase chacune, aucune statistique. Le sprite du joueur reste le même au début (variante visuelle ensuite, si assets).
- **Effet** : un seul champ d'état `player.race` + drapeau dérivé `has_implant` (augmenté, cyborg). Utilisé à la douane, par Sol, et par 2-3 répliques existantes (ex. Hector : « Avec ta tête, ne traîne pas sur l'avenue »).
- **Tests** : les suites actuelles démarrent avec une race par défaut (humain) via le même écran, cliqué par geste.
## 4. Conséquences de système [proposition]
- **Crédit** : crédits liés à l'implant ; un clandestin n'en a qu'en liquide, via intermédiaires [proposition]. Deuxième solde dans le HUD v8 (« 120 cr ») affiché seulement à Steel ; le dollar reste dans le Sac.
- **Surveillance** : jauge discrète « Repérage » (0-3) dans la cellule HUD, montée par portiques, caméras, actes visibles (courir, parler à un mutant devant une caméra) ; baisse avec le temps et dans les zones aveugles (Sous-Ville, arrière-cours). À 3 : contrôle par une patrouille.
- **Contrôles** : portiques et patrouilles lisent l'implant [décision : seuls augmentés et cyborgs en ont]. Un humain ou mutant entré par la Sous-Ville est clandestin : un contrôle = choix (payer en crédits via un intermédiaire, mentir, fuir). Pas de combat dans ce périmètre.
- **Statut humain / mutant** : le Service Militarisé abat les mutants identifiés [canon] ; un PNJ mutant ne se montre que dans la Sous-Ville ou derrière une porte. Être vu à l'aider monte le Repérage.
- **Pas de nouvelle mécanique lourde** dans P1 : Repérage et crédit seulement ; le combat n'est pas prévu ici.

## 5. Quête : pour l'instant [décision]
La quête « La porte d'acier » mène jusqu'à **l'entrée dans la ville** (douane ou Sous-Ville) puis s'arrête. L'objectif devient « Arrivé à Steel-Megalopolis ». Les pistes A/B/C de la suite (guichet d'IO, ancien réparateur HC, relais radio de la Sous-Ville) sont **mises en attente** jusqu'à ce que la carte soit faite. Contrainte maintenue : le labo ne s'ouvre pas avant 2202 et l'homme n'en sort jamais.
## 6. PNJ clés (nouveaux, aucun personnage du roman) [proposition]
| PNJ | Lieu | Désir | Peur | Secret | Voix |
|---|---|---|---|---|---|
| **Odile Varga**, guichetière de la douane | S0 | finir sa journée sans incident | une erreur à son nom | laisse passer un cousin par mois contre des dollars | phrases en formulaire, « motif ? » |
| **Teng**, changeur | S1 / S2 | les dollars, valeur refuge | qu'IO interdise le change | taux truqué sur les petites sommes | compte à voix haute, aimable, rapide |
| **Sergent Halloran**, Service Militarisé | S0 / S3 | une promotion vers l'intérieur | être renvoyé en patrouille désert | a perdu un frère dans une rafle « ratée » | sec, ironique, ne finit jamais ses menaces |
| **Mère Ruiz**, foyer de travailleurs | Lower-Town (L3) | loger tout le monde au chaud | le contrôle de nuit | cache une famille mutante dans la cave | chaleureuse, autoritaire, tutoie |
| **Ansel Pike**, ex-réparateur sous-traitant HC | S2 | être cru une fois | qu'on le cherche pour ce qu'il sait | a entendu le même message il y a des années | décousu, précis sur les détails techniques |
| **Le frère de Bruno** (nom à donner), passeur mutant, remplace « Corbeau » | S4 | une route sûre pour les siens | les lampes « qui voient sous la peau » (écho de Bruno) | travaille aussi pour une gang de China Lake | murmure, humour très noir |

## 7. Besoins d'assets
**Existants dans la maquette** (`src/a/.../art-source`, à **contrôler à l'angle v4** comme pour Dusk-Town, rejets probables) :
| Planche | Contenu | Usage visé |
|---|---|---|
| `city-v3.png` | 6 immeubles néons / industriels | S1, S3 |
| `settlement-v9-city.png` | 6 immeubles sombres à enseignes | S1, S2 |
| `city-upper-v3.png` | 2 bâtiments marbre et or | S5 |
| `scenery-city-v4.png` | stand de rue, distributeurs, benne, climatiseurs, jardinière, abribus | S1-S3 |
| `city-props-v3.png` | panneau holo, lampadaire, arbre en bac, voiture, banc lumineux, totem | S3, S5 |
| `city-people-v3.png` + portraits | 6 citadins (dont soldat en bleu, blouse blanche) | PNJ Steel (Vera v2 en venait) |
**À générer** : paroi du sarcophage et portes géantes (fond de S0), guérite et douane, portique scanner, caméras et drones, sol béton mouillé et grilles, textures nuit et néon d'intérieurs, cabanes de tôle, conduites, braseros (S4), dalle marbre et ciel artificiel (S5), soldats IO noir et gris [canon Ch. I §345], intérieurs (douane, change, foyer, bureau IO).
**Audio** : une ambiance par niveau (Lower / Sous-Ville / Upper), à fournir par Valentin comme pour Dusk-Town.

## 8. Risques
- **Nuit permanente** : lisibilité et contraste UI v8 à re-mesurer (le test sable clair devient un test néon et sombre).
- **Angle v4 des assets maquette** : beaucoup de planches risquent d'être refusées (cas v7) → budget de génération.
- **Échelle** : le dôme est titanesque, une zone de 48 m n'en montre rien ; il se lit en fond (S0) et par le plafond (S1-S3), jamais en entier.
- **Canon daté** : tentation d'utiliser Klay, Knox, Lysandre, Sine Vincula. Interdit en 2175 tant que Valentin ne date pas.
- **Système** : Repérage et crédit ne doivent pas devenir une surcouche UI ; une cellule HUD au plus.
- **Contradiction du roman** sur « capitale de l'Ex UFSA » : aucun texte du jeu ne la reprend.

## 9. Planches d'ambiance (**pistes**, pas des assets du jeu)
`docs/villes/steel/ambiance/` : `01-entree-sarcophage.jpg` (le dôme y paraît trop petit), `02-centre-neons.jpg` (contient du faux texte et un bâtiment-dôme : à ignorer), `03-sous-ville.jpg` (vue plus basse que v4), `04-upper-town.jpg` (angle v4), `04b-upper-town-ciel-artificiel.jpg` (vue frontale pour le ciel synthétique, angle non v4).

## 10. Questions restantes pour Valentin
1. **Nilo selon la race.** (a) Nilo suit toujours, il passe là où passe le joueur ; (b) Nilo n'a pas d'implant : avec un joueur augmenté ou cyborg, il doit passer par la Sous-Ville ou attendre à Dusk-Town ; (c) Nilo est mutant caché. **Recommandation : (a)** pour le premier lot (zéro système en plus), (b) plus tard si on veut une séparation.
2. **Mutant attaqué à vue, sans système de combat.** (a) Scène : sommation, tirs, le joueur s'enfuit vers le désert, PV perdus, retour à la route ; (b) écran « capturé » puis relâché dans la Sous-Ville (§1087) : ça devient l'entrée elle-même ; (c) le joueur est repéré de loin et ne peut pas approcher (avertissement de Sol). **Recommandation : (a)**, simple, lisible, et Sol prend le relais.
3. **Le choix de race au début.** (a) écran de choix avant Dusk-Town, modifiable seulement en nouvelle partie ; (b) race tirée de l'origine ou d'un dialogue d'ouverture ; (c) choix tardif, au moment du départ pour Steel. **Recommandation : (a)**.
