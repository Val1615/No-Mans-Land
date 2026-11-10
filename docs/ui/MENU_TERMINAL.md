# Menu principal : Terminal Human Corp

Fiche de direction artistique, pour Rivet.  
Rédigée le 10 novembre 2026 (heure de Paris), par Ocre.

La maquette de référence, `docs/ui/proto_menu_terminal.jpg`, est une **maquette générée**, pas une capture du jeu. Un contrôle de construction des calques (fond, tampon, cadre, sans le texte) se trouve dans `docs/ui/controle_menu_terminal.jpg`. Ce n'est pas non plus une capture.

Les calques images sont dans `assets/ui/menu_terminal/`, décrits plus bas et dans `assets/ui/menu_terminal/manifest.json`. Une variante portrait (1080 × 1920), pour le téléphone, est décrite au §8.

---

## Statuts

Je distingue clairement trois choses.

- **Canon.** Ce que le jeu et le roman tiennent déjà pour vrai : l'année 2175, Steel-Mégalopolis, Center-Town, le carrefour Arcadius, Human Corp, Teng, Orc Énergie, Groovy Vibes et Groovy-Tron. Je m'appuie aussi sur des formules déjà présentes dans le jeu (« Building a better tomorrow. », « Human Corp sponsorise le sourire. », « Souriez. C'est mesuré. »).
- **Décision.** Valentin, le 10 novembre 2026 (heure de Paris) : le menu principal suit la direction « Terminal Human Corp », un terminal CRT ambre diégétique de la mégacorporation. Il l'a voulu animé, et très « terminal informatique ».
- **Proposition.** Tout le reste de cette fiche : nom du système d'exploitation, identifiants du poste, textes du boot et du bandeau, rythme des animations, traitement visuel du cadre. Rien de tout cela n'est canon tant que ce n'est pas joué et tenu.

Les plaques déjà gravées sur le calque `cadre.png` (numéro de poste HC-2175-TA, « Secteur 09 / Zone 12 », slogan « L'unité avant tout », norme HC-STD-2175) sont des inventions de la maquette. Elles restent sur l'asset. Je les reprends dans les textes pour rester cohérente avec le cadre, sans les élever au canon.

---

## 1. Intention et contraintes

Le joueur allume un terminal citoyen Human Corp, pas un menu posé sur une illustration. L'écran est diégétique : on est déjà un peu dans Steel, déjà un peu sous surveillance, avant même d'avoir commencé.

Ça n'autorise pas le décor à manger l'interface. Les choix restent lisibles, discrets, jamais masqués : ni par le tampon, ni par le ticker, ni par un glitch, ni par le fond de ville. L'ambre porte le texte. La ville derrière reste atténuée, pour donner de la profondeur, pas pour concurrencer les lignes.

Contraintes que je tiens pour acquises :

- **Lisibilité d'abord.** Contraste élevé, phosphore sur fond presque noir. Si le fond de ville gêne une ligne, on assombrit localement derrière le texte (un voile très léger, pas un cartouche opaque).
- **Rien ne cache les choix.** Le tampon reste en bas à droite, hors de la liste. Les effets CRT se tiennent sages au moment de la lecture.
- **Mouvement réduit.** On branche l'option déjà présente, `reduceMotion` (« Réduire les animations » dans Options), et `prefers-reduced-motion` du système. Dans ce mode : pas de scintillement, pas de glitch, pas de dérive des scanlines, pas de séquence d'allumage (on arrive directement à l'état de repos). Le curseur peut rester fixe, ou pulser très lentement. Le ticker peut alterner ses messages sans défilement, toutes les quatre secondes environ.
- **Boot sautable.** N'importe quelle touche ou clic saute la séquence et affiche le menu au repos. Si le mouvement réduit est actif, on la saute d'office.

Le menu pause n'a pas été tranché. **Proposition :** même langage visuel, sans rallumer le tube. L'écran est déjà allumé, les lignes se réécrivent.

---

## 2. Palette

On reste cousu à l'ambre déjà en jeu (`--c: #f2b44a` dans `src/style.css`), pour que le menu et l'HUD parlent la même langue.

| Rôle | Hex | Usage |
|---|---|---|
| Phosphore principal | `#F2B44A` | Texte courant, entrées du menu au repos, lueur de base |
| Phosphore vif | `#FFD078` | Titre, ligne d'allumage, sélection, flash de confirmation |
| Phosphore atténué | `#C4892E` | Journal de boot, barre de statut, ticker |
| Ambre clair | `#FDE9C2` | Déjà `--t` dans l'UI. À réserver aux sous-textes, pas au phosphore du tube |
| Fond d'écran | `#0A0804` | Sous le calque ville, au cas où le fond manquerait |
| Alerte | `#C43B2A` | Encre du tampon, messages d'erreur rares. Avec parcimonie, jamais en fond de menu |
| Métal du cadre | (image) | On ne le repeint pas. Le calque `cadre.png` porte la lunette |

**Lueurs (glow).** Sur le texte, un halo en trois couches, par exemple :

`text-shadow: 0 0 4px #F2B44A, 0 0 12px rgba(242,180,74,.55), 0 0 28px rgba(242,180,74,.22);`

Le titre a droit à un peu plus (ajouter une quatrième couche, autour de 40 px, à 12 % d'opacité). Le journal de boot, un peu moins. En mouvement réduit, on garde une lueur fixe et courte (la première couche suffit).

---

## 3. Typographie

Les deux polices sont **déjà dans le dépôt**, sous licence SIL Open Font License 1.1, dans `assets/fonts/` :

- **VT323** (Peter Hull), famille CSS déjà déclarée `'VT'`. C'est le caractère du tube : titre, journal de boot, liste du menu, commandes `EXEC`, ticker si on le veut plus « terminal ».
- **IBM Plex Mono** Regular et Medium (IBM), famille `'Plex'`. Plus lisible sur la durée : panneaux Options, Crédits, Chargement, et tout le menu si le joueur active l'option « Police : Lisible » (`options.readable`), comme aujourd'hui.

Tailles proposées, données pour le canevas 1920 × 1080. Elles suivent l'échelle du terminal si la fenêtre n'est pas en 16:9 plein cadre.

| Élément | Police | Taille | Interligne / chasse |
|---|---|---|---|
| Titre NO MAN'S LAND | VT323 | 112 px | chasse 0,08 em, capitales |
| Entrées du menu | VT323 | 34 px | interligne 1,6. Zone tactile d'au moins 44 px de haut |
| Journal de boot | VT323 | 20 px | interligne 1,25 |
| Commande `EXEC` | VT323 | 20 px | comme le boot |
| Barre de statut | IBM Plex Mono | 16 px | interligne 1,35 |
| Ticker | IBM Plex Mono | 15 px | une seule ligne, défilement horizontal |
| Sous-panneaux (Options, etc.) | IBM Plex Mono | 16 à 18 px | comme l'UI actuelle, retravaillée dans le même ambre |

Le titre de la maquette a un air de matrice à points. **Proposition :** VT323 suffit, avec la chasse et la lueur. Si on veut le pointillisme de la maquette, on peut l'approcher en CSS (un léger `mask` de points, ou un fill semi-transparent sur une grille), sans passer par une image du titre. Le titre reste du texte, pour l'accessibilité et les traductions plus tard.

---

## 4. Disposition de l'écran

Canevas de référence : **1920 × 1080**. Le terminal se pose en `contain` dans la fenêtre, bandes noires si le cadre n'est pas 16:9. Toutes les coordonnées ci-dessous sont relatives à ce canevas, puis mises à l'échelle.

### 4.1 Rectangle de l'écran (trou du tube)

Détecté sur la région noire de `cadre.png`, puis décrit en rectangle arrondi pour que le contenu code se cale pile.

| | px |
|---|---|
| x | 168 |
| y | 117 |
| w | 1584 |
| h | 821 |
| rayon d'angle | 54 |
| fondu du bord | 5 px, uniquement vers l'intérieur du trou (l'ombre interne du cadre reste sur le calque métal) |

Le fichier `ecran_masque.png` donne le même trou en blanc (alpha 0 ailleurs), avec le même fondu. Rivet peut s'en servir pour clipper le fond, le texte et les effets.

### 4.2 Bloc titre, liste, statut, ticker

À l'intérieur du rectangle écran, avec une marge intérieure d'environ 56 px :

- **Journal de boot**, en haut à gauche, le temps de la séquence. Il peut rester, plus discret, une fois le menu posé, ou s'effacer pour laisser le titre respirer. **Proposition :** il s'efface (fondu 250 ms) juste avant l'apparition du titre, pour ne pas encombrer.
- **Titre NO MAN'S LAND**, centré horizontalement, autour de 38 % de la hauteur de l'écran.
- **Liste du menu**, centrée sous le titre, alignée à gauche sur la colonne des libellés, avec le prompt `>` (ou `■` pour la ligne active) dans la marge gauche. Entrées, dans cet ordre :

  1. CONTINUER  
  2. NOUVELLE PARTIE  
  3. CHARGER  
  4. OPTIONS  
  5. CRÉDITS  
  6. QUITTER  

  CONTINUER est désactivé, en phosphore atténué, s'il n'y a pas de sauvegarde. Le sous-texte de la dernière sauvegarde (déjà prévu dans le shell actuel) peut s'afficher en 16 px sous l'entrée, sans bouger les autres lignes.

- **Barre de statut**, en bas à gauche, au-dessus du ticker, deux lignes (voir les textes plus bas).
- **Ticker de surveillance**, une bande d'environ 36 à 44 px de haut, tout le bas de l'écran, au-dessus de la lèvre du cadre. Il ne monte jamais sur la liste.
- **Tampon « Accès non autorisé »**, en bas à droite de l'écran, hors de la liste. Position proposée à 1920 × 1080 : **x = 1286, y = 708, w = 436, h = 232**, opacité **0,85**. Il apparaît en fin de boot, avec un petit flash. **Proposition :** mode de fusion `multiply` s'il paraît trop vif sur le fond (la maquette le montrait un peu plus usé par le phosphore).

Le jeu a déjà deux entrées en plus, que cette liste de titre ne reprend pas : **Reprendre** (menu pause) et **Codex**. **Proposition :** on les garde dans le même langage (`REPRENDRE`, `CODEX`) au moment voulu, sans les inventer ici comme décision.

Sur mobile, on réduit typo et marges pour que les six choix restent tapables (44 px de haut au minimum), sans casser le cadre.

### 4.3 Plaques du cadre (déjà dans l'image, on ne les redessine pas)

Elles appartiennent à `cadre.png` :

- haut : `HUMAN CORP` / `CITIZEN TERMINAL UNIT - HC-2175-TA`
- haut droite : `HAUTE TENSION` / `NE PAS OUVRIR`
- gauche : `SECTEUR 09` / `ZONE 12` / `8847-2175-TA`
- droite : `PROPRIÉTÉ DE HUMAN CORP` / `NE PAS DÉPLACER`
- bas gauche : `CONFORME HC-STD-2175` / `N° 8847-TA-03`
- bas droite : `2175` / `L'UNITÉ AVANT TOUT`

---

## 5. Timeline d'animation

Durées en millisecondes. Le timing est une **proposition**, le sentiment recherché ne l'est pas : un vrai tube qui s'allume, puis un système qui tape, puis un menu qui attend.

### 5.1 Allumage et boot (sautable)

| t (ms) | Quoi |
|---|---|
| 0 | Cadre déjà visible. Écran noir (le fond ville et le texte sont à opacité 0). |
| 0 à 80 | Court silence. Éventuel souffle du tube (son, optionnel). |
| 80 à 280 | Une ligne horizontale phosphore vif, 2 px de haut, apparaît au milieu de l'écran et s'étend de gauche à droite. |
| 280 à 700 | La ligne s'ouvre à la verticale (le tube « se déplie »), bref flash blanc-ambre. |
| 700 à 1500 | Réchauffement du phosphore : le fond ville monte de 0 à 100 %, légère surexposition vers 1200 puis retour. |
| 1500 | Le journal de boot commence à se taper, ligne après ligne, à **36 caractères par seconde** (fourchette 30 à 40). Pause de 60 ms entre deux lignes. Curseur bloc en fin de ligne. |
| fin du journal (environ 1500 + durée du texte, typiquement 8 à 11 s si on ne saute pas) | Le journal fond (250 ms). |
| +0 à 800 | Révélation du titre NO MAN'S LAND : soit lettre à lettre, soit un balayage de scanline de haut en bas, lueur un peu plus forte le temps de l'apparition. |
| +800 à 1400 | Les entrées du menu apparaissent une par une, toutes les 90 ms, déjà précédées de `>`. |
| +1400 à 1700 | Barre de statut, puis le ticker démarre. |
| +1700 à 1900 | Le tampon se pose, opacité 0 à 0,85, avec un flash ambre de 120 ms sur sa zone (pas sur tout l'écran). |

N'importe quelle touche ou clic pendant cette séquence coupe tout et affiche l'état de repos (titre, menu, statut, ticker, tampon). Pas de punition, pas de message d'erreur.

### 5.2 Boucles au repos

| Effet | Rythme | Détail |
|---|---|---|
| Curseur bloc | 530 ms allumé, 530 ms éteint | Curseur plein, à droite de la ligne sélectionnée, ou en bas si on affiche une ligne de commande. C'est le clignotement classique. |
| Scanlines | Fixes, dérive optionnelle très lente (8 à 12 s pour 2 px) | Lignes horizontales sombres, 1 px toutes les 3 px, opacité 8 à 12 %. Elles ne doivent pas gêner la lecture. |
| Scintillement | Toutes les 50 à 80 ms | Variation de luminosité du phosphore, entre 96 et 100 %. À peine perceptible. |
| Glitch | Toutes les 8 à 20 s, durée **120 ms** | Déchirure horizontale d'une bande de 8 à 16 px, plus un léger décalage chromatique (canal rouge / vert, 1 à 2 px). Jamais sur la ligne active au moment d'une confirmation. |
| Ticker | Défilement ~45 px/s | Boucle continue, séparateur `  //  ` entre les messages. |

### 5.3 Survol, sélection, confirmation

- **Sélection** (clavier haut/bas, ou survol souris) : vidéo inverse (texte `#0A0804` sur un pavé `#F2B44A`) et prompt `>` à gauche. La maquette montrait un `■` sur CONTINUER : on peut le garder pour la ligne active, et `>` pour les autres. Je privilégie la consigne : inverse + `>`.
- **Confirmation** : flash court de 100 ms sur la ligne (phosphore vif), puis une commande tapée à 36 car/s, par exemple `> EXEC NOUVELLE_PARTIE`. Ensuite seulement on enchaîne (création de personnage, sous-panneau, etc.).
- Commandes proposées : `> EXEC CONTINUER`, `> EXEC NOUVELLE_PARTIE`, `> EXEC CHARGER`, `> EXEC OPTIONS`, `> EXEC CREDITS`, `> EXEC QUITTER`.

### 5.4 Sons (optionnels)

Tous branchés sur le volume « Effets » déjà prévu, coupés si le volume est à zéro.

- Bourdon grave du tube, en boucle, très bas, tant que le menu est ouvert.
- Clics de touche sur le déplacement, la frappe du boot et la commande `EXEC`.
- Bip court à la confirmation.
- Attaque douce à l'allumage (une montée, pas une alarme).
- Léger parasite sur le glitch.

Ce sont des suggestions. Je ne livrerai les sons que si on me les demande.

---

## 6. Textes du terminal

Tous prêts à brancher. Les identifiants de poste et le nom de l'OS sont des **propositions**, alignées sur les plaques du cadre. Les toponymes et les marques sont ceux du jeu. Je n'invente aucune autre corporation : Human Corp, Teng, Orc Énergie, Arcadius. Groovy Vibes et Groovy-Tron uniquement sous ces noms.

### 6.1 Journal de boot (14 lignes)

À taper tel quel, une ligne après l'autre :

```
HUMAN CORP  //  CITIZEN OS v4.7.19
TERMINAL CITOYEN  HC-2175-TA
HORLOGE INTERNE  2175-04-12  03:42:17
IDENTIFIANT  HC-CTZN-8847-2175-TA
CLASSEMENT  OMEGA-7  (PROVISOIRE)
SITE  STEEL-MEGALOPOLIS  //  CENTER-TOWN, CARREFOUR ARCADIUS
-- chargement des privileges residuels...
-- memoire vive      64 Ko     OK
-- memoire morte     128 Ko    OK
-- reseau Human Corp           CONNECTE    debit surveille
-- module de conformite        ACTIF
-- identification citoyen      EN ATTENTE
-- integrite systeme           OK
-- pret a recevoir les commandes
```

Les lignes techniques (`-- memoire vive`, etc.) sont volontairement sans accents, comme un vieux terminal un peu paresseux sur l'encodage. Les libellés du menu, eux, portent leurs accents (CRÉDITS, QUITTER). **Proposition de variante un peu plus ironique** pour deux lignes, si on veut appuyer le ton, à la place des lignes mémoire :

```
-- memoire vive      64 Ko     suffisant pour un citoyen
-- memoire morte     128 Ko    vos droits aussi
```

Je préfère la version sobre pour le boot, et garder l'ironie pour le ticker. La ligne de clôture peut aussi être : `-- systeme pret. votre cooperation est appreciee.`

### 6.2 Barre de statut

Deux lignes, en phosphore atténué :

```
TERMINAL HC-2175-TA  //  STEEL-MEGALOPOLIS  //  CENTER-TOWN
CITOYEN NON IDENTIFIE  //  ACCES SOUS SURVEILLANCE
```

### 6.3 Ticker de surveillance (12 messages)

À enchaîner en boucle, dans cet ordre ou mélangés à chaque ouverture du menu :

1. `HUMAN CORP. BUILDING A BETTER TOMORROW.`
2. `HUMAN CORP SPONSORISE LE SOURIRE.`
3. `SOURIEZ. C'EST MESURE.`
4. `COUVRE-FEU SECTORIEL : 22 H 00 A 05 H 00. LES CONTROLES SONT ALEATOIRES.`
5. `CENTER-TOWN : CIRCULATION FLUIDE AU CARREFOUR ARCADIUS. TEMPS D'ATTENTE ACCEPTABLE.`
6. `ORC ENERGIE : AJUSTEMENT DE CHARGE SUR LE RESEAU. ECONOMISEZ, CITOYEN.`
7. `TENG : LE CHANGE EST OUVERT. COMPTEZ DEUX FOIS.`
8. `CONCERT GROOVY CREW, SPONSORISE PAR HUMAN CORP. CONTROLE D'IDENTITE A L'ENTREE.`
9. `PULSE PLAZA : AFFLUENCE ELEVEE. SOURIEZ, VOUS ETES ENREGISTRES.`
10. `FREQUENCE STRIP : PROGRAMMATION CONFORME. NIVEAU SONORE DANS LES LIMITES AUTORISEES.`
11. `STEEL ARENA : PROCHAINE EPREUVE SOUS PATRONAGE HUMAN CORP. PLACES SOUS QUOTA.`
12. `HUMAN CORP VOUS VEILLE. VOUS DORMEZ MIEUX AINSI.`

Les trois premiers reprennent des formules déjà entendues dans le jeu. Les autres sont des **propositions**.

### 6.4 Erreurs et œufs de Pâques

À afficher en phosphore atténué, ou en alerte s'il le faut, jamais par-dessus les choix plus d'une seconde ou deux.

| Déclencheur | Ligne |
|---|---|
| CONTINUER sans sauvegarde | `AUCUNE SESSION ANTERIEURE. VOUS N'EXISTEZ PAS ENCORE POUR NOUS.` |
| Commande inconnue / frappe libre | `COMMANDE INCONNUE. CETTE TENTATIVE A ETE CONSIGNEE.` |
| Demande d'aide (`AIDE`, `HELP`, F1) | `L'AIDE N'EST PAS DISPONIBLE POUR VOTRE CLASSEMENT.` |
| Action non prévue | `CITOYEN, CETTE FONCTION N'EST PAS INCLUSE DANS VOTRE FORFAIT.` |
| Accès refusé (entrée grisée, etc.) | `ACCES REFUSE. VEUILLEZ SOURIRE A LA CAMERA ET REESSAYER.` |
| QUITTER | `SESSION CONSIGNEE. HUMAN CORP VOUS REMERCIE POUR VOTRE TEMPS.` |
| Spam de flèches ou de clics | `LES RACCOURCIS NON DOCUMENTES SONT UNE INFRACTION LEGERE.` |
| Cinq appuis sur le numéro de version (déjà en place pour le mode DEV) | `MODE MAINTENANCE DEVERROUILLE.` (on garde le comportement actuel, on change juste la formulation) |

---

## 7. Calques : images et code

Tout ce qui n'est pas listé comme fichier image se fait **en code** (CSS, canvas, ou les deux) : journal de boot, logo typographique NO MAN'S LAND, liste du menu, barre de statut, ticker, curseur, scanlines, scintillement, glitch, lueurs. Pas d'image figée de ces éléments, pour pouvoir les animer, les traduire et les brancher sur le mouvement réduit.

### 7.1 Table d'empilement (du fond vers l'avant)

| Calque | Fichier | Animé ou fixe | Comment |
|---|---|---|---|
| Fond de ville ambre | `assets/ui/menu_terminal/fond_ecran.png` | Fixe. **Proposition :** très lente dérive (8 à 15 px en 20 s, aller-retour), coupée si mouvement réduit | 1920 × 1080. Il s'assied sous le cadre, visible uniquement par le trou (clip avec `ecran_masque.png` ou le rectangle arrondi). |
| Contenu texte | (code) | Animé | Boot, titre, menu, statut, curseur, ticker. Clipé dans le rectangle écran. |
| Tampon « Accès non autorisé » | `assets/ui/menu_terminal/tampon_acces_non_autorise.png` | Fixe, une fois posé. Apparaît en fin de boot avec un petit flash | Position 1286, 708 (436 × 232) à 1920 × 1080, opacité 0,85. Ne recouvre pas les choix. Fichier source recadré, fond blanc détouré, grain d'encre conservé. |
| Effets CRT | (code) | Animé | Scanlines, scintillement, vignette, éventuelle courbure légère. La courbure, si on en met, doit rester subtile et ne pas flouter le texte (on peut la limiter au fond). Coupés ou figés si mouvement réduit. |
| Cadre métal | `assets/ui/menu_terminal/cadre.png` | Fixe, toujours au-dessus | 1920 × 1080, zone écran entièrement transparente (alpha 0), bord en rectangle arrondi légèrement fondu. L'ombre interne de la lunette reste sur ce calque. |

Fichiers utiles en plus :

- `assets/ui/menu_terminal/ecran_masque.png` : blanc = zone écran, transparent ailleurs.
- `assets/ui/menu_terminal/manifest.json` : canevas, rectangle, positions, mêmes infos que cette table.

Contrôle de construction (fond + tampon + cadre, sans texte) : `docs/ui/controle_menu_terminal.jpg`. Maquette générée complète, avec le texte peint pour le ton : `docs/ui/proto_menu_terminal.jpg`. La variante portrait (mêmes principes, canevas 1080 × 1920) est au §8.

### 7.2 Notes d'implémentation (propositions, pas un cahier des charges technique)

Je n'écris pas le code, je propose une voie possible.

- Réutiliser la structure actuelle `#menu` / `src/ui/shell.js` / `src/style.css` (lot v10), en remplaçant le fond `menu-fond.jpg` et les boutons opaques par les calques et le langage terminal. On ne jette pas les sauvegardes, les options ni le déblocage du mode DEV.
- Couches CSS empilées dans l'ordre du tableau, le texte en HTML (accessibilité, navigation clavier déjà là). Un canvas au-dessus du fond, sous le cadre, peut porter le bruit, le scintillement et le glitch sans toucher au DOM du menu.
- Courbure du tube : filtre SVG ou un léger `perspective`, uniquement si le texte reste net. Sinon, une vignette et le cadre suffisent : la maquette portait déjà beaucoup de « tube » par la lunette.
- Brancher `options.reduceMotion` (déjà lu dans le shell) et `prefers-reduced-motion`.
- Polices : les `@font-face` existent déjà. Rien à rajouter au dépôt de polices.

---

## 8. Version portrait (mobile)

Le jeu tourne aussi en portrait, notamment à 390 px de large sur téléphone. Ce n'est pas une autre direction : c'est le même terminal, redressé. **Proposition de bascule :** on prend la variante portrait quand la hauteur de la fenêtre est supérieure à sa largeur, la variante paysage sinon.

Le canevas portrait est **1080 × 1920**. Comme en paysage, le terminal se pose en `contain` dans la fenêtre. **On n'étire jamais le cadre de façon non uniforme** (pas de `sx` différent de `sy`, pas de `cover` qui rogne une plaque). S'il ne tient pas honnêtement, on le retire : voir le repli plus bas.

### 8.1 Calques portrait

Même ordre d'empilement qu'en paysage. Le tampon réutilise le fichier déjà livré, simplement recentré.

| Calque | Fichier | Animé ou fixe | Comment |
|---|---|---|---|
| Fond de ville ambre | `assets/ui/menu_terminal/fond_ecran_portrait.png` | Fixe. Même dérive lente optionnelle qu'en paysage, coupée si mouvement réduit | 1080 × 1920, visible par le trou |
| Contenu texte | (code) | Animé | Boot raccourci, titre sur deux lignes, menu vertical, ticker en bas |
| Tampon « Accès non autorisé » | `assets/ui/menu_terminal/tampon_acces_non_autorise.png` (le même) | Fixe, une fois posé. Apparaît en fin de boot avec un petit flash | Position **x = 309, y = 1416, w = 458, h = 243**, opacité **0,85**. Centré en bas de l'écran, largeur égale à 55 % de l'écran, au-dessus du ticker. Ne recouvre pas les choix |
| Effets CRT | (code) | Animé | Scanlines, scintillement, vignette, courbure éventuelle. Figés ou coupés si mouvement réduit |
| Cadre métal | `assets/ui/menu_terminal/cadre_portrait.png` | Fixe, toujours au-dessus | 1080 × 1920, zone écran entièrement transparente, même méthode que `cadre.png` (trou en rectangle arrondi, fondu vers l'intérieur, ombre interne conservée) |

Masque : `assets/ui/menu_terminal/ecran_masque_portrait.png` (blanc = zone écran). Les géométries sont aussi dans `manifest.json`, clé ajoutée `portrait` (les clés paysage restent inchangées).

Rectangle de l'écran, à 1080 × 1920 :

| | px |
|---|---|
| x | 122 |
| y | 132 |
| w | 832 |
| h | 1625 |
| rayon d'angle | 60 |
| fondu du bord | 5 px, uniquement vers l'intérieur |

Contrôle de construction (fond + tampon + cadre, sans texte) : `docs/ui/controle_menu_terminal_portrait.jpg`. Ce n'est pas une capture de jeu.

### 8.2 Disposition du texte

Si on se contentait de réduire le titrage paysage à l'échelle du canevas, à 390 px de large les entrées du menu tomberaient à une douzaine de pixels : illisible, et injouable au doigt. Les tailles ci-dessous sont donc des **planchers en pixels CSS, calés pour une largeur de fenêtre de 390 px**. Quand la fenêtre grossit, on peut les laisser suivre l'échelle du terminal, sans redescendre sous ces valeurs.

| Élément | Police | Taille à 390 px de large | Notes |
|---|---|---|---|
| Titre, sur deux lignes : `NO MAN'S` / `LAND` | VT323 | 44 à 48 px | Centré, chasse un peu serrée, lueur comme en paysage |
| Entrées du menu | VT323 | 18 à 20 px | Une sous l'autre, au centre. **Hauteur de cible d'au moins 44 px** (48 px de préférence), préfixe `>` compris |
| Journal de boot (6 lignes) | VT323 | 13 à 14 px | En haut à gauche, il s'efface avant le titre, comme en paysage |
| Barre de statut | IBM Plex Mono | 12 px | Une ou deux lignes courtes, sous le titre ou juste au-dessus du ticker, jamais au milieu des choix |
| Ticker | IBM Plex Mono | 12 px | Une bande en bas de l'écran, au-dessus de la lèvre du cadre, qui ne monte pas sur le menu ni sur le tampon |

Ordre vertical, du haut vers le bas : journal de boot (le temps de la séquence), titre sur deux lignes, liste du menu, tampon, ticker. La barre de statut se glisse sous le titre ou au-dessus du ticker, selon ce qui reste le plus lisible. Le tampon, déjà placé en bas et au centre, laisse la colonne des choix libre.

Journal de boot raccourci, **proposition**, six lignes :

```
HUMAN CORP  //  CITIZEN OS v4.7.19
TERMINAL CITOYEN  HC-2175-TA
SITE  STEEL-MEGALOPOLIS  //  CENTER-TOWN
-- module de conformite        ACTIF
-- identification citoyen      EN ATTENTE
-- pret a recevoir les commandes
```

Les messages du ticker, les commandes `EXEC` et les lignes d'erreur restent ceux du §6. L'allumage, le clignotement du curseur, le scintillement, le glitch et le mouvement réduit suivent la timeline du §5. Sur un premier lancement en portrait, **proposition :** on peut raccourcir un peu les silences du boot (le journal a moins de lignes, le titre arrive plus tôt), sans changer les durées d'animation d'un caractère ou d'un flash.

### 8.3 Repli, en dessous de 390 px ou sur un très petit écran

Les plaques du cadre sont décoratives. On peut les retirer sans rien perdre du menu.

**Proposition de repli :** si la fenêtre passe sous 390 px de large, ou si le cadre `contain` devient trop mince pour rester honnête (plaques illisibles, marges écrasées), on enlève le cadre entièrement. L'écran (fond de ville, texte, tampon, effets CRT) passe en plein cadre, avec une marge intérieure d'une dizaine de pixels. Les scanlines, la vignette et l'éventuelle courbure restent, rendues en code. Le fond portrait peut être conservé, recadré avec `cover` uniquement sur cette image de ville, jamais sur le cadre.

Dans tous les cas, on n'étire pas le cadre pour le faire tenir.

---

Voilà pour Rivet de quoi construire, paysage et portrait. Je reste disponible pour caler un rythme, un libellé ou une passe sur le tampon une fois le premier allumage sous les yeux.
