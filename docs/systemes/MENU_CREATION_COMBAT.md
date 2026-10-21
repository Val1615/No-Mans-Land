# Menu, sauvegarde, codex, création de personnage, combat : conception (phase 1, rien n'est codé)

Légende : **[canon]** roman tome 1 (§ = ligne de l'extraction) · **[décision]** Valentin · **[proposition]** à valider · **[leçon]** maquette `src/a` / bilan `src/b`.
Style : UI v8 « radio de récupération ambre » (`docs/ui/INTERFACE_V8.md`). Maquettes : `docs/systemes/maquettes/`.

## 0. Décisions de Valentin (21/10/2026)
- **[décision]** Nilo est retiré dès le début ; il sera débloqué plus tard par une quête (non écrite).
- **[décision]** La race est choisie au début, dans la création de personnage.
- **[décision]** Menu principal : Nouveau jeu, Continuer, Charger / Sauvegarder, Options, Codex, Crédits, Quitter (adapté au web).
- **[décision]** Création de personnage de cRPG : nom, race (humain, mutant, augmenté, cyborg), origine, compétences, points d'attributs.
- **[décision]** Combat tactique au tour par tour façon vieux Fallout, plus fluide et moins lent.

## 1. Leçons de la maquette [leçon]
- Elle avait création (4 origines, 7 attributs, 10 compétences, profils prêts) et combat (PA, portée, couvert, visée, fumée, garde, réaction). Bilan : « personnalisation visuelle et équilibre limités », « IA et objectifs limités » (`02_Etat-reel-et-ecarts` l.28-30).
- À ne pas reprendre : « ISIO » et la jauge « Aura » de création (ISIO absent du roman ; l'Aura est rare et apprise, Ch. VI §1467, §1488 [canon] : pas un choix de départ) ; 7 attributs proches de SPECIAL.
- À garder : profils prêts à jouer pour qui ne veut pas répartir ; zones de visée.

## 2. Menu principal [proposition]
```
NO MAN'S LAND
> Continuer            (dernière sauvegarde ; grisé s'il n'y en a pas)
  Nouveau jeu          → création de personnage
  Charger / Sauvegarder → emplacements (sauvegarder seulement en partie)
  Options
  Codex
  Crédits
  Quitter              (web : retour à l'écran titre ; « fermer l'onglet » rappelé)
```
- En partie : touche Échap / bouton ≡ ouvre le même menu en pause, avec « Reprendre » en tête.
- Fond : scène d'ambiance de Dusk-Town, musique de Dusk-Town.

**Options**
| Rubrique | Réglages |
|---|---|
| Son | musique (0-100), effets (0-100), couper tout (S) |
| Interface | mode minimal par défaut (H), taille du texte (100 / 115 / 130 %), contraste renforcé (voile 0,85) |
| Combat | vitesse des tours ennemis (×1 / ×2 / ×4), confirmation des actions (double tap / toujours / jamais sur bureau), afficher les chances au survol |
| Accessibilité | texte des dialogues instantané ou défilant, police sans VT323 (Plex seule), réduire les animations |
| Langue | Français (seule langue pour l'instant) |

## 3. Sauvegarde [proposition]
- **localStorage**, clé `nml_save_<n>` : 3 emplacements manuels + 1 **autosave** (à chaque changement de lieu, et avant un combat) + « Continuer » = la plus récente.
- **Sauvegardé** : version du format, date, lieu et position, joueur (nom, race, origine, attributs, compétences, traits, PV, $, crédits, inventaire), drapeaux de quêtes et de PNJ, lieux découverts, quartiers vus, état des compagnons (Nilo absent), réglages **hors** sauvegarde (options séparées, `nml_options`).
- **Pas sauvegardé** : chemins en cours, combat en cours (on recharge l'autosave d'avant combat).
- Vignette : lieu + quartier + date ; pas de capture d'écran (taille).
- Sauvegarde interdite pendant un dialogue ou un combat.

## 4. Codex [proposition]
- Entrées **canon seulement**, débloquées en jeu (lieu visité, mot entendu, objet trouvé). Catégories : Lieux, Factions, Peuples, Objets.
- Chaque entrée : texte court en voix de récupérateur + mention de la source (« Ch. I §75 ») dans les crédits du codex, pas dans le texte.
- Exemples débloquables dès Dusk-Town : Dusk-Town, Human Corporation (« un labo sous la ville, verrouillé ») [Ch. I §75], Service Militarisé [Ch. I §123], Steel-Megalopolis (sarcophage, crédit) [Ch. I §481, décision], Mutants [Ch. I §105].
- Entrée non débloquée : « ??? ».

## 5. Création de personnage [proposition sauf mention]
Deux écrans + récapitulatif. Bouton « Profil prêt » pour sauter la répartition.

**Écran 1 : Identité.** Nom (libre, 16 caractères) ; **race** [décision] ; origine (selon la race) ; apparence : 4 portraits par race (aperçu portrait à gauche).

**Écran 2 : Attributs, compétences, traits.**

**Attributs (6)**, de 1 à 8, base 3, **12 points** à répartir :
| Attribut | Sert à |
|---|---|
| Carrure | PV, corps à corps, porter |
| Réflexes | PA, initiative, esquive |
| Œil | précision, portée, repérer les portes camouflées |
| Méninges | technique, médecine, nombre de compétences favorites |
| Bagou | prix, mensonges crus, réactions des PNJ |
| Nerfs | résistance à la peur, tir sous pression, ne pas fuir |

**Compétences (11)**, 0-100, 3 **favorites** (+15 au départ, progression plus rapide) ; usages concrets **déjà** dans Dusk-Town :
| Compétence | Usage existant ou proche |
|---|---|
| Armes à feu | combat |
| Corps à corps | combat |
| Discrétion | rues vides de Dusk-Town, éviter la patrouille (Teo : « marche à l'ombre des façades ») |
| Crochetage | portes murées, cave, futur accès Steel |
| Parole | faire dire la vérité à Ezequiel, mentir à Anselme sans être cru plus tard |
| Troc | prix d'Anselme (4 $), de Sol (3 $), de Teo (5 $) ; l'échange objet contre objet arrivera avec elle |
| Médecine | soins de Vera (15 $) ou se soigner soi-même |
| Mécanique | le joint de la pompe de Mara, le cric de la porte d'acier |
| Survie | eau et rations sur la route de Steel |
| Électronique | interphone du labo, portiques et terminaux de Steel |
| Observation | entrées camouflées, signal du miroir de Teo |

**Traits** (0 à 2, chacun avec contrepartie) : Pas de nerfs (PA +1, Nerfs −2), Œil de pillard (objets en plus, prix +10 %), Gueule cassée (intimide, Bagou −1 en commerce), Insomniaque (tour de garde, PV max −3), Pieds de sable (marche désert sans fatigue, ville −Discrétion).

**Races** [décision pour l'entrée de Steel ; détails = proposition]
| Race | Implant | Douane de Steel | Réactions | Effet mécanique léger |
|---|---|---|---|---|
| Humain | non | refusé [décision] | neutre partout ; Dusk-Town plus à l'aise | Bagou +1 |
| Mutant | non | attaqué à vue [décision] | Service Militarisé hostile [canon Ch. I §105] ; Sol se confie | Carrure +1, résistance aux radiations, Bagou −1 avec les soldats |
| Augmenté | oui [décision] | passe | Dusk-Town méfiante (« on dirait du matériel d'IO ») | Électronique +15 |
| Cyborg | oui [décision] | passe | méfiance ; PNJ des Sables évitent | Carrure +1, PV +5, Médecine soigne moins (pièces) |
[canon] Les quatre peuples existent (Ch. XII §3626 : « Humains, Mutants, Augmentés ou Cyborgs… et même des Androïdes ») ; les implants identifient (Ch. I §157, Ch. VII §1652). Androïde non jouable.

**Origines (3 par race, 2175)** [proposition] :
- Humain : Récupératrice des ruines · Caravanier sans caravane · Fille de fermiers de l'oasis.
- Mutant : Né dans les Sables (caché à Dusk-Town) · Rescapé d'une rafle · Errant des terres brûlées.
- Augmenté : Ouvrier de Lower-Town congédié · Ancien flic de la ville basse (SMPD [canon Ch. II §665], ambiguïté 2175) · Coursier d'IO perdu dans le désert.
- Cyborg : Vétéran réformé du Service Militarisé · Corps reconstruit après un accident de machine · Gardien de convoi au bras de série.
Chaque origine : +1 attribut, 1 compétence favorite imposée, 1 objet, 1 réplique spéciale avec 1 PNJ de Dusk-Town.

## 6. Combat [proposition]
**Principe** : vieux Fallout (PA, tour par tour, zones de visée), sans attentes mortes.
- **Entrée/sortie sans changement d'écran** : même scène, même caméra v4 ; un liseré ambre + bandeau « COMBAT » ; la grille apparaît en surimpression discrète. Fin : grille et bandeau s'effacent, la musique revient.
- **Initiative** : Réflexes + d4, ordre affiché en frise de portraits en haut (petite, translucide).
- **PA** : 6 + (Réflexes − 3) / 2, arrondi ; plafonnés à 10. Coûts : 1 PA = 1 m (2 cases de la grille 0,5 m existante) ; tir simple 3, visé 4 (+1 zone), rafale 5, recharger 2, objet 2, se baisser 1 (couvert +).
- **Portée / couverture / ligne de vue** : rayon sur la grille de collisions existante (bâtiments, meubles, props) ; couvert partiel (props bas : caisses, sacs de sable, épave) −20 %, total = pas de tir ; ligne de vue rouge si bloquée.
- **Visée de zone** : torse / tête / bras / jambes [leçon : maquette] ; tête −30 % mais critique ; jambes ralentit ; bras désarme.
- **Fluidité** : déplacement continu (aucun pas à pas) ; **tours ennemis en simultané visuel** quand ils n'interagissent pas entre eux ; vitesse ×1/×2/×4 (option, et maintien d'une touche) ; aucune pause ni confirmation hors action risquée ; fin de tour automatique à 0 PA ; caméra ne bouge que si l'action sort de l'écran.
- **Aperçu au survol / appui long** : chemin et coût en PA sur la grille, chance de toucher par zone, dégâts estimés, couvert de la cible. Sur mobile : 1er tap = aperçu, 2e tap = confirmer.
- **Fuite** : sortir du champ de vision ennemi 2 tours, ou atteindre un bord de zone.
- **Mobile** : barre d'actions en bas (4 boutons max visibles + « … »), zones de visée en 4 gros boutons au-dessus, frise d'initiative réduite à 5 portraits.
- **Premier usage** : la douane de Steel pour un mutant (attaqué à vue) [décision] ; la patrouille du Transit.

## 7. Ordre de production [proposition]
1. Menu principal + options + sauvegarde (le jeu actuel devient « Nouveau jeu » avec personnage par défaut).
2. Création (écrans 1-2), retrait de Nilo, race et implant dans l'état.
3. Codex (entrées de Dusk-Town).
4. Combat : déplacement + tir + couvert sur une rencontre test, puis visée, IA, mobile.
Tests au pixel et par gestes comme pour v8-v9 à chaque étape.

## 8. Maquettes (pistes, `docs/systemes/maquettes/`)
`menu.png` (fond généré `menu-fond-genere.jpg`) · `creation-1-identite.png` · `creation-2-attributs.png` · `combat-desktop.png` · `combat-mobile.png` (390×844) · `options.png` · `codex.png`. Fonds de combat, d'options et de codex = vraies captures du jeu (Le Transit, La Pompe), Nilo retiré. Soldats = sprite provisoire de la maquette (`city-people-v3-0`), à remplacer. Script : `generer_maquettes.py`.
