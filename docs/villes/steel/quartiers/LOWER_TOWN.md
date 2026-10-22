# Steel-Megalopolis · Lower-Town (fiche de quartier, rien n'est codé)

Légende : **[canon]** roman tome 1 (§ = ligne de l'extraction texte, mêmes numéros que `CANON_ARBITRAGES.md`) · **[décision]** Valentin · **[proposition]** à valider.
Jeu en 2175, roman en 2202 : aucun personnage du roman n'apparaît (CANON_ARBITRAGES §9).

## 1. Rôle et population
- La partie basse de la ville, « plongée dans une nuit permanente » [canon Ch. II §696], « centre de la population et donc de la criminalité » [canon Ch. II §720].
- On y descend depuis le centre par un chemin en pente, croisé par des travailleurs de Lower-Town qui montent à leurs bureaux [canon Ch. XII §3544].
- Habitat pauvre et délabré, mendiants, vendeurs à la sauvette, gangs, véhicules à l'arrêt faute d'entretien, SMPD présente [canon §3544].
- Identité de jeu : l'industrie, ateliers et usines qui font tourner le dessus [décision, palette « Lower industrie »].
- Population jouable : ouvriers avec implant de base, familles entassées, quelques clandestins venus de la Sous-Ville [proposition]. Les mutants restent cachés : hors Sous-Ville ils sont abattus sans sommation [canon Ch. I §105, Ch. VII §1716].
- Monnaie : crédit [décision]. Le dollar circule en dessous, et ici sous le comptoir [proposition, cohérent avec CANON §9 octies].

## 2. Ambiance
- Palette : noir de suie, gris acier, rouille brune, une note orange de four et de sodium ; presque pas de violet ni de cyan, que l'on garde pour Center-Town [proposition].
- Lumière : nuit totale sous le plafond d'Upper-Town [canon §696, §3374], quelques enseignes de petits commerces [canon §3544], lampes à sodium sur poteaux, lueur des fours par les portes d'atelier [proposition].
- Matériaux : béton taché, tôle ondulée, poutrelles rivetées, passerelles grillagées, tuyaux au-dessus des rues, vitres cassées remplacées par du plastique [proposition].
- Sons : marteau-pilon lointain et régulier, vapeur qui fuse, sirène de relève, radio d'un atelier, pas mouillés, une voiture de la SMPD au ralenti [proposition].
- Air : odeur d'huile et de métal chaud ; la ville paraît basse de plafond, on ne voit jamais le haut [proposition].

## 3. Plan (zone `steel_lower`, 48 × 36 m) [proposition]
Orientation : x vers l'est, z vers le sud, comme `steel_center`.
- **La Descente** (bord ouest, z 16-20) : rampe en pente douce qui arrive de Center-Town. Portique de contrôle à mi-pente, en panne une fois sur deux. Jonction réciproque : `c_est` (Center-Town, x 48, z 18) ↔ `l_ouest` (Lower-Town, x 0, z 18). Le portique fait monter le Repérage d'un cran dans le sens de la montée seulement.
- **Rue des Fours** (axe est-ouest, z 15-21) : rue principale, ateliers des deux côtés, gros tuyaux suspendus. Voitures en panne garées de travers.
- **Place de la Relève** (centre, x 20-30, z 21-29) : dalle de béton devant l'usine, horloge de pointage, file d'ouvriers aux heures de relève. Lieu public, caméras.
- **Allée du Foyer** (sud-ouest, ruelle étroite de 2 m) : mène au foyer de Mère Ruiz. Zone aveugle, le Repérage y redescend.
- **Passerelle haute** (nord, z 4-6) : grillage qui longe l'usine, accès par un escalier métallique. Raccourci et point de vue sur la rue.
- **Escalier de la Fosse** (sud-est, x 42, z 34) : escalier de service grillagé vers la Sous-Ville, cadenassé. Jonction réciproque `l_fosse` ↔ `v_fosse` (nouvelle sortie aux Poutres). Ouvert par la clé de Mère Ruiz ou depuis le bas.
- **Vers Asia-Ground** (bord sud, x 8, z 36) : bout de rue qui continue vers le quartier marchand. Jonction `l_sud` ↔ `a_nord`.

## 4. Services (nom affiché seulement une fois découverts) [proposition]
| Avant découverte | Après | Ce qu'on y trouve |
|---|---|---|
| Porte basse, fumée | **Le Foyer Ruiz** | lit (soin, sauvegarde), soupe, rumeurs, 4 cr la nuit |
| Atelier ouvert | **Atelier Bastide** | réparation, pièces, revente de ferraille au poids |
| Guichet grillagé | **Pointage Usine 7** | travail à la journée (contre crédits, implant requis) |
| Comptoir sans enseigne | **Chez Moss** | boissons, contacts, change officieux dollar → crédit |

## 5. PNJ [proposition, Mère Ruiz reprise du plan §6]
| PNJ | Fonction | Envie | Peur | Secret | Voix |
|---|---|---|---|---|---|
| **Mère Ruiz** | tient le foyer de travailleurs | loger tout le monde au chaud | le contrôle de nuit | cache une famille mutante dans la cave | chaleureuse, autoritaire, tutoie |
| **Joaquim Bastide** | ferrailleur, atelier de réparation | racheter son atelier à l'usine | perdre la main droite, déjà abîmée | revend des pièces volées à l'Usine 7 | phrases courtes, parle à ses machines |
| **Contremaître Ilse Raack** | tient le pointage de l'Usine 7 | tenir les quotas | qu'IO remplace l'équipe par des machines | inscrit des morts au pointage et garde leurs paies | lit des chiffres, ne regarde jamais en face |
| **Agent Dorn**, SMPD | patrouille de la rue | finir sa ronde sans histoire | être muté vers la Sous-Ville | prélève sa « protection » chez les commerçants | traînant, faussement copain |
| **Moss** | tenancier du comptoir | savoir avant tout le monde | les gangs de China Lake [canon lieu §2071] | renseigne Dorn quand ça l'arrange | murmure, pose une question à chaque réponse |
| **Pia** | gamine messagère, 11 ans | voir le ciel d'Upper-Town une fois | les sirènes de relève | porte le courrier de la famille cachée de Ruiz | rapide, vulgaire, rit fort |

## 6. Accroche de quête [proposition]
« Contrôle de nuit » : Mère Ruiz apprend par Pia que la SMPD contrôlera le foyer cette nuit. Il faut faire sortir la famille de la cave par l'Escalier de la Fosse avant la ronde de Dorn, ou acheter Dorn (crédits) avec ce que Moss sait sur lui, ou le retenir ailleurs. Le joueur clandestin risque lui-même le contrôle.

## 7. Bâtiments et props pour Création [proposition]
Angle caméra v4, nuit, palette §2.
1. **Atelier-usine** (grand, 14 × 10 m) : façade en tôle, grande porte coulissante entrouverte avec lueur de four, cheminée, tuyaux qui partent vers la rue. Sert d'Usine 7 et, en version réduite, d'Atelier Bastide.
2. **Immeuble ouvrier** (8 × 6 m, 4 niveaux visibles) : béton taché, linge, coursives extérieures, fenêtres bouchées au plastique. Rez-de-chaussée en boutique fermée par rideau.
3. **Foyer Ruiz** (10 × 7 m) : ancienne cantine d'usine, porte basse, vitre embuée chaude, soupirail de cave visible.
4. **Portique de contrôle** (à poser sur la rampe) : arche IO avec scanner, petit voyant, guérite vide.
Props : tuyaux suspendus (droit, coude), poteau sodium, horloge de pointage, voiture en panne, bidons, caisse de ferraille, palettes, grille d'escalier vers le bas, flaque huileuse, passerelle grillagée.
