# Rencontre du jalon 2 : « L'écluse des Verriers » (créatures mutantes)

Jalon 2 du chantier (voir [README.md](README.md)), famille **créatures mutantes**, variante du biome de verre. Création : Ocre, 18/11/2026 (heure de Paris). Même format que [PILOTE.md](PILOTE.md) et [CARAVANE.md](CARAVANE.md). Le nom du fichier suit la consigne : ni le README ni ARCHI.md n'en prévoient d'autre.

> **Écrite sur [`ARCHI.md`](ARCHI.md) et sur le format réel de `src/data/rencontres_caravane.js`** (lot 1 de Rivet) : format §4, `points` (examens et fouilles avec `alt`), `entrees`, `dureeSi`, `drapeauArrivee`, `enseignes`. Préfixes `rc_` / `rc_vr_` (modules du verre, nouveaux, réutilisables) / `rc_ecl_` (propres à l'écluse) / `g_rc_` / `gen_rc_`, 50 px/m. Scène 36 × 30 m (dans la plage 24 × 24 à 48 × 36), zone de combat 19 × 19 entièrement dedans. Ennemis en positions absolues sur des cases libres, à ≥ 8 m de l'entrée et répartis. **Aucun ennemi neutre** : les Verriers ne sont jamais dans la liste. **Aucune hauteur** : pas de `niveaux`, pas de `y`, tout le monde au sol ; le canal est **ensablé** presque jusqu'au bord, pour la même raison que le lit du pilote. Journal par case. Drapeaux de scène `ver_*` remis à zéro à la sortie ; drapeaux de monde `monde_verriers_*` justifiés au §7. Examen au toucher sur mobile. Ambiance qui suit l'heure du voyage : nouvelle courbe `glass` proposée au §11. Liseré de lune existant. Une seule lumière artificielle : la gueule du four, source visible.
>
> **Sans sprites** (consigne de Régie) : rien n'est produit dans ce lot. Les clés nouvelles sont listées au §10 ; la piste, le panneau, les rochers et le fût réutilisent les sprites publiés (`assets/rencontres/manifest.json`).

Maquette concept (MAQUETTE, pas une capture) : `/workspace/nml-shots/rencontres/mutants_concept.png` sur la machine d'Ocre. Elle montre une vue iso en volumes de principe et le plan coté. Le plan coté de ce document fait foi.

**Mutants et créatures : la distinction de cette rencontre.**
- Les **mutants** sont des gens : une race jouable (`race_mutant`), la population majoritaire du No Man's Land d'après la planche de référence « Population — Mutants », pourchassée par le Service Militarisé. Ici, ce sont les **Verriers** : une famille élargie qui vit au bord du verre, parce que le Service n'y entre pas.
- Les **créatures mutantes** de la famille de rencontres sont des **bêtes** : une harde de pécaris du verre, les **chanchos de ceniza**. Elles ont soif ; elles ne parlent pas ; elles n'ont rien d'humain.
- Le repo ne prévoyait encore **aucune faune hostile** (aucune créature dans `src/`). Les chanchos sont donc la première ; ils sont nommés et dessinés pour qu'aucun joueur ne les confonde avec des mutants humains (§6.5, §13).

## 1. Fiche
| Champ | Valeur |
|---|---|
| id | `ecluse_verriers` [proposition], préfixe de drapeaux `ver_` |
| Famille | Créatures mutantes, variante « verre » : la harde est l'obstacle, les mutants sont les hôtes |
| Terrains | `verre` (p = 0,20) **et** `piste` (p = 0,05) de `src/data/nml.js`, filtrés par le biome `glass` ; taux inchangés. Les deux sont nécessaires : une case traversée par la piste a le terrain `piste`, même dans le verre (`voyage.js`), et c'est le cas de I04, I03 et K03 |
| Biome | verre (`glass` du manifeste) : plaine de sable vitrifié au bord de la zone d'impact de Big Larry, traversée par un canal UFSA mort et ensablé |
| Cases de référence | **tirage sur n'importe quelle case de verre (I04, I03, J04 par exemple)** : aucune rencontre n'est attachée à une case, le catalogue tire sur terrain et biome, et le journal par case ne retient que ce qui s'est passé sur une case déjà visitée. Cases `glass` possibles : H02, I02, J02, K02, H03, J04, K04 (terrain `verre`) ; I03, I04, K03 (terrain `piste`). J03 (Big Larry, un lieu) ne tire jamais. Le pilote (désert, roche) et la caravane (désert) ne tirent pas sur le verre. Pour le test : forcée par le mode DEV |
| Moment | toute heure : la lumière suit le voyage (courbe `glass`, §11) ; le texte d'arrivée ne parle ni du jour ni de la nuit |
| Emprise | 36 × 30 m (x vers l'est, z vers le sud, origine au coin nord-ouest), **un seul niveau de marche, au sol** |
| Faction | aucune : une communauté de mutants indépendante, les « Verriers » (voir §13) |
| Rejouable | non : journal par case. Les Verriers sont **uniques** : `si` refuse la rencontre si `monde_verriers_vus` est posé (drapeau d'arrivée, jamais purgé) |
| Durée ajoutée | 1 h ; +4 h si le joueur attend la nuit avec eux (`dureeSi: { ver_attendu: 4 }`, champ existant) |

## 2. Pitch et situation
**Pitch.** Au bord du verre, une écluse morte barre un canal ensablé. Des mutants y vivent, sous une péniche retournée, et filtrent la rosée du verre. Ce matin, une harde de pécaris assoiffés est descendue dans la cuve de l'écluse. Le plus jeune des Verriers s'est enfermé dans la cabane de la pompe, avec toute l'eau du camp. Le gros mâle gris enfonce la porte du front.

**Situation.** Les **Verriers** sont une dizaine ; on en voit quatre. Avant, ils vivaient au bord de Dusk-Town. Les rafles du Service Militarisé les ont poussés vers le seul endroit où les camions ne vont pas : le verre. Le sable fondu par l'impact de Big Larry garde une chaleur qu'on ne sent pas. Les « gens de bonne peau » y perdent leurs cheveux en une saison. Les mutants, qui résistent mieux aux radiations, y vivent mal, mais ils y vivent. Ils fondent le verre en perles et en lames, condensent la rosée qui perle sur les dalles la nuit, et servent d'étape à la **filière** de Remedios (CARAVANE) : des passagers attendent ici que les camions du Service se lassent, avant d'entrer à Dusk-Town « par en dessous ».

**Les personnages.**
- **Tecla**, l'aînée, décide.
- **Balta** garde le camp. Il n'a que trois balles et une femme dans la Sous-Ville.
- **Rufina** souffle le verre. Elle est arrivée par la citerne de Remedios.
- **Nilo**, quatorze ans, tient la cabane.

Le joueur peut passer, troquer, soigner, s'informer, éloigner la harde de trois façons (l'eau, le feu, attendre la nuit) ou la combattre, rançonner les Verriers, ou les chasser. Les Verriers **ne se battent jamais contre le joueur** : menacés, ils reculent dans le verre, où un non-mutant ne les suit pas. La piste traverse la scène ; la sortie est est **ouverte** dès l'arrivée.

## 3. Ce que le décor raconte
Tout est examinable (clic sur ordinateur ; sur mobile, appui sur le point d'examen, avec un anneau ; pas d'examen au survol). Les indices marqués ★ mènent à la filière. Ceux marqués ◆ préparent une solution pour la harde.

| Où (x ; z) | Ce qu'on voit | Texte d'examen | Effet |
|---|---|---|---|
| Plaine de verre (vers 14 ; 3) | sable fondu en dalles brun-noir et vert bouteille sale, soulevées, craquelées, croûtes de sel blanc | « Le sable a fondu ici, il y a longtemps, et il a refroidi en dalles. Brun, noir, vert de bouteille sale. Ça craque sous la semelle comme de la glace sale. Rien ne pousse, sauf un lichen orange dans les fentes. » ◆ Observation 4 : « Dans les creux des dalles, des traces de groin dans le sel. Des bêtes viennent lécher quelque chose ici, la nuit. » | `flag:ver_indice_rosee` |
| Blindé vitrifié (27,5 ; 4,5) | véhicule blindé du Service à moitié pris dans le verre, peinture grise brûlée, écoutille ouverte | « Un blindé du Service, enfoncé dans le verre jusqu'aux essieux, comme dans de la boue qui aurait pris. La peinture grise a cloqué. L'écoutille est ouverte. Personne n'est venu le chercher. » Observation 5 : « Sur le flanc, à la craie : un cercle. Puis les mots "ILS NE VIENNENT PAS". » | ouvre la fouille du blindé (§9) |
| Panneau (1,4 ; 16,6) | panneau UFSA criblé (réutilisé) | « Le panneau a perdu presque toutes ses lettres. On lit encore : CANAL … ÉCLUSE 7. Quelqu'un a gratté le reste. » | — |
| Péniche retournée (7,5 ; 14,2) | coque de péniche à l'envers, à demi enterrée dans le limon, ouverture découpée au chalumeau, rideau de toile | « Une péniche, la quille en l'air, ensablée jusqu'au plat-bord. Ils ont découpé une porte dans la coque et tendu une toile devant. Dedans, il fait plus frais qu'ailleurs. C'est la maison. » | — |
| ★ Porte d'écluse (19,7 ; 12,5) | porte nord fermée, rouillée, passerelle de fer au-dessus ; des dizaines de perles de verre enfilées sur un fil, autour d'un montant | « La porte nord de l'écluse est soudée par la rouille. Autour du montant, un fil de fer, et sur le fil, des perles de verre sombre, rouge et vert. Des dizaines. Certaines sont ternies par le sable, d'autres brillent encore. » ★ Observation 3 : « Les plus vieilles sont en bas. Il y en a une neuve tout en haut, encore tranchante. Ce n'est pas un ornement : on compte quelque chose. » | `flag:ver_indice_perles` |
| Four (11,5 ; 19,4) | four à verre en terre et briques réfractaires, cheminée, gueule orange | « Un four de terre crue et de briques sauvées du canal. La gueule rougeoie. À côté, une canne de fer, des moules, et un tas de dalles de verre brisées en morceaux, prêtes à refondre. » | — |
| Condenseurs (17 ; 19) | trois cadres de bois, toiles goudronnées tendues en pente, jarres dessous | « Trois toiles tendues en pente sur des cadres. La nuit, le verre refroidit et la rosée coule le long de la toile jusqu'aux jarres. Les jarres sont renversées. Des traces de sabots, partout autour. » ◆ « La harde est passée ici avant l'écluse. » | `flag:ver_indice_condens` |
| Établi (7,5 ; 18,6) | établi de Rufina : pinces, perles qui refroidissent sur une plaque, lames de verre noir | « Des perles qui refroidissent sur une plaque de tôle, une rangée de lames de verre noir taillées en feuille, des pinces. » | point de vente et de vol (§9) |
| Cuve de l'écluse (27 ; 12) | limon craquelé, flaque de boue rouillée, jarres brisées, la harde | « La cuve de l'écluse, comblée de limon jusqu'à un mètre du bord. Une flaque de boue rouille au milieu, des tessons de jarres. » | — |
| Cabane de la pompe, porte nord (26 ; 16,2) | porte de planches renforcée de tôle, marquée de coups de boutoir | « La porte de la cabane de la pompe. La tôle est enfoncée à hauteur de genou, en trois endroits. Quelqu'un a coincé une poutre derrière. » | — |
| Cabane, fenêtre sud (26 ; 20,4) | fenêtre à barreaux, planches clouées, un œil derrière | dialogue de Nilo (§6.4) | — |
| ◆ Rigole est (34,5 ; 8,2), au bord du quai nord | ancienne rigole de vidange qui sort de la cuve vers l'est, dans le verre | « Une rigole de pierre part du bout de la cuve vers l'est et se perd dans le verre. Le vent vient de l'ouest. » | point du leurre d'eau (§6.2, §9) |

Lecture à 1280 et en 390 :
- dès l'arrivée, l'œil trouve d'abord **la porte d'écluse noire contre le verre clair** (la silhouette de la scène) ;
- puis **le four**, seule tache chaude ;
- puis la **harde grise dans la cuve**, qui bouge.

La péniche retournée se lit comme une maison au troisième regard. Nilo n'est pas visible.

**Lumière artificielle : une seule, la gueule du four.** C'est un `_neon` serré sur la bouche du four, source visible, même principe que le feu du bivouac de la caravane. La nuit, une **flaque chaude au sol** devant la gueule (la retouche demandée par Régie pour le bivouac, à appliquer ici d'emblée, §12.9). Le verre **ne luit pas** : ni phosphorescence, ni lueur radioactive, ni halo. C'est une matière morte, qui réfléchit la lumière du ciel et rien d'autre.

## 4. Plan coté (provisoire)
Vue de dessus, 1 caractère = 1 m.

Légende :
- **Verre et quai nord** :
  - `v` plaine de verre (praticable, déclencheur de rayonnement `T_verre`) ;
  - `d` dalles soulevées (solides, `couv: 1`) ;
  - `V` blindé vitrifié (solide, `couv: 2`) ;
  - `q` quai nord, béton (praticable) ;
  - `-` parapet du canal (0,7 m, solide, `couv: 1`) ;
  - `e` passages dans le parapet (escalier nord, cale sud-ouest, seuil de la cabane).
- **Canal et écluse** :
  - `:` limon du canal ensablé (praticable) ;
  - `P` péniche retournée ;
  - `|` porte nord de l'écluse (fermée) ;
  - `/` porte sud (ouverte, rabattue vers l'est) ;
  - `j` jarres brisées (décalque) ;
  - `~` flaque de boue (décalque).
- **Camp** :
  - `,` sable cendré ;
  - `E` établi ;
  - `K` four (gueule au sud) ;
  - `c` condenseurs (×3) ;
  - `o` fût ;
  - `H` cabane de la pompe ;
  - `S` panneau.
- **Piste et bords** : `=` piste (6 m) ; `R` rochers.
- **Personnages** :
  - `@` apparition ;
  - `B` Balta ;
  - `1` Tecla ;
  - `2` Rufina ;
  - `N` Nilo (après sa sortie) ;
  - `G` le gris ;
  - `h` les jeunes chanchos.
- **Sorties** : `O>` sortie ouest, `<E` sortie est.

```text
      0         1         2         3     
      012345678901234567890123456789012345
  0   vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
  1   vvvvvvvvvvvvvvvvvvvvvvvvvvVVVVVvvvvv
  2   vvvvvddvvvvvvvvvvvvvvvvvvvVVVVVvvvvv
  3   vvvvvddvvvvvvvddvvvvvvvvvvVVVVVvvvvv
  4   vvvvvvvvvvvvvvddvvvvvvvvvvvvvvvvvvvv
  5   vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
  6   vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
  7   qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq
  8   ------------eee---------------------
  9   :::::::::::::::::::|::::::::::::::::
 10   ::PPPPPPPPPPP::::::|::::h:jj::::::::
 11   ::PPPPPPPPPPP::::::|::::~~~~~~~::h::
 12   ::PPPPPPPPPPP:::::::::::~~~~~G~:::::
 13   ::PPPPPPPPPPP:::::::::::~~h~~~~:::::
 14   ::::::::::::::::::::///:::::::::::::
 15   ---eee------------------eee---------
 16   ,S,,,,,,,,KKK,cccccc,,,,HHHH,,,,,,,,
 17   ,,,,,,EEE,KKK,cccccco,,,HHHH,,,,,,,,
 18   ,,,,,,,2,,KKK,,,,,,,,,,,HHHH,,,,,,,,
 19   ,,,,,,,,,,,,,1,,,,,,,,,,HHHH,,,,,,,,
 20   ,,,,,B,,,,,,,,,,,,,,,,,,,N,,,,,,,,,,
 21 O>====================================<E
 22 O>====================================<E
 23 O>====================================<E
 24 O>=@==================================<E
 25 O>====================================<E
 26 O>====================================<E
 27   ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
 28   ,,,,,,,,RRR,,,,,,,,,,,,,,,,,,RRR,,,,
 29   ,,,,,,,,RRR,,,,,,,,,,,,,,,,,,RRR,,,,
```

Le schéma arrondit au mètre ; les cotes du tableau font foi. Les condenseurs sont trois cadres de 1,5 × 2 m, séparés de 0,5 m (passages de 0,5 m, trop étroits pour une case de 1 m : la rangée fait barrière, comme une haie).

### Éléments et solides
| id | Élément | x0-x1 | z0-z1 | Haut. (m) | Solide | Couverture combat |
|---|---|---|---|---|---|---|
| sol_verre | plaine de verre | 0-36 | 0-7 | 0 | non | 0 |
| sol_quai | quai nord, dalles de béton fendues | 0-36 | 7-8,5 | 0 | non | 0 |
| sol_limon | lit du canal ensablé | 0-36 | 9-15 | 0 | non | 0 |
| sol_cendre | camp, bas-côtés | 0-36 | 15,5-21 et 27-30 | 0 | non | 0 |
| sol_piste | piste damée (réutilisée) | 0-36 | 21-27 | 0 | non | 0 |
| dalles ×2 | dalles de verre soulevées | 5-7 / 14-16 | 2-4 / 3-5 | 1,2 / 0,9 | oui | 1 |
| blinde | blindé vitrifié du Service | 26-31 | 1-4 | 2,4 | oui | 2 |
| parapet_n | parapet nord du canal, sauf l'escalier x 12-15 | 0-12 et 15-36 | 8,5-9 | 0,7 | oui | 1 |
| parapet_s | parapet sud, sauf la cale x 3-6 et le seuil x 24-27 | 0-3, 6-24, 27-36 | 15-15,5 | 0,7 | oui | 1 |
| peniche | péniche retournée, porte au sud (x 7-8) | 2-13 | 9,5-14 | 3,0 | oui (on n'entre pas) | 2 |
| porte_n | porte nord de l'écluse, fermée, avec son bajoyer et la passerelle | 19-20,5 | 9-12 | 3,4 | oui | 2 |
| porte_s | porte sud, ouverte, rabattue contre le bajoyer sud | 20,5-23,5 | 14-15 | 3,4 | oui | 2 |
| jarres | jarres brisées (décalque, dans `rc_ecl_cuve_3q`) | 26-28 | 10-11 | 0 | non | 0 |
| boue | flaque de boue rouillée (décalque, idem) | 24-31 | 11-14 | 0 | non | 0 |
| etabli | établi de Rufina | 6-9 | 17,2-18 | 0,9 | oui | 1 |
| four | four à verre, gueule au sud en (11,5 ; 19) | 10-13 | 16,3-19 | 2,2 (cheminée 3,4) | oui | 2 |
| condens ×3 | condenseurs, cadres et toiles | 14-15,5 / 16-17,5 / 18-19,5 | 16,3-18,3 | 1,8 | oui | 1 |
| fut | fût (réutilisé `barrel`) | 20,7-21,3 | 17-17,6 | 0,9 | oui | 1 |
| cabane | cabane de la pompe, briques et tôle ; porte au nord (x 25,5-26,5), fenêtre au sud | 24-28 | 16,2-20 | 3,0 | oui | 2 |
| panneau | panneau UFSA (réutilisé) | 1,2-1,8 | 16,4-16,6 | 3,0 | oui (0,2 × 0,2) | 0 |
| rochers ×2 | blocs du bas-côté sud (réutilisés) | 8-11 / 29-32 | 27,8-29,3 / 27,9-29,4 | 1,6 / 1,2 | oui | 1 |

Un seul niveau de marche, au sol. Le canal est **ensablé** : le limon arrive à 0,7 m sous le haut des parapets, rendu par le sol `g_rc_limon` (plus sombre) et l'épaisseur peinte des parapets. Aucun `niveaux`, aucun `y`, aucun PNJ en hauteur. La passerelle de l'écluse est peinte sur le sprite de la porte nord : elle ne se parcourt pas.

**Chemins à pied depuis l'entrée** (règle d'ARCHI « tout atteignable ») :
- **Camp** : directement depuis la piste.
- **Cuve** : par le seuil x 24-27 (devant la porte de la cabane) ou par la cale x 3-6, puis le limon.
- **Quai nord et rigole est** : cale → limon (bande z 14-15 au sud de la péniche, puis x 13-15 entre la péniche et le parapet) → escalier x 12-15 → quai → vers l'est.
- **Verre et blindé** : par le quai.

### Apparition, sorties, déclencheurs
| id | Type | Position (m) | Rôle |
|---|---|---|---|
| spawn | apparition | (1,5 ; 24), regard vers l'est | on arrive par la piste depuis Dusk-Town ; la porte d'écluse, le four et la harde sont lisibles |
| S_O | sortie | x = 0, z 21-27 | demi-tour : retour à la carte, halte sur la case, itinéraire conservé |
| S_E | sortie | x = 36, z 21-27 | reprise du voyage vers Big Larry. **Jamais gardée** (sauf pendant le combat, règle existante) |
| T1 | déclencheur | x 4-6, z 15,5-27 | Balta interpelle le joueur une fois (§6.1, nœud `start`) |
| T_verre | déclencheur | x 0-36, z 0-7 | le rayonnement du verre, une fois par scène : non-mutant `hurt:1` + texte ; mutant : texte seul ; avec `compteur` : texte du compteur (§6.6) |
| pres_cabane | déclencheur | x 24-28 ; z 20-21 (le long de la façade sud) | ouvre le dialogue de Nilo par la fenêtre sur mobile, sans viser la petite fenêtre |
| fuite | combat | bords de la zone 19 × 19 | issue « fuite » : retour à la carte comme S_O |

### Zone de combat
Centre (24 ; 15), zone 19 × 19 (x 14,5-33,5 ; z 5,5-24,5), entièrement dans l'emprise : aucune case dans le vide.
- **Dedans** : la cuve, la porte de la cabane, les condenseurs, la piste et le quai.
- **Couverture** : les parapets comptent comme solides `couv: 1`. Les combattants se tirent par-dessus, ce qui ne sert à rien contre des bêtes au contact. Mais ce sont des obstacles qu'il faut contourner par le seuil ou l'escalier.

## 5. Mise en scène échelonnée (découverte progressive)
1. **Arrivée** (x 1,5) : la piste longe un camp au bord d'un canal mort. Au nord, le verre, clair, plat, presque blanc à midi ; la porte d'écluse noire qui se découpe dessus ; un four qui rougeoie. Dans la cuve, des bêtes grises remuent. Rien n'impose de s'arrêter.
2. **Le garde** (T1, x ≥ 4) : Balta, à la cale, fusil à un coup tenu bas. Il ne menace pas : il demande à voir le cou (§6.1). C'est le geste des soldats du Service à Dusk-Town, retourné.
3. **L'aînée** : Tecla, au four, décide comment on règle la harde ; elle propose l'eau, le feu ou l'attente (§6.2).
4. **La harde** : examiner la cuve, parler à Nilo par la fenêtre ; le gris cogne la porte de la cabane toutes les dix minutes (ligne de récit, pas d'événement chronométré).
5. **Après** : Nilo sort ; Tecla donne l'eau et des perles ; Rufina vend ; Balta parle de sa femme. Les indices (perles sur la porte, cercle sur le blindé) mènent à la filière, pour qui connaît Remedios.

## 6. PNJ : fiches et dialogues
Format : celui de `src/data/rencontres_caravane.js`. Nœuds `text` + `options`, avec `next` et `action` : `buy:`, `sell:`, `take:`, `give:`, `gain:`, `hurt:`, `heal:`, `flag:`, `combat:`, `rencontre:`. Tests : `test`, `pass`, `fail`, `partial`/`partialAt`, `opposed`. Conditions `if` composées `a&b|c`. Entrées multiples par `entrees`.

Conditions de race et d'origine par les drapeaux de création existants (`race_mutant`, `race_humain`, `race_augmente`, `race_cyborg`, `origine_sables`, `origine_rafle`, `origine_errant`). Les identifiants sont des propositions.

**[Attaquer] chez les Verriers** ne lance pas de combat : il mène au nœud commun `fuient` (§6.2). Les Verriers reculent dans le verre.

### 6.1 Balta, le garde
- **Portrait** : la quarantaine, large, une crête d'excroissances osseuses qui part de la nuque et descend sur l'épaule gauche, peau épaisse et grise au cou. Chemise sans col (il n'a rien à cacher ici), gilet de toile, foulard rouille. Fusil à un coup, trois cartouches dans une poche de poitrine. Une morsure fraîche au mollet droit, bandée à la hâte.
- **Caractère** : méfiant, juste, fatigué. Il attend sa femme, prise dans une rafle il y a trois hivers.
- **Stats** (jamais en combat contre le joueur) : PV 14, Volonté 6.
- **Sprite** : `gen_rc_balta` (à produire) + portrait. Position (5,5 ; 20,4), à la cale, regard vers la piste.

```text
start   (T1) (Il tient son fusil canon vers le sol. Il ne te regarde qu'à moitié : l'autre moitié surveille l'écluse.)
        « Pas plus loin. Pas avant que je t'aie vu le cou. »
  - « Mon cou ? »                                                → col
  - [si race_mutant] (Tu baisses ton col sans qu'il le redemande.) → col_mutant
  - « Je passe sur la piste. Je ne m'arrête pas. »               → passe
  - « Je m'en vais. »                                             → end
col     « À Dusk-Town, le Service fait baisser les cols. Ici aussi on regarde. Pas pour la même raison. Baisse-le. »
  - (Baisser le col.) [si race_humain]                            → col_humain
  - (Baisser le col.) [si race_augmente|race_cyborg]              → implant
  - (Baisser le col.) [si race_mutant]                            → col_mutant
  - « Non. »                                                      → refus
col_mutant (Il regarde, longtemps. Puis il remet le fusil à l'épaule.) « Bon. Ça t'a pris où, à toi ? … Laisse. On ne se demande pas ça. »
           action flag:ver_salue;flag:ver_confiance → harde_intro
col_humain (Il regarde ta peau intacte, puis tes mains, puis tes bottes.) « Rien. Alors tu viens de chez les gens de bonne peau. Tu ne portes pas leur gris. C'est déjà ça. »
           action flag:ver_salue → harde_intro
implant (Il voit la cicatrice de l'implant et recule d'un pas, sans lever son arme.) « Un implant d'IO parle à qui l'écoute. Et le Service écoute. Reste là où je te vois. »
           action flag:ver_salue;flag:ver_mefiance → harde_intro
refus   « Alors la piste est par là. Elle est large. »            action flag:ver_salue;flag:ver_mefiance → end
passe   « Bien. Continue. Et ne traîne pas sur le verre : il ne fait pas de cadeau aux gens de bonne peau. »   action flag:ver_salue → end

harde_intro (Un grognement, de l'autre côté du parapet. Puis un choc sourd contre une porte.)
        « Les chanchos. Ils sont descendus dans la cuve à l'aube. Le petit s'est enfermé dans la cabane, avec toute notre eau. Ils sentent l'eau. Moi, j'ai trois balles. L'an dernier, le gris en a pris deux sans ralentir. »
  - « Je peux aider. »                                            → aider
  - « Des chanchos ? »                                            → chanchos
  - « Ce n'est pas mon problème. »                                → pasmon
chanchos « Des cochons de cendre. Ils vivent dans le verre, comme nous, et ils mangent ce que le verre laisse pousser, c'est-à-dire presque rien. Ils boivent la rosée sur les dalles, la nuit. Ce sont des bêtes, et ils ont soif. Je ne leur en veux pas. Mais c'est notre eau qu'ils veulent. »
  - « Je peux aider. »                                            → aider
  - « Ce n'est pas mon problème. »                                → pasmon
aider   « Va voir la vieille, au four. C'est elle qui décide comment on fait. Moi, je tiens la cale. »   action flag:ver_q_harde → end
pasmon  « Personne ne te l'a demandé. »                           → end

encore  (entrée si ver_salue & !ver_harde_partie) « Encore là. »
  - [si !ver_q_harde] « Je peux aider, pour les bêtes. »          → aider
  - [si ver_q_harde & !ver_conseil_gris] « Le gris. Il se bat comment ? » → gris
  - [si !ver_soigne & !ver_soin_dit] « Ta jambe saigne. Montre. »  test medecine:4 → pass soin, fail soin_rate
  - [si !ver_ines] « Tu as l'air d'attendre quelqu'un. »          → ines
  - [si ver_ines & monde_lena_connue & !ver_message_ines] « J'ai croisé une fille de Novo Córdoba qui cherche son père dans la Sous-Ville. Lena. » → lena
  - [Attaquer]                                                    → rc_tecla:fuient
  - « Plus tard. »                                                → end
gris    « Il charge droit, comme un camion. Il s'arrête quand il a mal, et les autres s'arrêtent quand il s'arrête. Tape le gris. Laisse les jeunes. »   action flag:ver_conseil_gris → encore
soin    (Tu laves la morsure au mauvais alcool de Rufina et tu serres un vrai pansement. Il ne bronche pas.) « … Tu as des mains, toi. »   action flag:ver_soigne;flag:ver_confiance → encore
soin_rate « Laisse. Ça a vu pire. »                               action flag:ver_soin_dit → encore
ines    « Ma femme. Ines. Ils l'ont prise au marché de Dusk-Town, il y a trois hivers, avec douze autres. Le Service appelle ça un "transfert". En bas, on dit "la Sous-Ville". Personne n'en revient. Moi, j'attends au bord du verre, parce que c'est le seul endroit où ils ne viennent pas me chercher. »
        action flag:ver_ines → encore
lena    (Il se tait un moment.) « La Sous-Ville. Toujours la Sous-Ville. » (Il fouille sa poche, en sort une perle rouge.) « Si tu la revois : Ines, de Dusk-Town, celle qui chante faux. Qu'elle demande, en bas. Donne-lui ça, Ines la reconnaîtra. »
        action give:perles_verre;flag:ver_message_ines;flag:monde_message_ines → encore

apres   (entrée si ver_harde_partie) (Il a reposé le fusil contre le parapet.) « Le petit est dehors. L'eau aussi. Je te dois une balle. Je n'en ai que trois, alors c'est beaucoup. »
  - [si !ver_ines] « Tu as l'air d'attendre quelqu'un. »          → ines
  - [si ver_ines & monde_lena_connue & !ver_message_ines] « Lena, de Novo Córdoba, cherche son père dans la Sous-Ville. » → lena
  - « Garde tes balles. »                                         → end
```

### 6.2 Tecla, l'aînée
- **Portrait** : environ soixante-dix ans, petite, assise contre le four sur une caisse, couverture sur les genoux. Excroissances calcifiées aux tempes, comme des racines blanches sous la peau ; yeux laiteux (elle voit des formes et la chaleur, mal le reste) ; talisman de verre au cou. Voix basse, phrases courtes, humour sec.
- **Rôle** : c'est elle qui décide. Elle a mené les Verriers hors de Dusk-Town après les rafles.
- **Sprite** : `gen_rc_tecla` (à produire, **assise**, comme Quilla) + portrait. Position (13,2 ; 19,6), à droite de la gueule du four, regard vers la piste.

```text
start   (Elle tourne la tête vers ta voix avant que tu aies parlé.) « Tu marches comme quelqu'un qui a de bonnes bottes. Assieds-toi, ou pas. Le four ne fait pas la différence. »
  - [si race_mutant & !ver_eau_offerte] « Je suis des vôtres. »    → mutant
  - « Qui êtes-vous ? »                                           → qui
  - [si !ver_harde_partie] « Les chanchos. Comment je peux aider ? » → harde
  - [si ver_harde_partie & !ver_merci] « La cuve est vide. Le petit peut sortir. » → merci
  - « Le verre, là-haut. Qu'est-ce que c'est ? »                  → verre
  - [si monde_remedios_vue] « J'ai croisé la caravane de Remedios. » → remedios
  - [si ver_indice_perles & !ver_perles_dites] « Les perles, sur la porte de l'écluse. »  → perles
  - [si !ver_regle] « Je connais un sergent à Big Larry qui paierait cher pour savoir où vous dormez. » → menace
  - [Attaquer]                                                    → fuient
  - « Je m'en vais. »                                             → end

mutant  « Des vôtres. » (Elle tend la main, paume ouverte, et attend.) « Ici, on ne dit pas ça. On dit : "Tu as soif ?" Et l'autre répond. »
  - « J'ai soif. »                                                → mutant_eau
  - [si origine_rafle] « Ils m'ont pris, une fois. J'ai sauté du camion. »     → rafle
  - [si origine_sables] « J'ai grandi sous un foulard, à Dusk-Town. »          → sables
  - [si origine_errant] « Je viens de plus loin que la carte. »                → errant
mutant_eau « Bois. » (Une gourde de terre, l'eau tiède et propre.) « Si un jour il te faut un endroit où le Service ne vient pas, il y a de la place dans la coque. Pas de lit, mais pas de camion non plus. »
        action give:water;flag:ver_eau_offerte;flag:ver_confiance → start
rafle   « Alors tu as sauté au-dessus du verre, ou pas loin : leurs camions passent par la piste du cratère. On en a ramassé, des sauteurs. Certains avaient arraché la plaque du camion, comme un trophée. Garde la tienne. Elle te rappellera la route. »
        action flag:ver_eau_offerte;flag:ver_confiance → start
sables  « Alors Sol t'a vu grandir. Sol nous monte du fil et des aiguilles, une fois par saison. Dis-lui que la vieille du four a encore ses dix doigts. »
        action flag:ver_eau_offerte;flag:ver_confiance → start
errant  « Tu sens l'eau, alors, comme Nilo. Dis-moi où elle est, ici. »
  - (Tu fermes les yeux. Sous la proue de la péniche, à l'ouest. Profond.)   → errant_ok
errant_ok (Elle rit, pour la première fois.) « La citerne sous la proue. Même Balta ne la trouve pas sans moi. Prends un bidon, pour le nez. Et ne le dis à personne d'autre. »
        action give:water;flag:ver_eau_offerte;flag:ver_confiance;flag:ver_citerne_dite → start

qui     « Ceux qui vivent ici. À Dusk-Town, on nous appelait les Verriers, parce qu'on fond le verre. Le Service, lui, ne nous appelle pas : il ne vient pas jusqu'ici. » → start
verre   « Il y a eu un feu dans le ciel, il y a très longtemps. Le sable a fondu. Big Larry, le trou, c'est par là. Le verre garde au fond de lui une chaleur qu'on ne sent pas. Les gens de bonne peau y laissent leurs cheveux en une saison. Nous, en dix ans. C'est toute la différence, et cette différence, c'est une maison. »   → start

harde   « Trois jeunes et le gris. Ils ont soif, ils ont senti les jarres. Balta veut les tirer, avec ses trois balles. Il y a d'autres façons. »
  - « Leur donner de l'eau, ailleurs. »                           → leurre
  - « Le feu. Les bêtes ont peur du feu. »                         → feu
  - « Ils finiront par partir tout seuls ? »                       → attendre
  - « Je m'en occupe. À ma façon. »                                → combat_dit
  - « Plus tard. »                                                → start
leurre  « De l'eau, au bout de la cuve. Monte sur le quai nord par l'escalier, va jusqu'à la rigole de l'est et verse-la dedans, doucement. Le vent vient de l'ouest : ils la sentiront, et la rigole les mènera dans le verre. Un bidon suffit, si tu le fais bien. Le petit peut t'en passer un par la fenêtre, si tu n'en as pas. »
        action flag:ver_q_leurre → harde
feu     « Celles-là aussi ont peur du feu, si on le leur met sous le groin. Rufina te donnera un tison. Mais le gris ne recule pas devant une flamme qui tremble. »
        action flag:ver_q_tison → harde
attendre « À la nuit, quand le verre refroidit, ils retournent lécher la rosée sur les dalles. Si tu restes, tu attends avec nous. Quatre heures, peut-être cinq. Le petit aura chaud, mais il a toute l'eau. »
  - « J'attends avec vous. »                                      → attendu
  - « Pas le temps. »                                             → harde
attendu (Le soleil descend sur le verre. Balta ne lâche pas la cuve des yeux. Rufina fait cuire des galettes sur la sole du four, et Tecla te raconte Dusk-Town avant les rafles, quand on ne baissait pas les cols. À la nuit, le gris lève le groin, renifle vers le nord, et la harde remonte dans le verre. Nilo sort de la cabane en clignant des yeux.)
        action flag:ver_attendu;flag:ver_harde_partie;flag:ver_nilo_libre;heal:3 → merci
combat_dit « Alors vise le gris. Et ne tue que si tu ne peux pas faire autrement : un chancho mort, c'est de la viande, mais c'est aussi une mère qui ne revient pas l'année d'après. »
        action flag:ver_q_harde → end

merci   (Nilo a couru jusqu'au four, puis il s'est arrêté net à deux pas : il a quatorze ans et ne veut pas qu'on le voie courir.) « Il est entier. L'eau aussi. »
        action give:water:2;give:perles_verre:3;flag:ver_merci;flag:ver_nilo_libre;flag:monde_verriers_amis → merci2
merci2  « Les perles, c'est Rufina qui les fait. Celles-là, on ne les compte pas : elles sont pour toi. Montre-les sur la piste de Novo Córdoba, à qui il faut. Ceux qui savent sauront. »   → start

remedios (Elle sourit.) « Remedios. Sa citerne fuit toujours par le haut ? »
  - [si monde_lena_connue] « Elle ne fuit pas. Elle respire. »   → filiere
  - [si monde_remedios_repartie] « Elle a réparé. Elle monte vers Dusk-Town. » → remedios_ok
  - « Je ne sais pas. »                                           → remedios_non
filiere « Alors tu sais. Ce qui monte dans sa citerne descend parfois ici. On garde les gens quelques jours au bord du verre, le temps que les camions du Service se lassent. Ensuite, Remedios les reprend, ou Sol les fait entrer à Dusk-Town par en dessous. Rufina est arrivée comme ça. »
        action flag:ver_filiere_dite;flag:ver_confiance → start
remedios_ok « Bien. Elle passera par ici avant la ville. Elle passe toujours par ici avant la ville. »   → start
remedios_non « Alors c'est que tu ne sais pas. C'est très bien comme ça. »   → start
perles  « Demande à Rufina. Ce sont ses perles, et c'est son compte. »   → start

menace  (Tecla ne bouge pas. Balta, lui, a bougé.) « Un sergent à Big Larry. Ils ont tous un sergent à Big Larry. »
  - « Vingt dollars, et je l'oublie. »                             test intimider:7, opposed (Volonté 7) → pass menace_ok, fail menace_rate
  - « C'était une façon de parler. »                              → parler
parler  « Au bord du verre, les façons de parler font des morts. »   action flag:ver_mefiance → start
menace_ok « Rufina, donne-lui la boîte. » (Rufina compte. Ça ne fait pas vingt : quatorze dollars et trois perles.) « C'est tout ce qu'on a. Prends-le. Demain, il n'y aura plus personne ici à vendre : on a l'habitude. »
        action gain:14;give:perles_verre:3;flag:ver_regle;flag:ver_racket;flag:monde_verriers_menaces → end
menace_rate « Non. Tu n'iras pas à Big Larry : le Service paie les dénonciateurs en balles, et tu le sais. » (Balta épaule.) « La piste. »
  - « Je pars. »                                                  action flag:ver_regle;flag:ver_menace → end
  - [Attaquer]                                                    → fuient

fuient  (Tecla se lève sans aide. Ils ne courent pas. Ils reculent ensemble vers l'escalier du quai, puis dans le verre, Balta le dernier, le canon sur toi. Nilo saute par la fenêtre de la cabane et les rejoint.)
        [si !race_mutant] (Tu fais trois pas derrière eux. Le verre craque sous tes semelles, et ta peau te dit de reculer.)
        [si race_mutant] (Tu pourrais les suivre. Personne ne t'attend, là-bas.)
        « Le verre est à nous. Prends ce que tu veux dans la coque. Tu ne le garderas pas longtemps. »
        action flag:ver_regle;flag:ver_chasses;flag:monde_verriers_chasses → end
```

### 6.3 Rufina, la souffleuse
- **Portrait** : la trentaine, grande, cheveux noirs ras, tablier de cuir brûlé. Manches retroussées sur des **plaques sombres et lisses sur les avant-bras**, comme Lena. Elle vient de la même région, Novo Córdoba ; mais elle ne les cache plus, puisqu'ici elle n'en a pas besoin. Gants de cuir à la ceinture, canne de fer.
- **Caractère** : économe de mots, ironique, travaille en parlant. Arrivée il y a deux ans par la citerne de Remedios.
- **Sprite** : `gen_rc_rufina` (à produire) + portrait. Position (7,5 ; 18,8), devant l'établi, regard vers le four (11,5 ; 19).

```text
start   (Elle tire du four un fil de verre rouge sombre au bout d'une canne de fer, le tourne, le coupe. Une perle tombe dans une boîte.)
        « Si tu viens pour la vitrine, elle est sur l'établi. Si c'est pour moi, je travaille. »
  - « Qu'est-ce que tu vends ? »                                  → vente
  - [si !race_mutant & !ver_vu_bras] « Tes bras. »                 → bras
  - [si race_mutant & !ver_vu_bras] « Tes bras. Ça t'a prise jeune ? » → bras_mutant
  - [si ver_q_tison & !ver_tison] « Tecla dit que tu as un tison pour moi. » → tison
  - [si ver_indice_perles & !ver_perles_dites] « Les perles, sur la porte de l'écluse. » → perles
  - [si monde_lena_connue & !ver_lena_dite] « Tu connais Lena, de Novo Córdoba ? » → lena
  - [Attaquer]                                                    → rc_tecla:fuient
  - « Rien. »                                                     → end

vente   « De l'eau du condenseur, cinq. Des lames de verre noir, douze : ça coupe mieux que ton acier et ça casse plus vite, comme tout ce qui coupe bien. Je prends les rations : ici, rien ne pousse. »
  - [si !ver_eau1 & !ver_confiance] « Une eau. »                   action buy:water:5;flag:ver_eau1 → vente
  - [si !ver_eau1 & ver_confiance] « Une eau. » (prix d'ami)      action buy:water:3;flag:ver_eau1 → vente
  - [si ver_eau1 & !ver_eau2] « Une autre. »                       action buy:water:5;flag:ver_eau2 → vente
  - [si !ver_lame] « Une lame. »                                   action buy:poignard:12;flag:ver_lame → lame
  - [si inv:ration>=1 & !ver_ration_v] « Je te vends une ration. »  action sell:ration:5;flag:ver_ration_v → ration
  - « Rien. »                                                     → start
lame    « Enveloppe-la dans un chiffon. La première fois, elle coupe celui qui la porte. »   → vente
ration  « Cinq. Plus que la caravane, je sais. Ici, une ration, c'est une semaine de rosée. »   → vente

bras    « Des plaques, oui. Ça ne se lave pas et ça ne s'attrape pas, si c'est ta question. Chez nous, à Novo Córdoba, ça vient dans certaines familles, au bord du fleuve. Ailleurs, c'est autre chose : les os de Balta, la peau de Nilo, les yeux de Tecla. Le verre ne fait jamais deux fois la même chose. »
        action flag:ver_vu_bras → start
bras_mutant « À dix ans. Toi aussi, je le vois, mais je ne vois pas où. C'est bien : ça veut dire que tu as appris à le cacher. Ici, tu n'en as pas besoin. »
        action flag:ver_vu_bras → start
tison   (Elle sort du four un morceau de poutre qui brûle par un bout.) « Tiens-le par le manche, pas par le feu. Et ne le tends pas : avance avec. Une bête recule devant ce qui avance. »
        action flag:ver_tison → start
perles  « Une perle par passager. Quand quelqu'un arrive par la citerne de Remedios et repart vivant vers Dusk-Town, je fais une perle et je l'enfile sur la porte. Va compter, si tu veux. Moi, je ne compte plus. »
        action flag:ver_perles_dites → start
lena    (Elle pose la canne.) « La petite qui cherche son père ? À Novo Córdoba, tout le monde cherche un père ou un frère. Si elle monte vers Dusk-Town, elle passera par ici. Je lui garde une perle. »
        action flag:ver_lena_dite → start
```

### 6.4 Nilo, dans la cabane
- **Portrait** : quatorze ans, maigre, peau **marbrée** de taches brunes et ocre sur les mains, le cou et une joue, petits nodules au-dessus des sourcils. Chemise trop grande, pieds nus. Fier, bavard dès qu'il n'a plus peur.
- **Sprite** : `gen_rc_nilo` (à produire) + portrait. Invisible tant qu'il est dans la cabane : on lui parle **par la fenêtre sud** (point de dialogue en (26 ; 20,4) et déclencheur `pres_cabane`). Après sa sortie (`ver_nilo_libre`), il est debout en (25,5 ; 20,6), regard vers le four.

```text
start   (Entre les planches de la fenêtre, un œil, et une main marbrée de taches brunes.) « T'es du Service ? »
  - « Non. »                                                      → non
  - [si race_mutant] (Tu remontes ta manche, ou tu baisses ton col.) → mutant
  - « Et si je l'étais ? »                                        → si
non     « Le Service aussi, il dit toujours non. » (Un temps.) « Mais le Service ne viendrait pas jusqu'au verre pour trois cochons. »   → harde
mutant  (Il regarde.) « Ah. Comme Tecla, en moins vieux. »         action flag:ver_confiance → harde
si      « Alors t'aurais déjà tiré. »                              → harde
harde   (Un choc fait trembler toute la cabane, de l'autre côté.) « Le gris tape dans la porte. Toutes les dix minutes, je compte. J'ai toute l'eau ici, les jarres. Si je sors, ils entrent. Si je reste, ils cassent la porte. Moi, je passe par la fenêtre, mais l'eau, elle ne passe pas. »
  - « Tiens bon. »                                                → tiens
  - [si ver_q_leurre & !ver_jarre] « Passe-moi une jarre par la fenêtre. Je vais les attirer ailleurs. » → jarre
  - [si observation>=5|ver_indice_rosee] « Ils boivent où, d'habitude ? » → rosee
tiens   « Je tiens. Je tiens depuis l'aube. »                      action flag:ver_nilo_vu → end
jarre   « Une seule. Tecla va me tuer. » (Une petite jarre bouchée passe entre deux barreaux.)   action give:water;flag:ver_jarre;flag:ver_nilo_vu → end
rosee   « Sur les dalles, la nuit. Le verre fait de la rosée quand il refroidit, et ils la lèchent. Mais là, il fait chaud, et ils ont senti l'eau. »   action flag:ver_nilo_vu → harde

dehors  (entrée si ver_nilo_libre) « Ils sont partis ? Vraiment partis ? »
  - « Vraiment. »                                                 → blinde
  - « Tu as été courageux. »                                      → courage
courage « J'avais peur. Mais courageux et peur, Tecla dit que c'est pareil, vu de dehors. »   → blinde
blinde  [si !race_mutant] « Tu veux voir le verre ? Pas trop longtemps : toi, il te mange. Va voir le blindé, au nord. Il y a des gens du Service dedans, depuis longtemps. Personne n'est venu les chercher. C'est comme ça qu'on sait qu'ils ne viendront pas. »
        [si race_mutant] « Toi, le verre te mange moins. Va voir le blindé, au nord. Il y a des gens du Service dedans, depuis longtemps. Personne n'est venu les chercher. »
        action flag:ver_nilo_blinde → end
```

### 6.5 Les chanchos de ceniza (créatures, pas des gens)
- **Ce qu'ils sont** : des pécaris du verre. Bêtes trapues de 70 à 90 cm au garrot, cuir gris de cendre pelé par endroits, poils raides croûtés de poussière de verre qui accroche la lumière quand ils bougent. Défenses trop longues qui leur relèvent les babines, groin large, petits yeux. Le **gris** est presque blanc, une oreille fendue, une fois et demie la taille des jeunes.
- **Comportement** : ils ont soif et sentent l'eau des jarres ; le gris cogne la porte de la cabane, les jeunes fouillent la boue. Ce sont des **animaux**, sans outils, sans vêtements, sans voix : aucun signe d'humanité, rien qui puisse les faire prendre pour des mutants.
- **Sprites** : `gen_rc_chancho` (jeune) et `gen_rc_chancho_gris` (+ `_dos` chacun) ; pas de portrait. Hors combat, ils sont posés comme des PNJ figés, avec un examen (et non un dialogue) : jeunes en (24,5 ; 10,5), (26,5 ; 13,5), (33 ; 11,5) ; le gris en (29,5 ; 12) (mêmes cases qu'en combat, §8).

Examen de la harde (point en (25,5 ; 15,8), au seuil, et sur chaque bête) :

```text
harde   « Quatre bêtes grises dans la cuve de l'écluse. Des pécaris, ou ce qu'il en reste : le cuir pelé, croûté de poussière de verre qui brille quand ils bougent, des défenses trop longues qui leur relèvent les babines. Le plus gros, presque blanc, une oreille fendue, cogne la porte de la cabane du front, recule, et recommence. Ce ne sont pas des gens. Ce sont des bêtes, et elles ont soif. »
  - [si ver_tison & !ver_harde_partie] (Avancer le tison vers le gris.)   test volonte:5, partialAt 3 → pass tison_ok, partial tison_mal, fail tison_rate
  - [si !ver_harde_partie] [Attaquer]                             action combat:ecluse_verriers
  - (Reculer.)                                                    → end
tison_ok (Tu avances, sans t'arrêter. Le gris souffle, gratte le limon, puis tourne. Il s'en va par le bout de la cuve, les jeunes derrière lui, et la harde remonte dans le verre.)
        action flag:ver_harde_partie;flag:ver_harde_feu → end
tison_mal (Le gris charge, dévie au dernier moment et te laboure la cuisse au passage. Puis il file, et les jeunes avec lui.)
        action hurt:2;flag:ver_harde_partie;flag:ver_harde_feu → end
tison_rate (Ta main tremble, la flamme tremble avec. Le gris baisse la tête.)
        action combat:ecluse_verriers → end
```

### 6.6 Textes de déclencheurs et des points d'action
```text
T_verre  [si race_mutant] « Le verre est tiède sous les semelles, d'une tiédeur qui ne vient pas du soleil. Ta peau ne dit rien. Elle a l'habitude. »
         [si !race_mutant & inv:compteur>=1] « Le compteur se met à crépiter, de plus en plus vite. Tu sais ce que ça veut dire. Pas longtemps, ici. »   action hurt:1
         [sinon] « Le verre est tiède sous les semelles, d'une tiédeur qui ne vient pas du soleil. Au bout de quelques pas, un goût de métal dans la bouche. »   action hurt:1
         (une fois par scène : flag:ver_verre_dit)

rigole   (point (34,5 ; 8,2), si ver_q_leurre & !ver_harde_partie & inv:water>=1)
         test survie:4 → pass : « Tu verses l'eau en filet dans la rigole, tout au bout, sous le vent. Il ne se passe rien. Puis le gris lève le groin. Il quitte la porte, trotte vers l'est, lèche la pierre, et suit la rigole jusque dans le verre. Les jeunes suivent. »   action take:water;flag:ver_harde_partie;flag:ver_leurre
                         fail : « L'eau file dans le sable avant d'atteindre la rigole. Le gris lève la tête, te regarde, et ne bouge pas. »   action take:water   (on peut recommencer avec un autre bidon)
```

## 7. Manières d'agir et conséquences
| Approche | Comment | Conséquence |
|---|---|---|
| Passer | longer la piste jusqu'à S_E (Balta interpelle une fois) | reprise du voyage ; la harde reste ; journal : « vue » |
| Montrer son cou | réponse à Balta (§6.1) | mutant : confiance ; humain : neutre ; augmenté ou cyborg : méfiance (l'implant) |
| Commercer | Rufina : eau 5 $ (3 $ en confiance), lame de verre 12 $ (= `poignard`), rachat d'une ration 5 $ | échanges à stock limité |
| Soigner | Balta, Médecine 4 | confiance (prix d'ami) |
| S'informer | Tecla (le verre, les rafles, la filière si on connaît le secret de Remedios), Balta (Ines, la Sous-Ville), Rufina (les perles, Novo Córdoba), Nilo (la rosée, le blindé) | renseignements ; lien avec la caravane et Lena |
| Éloigner la harde par l'eau ◆ | Tecla → quai nord → rigole est, Survie 4, un bidon (ou la jarre de Nilo) | harde partie sans combat ; récompense de Tecla ; `monde_verriers_amis` |
| Éloigner la harde par le feu ◆ | Rufina donne le tison → examen de la harde → Volonté 5 (palier 3) | réussite : harde partie ; partiel : −2 PV et harde partie ; échec : combat |
| Attendre la nuit | Tecla → « J'attends avec vous » | +4 h au voyage à la sortie (`dureeSi`), +3 PV ; harde partie ; récompense ; la scène ne change pas de lumière (le texte raconte la nuit) |
| Combattre la harde | [Attaquer] sur la harde, ou échec du tison | voir §8 ; victoire = harde partie et récompense |
| Message pour Ines | Balta, si le joueur connaît Lena (`monde_lena_connue`) | une perle rouge ; `monde_message_ines` (accroche Sous-Ville) |
| Rançonner (issue tendue) | menacer de vendre l'emplacement au Service : Intimidation contre Volonté 7 | réussite : 14 $ + 3 perles, `monde_verriers_menaces` (ils partiront) ; échec : on te montre la piste, ou ils fuient |
| Voler | l'établi de Rufina : Discrétion 6 | lame + perles ; échec : « Repose. » (pas de combat ; méfiance) |
| Attaquer les Verriers | [Attaquer] chez Tecla, Balta ou Rufina | **pas de combat** : ils reculent dans le verre (`fuient`) ; la coque et l'établi sont libres ; `monde_verriers_chasses` |
| Partir | S_O à tout moment ; fuite pendant le combat | halte sur la case |

**Drapeaux de scène** (préfixe `ver_`, purgés à la sortie) : `ver_t1`, `ver_salue`, `ver_confiance`, `ver_mefiance`, `ver_q_harde`, `ver_q_leurre`, `ver_q_tison`, `ver_tison`, `ver_jarre`, `ver_conseil_gris`, `ver_soigne`, `ver_soin_dit`, `ver_ines`, `ver_message_ines`, `ver_indice_*`, `ver_eau_offerte`, `ver_citerne_dite`, `ver_filiere_dite`, `ver_perles_dites`, `ver_vu_bras`, `ver_lena_dite`, `ver_nilo_vu`, `ver_nilo_libre`, `ver_nilo_blinde`, `ver_harde_partie`, `ver_harde_feu`, `ver_harde_battue`, `ver_leurre`, `ver_attendu`, `ver_recule`, `ver_merci`, `ver_eau1-2`, `ver_lame`, `ver_ration_v`, `ver_racket`, `ver_menace`, `ver_vole`, `ver_regle`, `ver_chasses`, `ver_verre_dit`, `ver_f_*` (fouilles), `combat_ecluse_verriers_<issue>`.

**Drapeaux de monde** (**pas** de préfixe `ver_`, jamais purgés). Chacun est justifié par une suite prévue :
- `monde_verriers_vus` : drapeau d'arrivée ; rend la rencontre unique.
- `monde_verriers_amis` : la harde est partie grâce au joueur. Plus tard, Sol ou Remedios peuvent le reconnaître (« la vieille du four parle de toi »).
- `monde_verriers_menaces` : rançonnés. Les Verriers déménagent ; Dusk-Town peut le raconter.
- `monde_verriers_chasses` : attaqués, ils ont fui dans le verre. Même suite, en plus dur.
- `monde_message_ines` : le joueur porte le message de Balta. Accroche pour Lena, ou pour une quête de la Sous-Ville plus tard.

Rien ne lit ces drapeaux au jalon 2.

**Drapeau de monde à ajouter côté caravane** (proposition, §12.8) : `monde_lena_connue`, posé quand `car_vu_lena` l'est. Aujourd'hui, la connaissance de la filière (`car_vu_lena`, `car_lena_secret`) est purgée à la sortie de la caravane. Sans ce drapeau, les répliques « filière » et « Lena » de cette rencontre ne s'ouvrent jamais.

## 8. Combat optionnel (contre la harde seulement)
Système existant (`src/core/combat.js`, `src/data/combat.js`) avec les extensions du jalon 1 : positions **absolues**, `centre: { x: 24, z: 15 }` sans téléporter le joueur, `si` par ennemi, `rendSous`, `fuitTour`. Aucune hauteur : tout le monde est au sol.

| id | Sprite | Position absolue (x ; z) | Case | PV | PA | Init. | Arme | Mêlée / armes | Particularité |
|---|---|---|---|---|---|---|---|---|---|
| gris | gen_rc_chancho_gris | (29,5 ; 12), dans la boue | libre (limon) | 18 | 6 | 5 | `defenses` (§12.6) | 55 / 0 | `rendSous: 0.5` (ou `0.6` si `ver_conseil_gris`) : quand le gris détale, la harde le suit → **issue victoire** |
| jeune_a | gen_rc_chancho | (24,5 ; 10,5), près de la porte nord | libre (limon) | 8 | 7 | 7 | `defenses` | 40 / 0 | `fuitTour: 3` |
| jeune_b | gen_rc_chancho | (26,5 ; 13,5), devant le seuil | libre (limon) | 8 | 7 | 6 | `defenses` | 40 / 0 | `fuitTour: 3` |
| jeune_c | gen_rc_chancho | (33 ; 11,5), au bout de la cuve | libre (limon) | 8 | 7 | 6 | `defenses` | 35 / 0 | `fuitTour: 2` |

**Distances à l'entrée** (1,5 ; 24) : toutes ≥ 8 m.

| Bête | Distance |
|---|---|
| gris | 30,5 m |
| jeune_a | 26,7 m |
| jeune_b | 27,1 m |
| jeune_c | 33,9 m |

Les quatre positions sont distinctes : ouest, centre, sud et est de la cuve.

**Pas d'ennemi neutre** : Balta, Tecla, Rufina et Nilo ne sont **jamais** dans la liste. Ils restent à leur place, cachés en combat (`cacheCombat`), comme Lena. Les Verriers n'aident pas le joueur : le moteur n'a pas d'alliés, et Balta garde ses trois balles. Une ligne de récit le dit au début du combat.

**Couverture** :
- `couv: 1` : parapets, condenseurs, établi, fût, dalles, rochers ;
- `couv: 2` : portes d'écluse, cabane, four, péniche, blindé.

Contre des bêtes au contact, la couverture compte peu ; ce sont surtout des obstacles. Le joueur peut tirer depuis le quai nord ou le seuil, à travers le parapet.

**Issues** (format `issues` existant, **aucune mort**, ni d'homme ni de bête) :
- **victoire** (le gris détale sous 50 %, ou toute la harde a fui) : `flag:ver_harde_partie;flag:ver_harde_battue`. Texte : « Le gris s'arrête, souffle, et te tourne le dos. Il ne court pas : il s'en va. Les jeunes le suivent par le bout de la cuve, dans le verre. Balta abaisse son fusil. Il n'a pas tiré. »
- **fuite** : `rencontre:quitter` ; halte sur la case. Texte : « Tu enjambes le parapet et tu cours. Le gris ne te suit pas : ce n'est pas toi qu'il veut, c'est l'eau. »
- **reddition** (du joueur) : `flag:ver_recule`, la scène reprend (la harde reste ; on peut choisir une autre façon). Texte : « Tu recules, mains vides, jusqu'au parapet. Le gris te laisse partir. Derrière toi, la porte de la cabane craque encore. »
- **defaite** : `flag:ver_recule;give:water;warp:rc_ecluse_verriers:11.5:20.5` + 1 PV (règle existante). Texte : « Tu te réveilles contre le four. Tecla te tient la tête. "Le gris t'a fait voler. Bois." »

Ligne de début (`textes.debut`) : « Le gris lève la tête de la porte. Derrière toi, Balta crie : "Le gris ! Tape le gris !" Il ne tire pas. »

## 9. Objets à fouiller (butin et récompenses)
Objets existants (`water`, `ration`, `poignard`, `compteur`) sauf mention ; un seul objet nouveau, `perles_verre`.

| Où | Condition | Contenu |
|---|---|---|
| Récompense de Tecla | `ver_harde_partie`, en parlant à Tecla (nœud `merci`) | 2 `water` + 3 `perles_verre` ; `monde_verriers_amis` |
| Eau offerte | joueur mutant, nœud `mutant_eau`, ou origine errant (`errant_ok`) | 1 `water` |
| Jarre de Nilo | `ver_q_leurre`, par la fenêtre | 1 `water` (pour le leurre, mais on peut la garder) |
| Établi de Rufina (7,5 ; 18,6) | avant tout règlement : test Discrétion 6, échec = « Rufina pose la canne : "Repose." » + `ver_mefiance` (pas de combat) ; après `ver_chasses` : libre | 1 `poignard` (lame de verre) + 2 `perles_verre` ; vol réussi : `flag:ver_vole` |
| Coque de la péniche (7,5 ; 14,2) | `ver_chasses` | 3 `water`, 2 `ration`, 9 $ |
| Citerne sous la proue (2,5 ; 12) | `ver_citerne_dite` (origine errant) ou `ver_chasses` | errant : rien de plus (Tecla a déjà donné) ; après `ver_chasses` : 2 `water` |
| ◆ Blindé vitrifié (27,5 ; 4,5) | `ver_nilo_blinde` ou Observation 5 ; mutant : libre ; non-mutant : Volonté 4 pour fouiller vite (échec : `hurt:1` et on ressort) | 2 `ration` (rations militaires scellées « qui se mangent encore ») + 10 $ (vieux billets du Service, « qui passent encore à Dusk-Town ») ; non-mutant : `hurt:1` de toute façon |
| Rançon | `menace_ok` | 14 $ + 3 `perles_verre` |

**Nouvel objet** : `perles_verre` (« Perles de verre », objet d'échange). Pas de prix de vente au jalon 2 : il ne se vend pas, il se montre. C'est une accroche, pas une monnaie.

## 10. Clés d'assets : réutilisations et clés nouvelles à produire
**Produit et publié depuis** (lots `08e8356` et `200bc62`, voir §15). Même pipeline que le pilote et la caravane : Mega-Line, caméra du jeu, 50 px/m. Même manifeste `assets/rencontres/manifest.json`, mêmes champs.

Préfixes :
- `rc_vr_` pour les modules du **verre**, réutilisables par les autres rencontres de ce biome ;
- `rc_ecl_` pour les éléments propres à l'écluse ;
- `g_rc_` pour les sols.

**Le soleil** : même direction que le pilote (les modules réutilisés sont peints sous cette lumière). Seule la couleur change, et c'est l'ambiance de la scène qui la règle (§11).

**Réutilisé tel quel** (déjà publié, aucune clé modifiée) :
| Clé | Où | Note |
|---|---|---|
| `g_rc_piste` (+ `_b`, `_c`) | bande z 21-27 | la piste Dusk-Town → Big Larry |
| `rc_ds_panneau_ufsa_3q` | (1,2 ; 16,4) | « CANAL … ÉCLUSE 7 » est un texte d'examen, pas un décalque |
| `rc_ds_rochers_3q`, `rc_ds_rochers_b_3q` | bas-côté sud (29 ; 27,9) et (8 ; 27,8) | hors zone de combat |
| `assets/reused/barrel.webp` | (20,7 ; 17) | fût près des condenseurs |

**Clés nouvelles à produire** : 4 sols, 13 décors et décalques (4 modules `rc_vr_`, 9 `rc_ecl_`), 4 PNJ + portraits, 2 créatures.

| Clé | Rôle | Emprise L × P × H (m) | Notes |
|---|---|---|---|
| `g_rc_verre` (+ `_b`, `_c`) | plaine de verre : dalles brun-noir et vert bouteille sale, fentes, croûtes de sel, lichen orange | tuile 4 m | **sans** reflet spéculaire peint (les reflets viendraient d'une lumière qui n'est pas là) ; mat, avec des arêtes plus claires |
| `g_rc_quai` | béton du quai, fendu, joints ensablés | tuile 4 m | gris chaud, jamais bleuté |
| `g_rc_limon` (+ `_b`) | limon craquelé du canal ensablé, plus sombre que le sable | tuile 4 m | lit le creux du canal |
| `g_rc_cendre` (+ `_b`) | sable cendré du camp et des bas-côtés, gris-ocre | tuile 4 m | raccord avec `g_rc_piste` |
| `rc_vr_dalles_3q` (+ `_b`) | dalles de verre soulevées en éventail | 2 × 2 × 1,2 (`_b` 2 × 2 × 0,9) | module verre ; arêtes vives, pas de transparence (le verre est opaque, brun) |
| `rc_vr_blinde_vitrifie_3q` (+ `_texte`) | blindé du Service enfoncé dans le verre jusqu'aux essieux, peinture cloquée, écoutille ouverte | 5 × 3 × 2,4 | module verre ; cercle et inscription à la craie en calque `_texte` (calque normal, `etage: 1`, comme le tracteur) |
| `rc_vr_parapet_3q` (+ `_b`) | parapet de canal, béton et pierre de taille, 0,7 m, épaisseur côté canal peinte plus haute (lecture du creux) | 6 × 0,5 × 0,7 (`_b` 3 m) | module verre et canal ; poses bout à bout, joints cachés sous les passages |
| `rc_vr_escalier_quai_3q` | marches descendant du quai vers le limon (peintes en creux) | 3 × 0,5 × 0,7 | occupe le passage nord du parapet (x 12-15) |
| `rc_ecl_peniche_3q` | péniche retournée, quille en l'air, ensablée, porte découpée au sud avec rideau de toile | 11 × 4,5 × 3 | la plus grande silhouette basse ; la quille rouillée se lit comme un toit |
| `rc_ecl_porte_nord_3q` | porte d'écluse fermée, bajoyer de pierre, passerelle de fer, fil de perles autour du montant | 1,5 × 3 × 3,4 | **la silhouette de la scène** ; les perles doivent se lire comme des points rouges et verts, petits |
| `rc_ecl_porte_sud_3q` | porte d'écluse ouverte, rabattue | 3 × 1 × 3,4 | |
| `rc_ecl_four_3q` (+ `_neon`) | four à verre de terre et briques, cheminée, gueule au sud ; canne de fer, moules | 3 × 2,7 × 3,4 | `_neon` serré sur la gueule seule, orange (255,150,60) ; **source visible** |
| `rc_ecl_four_flaque` | flaque de lumière chaude au sol devant la gueule (décalque additif, nuit seulement) | 3 × 2 | à poser comme la retouche du bivouac (§12.9) ; jamais le jour |
| `rc_ecl_condenseur_3q` | cadre de bois, toile goudronnée en pente, jarres dessous (une renversée) | 1,5 × 2 × 1,8 | trois poses, une en miroir |
| `rc_ecl_etabli_3q` | établi de Rufina : plaque de tôle, perles, lames de verre noir, pinces | 3 × 0,8 × 0,9 | perles et lames en points lisibles |
| `rc_ecl_cabane_3q` | cabane de la pompe : briques, tôle, porte de planches enfoncée au nord, fenêtre à barreaux et planches au sud | 4 × 3,8 × 3 | la porte (côté cuve) et la fenêtre (côté piste) doivent se lire depuis la caméra |
| `rc_ecl_cuve_3q` | décalque : boue rouillée, tessons de jarres, piétinement de sabots | 9 × 4 | couche sol (`fond: true`) |
| `gen_rc_tecla` (+ `_dos`) | PNJ **assise** + portrait | 1,10 m assise | couverture, talisman de verre, excroissances aux tempes, yeux laiteux |
| `gen_rc_balta` (+ `_dos`) | PNJ + portrait | 1,82 m | crête osseuse nuque et épaule, fusil à un coup, foulard rouille, bandage au mollet |
| `gen_rc_rufina` (+ `_dos`) | PNJ + portrait | 1,74 m | tablier de cuir, manches retroussées, plaques sombres et lisses sur les avant-bras, canne de fer |
| `gen_rc_nilo` (+ `_dos`) | PNJ + portrait | 1,50 m | peau marbrée brun et ocre, chemise trop grande, pieds nus |
| `gen_rc_chancho` (+ `_dos`) | créature (jeune) | 0,75 m au garrot, ≈ 1,1 m de long | quadrupède : pivot au centre des pattes, pas de portrait |
| `gen_rc_chancho_gris` (+ `_dos`) | créature (vieux mâle) | 0,95 m au garrot, ≈ 1,5 m de long | presque blanc, oreille fendue, défenses longues |

**Nouvel objet** : `perles_verre` (« Perles de verre », icône 64/128 à produire).

**Nouvelle arme** proposée : `defenses` (§12.6).

## 11. Identité du biome (verre vitrifié et canal mort)
- **Biome** : la plaine de verre au bord de la zone d'impact de Big Larry, le long de la piste qui monte de Dusk-Town au cratère. Sable fondu en dalles, puis un canal de l'UFSA mort et ensablé, puis la piste et le sable cendré. Rien ne pousse : un lichen orange dans les fentes, c'est tout. C'est le premier biome **froid de couleur** du chantier, sans être bleu.
- **Palette** :
  - **Verre** : brun-noir `#2e2620`, vert bouteille sale `#46502e`, arêtes plus claires `#8a8a66`.
  - **Sel** : croûtes blanc cassé `#d8d2c0`.
  - **Rouille** (portes, péniche, blindé) : `#7e4426`.
  - **Béton et pierre** du canal : gris chaud `#8a8276`.
  - **Limon** : brun gris `#5e5446`. **Sable cendré** : gris-ocre `#a49a82`.
  - **Accents** : jaune soufre `#c8b048` (fil, toiles, lichens), orange du four `#ff9a48` (seule source), rouge sombre et vert des perles.
  - **Ciel du jour** : blanc-jaune délavé.
  - **Interdits** : aucun cyan, aucun violet, pas de vert « radioactif » ; la nuit reste bleu-gris comme le désert, sans teinte propre.
- **Lumière** : même direction de soleil que le pilote. **Courbe `glass` proposée** pour `src/data/ambiances.js`, même structure et mêmes heures que `desert` :
  - **Jour** : plus blanc et plus dur que l'ambre du désert, le verre écrase les couleurs.
  - **Nuit** : un peu plus sombre au sol, car le verre boit la lumière.

  ```js
  const NUIT_VERRE = { bg: '#0a0c12', hemi: ['#5a6684', '#121216', 0.55], sun: ['#8090c0', 0.3], tint: '#586282', actor: '#8a92ae', voile: 'rgba(6,8,14,.64)', lune: 1 };
  const AUBE_VERRE = { bg: '#261c16', hemi: ['#ecc09a', '#30261c', 1.0], sun: ['#ffa864', 0.9], tint: '#e4c8a8', actor: '#eed8c0', voile: 'rgba(18,12,8,.32)', lune: 0.25 };
  const JOUR_VERRE = { bg: '#2c2a22', hemi: ['#f6efd8', '#4a4434', 1.45], sun: ['#fff0c8', 1.55], tint: '#efe9da', actor: '#fbf8f0', voile: 'rgba(14,12,8,.20)', lune: 0 };
  glass: [[0, NUIT_VERRE], [5, NUIT_VERRE], [7, AUBE_VERRE], [8.5, JOUR_VERRE], [17.5, JOUR_VERRE], [19, AUBE_VERRE], [21, NUIT_VERRE], [24, NUIT_VERRE]],
  ```

  Scène `ambiance: 'glass'`. Repli si la courbe n'est pas ajoutée : `ambiance: 'desert'` ; c'est juste, en moins blanc.
- **Liseré de lune** : celui de Rivet, 1 px `#c8d2dc` côté lune. **Je tranche la question de Régie** pour toutes les scènes : opacité **50 %**, et **pas de liseré sur les pieds**. Il s'arrête au-dessus des chevilles, pour ne pas dessiner une ligne claire au contact du sol. Cela vaut pour le pilote, la caravane et cette scène.
- **Sol** : jamais uni. Fentes et sel sur le verre ; joints ensablés sur le quai ; craquelures et boue dans le canal ; traces de sabots autour des condenseurs.
- **À éviter** :
  - le verre qui luit ou qui scintille comme des bijoux ;
  - un halo autour du four ;
  - la brume verte « toxique » ;
  - des mutants difformes « de film d'horreur » (les mutations sont lisibles mais sobres, comme Lena) ;
  - des chanchos qui se tiennent debout, ou portent quoi que ce soit ;
  - les quatre Verriers alignés devant le four.

## 12. Points d'accroche pour Rivet
1. **Catalogue** `src/data/rencontres.js` : entrée `ecluse_verriers` du §14 (fichier `rencontres_verriers.js`, comme la caravane).
   - `prefixe: 'ver_'`, `terrains: ['verre', 'piste']`, `biomes: ['glass']` : avec `['verre']` seul, la rencontre ne tomberait jamais sur I04, I03 ni K03, qui ont le terrain `piste`.
   - `si: etat => !etat.flags.monde_verriers_vus`, `drapeauArrivee: 'monde_verriers_vus'`.
   - Taux de `TERRAINS` inchangés.
   - Tirage sur n'importe quelle case de verre (I04, I03, J04 par exemple) ; vérifié sur la grille : 7 cases `glass` en terrain `verre`, 3 en terrain `piste`, J03 exclue (lieu).
2. **Scène sans `niveaux`.**
   - Canal ensablé au niveau 0, creux rendu par `g_rc_limon` et l'épaisseur peinte des parapets (même principe que le lit du pilote, ARCHI §6.1).
   - Parapets en solides `couv: 1` avec trois passages.
   - Sorties : S_O = halte, S_E = reprise, **jamais gardée**.
3. **Visibilité et entrées.**
   - **Balta** : `entrees: [{ si: 'ver_harde_partie', node: 'apres' }, { si: 'ver_salue', node: 'encore' }]`.
   - **Nilo** : par la fenêtre (PNJ invisible type « voix de la citerne », `si: 'ver_jamais'`, ouvert par le point (26 ; 20,4) et `pres_cabane`) tant que `!ver_nilo_libre`. Puis debout, `entrees: [{ si: 'ver_nilo_libre', node: 'dehors' }]`.
   - **Tous les Verriers** : `si: '!ver_chasses'`, `cacheCombat: true`, `bloque: false`.
   - **Chanchos** : PNJ figés `si: '!ver_harde_partie'` avec un examen ou dialogue `rc_harde`, `cacheCombat: true` (le combat les remplace par ses unités).
4. **Nœud commun `fuient`** (rc_tecla), appelé depuis Balta et Rufina. Il ne lance **aucun** combat.
5. **Déclencheur `T_verre`** : zone z 0-7, une fois (`!ver_verre_dit`) ; trois variantes par `alt` (mutant, compteur, autre).
6. **Arme `defenses`** dans `ARMES` : `{ nom: 'Défenses', type: 'melee', pa: 3, portee: 1, degats: [2, 5] }` [proposition]. Repli : `barre` (4-6, un peu fort pour les jeunes ; baisser alors leurs PV à 6).
7. **Combat `ENCOUNTERS.ecluse_verriers`.**
   - Centre (24 ; 15).
   - Le gris `rendSous: 0.5`, ou `0.6` si `ver_conseil_gris` : deux entrées à `si` exclusifs, comme Morsa.
   - Jeunes : `fuitTour` 3, 3 et 2.
   - **Texte de reddition par ennemi**, si c'est facile (`textes.rend: { gris: 'Le gris détale.' }`), sinon « lève les mains » serait faux pour une bête. Repli : le gris en `fuitTour: 4` sans `rendSous`, et la victoire tombe quand tous ont fui.
   - Issues du §8. Reddition et défaite **ne quittent pas** la scène (`ver_recule`), la harde reste.
8. **Drapeau `monde_lena_connue`** à poser dans la caravane (`rencontres_caravane.js`) avec `car_vu_lena` : une ligne. C'est lui qui ouvre les répliques « filière » et « Lena » ici.
9. **Lumières.**
   - `enseignes: [{ id: 'ver_feu', building: 'ver_four', effet: 'pulse', periode: 7, intensite: 0.7 }]` sur `rc_ecl_four_3q_neon`.
   - La flaque `rc_ecl_four_flaque` (nuit seulement : opacité = 1 − luminance du jour, ou `lune`) : **même mécanisme que la retouche du bivouac**, à faire une fois pour les deux.
10. **Ambiance** `glass` (§11) dans `ambiances.js`, scène `ambiance: 'glass'`.
11. **Durée** : `duree: 1`, `dureeSi: { ver_attendu: 4 }`. L'attente ne change pas la lumière dans la scène : le texte raconte la nuit, et l'heure avance à la sortie.
12. **Prix** : eau 5 $ (3 $ si `ver_confiance`), lame 12 $ (`buy:poignard:12`), rachat de ration 5 $ (une fois).
13. **Nouvel objet** `perles_verre` dans `ITEMS_RENCONTRES` (sans prix de vente).
14. **Tests DEV** : forcer `ecluse_verriers`. Scénarios :
    - passer ;
    - montrer le cou (4 races) ;
    - les trois solutions pacifiques (eau, tison réussi, partiel, raté → combat ; attente) ;
    - combat (4 issues, dont reddition et défaite qui restent dans la scène) ;
    - soigner ;
    - message pour Ines (avec `monde_lena_connue` forcé) ;
    - filière (avec `monde_lena_connue`) ;
    - rançonner (réussi, raté) ;
    - voler ;
    - attaquer → fuite des Verriers puis fouilles ;
    - fuir ;
    - verre traversé par un mutant, un humain, un porteur de compteur.

## 13. Décisions de DA et de lore à signaler à Valentin
Rien n'est imposé ; tout est [proposition]. Les points 1 à 4 sont des **modifications de lore importantes**, à valider ou à refuser une par une.

**Modifications importantes**
1. **Le verre comme refuge des mutants.** La plaine vitrifiée de Big Larry est trop irradiée pour les « gens de bonne peau », supportable pour les mutants (`radResist`). Le Service n'y entre pas, et un blindé abandonné le prouve. C'est cohérent avec la fiche de race (« résiste aux radiations ») et avec la planche « Population — Mutants » (« leur adaptation est une force dans les terres contaminées »), mais cela fait du verre un **territoire mutant**, ce qui est nouveau.
2. **Les Verriers**, communauté de mutants sans faction, chassés de Dusk-Town par les rafles, qui servent d'**étape à la filière** de Remedios (CARAVANE §13.1) : les passagers attendent ici avant d'entrer à Dusk-Town « par en dessous », avec l'aide de Sol. **Cela étend le réseau** proposé dans CARAVANE. Si tu refuses la filière, les Verriers restent une simple communauté : il suffit de couper les répliques `filiere`, `perles` et la porte aux perles.
3. **Ines**, la femme de Balta, prise dans une rafle et jetée dans la Sous-Ville. C'est un deuxième nom dans la Sous-Ville après le père de Lena, avec un drapeau de monde `monde_message_ines` : une accroche, pas une quête.
4. **Première faune hostile du jeu** : les **chanchos de ceniza**, pécaris du verre. Le repo n'en prévoyait aucune ; la consigne du jalon dit « créatures mutantes ». Ce sont **des bêtes**, clairement distinctes des mutants humains (aucune posture, aucun objet, aucune voix). Ils ne sont pas « méchants » : ils ont soif. Le combat n'est qu'une des quatre façons de régler la scène, et personne ne meurt.

**Points de cohérence avec le canon et avec la caravane**

5. **Les « Féraux » de la planche de référence** (« mutant contaminé avancé », qui a perdu la raison) : **je ne les utilise pas**. Des humains mutés hostiles seraient exactement le cliché à éviter. Je propose de les réserver à un traitement à part, rare, et toujours comme des gens malades, jamais comme une horde.
6. **Les mutations sont diverses**, conformément à la planche de référence (excroissances osseuses, peau marbrée, yeux laiteux, excroissances calcifiées). Les **plaques sombres sur les avant-bras** (Lena, Rufina) sont présentées comme **une** forme parmi d'autres, « dans certaines familles au bord du fleuve, à Novo Córdoba ». C'est cohérent avec CARAVANE, sans en faire la marque de tous les mutants. **Correction** à CARAVANE §13.4, qui dit « le roman ne décrit pas les mutations » : la planche « Population — Mutants » du dossier de référence en décrit plusieurs ; ce document s'y conforme.
7. **Le geste du col retourné** : à Dusk-Town, les soldats font baisser les cols pour trouver les mutants (dialogues existants) ; ici, c'est Balta qui demande à voir le cou, pour s'assurer qu'on n'est **pas** du Service. Il se méfie d'un implant d'IO, qui « parle à qui l'écoute ».
8. **Big Larry** : le texte dit seulement « un feu dans le ciel, il y a très longtemps, le sable a fondu ». C'est cohérent avec le cratère d'impact du canon, sans date ni cause.
9. **Population** : la planche dit que les mutants sont la population majoritaire du No Man's Land ; les docs du jeu les montrent cachés à Dusk-Town. Les Verriers tiennent les deux : nombreux dehors, cachés près des villes. À trancher un jour pour le reste du jeu.

**Lieux, noms et objets**

10. **Canal UFSA et Écluse 7** : un réseau de canaux de l'UFSA, mort et ensablé (lore d'ambiance, comme le relais routier). Réutilisable pour d'autres rencontres « canal ».
11. **Nouveaux noms** : Tecla, Balta, Rufina, Nilo, Ines ; « les Verriers » ; « chanchos de ceniza ». Même saveur hispanophone que la caravane.
12. **Perles de verre** : une perle par passager sauvé, enfilée sur la porte de l'écluse (cousine des petits cercles du relais, CARAVANE §3). Les perles données au joueur sont une **reconnaissance** sur la piste de Novo Córdoba, sans valeur marchande au jalon 2.
13. **L'objet `plaque` de l'origine « Rescapé d'une rafle »** est une plaque de camion du Service, pas une plaque de peau. Tecla en parle comme d'un trophée. Si les plaques de peau sont validées, il faudra peut-être renommer l'objet pour éviter la confusion.

**DA**

14. **Biome de verre** :
    - palette brun-noir, vert bouteille sale, sel, rouille, soufre ;
    - jour plus blanc que le désert (courbe `glass`), nuit bleu-gris commune ;
    - le verre ne luit jamais ;
    - une seule lumière : la gueule du four, avec sa flaque chaude la nuit.
15. **Liseré de lune** : je tranche la question de Régie à 50 % d'opacité, sans liseré sur les pieds, pour toutes les scènes.
16. **Joueur mutant** (drapeaux `race_mutant` et origines existants) :
    - Balta le reconnaît sans examen ; Tecla lui offre l'eau et une place ;
    - chaque origine a sa réplique : Sol pour « Né dans les Sables », la plaque arrachée pour la rafle, l'eau sentie pour l'errant ;
    - Rufina devine qu'il cache une mutation ; Nilo se rassure ;
    - le verre ne le blesse pas ; le blindé est libre pour lui.

## 14. Entrée au format d'ARCHI.md §4
Poses définitives après production des sprites (même principe que le §15 de la caravane) ; positions en mètres, ancre des décors au coin sud-est de l'emprise ; format réel de `rencontres_caravane.js` (`D`, `R`, `points`, `entrees`, `enseignes`).

```js
export const VERRIERS = {
  nom: 'L\u2019écluse des Verriers', famille: 'creatures', terrains: ['verre', 'piste'], biomes: ['glass'], poids: 1, lieu: 'rc_ecluse_verriers', prefixe: 'ver_',
  duree: 1, dureeSi: { ver_attendu: 4 },                                       // attendre la nuit avec eux (§6.2)
  si: etat => !etat.flags.monde_verriers_vus, drapeauArrivee: 'monde_verriers_vus',
  arrivee: 'Un canal mort au bord du verre. Une écluse noire, un four qui rougeoie. Dans la cuve, des bêtes grises.',
  arriveeRetour: 'L\u2019écluse, au bord du verre.',
  scene: { size: { w: 36, d: 30 }, city: 'nml', ambiance: 'glass',          // repli 'desert' (§11)
    ground: { base: '#8a8270', skin: 'g_rc_cendre', tileM: 4, clean: true, marge: { skin: 'g_rc_verre', tileM: 4, m: 30, voile: 'rgba(14,12,8,.20)' },
      paint: [ { x: 0, z: 0, w: 36, d: 7, skin: 'g_rc_verre', tileM: 4 }, { x: 12, z: 0, w: 4, d: 4, skin: 'g_rc_verre_b', tileM: 4 }, { x: 28, z: 4, w: 4, d: 3, skin: 'g_rc_verre_c', tileM: 4 },
        { x: 0, z: 7, w: 36, d: 2, skin: 'g_rc_quai', tileM: 4 },
        { x: 0, z: 9, w: 36, d: 6, skin: 'g_rc_limon', tileM: 4 }, { x: 16, z: 9, w: 4, d: 4, skin: 'g_rc_limon_b', tileM: 4 },
        { x: 0, z: 21, w: 36, d: 6, skin: 'g_rc_piste', tileM: 4 }, { x: 8, z: 21, w: 4, d: 4, skin: 'g_rc_piste_b', tileM: 4 }, { x: 26, z: 23, w: 4, d: 4, skin: 'g_rc_piste_c', tileM: 4 },
        { x: 20, z: 27, w: 4, d: 3, skin: 'g_rc_cendre_b', tileM: 4 } ] },
    cadre: { desktop: { x: [12, 28], z: [12, 20] }, mobile: { x: [6, 28], z: [16, 22] } },
    buildings: [
      D('ver_cuve', 'rc_ecl_cuve_3q', 22, 10, 9, 4, { fond: true, ph: { h: 0.05 } }),
      D('ver_dalles', 'rc_vr_dalles_3q', 5, 2, 2, 2, { ph: { h: 1.2 }, solid: [R(5, 2, 2, 2, 1)] }),
      D('ver_dalles_b', 'rc_vr_dalles_b_3q', 14, 3, 2, 2, { ph: { h: 0.9 }, solid: [R(14, 3, 2, 2, 1)] }),
      D('ver_blinde', 'rc_vr_blinde_vitrifie_3q', 26, 1, 5, 3, { ph: { h: 2.4 }, solid: [R(26, 1, 5, 3, 2)] }),
      D('ver_blinde_texte', 'rc_vr_blinde_vitrifie_3q_texte', 26, 1, 5, 3, { etage: 1 }),
      // parapet nord (passage x 12-15 : escalier)
      D('ver_par_n1', 'rc_vr_parapet_3q', 0, 8.5, 6, 0.5, { solid: [R(0, 8.5, 6, 0.5, 1)] }), D('ver_par_n2', 'rc_vr_parapet_3q', 6, 8.5, 6, 0.5, { solid: [R(6, 8.5, 6, 0.5, 1)] }),
      D('ver_escalier', 'rc_vr_escalier_quai_3q', 12, 8.5, 3, 0.5, {}),
      D('ver_par_n3', 'rc_vr_parapet_3q', 15, 8.5, 6, 0.5, { solid: [R(15, 8.5, 6, 0.5, 1)] }), D('ver_par_n4', 'rc_vr_parapet_3q', 21, 8.5, 6, 0.5, { solid: [R(21, 8.5, 6, 0.5, 1)] }),
      D('ver_par_n5', 'rc_vr_parapet_3q', 27, 8.5, 6, 0.5, { solid: [R(27, 8.5, 6, 0.5, 1)] }), D('ver_par_n6', 'rc_vr_parapet_b_3q', 33, 8.5, 3, 0.5, { solid: [R(33, 8.5, 3, 0.5, 1)] }),
      D('ver_peniche', 'rc_ecl_peniche_3q', 2, 9.5, 11, 4.5, { ph: { h: 3 }, solid: [R(2, 9.5, 11, 4.5, 2)] }),
      D('ver_porte_n', 'rc_ecl_porte_nord_3q', 19, 9, 1.5, 3, { ph: { h: 3.4 }, solid: [R(19, 9, 1.5, 3, 2)] }),
      D('ver_porte_s', 'rc_ecl_porte_sud_3q', 20.5, 14, 3, 1, { ph: { h: 3.4 }, solid: [R(20.5, 14, 3, 1, 2)] }),
      // parapet sud (passages x 3-6 : cale ; x 24-27 : seuil de la cabane)
      D('ver_par_s1', 'rc_vr_parapet_b_3q', 0, 15, 3, 0.5, { solid: [R(0, 15, 3, 0.5, 1)] }),
      D('ver_par_s2', 'rc_vr_parapet_3q', 6, 15, 6, 0.5, { solid: [R(6, 15, 6, 0.5, 1)] }), D('ver_par_s3', 'rc_vr_parapet_3q', 12, 15, 6, 0.5, { solid: [R(12, 15, 6, 0.5, 1)] }),
      D('ver_par_s4', 'rc_vr_parapet_3q', 18, 15, 6, 0.5, { solid: [R(18, 15, 6, 0.5, 1)] }),
      D('ver_par_s5', 'rc_vr_parapet_3q', 27, 15, 6, 0.5, { solid: [R(27, 15, 6, 0.5, 1)] }), D('ver_par_s6', 'rc_vr_parapet_b_3q', 33, 15, 3, 0.5, { solid: [R(33, 15, 3, 0.5, 1)] }),
      D('ver_etabli', 'rc_ecl_etabli_3q', 6, 17.2, 3, 0.8, { ph: { h: 0.9 }, solid: [R(6, 17.2, 3, 0.8, 1)] }),
      D('ver_four', 'rc_ecl_four_3q', 10, 16.3, 3, 2.7, { ph: { h: 2.2 }, solid: [R(10, 16.3, 3, 2.7, 2)] }),       // en buildings pour son _neon
      D('ver_four_flaque', 'rc_ecl_four_flaque', 10, 19, 3, 2, { fond: true, nuit: true }),                          // §12.9 : nuit seulement
      D('ver_cond1', 'rc_ecl_condenseur_3q', 14, 16.3, 1.5, 2, { ph: { h: 1.8 }, solid: [R(14, 16.3, 1.5, 2, 1)] }),
      D('ver_cond2', 'rc_ecl_condenseur_3q', 16, 16.3, 1.5, 2, { ph: { h: 1.8 }, solid: [R(16, 16.3, 1.5, 2, 1)], miroir: true }),
      D('ver_cond3', 'rc_ecl_condenseur_3q', 18, 16.3, 1.5, 2, { ph: { h: 1.8 }, solid: [R(18, 16.3, 1.5, 2, 1)] }),
      D('ver_cabane', 'rc_ecl_cabane_3q', 24, 16.2, 4, 3.8, { ph: { h: 3 }, solid: [R(24, 16.2, 4, 3.8, 2)] }),
      D('ver_panneau', 'rc_ds_panneau_ufsa_3q', 1.2, 16.4, 0.6, 0.2, { solid: [R(1.4, 16.4, 0.2, 0.2, 0)] }),
      D('ver_rochers_b', 'rc_ds_rochers_b_3q', 8, 27.8, 3, 1.5, { solid: [R(8, 27.8, 3, 1.5, 1)] }),
      D('ver_rochers', 'rc_ds_rochers_3q', 29, 27.9, 3, 1.5, { solid: [R(29, 27.9, 3, 1.5, 1)] }),
    ],
    enseignes: [{ id: 'ver_feu', building: 'ver_four', effet: 'pulse', periode: 7, intensite: 0.7 }],   // gueule du four : seule lumière
    props: [{ sprite: 'barrel', x: 20.7, z: 17, fp: [0.6, 0.6] }],
    entree: { x: 1.5, z: 24, heading: Math.PI / 2 },
    sorties: [
      { id: 'ouest', label: 'Demi-tour (carte)', x: 0.6, z: 24, zone: { x0: 0, x1: 0.9, z0: 21, z1: 27 }, effet: 'halte' },
      { id: 'est', label: 'Reprendre la piste', x: 35.4, z: 24, zone: { x0: 35.1, x1: 36, z0: 21, z1: 27 }, effet: 'reprise' } ] },   // jamais gardée
  declencheurs: [
    { id: 'T1', zone: { x: 4, z: 15.5, w: 2, d: 11.5 }, si: '!ver_t1&!ver_salue&!ver_regle', enter: 'flag:ver_t1', dialogue: 'rc_balta' },
    { id: 'T_verre', zone: { x: 0, z: 0, w: 36, d: 7 }, si: '!ver_verre_dit', enter: 'flag:ver_verre_dit', texte: 'rc_verre' },      // §6.6 : alt mutant / compteur / autre
    { id: 'pres_cabane', zone: { x: 24, z: 20, w: 4, d: 1 }, si: '!ver_nilo_libre&!ver_chasses', dialogue: 'rc_nilo' } ],
  pnj: [
    { id: 'rc_balta', name: 'Balta', sprite: 'gen_rc_balta', x: 5.5, z: 20.4, faceTo: [1.5, 24], dialogue: 'rc_balta',
      entrees: [{ si: 'ver_harde_partie', node: 'apres' }, { si: 'ver_salue', node: 'encore' }], si: '!ver_chasses', cacheCombat: true, bloque: false },
    { id: 'rc_tecla', name: 'Tecla', sprite: 'gen_rc_tecla', x: 13.2, z: 19.6, faceTo: [1.5, 24], fige: true, dialogue: 'rc_tecla', si: '!ver_chasses', cacheCombat: true, bloque: false },
    { id: 'rc_rufina', name: 'Rufina', sprite: 'gen_rc_rufina', x: 7.5, z: 18.8, faceTo: [11.5, 19], dialogue: 'rc_rufina', si: '!ver_chasses', cacheCombat: true, bloque: false },
    { id: 'rc_nilo_voix', name: 'Nilo', sprite: 'gen_rc_nilo', x: 26, z: 19.8, dialogue: 'rc_nilo', si: 'ver_jamais', fige: true, bloque: false },   // voix par la fenêtre : jamais visible
    { id: 'rc_nilo', name: 'Nilo', sprite: 'gen_rc_nilo', x: 25.5, z: 20.6, faceTo: [11.5, 19], dialogue: 'rc_nilo', entrees: [{ si: 'ver_nilo_libre', node: 'dehors' }], si: 'ver_nilo_libre&!ver_chasses', cacheCombat: true, bloque: false },
    // la harde hors combat : bêtes figées, examen (pas de portrait)
    { id: 'rc_gris', name: 'Le gris', sprite: 'gen_rc_chancho_gris', x: 29.5, z: 12, faceTo: [26, 16], fige: true, portrait: false, dialogue: 'rc_harde', si: '!ver_harde_partie', cacheCombat: true },
    { id: 'rc_chancho_a', name: 'Chancho', sprite: 'gen_rc_chancho', x: 24.5, z: 10.5, faceTo: [27, 12], fige: true, portrait: false, dialogue: 'rc_harde', si: '!ver_harde_partie', cacheCombat: true },
    { id: 'rc_chancho_b', name: 'Chancho', sprite: 'gen_rc_chancho', x: 26.5, z: 13.5, faceTo: [26, 16], fige: true, portrait: false, dialogue: 'rc_harde', si: '!ver_harde_partie', cacheCombat: true },
    { id: 'rc_chancho_c', name: 'Chancho', sprite: 'gen_rc_chancho', x: 33, z: 11.5, faceTo: [28, 11], fige: true, portrait: false, dialogue: 'rc_harde', si: '!ver_harde_partie', cacheCombat: true },
  ],
  points: [ /* §3 et §9 : ver_verre_ex, ver_blinde (fouille), ver_panneau_ex, ver_peniche (coque si ver_chasses), ver_porte_ex (perles),
               ver_four_ex, ver_condens_ex, ver_etabli (vente / vol Discrétion 6 / libre si ver_chasses), ver_cuve_ex, ver_porte_cabane_ex,
               ver_fenetre (→ rc_nilo), ver_rigole (leurre, Survie 4), ver_citerne (proue), ver_harde (→ rc_harde) */ ],
  dialogues: DIALOGUES_VERRIERS,   // §6 : rc_balta, rc_tecla, rc_rufina, rc_nilo, rc_harde, rc_verre
  combat: { nom: 'La harde de l\u2019écluse', centre: { x: 24, z: 15 }, prefixe: 'ver_', drapeauxDebut: ['t1', 'combat'],
    ennemis: [
      { id: 'gris', nom: 'Le gris', sprite: 'gen_rc_chancho_gris', x: 29.5, z: 12, pv: 18, pa: 6, initiative: 5, arme: 'defenses', competences: { melee: 55, armes: 0 }, rendSous: 0.5, si: '!ver_conseil_gris' },
      { id: 'gris_c', nom: 'Le gris', sprite: 'gen_rc_chancho_gris', x: 29.5, z: 12, pv: 18, pa: 6, initiative: 5, arme: 'defenses', competences: { melee: 55, armes: 0 }, rendSous: 0.6, si: 'ver_conseil_gris' },
      { id: 'jeune_a', nom: 'Chancho', sprite: 'gen_rc_chancho', x: 24.5, z: 10.5, pv: 8, pa: 7, initiative: 7, arme: 'defenses', competences: { melee: 40, armes: 0 }, fuitTour: 3 },
      { id: 'jeune_b', nom: 'Chancho', sprite: 'gen_rc_chancho', x: 26.5, z: 13.5, pv: 8, pa: 7, initiative: 6, arme: 'defenses', competences: { melee: 40, armes: 0 }, fuitTour: 3 },
      { id: 'jeune_c', nom: 'Chancho', sprite: 'gen_rc_chancho', x: 33, z: 11.5, pv: 8, pa: 7, initiative: 6, arme: 'defenses', competences: { melee: 35, armes: 0 }, fuitTour: 2 } ],   // les Verriers jamais au combat
    issues: { victoire: 'flag:ver_harde_partie;flag:ver_harde_battue', fuite: 'rencontre:quitter',
              reddition: 'flag:ver_recule', defaite: 'flag:ver_recule;give:water;warp:rc_ecluse_verriers:11.5:20.5' },
    textes: { debut: 'Le gris lève la tête de la porte. Derrière toi, Balta crie : « Le gris ! Tape le gris ! » Il ne tire pas.',
      rend: { gris: 'Le gris détale.', gris_c: 'Le gris détale.' },                                          // §12.7 : texte de reddition par ennemi
      victoire: 'Le gris s\u2019arrête, souffle, et te tourne le dos. Il ne court pas : il s\u2019en va. Les jeunes le suivent par le bout de la cuve, dans le verre. Balta abaisse son fusil. Il n\u2019a pas tiré.',
      fuite: 'Tu enjambes le parapet et tu cours. Le gris ne te suit pas : ce n\u2019est pas toi qu\u2019il veut, c\u2019est l\u2019eau.',
      reddition: 'Tu recules, mains vides, jusqu\u2019au parapet. Le gris te laisse partir. Derrière toi, la porte de la cabane craque encore.',
      defaite: 'Tu te réveilles contre le four. Tecla te tient la tête. « Le gris t\u2019a fait voler. Bois. »' } },
};
```
`monde_verriers_vus` est posé à l'arrivée par `drapeauArrivee`, en plus du journal de la case. Le point de réveil de la défaite (11,5 ; 20,5) est devant la gueule du four, sur une case libre.
## 15. Poses définitives et sprites publiés
Sprites produits et publiés dans `assets/rencontres/` (groupe `rc_ecluse_verriers`, manifeste sans clé existante modifiée, vérifié par script) : lot 1 sols et décors `08e8356`, lot 2 PNJ et créatures `200bc62`. Même pipeline que le pilote et la caravane : modèle 3D aux cotes de ce document, rendu à la caméra du jeu (50 px/m), repeint image-à-image puis recalé par échelle uniforme + translation ; ombres de contact peintes au pied des décors ; aucun étirement. Planche : `nml-shots/rencontres/mutants_planche_sprites.png` ; MAQUETTE jour + nuit : `nml-shots/rencontres/mutants_maquette.png`.

**Tirage** : n'importe quelle case de verre (I04, I03, J04 par exemple), §1 ; la scène ne dépend pas de la case.

### 15.1 Table des poses (décors)
x, z = coin nord-ouest de l'emprise ; l'ancre du sprite tombe au coin sud-est au sol (x + w ; z + d). `depth` = (x + w) + (z + d) ; `ordre` = ordre de dessin conseillé (décalques `fond` d'abord).

| Clé | x | z | w | d | Solides (x, z, w, d, couv) | Ordre | Depth |
|---|---|---|---|---|---|---|---|
| `rc_ecl_four_flaque` | 10 | 19 | 3 | 2 | fond | 1 | 34 |
| `rc_ecl_cuve_3q` | 22 | 10 | 9 | 4 | fond | 2 | 45 |
| `rc_vr_dalles_3q` | 5 | 2 | 2 | 2 | 5, 2, 2, 2, 1 | 3 | 11 |
| `rc_vr_parapet_3q` | 0 | 8.5 | 6 | 0.5 | 0, 8.5, 6, 0.5, 1 | 4 | 15 |
| `rc_ds_panneau_ufsa_3q` | 1.2 | 16.4 | 0.6 | 0.2 | 1.4, 16.4, 0.2, 0.2, 0 | 5 | 18.4 |
| `rc_vr_parapet_b_3q` | 0 | 15 | 3 | 0.5 | 0, 15, 3, 0.5, 1 | 6 | 18.5 |
| `rc_vr_dalles_b_3q` | 14 | 3 | 2 | 2 | 14, 3, 2, 2, 1 | 7 | 21 |
| `rc_vr_parapet_3q` | 6 | 8.5 | 6 | 0.5 | 6, 8.5, 6, 0.5, 1 | 8 | 21 |
| `rc_vr_escalier_quai_3q` | 12 | 8.5 | 3 | 0.5 | — | 9 | 24 |
| `rc_ecl_peniche_3q` | 2 | 9.5 | 11 | 4.5 | 2, 9.5, 11, 4.5, 2 | 10 | 27 |
| `rc_ecl_etabli_3q` | 6 | 17.2 | 3 | 0.8 | 6, 17.2, 3, 0.8, 1 | 11 | 27 |
| `rc_vr_parapet_3q` | 6 | 15 | 6 | 0.5 | 6, 15, 6, 0.5, 1 | 12 | 27.5 |
| `rc_vr_parapet_3q` | 15 | 8.5 | 6 | 0.5 | 15, 8.5, 6, 0.5, 1 | 13 | 30 |
| `rc_ecl_four_3q` | 10 | 16.3 | 3 | 2.7 | 10, 16.3, 3, 2.7, 2 | 14 | 32 |
| `rc_ecl_porte_nord_3q` | 19 | 9 | 1.5 | 3 | 19, 9, 1.5, 3, 2 | 15 | 32.5 |
| `rc_vr_parapet_3q` | 12 | 15 | 6 | 0.5 | 12, 15, 6, 0.5, 1 | 16 | 33.5 |
| `rc_ecl_condenseur_3q` | 14 | 16.3 | 1.5 | 2 | 14, 16.3, 1.5, 2, 1 | 17 | 33.8 |
| `rc_vr_blinde_vitrifie_3q` | 26 | 1 | 5 | 3 | 26, 1, 5, 3, 2 | 18 | 35 |
| `rc_ecl_condenseur_3q (miroir)` | 16 | 16.3 | 1.5 | 2 | 16, 16.3, 1.5, 2, 1 | 19 | 35.8 |
| `rc_vr_parapet_3q` | 21 | 8.5 | 6 | 0.5 | 21, 8.5, 6, 0.5, 1 | 20 | 36 |
| `rc_ecl_condenseur_3q` | 18 | 16.3 | 1.5 | 2 | 18, 16.3, 1.5, 2, 1 | 21 | 37.8 |
| `rc_ecl_porte_sud_3q` | 20.5 | 14 | 3 | 1 | 20.5, 14, 3, 1, 2 | 22 | 38.5 |
| `barrel` | 20.7 | 17 | 0.6 | 0.6 | 20.7, 17, 0.6, 0.6, 1 | 23 | 38.9 |
| `rc_vr_parapet_3q` | 18 | 15 | 6 | 0.5 | 18, 15, 6, 0.5, 1 | 24 | 39.5 |
| `rc_ds_rochers_b_3q` | 8 | 27.8 | 3 | 1.5 | 8, 27.8, 3, 1.5, 1 | 25 | 40.3 |
| `rc_vr_parapet_3q` | 27 | 8.5 | 6 | 0.5 | 27, 8.5, 6, 0.5, 1 | 26 | 42 |
| `rc_vr_parapet_b_3q` | 33 | 8.5 | 3 | 0.5 | 33, 8.5, 3, 0.5, 1 | 27 | 45 |
| `rc_ecl_cabane_3q` | 24 | 16.2 | 4 | 3.8 | 24, 16.2, 4, 3.8, 2 | 28 | 48 |
| `rc_vr_parapet_3q` | 27 | 15 | 6 | 0.5 | 27, 15, 6, 0.5, 1 | 29 | 48.5 |
| `rc_vr_parapet_b_3q` | 33 | 15 | 3 | 0.5 | 33, 15, 3, 0.5, 1 | 30 | 51.5 |
| `rc_ds_rochers_3q` | 29 | 27.9 | 3 | 1.5 | 29, 27.9, 3, 1.5, 1 | 31 | 61.4 |

Calques : `rc_ecl_four_3q_neon` (additif, posé par le moteur sur le bâtiment `ver_four`, vraie source : la gueule ; le verre ne luit jamais) ; `rc_vr_blinde_vitrifie_3q_texte` (calque normal, `etage: 1`, jamais en miroir). `rc_ecl_four_flaque` est un décalque additif à n'afficher que la nuit (§12.9).

### 15.2 PNJ et créatures
| Clé | Position (x ; z) | Hauteur | Remarques |
|---|---|---|---|
| `gen_rc_balta` (+ `_dos`) | (5.5 ; 20.4) | 1.82 m | faceTo (1,5 ; 24) |
| `gen_rc_tecla` (+ `_dos`) | (13.2 ; 19.6) | 1.1 m | assise, faceTo (1,5 ; 24) |
| `gen_rc_rufina` (+ `_dos`) | (7.5 ; 18.8) | 1.74 m | faceTo (11,5 ; 19) |
| `gen_rc_nilo` (+ `_dos`) | (25.5 ; 20.6) | 1.5 m | si ver_nilo_libre, faceTo (11,5 ; 19) |
| `gen_rc_chancho` (+ `_dos`) | (24.5 ; 10.5) | garrot 0.75 m, long. ≈ 1.1 m ; height_m 1.318 (hauteur du billboard, sprite à 200 px/m) | figé, examen harde |
| `gen_rc_chancho` (+ `_dos`) | (26.5 ; 13.5) | garrot 0.75 m, long. ≈ 1.1 m ; height_m 1.318 (hauteur du billboard, sprite à 200 px/m) | figé, miroir |
| `gen_rc_chancho` (+ `_dos`) | (33 ; 11.5) | garrot 0.75 m, long. ≈ 1.1 m ; height_m 1.318 (hauteur du billboard, sprite à 200 px/m) | figé |
| `gen_rc_chancho_gris` (+ `_dos`) | (29.5 ; 12) | garrot 0.95 m, long. ≈ 1.5 m ; height_m 1.541 (hauteur du billboard, sprite à 200 px/m) | figé, tête vers la cabane (sud-est) |

PNJ : ancre au pied, au centre (`anchor` du manifeste), portraits `portrait-gen_rc_balta`, `-tecla`, `-rufina`, `-nilo` (192 px). Créatures : ancre au **centre des pattes** au sol (pas le bas du sprite), vue de face tête vers le sud-ouest, vue de dos tête vers le nord-est, le miroir donne les deux autres côtés ; pas de portrait.

### 15.3 Clés publiées
| Clé | px | Ancre | Emprise L × P × H (m) |
|---|---|---|---|
| `g_rc_verre` | 512 × 512 | — | tuile 4 m |
| `g_rc_verre_b` | 512 × 512 | — | tuile 4 m |
| `g_rc_verre_c` | 512 × 512 | — | tuile 4 m |
| `g_rc_quai` | 512 × 512 | — | tuile 4 m |
| `g_rc_limon` | 512 × 512 | — | tuile 4 m |
| `g_rc_limon_b` | 512 × 512 | — | tuile 4 m |
| `g_rc_cendre` | 512 × 512 | — | tuile 4 m |
| `g_rc_cendre_b` | 512 × 512 | — | tuile 4 m |
| `rc_vr_dalles_3q` | 141 × 118 | [80, 111] | 2 × 2 × 1.2 |
| `rc_vr_dalles_b_3q` | 141 × 103 | [80, 96] | 2 × 2 × 0.9 |
| `rc_vr_blinde_vitrifie_3q` | 293 × 203 | [204, 196] | 5 × 3 × 2.4 |
| `rc_vr_parapet_3q` | 267 × 128 | [248, 121] | 6 × 0.5 × 0.7 |
| `rc_vr_parapet_b_3q` | 143 × 88 | [124, 81] | 3 × 0.5 × 0.7 |
| `rc_vr_escalier_quai_3q` | 142 × 100 | [123, 93] | 3 × 0.5 × 0.7 |
| `rc_ecl_peniche_3q` | 604 × 337 | [472, 330] | 11 × 4.5 × 3 |
| `rc_ecl_porte_nord_3q` | 153 × 221 | [64, 214] | 1.5 × 3 × 3.4 |
| `rc_ecl_porte_sud_3q` | 162 × 177 | [129, 170] | 3 × 1 × 3.4 |
| `rc_ecl_four_3q` | 206 × 213 | [125, 206] | 3 × 2.7 × 3.4 |
| `rc_ecl_condenseur_3q` | 120 × 146 | [59, 139] | 1.5 × 2 × 1.8 |
| `rc_ecl_etabli_3q` | 149 × 100 | [121, 93] | 3 × 0.8 × 0.9 |
| `rc_ecl_cabane_3q` | 290 × 256 | [176, 249] | 4 × 3.8 × 3 |
| `rc_ecl_four_3q_neon` | 206 × 213 | [125, 206] | calque `neon` de `rc_ecl_four_3q` |
| `rc_vr_blinde_vitrifie_3q_texte` | 293 × 203 | [204, 196] | calque `texte` de `rc_vr_blinde_vitrifie_3q` |
| `rc_ecl_cuve_3q` | 493 × 211 | [375, 206] | 9 × 4 × 0 |
| `rc_ecl_four_flaque` | 189 × 89 | [128, 85] | 3 × 2 × 0 |
| `gen_rc_balta` | 216 × 512 | [108, 511] | 1.82 m de haut |
| `portrait-gen_rc_balta` | 192 × 192 | — | portrait |
| `gen_rc_balta_dos` | 210 × 512 | [105, 511] | 1.82 m de haut |
| `gen_rc_tecla` | 330 × 512 | [165, 511] | 1.1 m de haut |
| `portrait-gen_rc_tecla` | 192 × 192 | — | portrait |
| `gen_rc_tecla_dos` | 334 × 512 | [167, 511] | 1.1 m de haut |
| `gen_rc_rufina` | 180 × 512 | [90, 511] | 1.74 m de haut |
| `portrait-gen_rc_rufina` | 192 × 192 | — | portrait |
| `gen_rc_rufina_dos` | 154 × 512 | [77, 511] | 1.74 m de haut |
| `gen_rc_nilo` | 160 × 512 | [80, 511] | 1.5 m de haut |
| `portrait-gen_rc_nilo` | 192 × 192 | — | portrait |
| `gen_rc_nilo_dos` | 154 × 512 | [77, 511] | 1.5 m de haut |
| `gen_rc_chancho` | 228 × 231 | [128, 185] | garrot 0.75, long. 1.1 (billboard 1.318) |
| `gen_rc_chancho_dos` | 228 × 242 | [100, 193] | garrot 0.75, long. 1.1 (billboard 1.381) |
| `gen_rc_chancho_gris` | 308 × 270 | [172, 213] | garrot 0.95, long. 1.5 (billboard 1.541) |
| `gen_rc_chancho_gris_dos` | 308 × 327 | [136, 258] | garrot 0.95, long. 1.5 (billboard 1.866) |

### 15.4 Bloc JS aligné
Le bloc du §14 est déjà aligné sur ces poses (mêmes x, z, w, d, solides, miroir du condenseur central, `fond` des deux décalques). Lignes générées depuis la table (mut_v1/poses_mut.py), à coller telles quelles si le §14 bouge :

```js
{ sprite: 'rc_ecl_four_flaque', x: 10, z: 19, w: 3, d: 2, fond: true }  // flaque de lumière du four, nuit seulement (retouche à la manière du bivouac, §12.9),
{ sprite: 'rc_ecl_cuve_3q', x: 22, z: 10, w: 9, d: 4, fond: true }  // décalque sol : boue, tessons, sabots ; sous tout le reste,
{ sprite: 'rc_vr_dalles_3q', x: 5, z: 2, w: 2, d: 2, solid: [{ x: 5, z: 2, w: 2, d: 2, couv: 1 }] },
{ sprite: 'rc_vr_parapet_3q', x: 0, z: 8.5, w: 6, d: 0.5, solid: [{ x: 0, z: 8.5, w: 6, d: 0.5, couv: 1 }] }  // parapet nord,
{ sprite: 'rc_ds_panneau_ufsa_3q', x: 1.2, z: 16.4, w: 0.6, d: 0.2, solid: [{ x: 1.4, z: 16.4, w: 0.2, d: 0.2, couv: 0 }] }  // réutilisé,
{ sprite: 'rc_vr_parapet_b_3q', x: 0, z: 15, w: 3, d: 0.5, solid: [{ x: 0, z: 15, w: 3, d: 0.5, couv: 1 }] }  // parapet sud, bout ouest (cale x 3-6),
{ sprite: 'rc_vr_dalles_b_3q', x: 14, z: 3, w: 2, d: 2, solid: [{ x: 14, z: 3, w: 2, d: 2, couv: 1 }] },
{ sprite: 'rc_vr_parapet_3q', x: 6, z: 8.5, w: 6, d: 0.5, solid: [{ x: 6, z: 8.5, w: 6, d: 0.5, couv: 1 }] }  // parapet nord,
{ sprite: 'rc_vr_escalier_quai_3q', x: 12, z: 8.5, w: 3, d: 0.5 }  // passage nord : non solide,
{ sprite: 'rc_ecl_peniche_3q', x: 2, z: 9.5, w: 11, d: 4.5, solid: [{ x: 2, z: 9.5, w: 11, d: 4.5, couv: 2 }] }  // porte au sud x 7-8 (on n’entre pas),
{ sprite: 'rc_ecl_etabli_3q', x: 6, z: 17.2, w: 3, d: 0.8, solid: [{ x: 6, z: 17.2, w: 3, d: 0.8, couv: 1 }] },
{ sprite: 'rc_vr_parapet_3q', x: 6, z: 15, w: 6, d: 0.5, solid: [{ x: 6, z: 15, w: 6, d: 0.5, couv: 1 }] }  // parapet sud,
{ sprite: 'rc_vr_parapet_3q', x: 15, z: 8.5, w: 6, d: 0.5, solid: [{ x: 15, z: 8.5, w: 6, d: 0.5, couv: 1 }] }  // parapet nord,
{ sprite: 'rc_ecl_four_3q', x: 10, z: 16.3, w: 3, d: 2.7, solid: [{ x: 10, z: 16.3, w: 3, d: 2.7, couv: 2 }] }  // gueule au sud en (11,5 ; 19) ; + _neon (le moteur le pose sur les buildings),
{ sprite: 'rc_ecl_porte_nord_3q', x: 19, z: 9, w: 1.5, d: 3, solid: [{ x: 19, z: 9, w: 1.5, d: 3, couv: 2 }] }  // la silhouette de la scène ; perles côté est,
{ sprite: 'rc_vr_parapet_3q', x: 12, z: 15, w: 6, d: 0.5, solid: [{ x: 12, z: 15, w: 6, d: 0.5, couv: 1 }] }  // parapet sud,
{ sprite: 'rc_ecl_condenseur_3q', x: 14, z: 16.3, w: 1.5, d: 2, solid: [{ x: 14, z: 16.3, w: 1.5, d: 2, couv: 1 }] },
{ sprite: 'rc_vr_blinde_vitrifie_3q', x: 26, z: 1, w: 5, d: 3, solid: [{ x: 26, z: 1, w: 5, d: 3, couv: 2 }] }  // + rc_vr_blinde_vitrifie_3q_texte en etage: 1 sur la même emprise,
{ sprite: 'rc_ecl_condenseur_3q', x: 16, z: 16.3, w: 1.5, d: 2, solid: [{ x: 16, z: 16.3, w: 1.5, d: 2, couv: 1 }], miroir: true },
{ sprite: 'rc_vr_parapet_3q', x: 21, z: 8.5, w: 6, d: 0.5, solid: [{ x: 21, z: 8.5, w: 6, d: 0.5, couv: 1 }] }  // parapet nord,
{ sprite: 'rc_ecl_condenseur_3q', x: 18, z: 16.3, w: 1.5, d: 2, solid: [{ x: 18, z: 16.3, w: 1.5, d: 2, couv: 1 }] },
{ sprite: 'rc_ecl_porte_sud_3q', x: 20.5, z: 14, w: 3, d: 1, solid: [{ x: 20.5, z: 14, w: 3, d: 1, couv: 2 }] },
{ sprite: 'rc_vr_parapet_3q', x: 18, z: 15, w: 6, d: 0.5, solid: [{ x: 18, z: 15, w: 6, d: 0.5, couv: 1 }] }  // parapet sud,
{ sprite: 'rc_ds_rochers_b_3q', x: 8, z: 27.8, w: 3, d: 1.5, solid: [{ x: 8, z: 27.8, w: 3, d: 1.5, couv: 1 }] }  // réutilisé,
{ sprite: 'rc_vr_parapet_3q', x: 27, z: 8.5, w: 6, d: 0.5, solid: [{ x: 27, z: 8.5, w: 6, d: 0.5, couv: 1 }] }  // parapet nord,
{ sprite: 'rc_vr_parapet_b_3q', x: 33, z: 8.5, w: 3, d: 0.5, solid: [{ x: 33, z: 8.5, w: 3, d: 0.5, couv: 1 }] }  // parapet nord, bout est,
{ sprite: 'rc_ecl_cabane_3q', x: 24, z: 16.2, w: 4, d: 3.8, solid: [{ x: 24, z: 16.2, w: 4, d: 3.8, couv: 2 }] }  // porte au nord (face cachée, traces au coin NE), fenêtre au sud,
{ sprite: 'rc_vr_parapet_3q', x: 27, z: 15, w: 6, d: 0.5, solid: [{ x: 27, z: 15, w: 6, d: 0.5, couv: 1 }] }  // parapet sud (seuil x 24-27),
{ sprite: 'rc_vr_parapet_b_3q', x: 33, z: 15, w: 3, d: 0.5, solid: [{ x: 33, z: 15, w: 3, d: 0.5, couv: 1 }] }  // parapet sud, bout est,
{ sprite: 'rc_ds_rochers_3q', x: 29, z: 27.9, w: 3, d: 1.5, solid: [{ x: 29, z: 27.9, w: 3, d: 1.5, couv: 1 }] }  // réutilisé,
```

### 15.5 Défauts connus (v1, mis à jour par la retouche v1.1)
- La porte nord de la cabane est sur une face cachée à cette caméra : elle est signalée par des planches éclatées au coin nord-est ; le dialogue passe par la fenêtre sud, visible.
- Le gris : l'oreille fendue ne se lit pas à la taille du jeu (visible seulement à la planche).
- Rufina : ses plaques d'avant-bras sont un peu « écailles » ; Nilo : les taches de sa chemise reprennent le motif de sa peau.
- `g_rc_verre` : motif de dalles répétitif à 4 m sur les grandes surfaces ; semer `_b` et `_c`.
- Escalier v1.1 : la descente se lit, mais l'emprise ne fait que 0,5 m de profondeur ; les cinq marches sont donc minces à la taille du jeu, et le liseré de sable du bas touche le bord gauche de la toile.

**Corrigé en v1.1** (mêmes clés, mêmes px, mêmes ancres ; rien à recâbler) :
- `gen_rc_chancho_dos` et `gen_rc_chancho_gris_dos` : vraies vues de dos 3/4 (croupe et queue vers la caméra, tête au nord-est presque cachée par les épaules, quatre sabots au sol), peintes sur un nouveau modèle bloc arrondi ; le centre des sabots est posé sur l'ancre v1.
- `rc_vr_escalier_quai_3q` : géométrie refaite. Palier au niveau du quai au nord, cinq marches qui descendent vers le canal (sud), contremarches sombres, échiffres en pente, sable amassé au pied ; plus de mur en haut.
- `rc_vr_blinde_vitrifie_3q` : tôle gris acier vitrifiée, quelques coulures de rouille seulement ; socle de verre intact. Le calque `_texte` n'a pas changé et reste aligné (même toile, même ancre).
- `gen_rc_chancho` (le jeune) : cuir gris de cendre ; les défenses et le groin n'ont pas changé.
