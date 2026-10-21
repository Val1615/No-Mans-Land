# Steel-Megalopolis : dossier de conception (pour validation, **rien n'est codé**)

Légende : **[canon]** roman tome 1 (§ = ligne de l'extraction texte, mêmes numéros que `CANON_ARBITRAGES.md`) · **[décision]** décision de Valentin · **[proposition]** à valider · **[leçon]** tirée de la maquette `src/a` ou du dossier de conception `src/b`, jamais repris tel quel.
Jeu : **2175**. Roman : **5 octobre 2202** (Ch. I §288). Un fait du roman décrit 2202.

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

## 2. Y arriver depuis Dusk-Town [proposition]
1. **Départ** : le bord est du Transit (« Route des patrouilles », v7) devient praticable une fois l'objectif Steel actif. Deux façons :
   - **à pied**, une journée (le régiment met « une bonne journée », Ch. I §61 [canon]) : coûte eau et rations (Sol, Anselme servent enfin), un événement de route (patrouille à éviter, abri) ;
   - **avec la caravane d'Ileana** (elle « attend une caravane qui ne vient pas », v2) : elle arrive enfin, place payante en $, plus sûr, mais un convoi se fait contrôler.
2. **Le périmètre** : désert, route, **guérite** à plusieurs km du dôme [canon], puis la **porte** [canon].
3. **Papiers** : le joueur n'a pas d'implant IO (à trancher, Q2). Au guichet de la douane : **laissez-passer temporaire** (plaque ou bracelet scanné) contre $, durée limitée, motif déclaré. Mentir sur le motif = choix. Alternative : un passeur par une **route de la Sous-Ville** [canon : routes de sortie §1716], illégal, pas de papiers, recherché si contrôlé.
4. **Change** : comptoir de change à la douane : dollars → crédits à un taux mauvais et à frais fixes ; meilleur taux au marché noir (Asia-Ground ou Sous-Ville), avec risque. Les crédits sont **liés au laissez-passer** (pas de pièces) : un clandestin ne paie qu'en liquide via intermédiaires.
5. **Nilo** : statut à fixer (Q2). S'il n'a pas de papiers, il doit rester à la caravane, ou passer avec toi par la Sous-Ville.

## 3. Zones reliées à pied, ordre de production réaliste [proposition]
Même règle que Dusk-Town : 48×36 m par zone, bouts de rue = jonctions, bords annoncés ; transitions verticales = ascenseur / escalier / contrôle, toujours dans les deux sens.

| Lot | Zones | Contenu jouable |
|---|---|---|
| **P1 (premier périmètre)** | **S0 Périmètre** (route, guérite, douane, porte) · **S1 Lower-Town · La Porte** (rue d'arrivée sous le dôme, nuit, industrie, bureau de change, foyer de travailleurs) | entrée, papiers, change, 2 intérieurs, 4 PNJ, suite de quête étape 1 |
| P2 | **S2 Asia-Ground** (marché, stands, marché noir) · **S3 Center-Town** (néons, écrans, tours, portiques scanner, bureau d'IO accessible au public) | surveillance, contrôles, quête étape 2 |
| P3 | **S4 Sous-Ville** (sous S1, par une entrée de service) | mutants, précarité, braseros, route clandestine retour vers l'extérieur |
| P4 | **S5 Upper-Town** (ascenseur contrôlé depuis S3) · **S6 China Lake** | accès rare, mafia, conclusion de la piste choisie |

Un lot n'est commencé que quand le précédent est validé sur ordinateur et téléphone [leçon].

## 4. Conséquences de système [proposition]
- **Crédit** : deuxième solde dans le HUD v8 (« 120 cr ») affiché seulement à Steel ; le dollar reste dans le Sac.
- **Surveillance** : jauge discrète « Repérage » (0-3) dans la cellule HUD, montée par portiques, caméras, actes visibles (courir, parler à un mutant devant une caméra) ; baisse avec le temps et dans les zones aveugles (Sous-Ville, arrière-cours). À 3 : contrôle par une patrouille.
- **Contrôles** : portiques et patrouilles lisent le laissez-passer ; expiré ou absent = choix : payer une amende en crédits, mentir, fuir (combat hors périmètre de cette proposition).
- **Statut humain / mutant** : le Service Militarisé abat les mutants identifiés [canon] ; un PNJ mutant ne se montre que dans la Sous-Ville ou derrière une porte. Être vu à l'aider monte le Repérage.
- **Pas de nouvelle mécanique lourde** dans P1 : Repérage et crédit seulement ; le combat n'est pas prévu ici.

## 5. Suite de « quelqu'un répond encore sous Dusk-Town » (choisir 1, Q3) [proposition]
Contrainte de fond : **le labo ne s'ouvre pas avant 2202** et **l'homme n'en sort jamais** (en 2202, Luis sort seul, capsules vides, Prélude [canon]). Toute piste finit sans ouvrir la porte.
- **A. Le guichet** : déclarer le survivant au bureau public d'IO (Center-Town). Formulaires, crédits, file d'attente ; un employé trouve la fiche : « Site de Dusk-Town : scellé, sans personnel, dossier clos ». Choix final : insister (Repérage +, on te remarque), ou vendre l'information à un acheteur discret. Humour noir administratif ; IO sait, ou ne veut pas savoir.
- **B. Ceux qui l'ont construit** : à Asia-Ground, une vieille pharmacienne ou un réparateur a travaillé jadis pour un sous-traitant de Human Corporation. Il reconnaît le message « confinement ». Il ne peut pas ouvrir (« ça s'ouvre de l'intérieur ») mais donne une fréquence ou un code d'interphone : retour possible à Dusk-Town pour **parler encore** à l'homme, qui finit par ne plus répondre.
- **C. Ceux d'en bas** : dans la Sous-Ville, des mutants qui travaillent dans les machineries savent qu'un vieux réseau de câbles relie encore des sites d'avant-guerre. Fabriquer un relais radio (pièces, crédits ou service rendu). Choix : le relais sert au survivant, ou les mutants le gardent pour eux (et te le revaudront).
Recommandation : **B** (petite, sans faction datée, prolonge la voix sans rien révéler), **C** en extension P3.

## 6. PNJ clés (nouveaux, aucun personnage du roman) [proposition]
| PNJ | Lieu | Désir | Peur | Secret | Voix |
|---|---|---|---|---|---|
| **Odile Varga**, guichetière de la douane | S0 | finir sa journée sans incident | une erreur à son nom | laisse passer un cousin par mois contre des dollars | phrases en formulaire, « motif ? » |
| **Teng**, changeur | S1 / S2 | les dollars, valeur refuge | qu'IO interdise le change | taux truqué sur les petites sommes | compte à voix haute, aimable, rapide |
| **Sergent Halloran**, Service Militarisé | S0 / S3 | une promotion vers l'intérieur | être renvoyé en patrouille désert | a perdu un frère dans une rafle « ratée » | sec, ironique, ne finit jamais ses menaces |
| **Mère Ruiz**, foyer de travailleurs | S1 | loger tout le monde au chaud | le contrôle de nuit | cache une famille mutante dans la cave | chaleureuse, autoritaire, tutoie |
| **Ansel Pike**, ex-réparateur sous-traitant HC | S2 | être cru une fois | qu'on le cherche pour ce qu'il sait | a entendu le même message il y a des années | décousu, précis sur les détails techniques |
| **Corbeau**, passeur mutant | S4 | une route sûre pour les siens | les lampes « qui voient sous la peau » (écho de Bruno) | travaille aussi pour une gang de China Lake | murmure, humour très noir |

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
