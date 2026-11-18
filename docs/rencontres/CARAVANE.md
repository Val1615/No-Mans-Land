# Rencontre du jalon 2 : « La citerne qui respire » (caravane marchande)

Jalon 2 du chantier (voir [README.md](README.md)), famille **caravane marchande (échange)**. Création : Ocre, 18/11/2026 (heure de Paris). Même format que [PILOTE.md](PILOTE.md).

> **Écrite sur [`ARCHI.md`](ARCHI.md) dès le départ** : format §4, préfixes `rc_` / `rc_ds_` / `g_rc_` / `gen_rc_`, 50 px/m, scène 35 × 26 m (dans la plage 24 × 24 à 48 × 36) avec la zone de combat 19 × 19 entièrement dedans, ennemis en positions absolues sur cases libres, à ≥ 8 m de l'entrée et répartis, pas d'ennemi neutre, **aucune hauteur** (ni pour les unités de combat, ni pour les PNJ : la scène n'a pas de `niveaux`), journal par case, drapeaux de scène `car_*` remis à zéro à la sortie (même règle que `emb_*`), examen au toucher sur mobile, Observation seule (aucun trait spécial).
>
> **Sans sprites** (consigne de Régie, 18/11) : rien n'est produit tant que le cadrage du jalon 1 n'est pas vérifié. Les clés nouvelles sont listées au §10 ; tout le reste réutilise les modules du désert déjà publiés (`assets/rencontres/manifest.json`).

Maquette concept (MAQUETTE, pas une capture) : `/workspace/nml-shots/rencontres/caravane_concept.png` sur la machine d'Ocre (vue iso composée avec les sprites publiés et des volumes de principe pour les éléments nouveaux, + plan coté). Le plan coté de ce document fait foi.

## 1. Fiche
| Champ | Valeur |
|---|---|
| id | `caravane_relais` [proposition], préfixe de drapeaux `car_` |
| Famille | Caravane marchande (échange) |
| Terrains | `piste` (p = 0,05) de `src/data/nml.js` ; taux inchangés |
| Biome | désert (`desert` du manifest) : reg caillouteux au pied d'un talus de grès |
| Cases de référence | la piste Douane ouest → Station de répartition : **J07 (9,6)** et **J08 (9,7)** ; prolongement vers Novo Córdoba : K10 (10,9). Toutes en biome `desert`. Pour le test : forcée par le mode DEV |
| Moment | jour (même soleil que le pilote, pour que les modules réutilisés restent justes) |
| Emprise | 35 × 26 m (x vers l'est, z vers le sud, origine au coin nord-ouest), **un seul niveau de marche, au sol** |
| Faction | aucune : caravane indépendante (voir §13) |
| Rejouable | non : journal par case comme le pilote. De plus, la caravane de Remedios est **unique** : `si` refuse la rencontre si `monde_remedios_vue` est posé (drapeau de monde, hors préfixe `car_`, jamais purgé) |
| Durée ajoutée | 1 h ; +1 h si la citerne a été réparée (`car_repare`) |

## 2. Pitch et situation
**Pitch.** Une caravane marchande a fait halte au vieux relais du puits sec. Sa citerne penche : un ressort a cassé. La patronne vend, le mécano jure sous la remorque, le garde surveille la piste. Et la citerne d'eau, qui ne contient pas d'eau, respire.

**Situation.** La caravane de **Doña Remedios** fait le circuit Novo Córdoba → Station de répartition → Douane ouest → Dusk-Town, une fois par lune quand tout va bien. Elle a un mois de retard : à Dusk-Town, on l'attend (Ileana, Teo, et d'autres qui ne sortent pas le jour). Ce matin, sur une ornière, la lame maîtresse du ressort arrière de la citerne a cassé net. Ciro, le mécanicien, est dessous depuis l'aube ; Fierro, le garde, tient le puits et la piste ; Remedios a ouvert le comptoir, parce qu'une caravane arrêtée qui ne vend rien perd deux fois.

Le secret : la citerne n'a pas porté d'eau depuis des années. Son double fond porte des **passagers**, des gens que le Service Militarisé ramasse dans ses rafles. Aujourd'hui, il n'y en a qu'une : **Lena**, mutante de Novo Córdoba, qui monte vers Dusk-Town pour chercher un chemin vers la Sous-Ville de Steel, où son père a été jeté.

Le joueur peut acheter, vendre, troquer, apprendre ce qui se passe sur les pistes, réparer la citerne, escorter la caravane, découvrir Lena et garder ou vendre son silence, voler, ou attaquer. Personne ne l'oblige à s'arrêter : la piste traverse la scène et la sortie est est **ouverte** dès l'arrivée.

## 3. Ce que le décor raconte
Tout est examinable (clic sur ordinateur ; sur mobile, appui sur le point d'examen, avec un anneau comme les portes ; pas d'examen au survol). Les indices marqués ★ mènent au secret de la citerne.

| Où (x ; z) | Ce qu'on voit | Texte d'examen | Effet |
|---|---|---|---|
| Façade du relais (4,5 ; 15) | relais routier UFSA en pisé, toit effondré, vieille pompe à carburant | « Un relais de l'UFSA. Sur le mur, à hauteur d'homme, des centaines de traits gravés au couteau, par paquets de cinq. Chaque caravane qui passe en ajoute un. Les plus vieux sont presque effacés par le sable ; il y a un long blanc, puis les traits reprennent, plus espacés. Le dernier est frais. » ★ Observation 4 : « À côté du dernier trait, un petit cercle. Puis un deuxième, plus ancien. Et d'autres, en remontant. Pas à chaque caravane. » | `flag:car_indice_cercles` |
| Panneau (1,5 ; 17,6) | panneau UFSA criblé | « Le panneau a perdu ses lettres. Quelqu'un y a peint à la chaux un seau et une flèche vers le relais. Le seau a été barré, plus tard, d'un trait noir. » | — |
| Puits (13,5 ; 15,5) | margelle de pierre, treuil, seau | « Un puits sec. Le treuil tourne encore. Au bout de la corde, le seau remonte plein de sable fin. Les caravanes ne s'arrêtent plus ici pour l'eau, mais pour l'ombre du talus et le seul sol plat à dix kilomètres. » Observation 4 : « Accrochée à un clou, juste sous la margelle : une gourde pleine. Quelqu'un garde sa réserve là où personne ne cherche plus d'eau. » | ouvre la fouille `car_gourde` (§9) |
| Ferraille de l'atelier (10 ; 12,6) | tas de jantes, un essieu, des lames de ressort collées par la rouille | « L'ancien atelier du relais : jantes, un demi-essieu, un paquet de lames de ressort soudées par la rouille. » | fouille de la quête (§9) |
| Portière du tracteur (15,2 ; 12,6) | lettres peintes à la main, écaillées | « Sur la portière : TRANSPORTES REMEDIOS — NOVO CÓRDOBA · DUSK-TOWN. Le nom de Dusk-Town a été repeint plus récemment que le reste. » | — |
| Bivouac (17,5 ; 17) | trois pierres, marmite, tabourets-caisses | « Des haricots qui mijotent sur trois pierres. Une fumée mince monte droit : pas de vent. » ★ Observation 3 : « Quatre gamelles, cinq cuillères. Trois personnes en vue. » | `flag:car_indice_cuilleres` |
| Traces (24 ; 16,5) | arcs de pneus, trous de cric | « Les camions sont entrés en arc, comme on range des chariots. Sous la citerne, trois trous de cric : trois essais, le sable n'a pas tenu. » | — |
| ★ Citerne (33,5 ; 13,6) | citerne sur remorque, penchée vers l'arrière, vanne sèche | « Une citerne d'eau sur remorque, penchée vers l'arrière : le ressort a lâché. Sous la vanne, le sable est sec. Pas une goutte. » Observation 5 (ou Observation 3 si `car_indice_cercles` ou `car_indice_cuilleres`) : « Sur le dessus, une rangée de petits trous percés à la mèche, propres, récents. On n'aère pas de l'eau. » | `flag:car_vu_citerne` ; ouvre le nœud « frapper » (§6.4) |
| Bâche (31,5 ; 18,4) | bâche tendue, sacs, bidons bleus | « Les bidons bleus de la caravane, les mêmes qu'on voit partout entre Dusk-Town et la douane. Fierro a posé sa couverture juste à côté. » | — |
| Comptoir (25,5 ; 13,4) | flanc de remorque rabattu en comptoir, auvent | « Le flanc de la remorque, rabattu sur deux chaînes, fait comptoir. Dessous, un coffre cadenassé. Remedios ne s'en éloigne jamais de plus de deux pas. » | — |

Lecture à 1280 et en 390 : dès l'arrivée, l'œil trouve d'abord **la citerne qui penche** (la raison de l'arrêt), puis le **comptoir sous l'auvent** (la raison de s'approcher), puis Fierro au puits, sur le chemin. Ciro n'est que deux jambes sous la citerne. Lena n'est pas visible. Aucune lumière artificielle : il fait jour, et la seule « source » qui bouge est la fumée de la marmite, peinte avec son foyer, sans halo.

## 4. Plan coté (provisoire)
Vue de dessus, 1 caractère = 1 m. Légende : `t` talus nord (module plein, **non praticable**, z 0-8,5 ; la pente z 5-8,5 est solide `couv: 1`, le plateau n'est pas atteignable), `r` relais (ruine), `f` ferraille, `:` cour de galets (sol `g_rc_lit`), `p` puits, `o` fût, `T` tracteur (cabine à l'ouest), `M` remorque-étal (comptoir au sud), `C` citerne (penchée), `k` ballots (×2), `b` bivouac, `B` bâche, `=` piste (6 m), `,` sable, `S` panneau, `R` rochers, `x` traces au sol (décalque), `@` apparition, `F` Fierro, `1` Remedios, `2` Ciro (sous la citerne), `L` Lena (si découverte). `O>` sortie ouest, `<E` sortie est.

```text
      0         1         2         3    
      01234567890123456789012345678901234
  0   ttttttttttttttttttttttttttttttttttt
  1   ttttttttttttttttttttttttttttttttttt
  2   ttttttttttttttttttttttttttttttttttt
  3   ttttttttttttttttttttttttttttttttttt
  4   ttttttttttttttttttttttttttttttttttt
  5   ttttttttttttttttttttttttttttttttttt
  6   ttttttttttttttttttttttttttttttttttt
  7   ttttttttttttttttttttttttttttttttttt
  8   ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
  9   ,rrrrrrr,,,,,,TTTTTTT,,,,,,,,,,,,,,
 10   ,rrrrrrrfff,kkTTTTTTT,MMMMMM,CCCCC,
 11   ,rrrrrrrfff,,,TTTTTTT,MMMMMM,CCCCC,
 12   ,rrrrrrr::::::::,,,,kkMMMMMM,CCCCC,
 13   ,rrrrrrr::::pp::bbb,kkxxxxxxxx,2,,,
 14   ,,,,,,,,::::pp::bbb,,xxxx1xxLxBBB,,
 15   ,,,,,,,,::::::::bbb,,xxxxxxxxxBBB,,
 16   ,,,,,,,,,,,,oF,,,,,,,xxxxxxxxxBBB,,
 17   ,S,,,,,,,,,,,,,,,,,,,xxxxxxxxxBBB,,
 18 O>===================================<E
 19 O>===================================<E
 20 O>===================================<E
 21 O>=@=================================<E
 22 O>===================================<E
 23 O>===================================<E
 24   ,,,,,,RRR,,,,,,,,,,,,,,,RRR,,,,,,,,
 25   ,,,,,,RRR,,,,,,,,,,,,,,,RRR,,,,,,,,
```

### Éléments et solides
| id | Élément | x0-x1 | z0-z1 | Haut. (m) | Solide | Couverture combat |
|---|---|---|---|---|---|---|
| sol_sable | terrasse et bas-côtés | 0-35 | 8,5-18 et 24-26 | 0 | non | 0 |
| sol_piste | piste damée, ornières | 0-35 | 18-24 | 0 | non | 0 |
| sol_galets | cour de galets autour du puits (le lit d'un ancien oued) | 8-16 | 12-16 | 0 | non | 0 |
| talus | talus nord, 3 modules + bout est | 0-35 | 0-8,5 | 0 → 2,5 | pente z 5-8,5 solide `couv: 1` ; plateau z 0-5 inatteignable (pas de `niveaux`, pas de sente) | 1 |
| relais | relais UFSA en ruine, toit effondré | 1-8 | 9,5-14,5 | 3,2 | oui (on n'entre pas) | 2 |
| ferraille | tas de l'atelier | 8,5-11,5 | 10-12 | 1,0 | oui | 1 |
| ballots_b | ballots près de la cabine | 12-14 | 9,6-10,8 | 1,1 | oui | 1 |
| tracteur | camion tracteur bâché, cabine à l'ouest | 14-21,5 | 9,5-12,1 | 3,3 | oui | 2 |
| remorque | remorque-étal, flanc rabattu en comptoir au sud | 22,5-28,5 | 9,8-13,0 | 3,0 (comptoir 1,0) | oui (comptoir compris) | 2 (1 au comptoir) |
| citerne | citerne sur remorque, penchée vers l'est | 29-34,5 | 10,5-12,9 | 2,6 | oui | 2 |
| ballots | ballots et caisses cordées | 20,4-22,4 | 12,4-13,6 | 1,2 | oui | 1 |
| puits | margelle, treuil | 12,5-14,5 | 13-15 | 2,6 (margelle 0,8) | oui | 1 |
| fut | fût vide (réutilisé `barrel.webp`) | 11,7-12,3 | 16,3-16,9 | 0,9 | oui | 1 |
| bivouac | foyer, marmite, tabourets-caisses | 16-19 | 13,5-16,5 | 1,2 (fumée peinte au-dessus) | foyer seul 17-18 ; 14,5-15,5 | 0 |
| bache | bâche tendue, bidons bleus (réutilisée) | 30-33,5 | 14,5-18 | 1,6 | bords nord (z 14,5-15) et est (x 33-33,5) | 1 |
| traces | décalque au sol | 21-30 | 13-18 | 0 | non | 0 |
| panneau | panneau UFSA (réutilisé) | 1,2-1,8 | 17-17,2 | 3,0 | oui (0,2 × 0,2) | 0 |
| rochers ×2 | blocs du bas-côté sud (réutilisés) | 6-9 / 24-27 | 24,3-25,8 / 24,4-25,9 | 1,6 / 1,2 | oui | 1 |

Un seul niveau de marche, au sol : pas de `niveaux`, pas de PNJ en hauteur, pas de `y`. Le talus sert de fond et de bord nord ; il ne se gravit pas.

### Apparition, sorties, déclencheurs
| id | Type | Position (m) | Rôle |
|---|---|---|---|
| spawn | apparition | (1,5 ; 21), regard vers l'est | on arrive par la piste ; la citerne qui penche, l'auvent et Fierro au puits sont lisibles ; Ciro (deux jambes) se devine |
| S_O | sortie | x = 0, z 18-24 | demi-tour : retour à la carte, halte sur la case, itinéraire conservé |
| S_E | sortie | x = 35, z 18-24 | reprise du voyage. **Jamais gardée** : la caravane ne bloque pas la piste (sauf pendant le combat, règle existante « sortie bloquée tant qu'un hostile tient la position ») |
| T1 | déclencheur | x 7-9, z 9-24 | Fierro interpelle le joueur une fois (§6.1, nœud `start`) |
| pres_citerne | déclencheur | x 28,5-35 ; z 12,9-14,5 (le long de la citerne) | rien de plus que l'examen : permet l'examen de la citerne sur mobile sans viser la petite zone |
| fuite | combat | bords de la zone 19 × 19 | issue « fuite » : retour à la carte comme S_O |

### Zone de combat
Centre (22 ; 16,5), zone 19 × 19 (x 12,5-31,5 ; z 7-26), entièrement dans l'emprise : aucune case dans le vide. La pente du talus en bord nord compte comme solide `couv: 1`.

## 5. Mise en scène échelonnée (découverte progressive)
1. **Arrivée** (x 1,5) : la piste, le relais en ruine à gauche, les trois véhicules rangés en arc, la citerne qui penche, la fumée de la marmite. Rien n'impose de s'arrêter : la sortie est est ouverte.
2. **Le garde** (T1, x ≥ 7) : Fierro, assis au pied du puits, se lève à moitié et interpelle. Il ne menace pas : il fixe les règles (§6.1).
3. **Le comptoir** : Remedios ouvre la conversation dès qu'on lui parle ; commerce, troc, nouvelles, panne (§6.2).
4. **La panne** : Ciro, sous la citerne, demande une clé, puis une lame de ressort ; la ferraille de l'atelier en contient une (§6.3, §9).
5. **Le secret** : les indices (cercles sur le mur, cinq cuillères) rendent l'examen de la citerne plus facile ; une fois les trous d'aération vus, on peut frapper. Trois coups répondent. Lena sort respirer (§6.4). Le joueur peut ne jamais la voir.

## 6. PNJ : fiches et dialogues
Format des dialogues : celui de `src/data/dialogues_*.js` et de `src/data/rencontres.js` (nœuds `text` + `options` ; `next`, `action` avec `pay:`, `buy:`, `sell:`, `take:`, `give:`, `gain:`, `hurt:`, `flag:`, `combat:`, `rencontre:` ; `test`, `pass`, `fail`, `partial`/`partialAt`, `opposed` ; `if` composés `a&b|c`). Conditions de race par les drapeaux de création existants (`race_mutant`, `race_humain`…). Les identifiants sont des propositions.

### 6.1 Fierro, le garde
- La cinquantaine, sec, moustache grise, poncho brun sur un gilet de cuir, chapeau à bord plat, fusil à canon long tenu bas. Ancien gardien de troupeaux. Parle peu, ne répète jamais, ne sourit pas. Il protège la caravane, pas le joueur ; il n'a rien contre le joueur.
- Stats : PV 16, PA 7, initiative 7, `fusil`, mêlée 35 %, armes 60 %, Volonté 7.
- Sprite : `gen_rc_fierro` (à produire) + portrait. Position (13,2 ; 16,8), au pied du puits, à côté d'un fût, regard vers la piste.

```text
start   (T1) (Il se lève à moitié.) « Halte. Les mains loin de la ceinture. » (Il ne lève pas son fusil. Il n'en a pas besoin.)
  - « Je suis de passage. »                                   → passage
  - « Vous vendez quelque chose ? »                           → vente
  - [si race_mutant] « Je ne cherche pas d'ennuis. Le Service les trouve tout seul. » → mutant
  - « Joli fusil. Il est à vendre ? »                         → fusil
  - [Attaquer]                                                action combat:caravane_relais
passage « La piste est à tout le monde. Passe au large du camp, pas entre les camions. » action flag:car_salue → end
vente   « La Doña vend. À la remorque. Tu achètes, tu paies, tu repars. Tu traînes, je te regarde traîner. » action flag:car_salue → end
mutant  (Il te regarde plus longtemps que les autres.) « Ici, personne ne pose la question. Va voir la Doña. Dis-lui que je t'envoie. » action flag:car_salue;flag:car_recommande → end
fusil   « Il est à moi depuis plus longtemps que toi tu marches. Non. » → start

encore  (si car_salue) « Tu es encore là. »
  - « Une caravane a besoin d'un garde comme toi ? »          → garde
  - « La piste est sûre, vers le nord ? »                     → nord
  - [si car_gourde] « Il y avait une gourde dans le puits. »  → gourde
  - « Rien. »                                                 → end
garde   « Parce que les pistes ont des péages, et que je n'aime pas payer. » → encore
nord    « Une femme avec des lunettes de soudeur prend quinze dollars entre la douane et Dusk-Town. Elle prend, et elle laisse vivre. Plus au nord, le Service ne prend rien. Il emmène. » → encore
gourde  « Il y avait. » (Il attend.)
  - Lui rendre une eau.        [si inv:water>=1] action take:water;flag:car_gourde_rendue → gourde_ok
  - « Je n'ai rien vu. »       action flag:car_fierro_froid → gourde_ko
gourde_ok « Bien. Tu peux rester. » → end
gourde_ko « Alors tu ne vois pas grand-chose. Fais attention où tu marches. » → end   (Remedios ne fait plus de remise : §6.2)
```

### 6.2 Doña Remedios, la patronne
- Soixante ans, ronde, châle garance sur une chemise d'homme, chapeau de paille à large bord, crayon derrière l'oreille, carnet de comptes attaché à la ceinture par une ficelle. Commerçante jusqu'au bout des ongles, chaleureuse tant qu'on paie, dure dès qu'on menace les siens. Elle transporte des gens depuis trente ans et n'en parle jamais la première.
- Stats : PV 12, PA 6, initiative 4, `pistolet`, mêlée 20 %, armes 40 %, Volonté 6.
- Sprite : `gen_rc_remedios` (à produire) + portrait. Position (25,5 ; 14,3), devant le comptoir, regard vers la piste.

```text
start   « Approche, approche. Pas trop près du comptoir, Fierro devient nerveux quand on touche à la marchandise. Je suis Remedios. Ici on vend, on achète, on troque, et on ne pose pas de questions. Toi, tu en as, des questions ? »
  - « Montre-moi ce que tu vends. »                           → vente
  - « J'ai des choses à vendre. »                             → achat
  - [si !car_remise & !car_fierro_froid] « Tes prix sont raides pour du sable. »   test troc:5, partialAt 4 → pass remise, partial remise_moitie, fail remise_rate
  - « Qu'est-ce qui se passe sur les pistes ? »               → nouvelles
  - [si !car_repare] « Ta citerne penche. »                   → panne
  - [si car_recommande] « Fierro m'envoie. »                  → recommande
  - [si car_vu_lena] « Ta citerne respire. »                  → secret
  - [si car_repare & !car_merci] « Ciro dit que la citerne tient. »   → merci
  - [si car_merci & !car_escorte_dit] « Ton offre tient toujours ? »  → escorte
  - [Attaquer]                                                action combat:caravane_relais
  - « Bonne route. »                                          → end

vente   « Eau filtrée, six dollars : c'est l'eau qui a fait la route. Rations, huit. Un poignard, quinze. Et un pistolet, un seul, quarante, avec sa graisse. »
          (prix avec car_remise : 5 / 7 / 14 / 36 ; avec car_remise_ami : 4 / 6 / 12 / 32 ; stock : 3 eaux, 2 rations, 1 poignard, 1 pistolet)
  - [si !car_eau3] Une eau.              action buy:water:<prix>;flag:car_eau<n+1>   (car_eau1 → car_eau2 → car_eau3)
  - [si !car_ration2] Une ration.        action buy:ration:<prix>;flag:car_ration<n+1>
  - [si !car_poignard] Le poignard.      action buy:poignard:<prix>;flag:car_poignard
  - [si !car_pistolet] Le pistolet.      action buy:pistolet:<prix>;flag:car_pistolet
  - [si car_eau3] « Plus d'eau ? »       → rupture
  - « Ça ira. »                          → start
rupture « Le reste est pour Dusk-Town. Tu veux qu'Anselme me tire les oreilles ? » → vente

achat   « Je prends les armes et ce qui se mange. Pas les histoires. »
  - [si inv:fusil>=1]     Le fusil (18 $).      action sell:fusil:18
  - [si inv:pistolet>=1]  Le pistolet (15 $).   action sell:pistolet:15
  - [si inv:poignard>=1]  Le poignard (5 $).    action sell:poignard:5
  - [si inv:barre>=1]     La barre (3 $).       action sell:barre:3
  - [si inv:ration>=1]    Une ration (4 $).     action sell:ration:4
  - [si inv:carnet_chauffeur>=1] « Un carnet de livreur. »   → carnet
  - [si inv:cric>=1]      « Un cric de camion. »   → cric
  - « C'est tout. »                             → start
carnet  (Elle lit, lèvres serrées.) « "Ne s'arrêter pour personne." C'est Benito, il roule pour Anselme. Il s'est arrêté quand même, hein ? Garde-le, Anselme voudra savoir. Benito est passé ici à pied il y a trois jours, vers la douane. Vivant, et très en colère. » → achat
cric    « Ciro te l'arracherait des mains. Va le lui montrer avant de me le vendre : il en a plus besoin que moi. » → achat

remise        « Tu comptes comme ma mère. Bon : un dollar de moins sur tout, quatre sur le pistolet. »   action flag:car_remise → vente
remise_moitie « Un dollar de moins sur l'eau, et c'est parce que tu as de beaux yeux. »   action flag:car_remise_eau → vente   (eau à 5 $, le reste inchangé)
remise_rate   « Le prix est le prix. Le sable, lui, est gratuit : regarde, il y en a partout. » → start

nouvelles « Ce que j'ai vu, ou ce qu'on raconte ? »
  - « Ce que tu as vu. »           → vu
  - « Ce qu'on raconte. »          → raconte
  - « Et Dusk-Town ? »             → dusk
vu      « Au nord, entre la douane et Dusk-Town, une femme avec des lunettes de soudeur fait payer le passage. Quinze dollars. Paie, ou passe par le lit à sec, mais ne discute pas trop : elle a des gamins sur les talus, et un mannequin qui arrête tout le monde. » → nouvelles
raconte « La Station de répartition, au sud, trie des conteneurs que personne ne vient chercher. Les machines d'IO n'ont pas de bras pour te voler, mais elles comptent les visages. Et à la douane ouest, les implants passent ; les autres font demi-tour, ou un détour par en dessous. » → nouvelles
dusk    « On y monte. On y est attendus depuis un mois : une femme du ranch qui boit chez Hector, un gamin qui veut une place à n'importe quel prix. Et des gens qui ne sortent pas le jour. Ceux-là aussi attendent. » → start

panne   « Le ressort arrière. La lame maîtresse a cassé net sur une ornière. Ciro est dessous depuis ce matin. Si tu sais tenir une clé, va le voir. Si tu sais où trouver une lame de ressort, va le voir plus vite. » action flag:car_q_panne → start

recommande (Elle jette un œil vers le puits, puis vers toi.) « Fierro n'envoie jamais personne. Bon. Pour toi, l'eau est à quatre, comme à Dusk-Town. Et si un jour tu dois partir loin sans qu'on te demande tes papiers, cherche la caravane. Demande Remedios, partout où il y a de l'ombre. » action flag:car_remise_ami → start

secret  (Elle pose son crayon.) « Une citerne, ça travaille quand il fait chaud. Le métal. »
  - « Le métal ne frappe pas trois coups. »        → secret2
  - « Si tu le dis. »                               → start
secret2 « … Bon. Écoute. À Dusk-Town, le Service passe et ramasse. Ceux qu'il ramasse, on ne les revoit pas, ou on les revoit en bas, sous Steel. Moi, je transporte des gens qui ne veulent pas être ramassés, dans un sens ou dans l'autre. Ils paient comme ils peuvent. Et toi, tu vas faire quoi de ça ? »
  - « Rien. Je n'ai rien entendu. »                action flag:car_lena_secret;flag:car_remise_ami → client
  - [si race_mutant] « Tu as encore de la place ? »   action flag:car_lena_secret;flag:car_remise_ami → place
  - « Combien vaut mon silence ? »                 test intimider:6, opposed (Volonté 6) → pass racket_ok, fail racket_rate
  - « Le Service paie bien pour ce genre de cargaison. »   → menace
client  « Alors tu es un client. Les clients, je les aime. L'eau est à quatre pour toi. » → start
place   « Pour toi, toujours. Pas aujourd'hui : on monte vers Dusk-Town, et la place est prise. Mais la caravane repasse. » → start
menace  « Le Service paie en balles, comme toujours. Fierro ! » action combat:caravane_relais
racket_ok (Elle compte des billets, lentement, sans te regarder.) « Vingt-cinq. Prends-les, et prends la piste. Et sache une chose : la piste est longue, et Fierro a une très bonne mémoire. »
          action gain:25;flag:car_regle;flag:car_racket;flag:monde_remedios_rackettee → end
racket_rate « Non. Tu n'as pas la tête de quelqu'un qui va jusqu'à la douane pour vendre une gamine. Tu as la tête de quelqu'un qui part. Pars. »
  - « Je pars. »        action flag:car_regle;flag:car_menace → end
  - [Attaquer]          action combat:caravane_relais

merci   « Ciro dit que tu as les mains propres et la tête dure. Chez lui, c'est un compliment. Voilà quinze dollars, et deux bidons pour la route. Et j'ai une autre offre. »
          action gain:15;give:water:2;flag:car_merci → escorte
escorte « On repart dans une heure, vers la douane ouest, puis Dusk-Town. Un fusil de plus sur le toit, ça décourage les péages. Douze dollars à l'arrivée, et la soupe en route. Tu viens ? »
  - « Je viens. »             action flag:car_escorte_dit → escorte_ok
  - « Pas ma direction. »     action flag:car_escorte_dit → escorte_non
escorte_ok  « Fierro te fera une place sur le toit du tracteur. Ne marche pas sur la bâche. » action flag:car_regle;flag:car_escorte;rencontre:quitter:escorte → end
escorte_non « Comme tu veux. On te doit un service. La caravane a de la mémoire, elle aussi. » action flag:car_regle → end
```

### 6.3 Ciro, le mécanicien
- Trente ans, rond, visage noir de graisse, salopette coupée aux genoux, bandana olive. Parle sans arrêt, surtout à la citerne. Sous la remorque, on ne voit que ses jambes et sa caisse à outils.
- Stats : PV 12, PA 6, initiative 6, `barre` (sa clé de 17), mêlée 40 %, armes 15 %, Volonté 4, `fuitTour: 2` (il n'est pas un combattant).
- Sprites : `gen_rc_ciro_dessous` (jambes qui dépassent de sous la citerne, si `!car_repare`) puis `gen_rc_ciro` debout (si `car_repare`). Positions : dessous, pieds en (31,5 ; 13,5) ; debout en (30 ; 14,2).

```text
start   (Deux jambes dépassent de sous la citerne. Une voix sort du dessous.) « Si tu viens pour regarder, il y a de meilleurs spectacles à Steel. Si tu viens pour aider, passe-moi la clé de dix-sept. Non, l'autre. »
  - Passer la clé.                                                 → cle
  - [si mecanique>=4] « Ressort à lames. Lame maîtresse fendue à l'œil, je parie. »   → expert
  - « Bon courage. »                                               → end
cle     « Merci. (Un temps.) La lame maîtresse a cassé. Je peux serrer ce que je veux, sans lame la citerne repose sur l'essieu, et l'essieu ne va pas aimer la piste. » action flag:car_q_lame → besoin
expert  « Enfin quelqu'un qui parle la langue. Oui. Il me faut une lame de la même largeur. Une lame de camion du Service ferait l'affaire : ils roulent sur les mêmes essieux que nous, de vieux essieux de l'UFSA. » action flag:car_q_lame → besoin
besoin  « Le relais avait un atelier, juste à côté. Les ateliers gardent tout. Fouille la ferraille. Une lame de la largeur de ta main, rapporte-la, et la Doña te paiera. Elle pleure en payant, mais elle paie. »
  - [si inv:lame_ressort>=1] « Comme celle-là ? »                  → lame
  - [si inv:cric>=1 & !car_cric] « J'ai un cric de camion, si le tien s'enfonce. »   → cric
  - « Je vais voir. »                                              → end
cric    (Il sort la tête : un visage rond, noir de graisse.) « Un cric à semelle large ! Le mien s'enfonce dans le sable depuis ce matin. Je connais cette soudure : c'est le cric d'Anselme. Prête-le-moi, je te le rends à la fin. » action flag:car_cric → besoin
lame    « Bon acier. Rouillé dehors, sain dedans. Bon. Il faut soulever la citerne pendant que je serre. »
  - [si car_cric] Glisser le cric d'Anselme sous le châssis.       → repare
  - Tenir la citerne à l'épaule.        test force:5 → pass repare, fail repare_mal
  - « Je reviens avec de l'aide. »      → end
repare     (Une heure de jurons et de clés plus tard, la citerne se redresse.) « Elle tiendra jusqu'à Dusk-Town. Après, Dieu et la piste décident. Va voir la Doña, elle te doit quelque chose. »
           action take:lame_ressort;flag:car_repare;flag:monde_remedios_repartie → end
repare_mal (La citerne glisse, retombe sur ta botte, se relève.) « Ça va, ta jambe ? … Elle tiendra. Toi, je ne sais pas. »
           action hurt:2;take:lame_ressort;flag:car_repare;flag:monde_remedios_repartie → end

debout  (si car_repare) « Elle tient. Toi aussi, apparemment. »
  - « Pourquoi des trous sur le dessus de ta citerne ? »   [si car_vu_citerne & !car_vu_lena] → trous
  - « Bonne route. »                                        → end
trous   « Pour que l'eau respire. » (Il ne rit pas de sa propre blague.) « Demande à la Doña. Moi, je répare. » → end
```

### 6.4 Lena, la passagère
- Dix-neuf ans, maigre, cheveux ras sous un foulard olive, chemise trop grande aux manches longues. Mutante : ses avant-bras portent des plaques plus sombres, lisses comme une cicatrice ; elle les cache dès qu'on les regarde [proposition de DA, aucune description canon des mutations]. Calme, ironique, épuisée par neuf jours de citerne.
- **Pas de combat** : elle n'est jamais dans la liste des ennemis. Si le combat éclate, elle reste dans la citerne.
- Sprite : `gen_rc_lena` (à produire) + portrait. Visible seulement si `car_vu_lena` ; position (28,75 ; 14,2), entre la remorque et la citerne, regard vers le joueur.

```text
frapper (examen de la citerne, si car_vu_citerne) (Tu frappes deux coups sur la tôle.)
  - Attendre.            → reponse
  - Laisser tomber.      → end
reponse (Trois coups répondent, de l'intérieur. Puis une trappe grince à l'avant de la citerne.) action flag:car_vu_lena → end   (Lena apparaît)

start   « Ne crie pas. Je sors juste respirer. Il fait cinquante degrés là-dedans. »
  - « Tu voyages comme ça depuis longtemps ? »   → voyage
  - « Où vas-tu ? »                              → but
  - [si race_mutant] « Moi aussi, ils me cherchent. »   → pareil
  - [si inv:water>=1] Lui tendre une eau.        action take:water;flag:car_lena_aidee;flag:car_remise_ami → eau
  - « Retourne te cacher. »                      → end
voyage  « Depuis Novo Córdoba. Neuf jours. On s'habitue. Non, on ne s'habitue pas. » → start
but     « À Dusk-Town. Et après, plus bas que Dusk-Town. Mon père a été pris dans une rafle il y a deux mois. Ceux qu'ils prennent, ils les jettent sous Steel, dans la Sous-Ville. On dit qu'à Dusk-Town, quelqu'un connaît un chemin par en dessous. »
  - « Je connais Dusk-Town. »                    → dusk
  - « Bonne chance. »                            → end
dusk    « Alors dis-moi une chose vraie sur Dusk-Town. »
  - « Personne dans les rues. Tout le monde derrière les murs. »   → dusk_ok
  - « Le Service y passe souvent. Très souvent. »                  → dusk_ok
dusk_ok « Comme moi dans la citerne. Bien. Je saurai me cacher. » action flag:car_lena_aidee → end
pareil  (Elle te regarde, longtemps, puis sourit pour la première fois.) « Alors tu sais. Un conseil, entre nous : si tu passes par la douane ouest, ne passe pas par la douane ouest. » action flag:car_lena_aidee → start
eau     « … Merci. Là-dedans, on boit la même eau que la citerne : aucune. » → start
```

## 7. Manières d'agir et conséquences
| Approche | Comment | Conséquence |
|---|---|---|
| Passer | longer la piste jusqu'à S_E, sans s'arrêter (Fierro interpelle une fois, rien de plus) | reprise du voyage ; la caravane reste en panne (`car_regle` non posé, journal : « vue ») |
| Commercer | acheter ou vendre au comptoir (stock limité) ; carnet du chauffeur et cric d'Anselme reconnus | argent contre eau, rations, armes |
| Troquer, marchander | Troc 5 (palier 4) ; ou par la confiance (Fierro recommande, Lena aidée, secret gardé) | prix réduits (`car_remise`, `car_remise_eau`, `car_remise_ami`) |
| S'informer | Remedios (vu, raconte, Dusk-Town), Fierro (le nord), Lena (la douane) | renseignements : péage de Quilla, Station de répartition, douane ouest, attente à Dusk-Town |
| Réparer (quête courte) | Ciro → ferraille (Mécanique 4 ou Force 6) → lame → soulever (Force 5, ou cric d'Anselme) | 15 $ + 2 eaux ; la caravane repart (`monde_remedios_repartie`) ; offre d'escorte |
| Escorter | accepter l'offre de Remedios après la réparation | sortie avec reprise du trajet, 12 $ à l'arrivée et 3 cases sans tirage de rencontre (extension, §12) |
| Garder le secret | découvrir Lena, ne rien dire, l'aider | eau à 4 $ ; Lena renseignée sur Dusk-Town ; rien de plus (la récompense est la confiance) |
| Rançonner (issue tendue) | menacer de vendre la cargaison au Service : Intimidation contre Volonté 6 | 25 $, `monde_remedios_rackettee` ; échec = on te montre la piste, ou combat |
| Dénoncer | « Le Service paie bien… » | combat immédiat |
| Voler | le coffre sous le comptoir : Discrétion 7 (Remedios à deux pas) | 35 $ et provisions ; échec = combat |
| Combattre | à tout moment | voir §8 |
| Partir | S_O à tout moment ; fuite pendant le combat | halte sur la case |

Drapeaux de scène (préfixe `car_`, purgés à la sortie) : `car_salue`, `car_recommande`, `car_gourde`, `car_gourde_rendue`, `car_fierro_froid`, `car_indice_*`, `car_vu_citerne`, `car_vu_lena`, `car_lena_secret`, `car_lena_aidee`, `car_remise*`, `car_eau1-3`, `car_ration1-2`, `car_poignard`, `car_pistolet`, `car_q_panne`, `car_q_lame`, `car_cric`, `car_repare`, `car_merci`, `car_escorte_dit`, `car_escorte`, `car_racket`, `car_menace`, `car_vole`, `car_regle`, `car_vaincue`, `combat_caravane_relais_<issue>`.

Drapeaux de monde (**pas** de préfixe `car_`, jamais purgés, lus plus tard à Dusk-Town) : `monde_remedios_vue`, `monde_remedios_repartie`, `monde_remedios_rackettee`, `monde_remedios_vaincue`.

## 8. Combat optionnel
Système existant (`src/core/combat.js`, `src/data/combat.js`) avec les extensions du jalon 1 : positions **absolues**, `centre: { x: 22, z: 16.5 }` sans téléporter le joueur, `si` par ennemi, `rendSous`, `fuitTour`. Aucune hauteur : tout le monde est au sol.

| id | Sprite | Position absolue (x ; z) | Case | PV | PA | Init. | Arme | Mêlée / armes | Particularité |
|---|---|---|---|---|---|---|---|---|---|
| fierro | gen_rc_fierro | (13,2 ; 16,8), au pied du puits | libre (terrasse) | 16 | 7 | 7 | fusil | 35 / 60 | couverture 1 (puits, fût) ; le plus dangereux |
| remedios | gen_rc_remedios | (25,5 ; 14,3), devant le comptoir | libre (terrasse) | 12 | 6 | 4 | pistolet | 20 / 40 | couverture 1 (comptoir) ; `rendSous: 0.5` : quand elle se rend, la caravane se rend → **issue victoire** |
| ciro | gen_rc_ciro | (31 ; 14,2), sorti de sous la citerne | libre (terrasse) | 12 | 6 | 6 | barre | 40 / 15 | `fuitTour: 2` |

Pas d'ennemi neutre : Lena n'est jamais dans la liste. Distances à l'entrée (1,5 ; 21) : Fierro 12,4 m, Remedios 24,9 m, Ciro 30,3 m (toutes ≥ 8 m) ; trois positions distinctes, à l'ouest, au centre et à l'est du camp.

Couverture : puits, fût, ballots, bâche, rochers, comptoir, pente du talus = 1 ; tracteur, remorque, citerne, relais = 2.

Issues (format `issues` existant, aucune mort) :
- **victoire** (dont la reddition de Remedios sous 50 % de PV) : la caravane se rend et s'enferme dans la cabine du tracteur ; le coffre et la bâche sont fouillables. `flag:car_regle;flag:car_vaincue;flag:monde_remedios_vaincue`. Texte : « Remedios lève les mains, le crayon toujours entre les doigts. "Prends le coffre. Laisse-nous la citerne." Fierro ne dit rien. Il te regarde, et il retient ton visage. »
- **fuite** : `rencontre:quitter` ; halte sur la case. Texte : « Tu cours. Derrière toi, personne ne te poursuit : une caravane ne quitte pas ses camions. »
- **reddition** (du joueur) : `payMax:15;flag:car_regle`. Texte : « Fierro ramasse tes billets du bout du canon. "Maintenant, la piste." »
- **defaite** : `payMax:15;give:water;flag:car_regle;warp:rc_caravane_relais:1.5:21` + 1 PV (existe). Texte : « Tu te réveilles à l'ombre du panneau. Quelqu'un a laissé un bidon près de ta main. La caravane ne laisse personne sans eau, même ceux qui l'ont attaquée. »

## 9. Objets à fouiller (butin et récompenses)
Objets existants (`ITEMS`, armes du combat, `cric` de Dusk-Town, `carnet_chauffeur` du pilote) sauf mention.

| Où | Condition | Contenu |
|---|---|---|
| Ferraille de l'atelier (10 ; 12,6) | `car_q_lame` ; test Mécanique 4 (« démonter la bonne lame ») ou Force 6 (« arracher le paquet ») ; échec = on peut réessayer avec l'autre test | 1 `lame_ressort` (**nouvel objet**, objet de quête sans valeur marchande) ; sinon : « Des lames trop étroites, des jantes, du sable. » |
| Puits (13,5 ; 15,5) | `observation>=4` | 1 `water` (la gourde de Fierro) + `flag:car_gourde` |
| Coffre sous le comptoir (25,5 ; 13,4) | après victoire : libre ; avant : test Discrétion 7, échec = `combat:caravane_relais` | 35 $, 2 `water`, 2 `ration`, le `pistolet` s'il n'a pas été acheté ; vol réussi : `flag:car_vole` |
| Bâche (29,8 ; 16,2), côté ouest | après victoire | 3 `water` |
| Récompense de la réparation | `car_repare`, en parlant à Remedios | 15 $ + 2 `water` ; puis offre d'escorte (12 $ à la sortie) |
| Rançon | `racket_ok` | 25 $ |

## 10. Clés d'assets : réutilisations et clés nouvelles à produire
**Rien n'est produit avant la vérification du cadrage du jalon 1** (Régie). Même pipeline que le pilote (Mega-Line, caméra du jeu, 50 px/m, même soleil), même manifeste `assets/rencontres/manifest.json`, mêmes champs. Préfixe `rc_car_` pour les éléments propres à la caravane, `rc_ds_` pour les modules du désert réutilisables.

**Réutilisé tel quel** (déjà publié, aucune clé modifiée) :
| Clé | Où | Note |
|---|---|---|
| `g_rc_sable` (+ `_b`, `_c`) | `ground.skin`, terrasse et bas-côtés | |
| `g_rc_piste` (+ `_b`, `_c`) | bande z 18-24 (tuiles à z 18 et 22 : ornières à z 19 et 20,8) | |
| `g_rc_lit` (+ `_b`) | cour de galets du puits, x 8-16, z 12-16 | lit d'un ancien oued |
| `rc_ds_talus_b_3q` | x 0-10 et x 20-30, z 0-8,5 | deux poses non voisines ; l'extrémité ouest coupée tombe au bord de la scène, face cachée |
| `rc_ds_talus_a_3q` | x 10-20 | ses empreintes peintes dans la pente : « Fierro monte guetter à l'aube » (examen facultatif) |
| `rc_ds_talus_fin_3q` | x 30-35 | falaise est au bord de la scène |
| `rc_ds_rochers_3q`, `rc_ds_rochers_b_3q` | bas-côté sud (24 ; 24,3) et (6 ; 24,4) | couvertures 1 dans la zone de combat |
| `rc_ds_panneau_ufsa_3q` | (1,2 ; 17) | le seau à la chaux est un texte d'examen, pas un décalque |
| `rc_emb_bache_cache_3q` | (30 ; 14,5) | bâche de la caravane, bidons bleus |
| `assets/reused/barrel.webp` | (11,7 ; 16,3) | fût vide près du puits |

**Clés nouvelles à produire** (9 décors, 9 sprites de PNJ, 4 portraits) :
| Clé | Rôle | Emprise L × P × H (m) | Notes |
|---|---|---|---|
| `rc_ds_relais_ufsa_3q` | relais routier UFSA en pisé, toit effondré, pompe à carburant rouillée | 7 × 5 × 3,2 | module désert réutilisable ; traits gravés sur la façade sud (petits, lisibles à 50 px/m comme une texture) |
| `rc_ds_puits_3q` | puits sec : margelle de pierre, treuil de bois, seau | 2 × 2 × 2,6 | module désert réutilisable |
| `rc_car_ferraille_3q` | tas de l'atelier : jantes, demi-essieu, paquet de lames de ressort | 3 × 2 × 1,0 | les lames doivent se lire (objet de quête) |
| `rc_car_tracteur_3q` (+ `_texte`) | camion tracteur à cabine avancée, bâché, cabine à l'ouest | 7,5 × 2,6 × 3,3 | portière sud peinte « TRANSPORTES REMEDIOS — NOVO CÓRDOBA · DUSK-TOWN » en calque `_texte` ; bâche rapiécée garance et ocre |
| `rc_car_remorque_etal_3q` | remorque dont le flanc sud rabattu sur chaînes fait comptoir, auvent de toile, coffre sous le comptoir | 6 × 3,2 × 3,0 | marchandise lisible : bidons, rations, outils pendus |
| `rc_car_citerne_3q` | citerne cylindrique sur remorque, **penchée vers l'est** (ressort cassé), trappe à l'avant, rangée de trous sur le dessus | 5,5 × 2,4 × 2,6 | l'inclinaison doit se voir de loin ; trous discrets (indice, pas signal) |
| `rc_car_bivouac_3q` | trois pierres, marmite, tabourets-caisses, fumée mince peinte | 3 × 3 × 1,2 | fumée grise sans halo, foyer visible ; calque `_neon` serré sur les flammes (feu vert de Régie : vraie source, seule lumière de la scène) |
| `rc_car_ballots_3q` (+ `_b`) | ballots de toile et caisses cordées | 2 × 1,2 × 1,2 | `_b` plus bas et plus long |
| `rc_car_traces_3q` | décalque au sol : arcs de pneus, trous de cric, taches d'huile | 9 × 5 | couche sol |
| `gen_rc_remedios` (+ `_dos`) | PNJ + portrait | 1,62 m | châle garance, chapeau de paille, carnet à la ficelle |
| `gen_rc_fierro` (+ `_dos`) | PNJ + portrait | 1,84 m | poncho brun, chapeau plat, fusil long tenu bas |
| `gen_rc_ciro` (+ `_dos`) | PNJ + portrait | 1,70 m | salopette coupée, bandana olive, clé de 17 |
| `gen_rc_ciro_dessous` | jambes qui dépassent de sous la citerne, caisse à outils | 0,35 m de haut, ≈ 1,3 m de long | sprite bas au sol, à produire au pipeline 3D (pas de `y`, pas de miroir) ; seule la partie visible est peinte, le reste est sous la citerne |
| `gen_rc_lena` (+ `_dos`) | PNJ + portrait | 1,66 m | foulard olive, chemise aux manches longues ; plaques sur les avant-bras, sobres |

Nouvel objet : `lame_ressort` (« Lame de ressort », objet de quête, sans valeur marchande).

## 11. Identité du biome (piste sud, reg et talus de grès)
- **Biome** : désert de la piste sud, entre la Douane ouest et la Station de répartition. Reg caillouteux, talus de grès au nord, un ancien oued dont il ne reste que des galets autour d'un puits mort. Moins hostile que le pilote : ici, on s'arrête pour vivre, pas pour piéger.
- **Palette** : base identique au pilote (ocre et sable ambre `#d9b47a` / `#c9a46a`, rouille, bois blanchi, ombres brun chaud). Accents de la caravane, tous terreux : **garance** `#8e4a32` (châle, bâche), **ocre jaune** `#c9963e` (toiles, lettres peintes), **olive** `#6b6a3a` (foulards, bandana), bleu des seuls bidons. Les toiles sont rapiécées de plusieurs teintes, jamais vives.
- **Lumière** : même soleil que le pilote (les modules réutilisés sont peints sous cette lumière ; un autre soleil créerait deux directions d'ombre dans la même scène). L'heure se lit par la vie du camp : marmite qui fume, linge à sécher sur les ridelles. Réglage proposé : celui du pilote, voile divisé par trois comme demandé pour le jalon 1 (`tint` léger ou nul).
- **Sol** : jamais uni. Ornières sur la piste, galets autour du puits, traces de pneus en arc et trous de cric dans le sable de la terrasse.
- **À éviter** : halo sans source (aucune lampe, aucun néon), violet et cyan (réservés à Steel), végétation verte, caravane propre et neuve, trois PNJ alignés devant un comptoir.

## 12. Points d'accroche pour Rivet
1. Catalogue `src/data/rencontres.js` : entrée `caravane_relais` du §14, `prefixe: 'car_'`, `terrains: ['piste']`, `biomes: ['desert']` ; `si` refuse une case réglée **et** refuse si `monde_remedios_vue` (caravane unique) ; taux de `TERRAINS` inchangés.
2. Scène sans `niveaux` : talus en décor plein (pente solide `couv: 1`, plateau inatteignable), tout au sol. Sorties : S_O = halte, S_E = reprise, **jamais gardée**.
3. Visibilité : Lena `si: 'car_vu_lena&!car_vaincue'` ; Ciro dessous `si: '!car_repare&!car_vaincue'`, debout `si: 'car_repare&!car_vaincue'` ; Remedios et Fierro `si: '!car_vaincue'` (après une victoire, ils s'enferment dans la cabine).
4. Fierro : deux entrées de dialogue (`start` par T1, une seule fois ; `encore` si `car_salue`), comme Quilla et son nœud `alerte`.
5. Commerce : `buy:` et `sell:` existants ; stock limité par drapeaux `car_eau1-3`, `car_ration1-2`, `car_poignard`, `car_pistolet` ; prix selon `car_remise_ami` > `car_remise` > `car_remise_eau` > base (plusieurs options à `if` exclusifs, ou une petite fonction de prix si tu préfères).
6. Examen de la citerne : Observation 5, ou 3 si `car_indice_cercles|car_indice_cuilleres` ; ensuite nœud `frapper` (examen à options, comme la fouille à condition du pilote).
7. **Extension « escorte »** (petite, à décider) : `rencontre:quitter:escorte` = sortie avec reprise du trajet + `gain:12` à la sortie + `region.escorte = 3` (les 3 cases suivantes ne tirent pas de rencontre) + `heures += 1`. **Repli** si trop coûteux : `gain:12` puis sortie `reprise` simple.
8. Durée : `duree: 1`, +1 h si `car_repare` (`duree` en fonction de l'état, ou `heures` ajoutées par l'action `repare`).
9. Drapeaux de monde `monde_remedios_*` : hors préfixe, **non purgés** par `retirerLieu`, sauvegardés comme les autres drapeaux. Rien ne les lit encore ; ils serviront à Dusk-Town (Ileana, Teo, Anselme) plus tard.
10. Combat `ENCOUNTERS.caravane_relais` (§8) : centre (22 ; 16,5), `rendSous: 0.5` pour Remedios → victoire, `fuitTour: 2` pour Ciro ; Lena jamais dans la liste.
11. Tests DEV : forcer `caravane_relais` ; scénarios passer, acheter / vendre, marchander, réparer (avec et sans cric), escorter, découvrir Lena et garder le secret, rançonner (réussi, raté), voler, combattre (4 issues), fuir.
12. Nouvel objet : `lame_ressort` dans `ITEMS_RENCONTRES`.

## 13. Décisions de DA et de lore à signaler à Valentin
Rien n'est imposé ; tout est [proposition].
1. **Une filière de passeurs pour mutants (modification de lore importante).** La caravane de Remedios transporte en secret, dans le double fond d'une fausse citerne, des gens que le Service Militarisé ramasse (surtout des mutants), « dans un sens ou dans l'autre ». C'est cohérent avec le canon (rafles du Service à Dusk-Town, mutants abattus ou jetés dans la Sous-Ville) mais cela crée un **réseau** qui n'existe pas encore dans nos docs. À valider, ou à réduire à un cas isolé (Lena seule).
2. **C'est la caravane qu'attend Ileana** (Dusk-Town Q1 : « elle attend une caravane qui ne vient pas ») et celle où Teo veut une place. La rencontre explique le retard (panne, péages) et pose des drapeaux de monde (`monde_remedios_repartie`, `_rackettee`, `_vaincue`) pour que Dusk-Town puisse réagir plus tard (arrivée, ou jamais). Rien n'est câblé à Dusk-Town au jalon 2.
3. **Circuit de la caravane** : Novo Córdoba → Station de répartition → Douane ouest → Dusk-Town. Novo Córdoba est une proposition réutilisable (hors roman) ; je ne décris pas la ville.
4. **Lena** : mutante de Novo Córdoba qui cherche son père, pris dans une rafle et jeté dans la Sous-Ville ; elle a entendu dire qu'un chemin passe « par en dessous » depuis Dusk-Town (cohérent avec ta décision sur l'entrée de Steel par la Sous-Ville). **Apparence mutante** : plaques sombres et lisses sur les avant-bras, sobres ; le roman ne décrit pas les mutations, c'est donc une proposition de DA.
5. **Le relais UFSA** : ancien réseau de relais routiers de l'UFSA, puits mort ; les caravanes y gravent un trait par passage depuis un siècle (un long blanc, puis la reprise). Les petits cercles marquent les passagers clandestins. Lore d'ambiance, sans date.
6. **Faction : aucune.** Remedios, Fierro, Ciro et Lena sont indépendants. Fierro pourrait plus tard devenir un ancien des Los Invictos (lien avec Ileana) ; je ne l'ai pas fait.
7. **Nouveaux noms** : Remedios, Fierro, Ciro, Lena, Benito (le livreur d'Anselme du pilote, enfin nommé). Saveur argentine, comme le pilote.
8. **Clins d'œil au pilote**, sans réutiliser la bande : Remedios et Fierro parlent du péage de « la femme aux lunettes de soudeur » ; Remedios reconnaît le carnet du chauffeur ; Ciro reconnaît le cric d'Anselme (quête de Dusk-Town).
9. **Prix de piste** : eau 6 $ (4 $ à Dusk-Town), ration 8 $, poignard 15 $, pistolet 40 $ ; rachat à environ 40 % ; remises par le troc ou la confiance.
10. **DA** : même soleil que le pilote (cohérence des modules réutilisés) ; accents garance, ocre jaune et olive pour la caravane ; aucune source lumineuse (la fumée de la marmite est peinte avec son foyer, sans halo) ; pas de violet ni de cyan.
11. **Variante pour un joueur mutant** : Fierro le recommande, Remedios lui propose une place, Lena lui donne un conseil sur la douane ouest (drapeau de création `race_mutant` existant).
12. **Caravane unique** : Remedios ne se rencontre qu'une fois par partie (`monde_remedios_vue`). Les autres caravanes du jalon 2 (variantes par biome) auront d'autres équipages.

## 14. Entrée au format d'ARCHI.md §4
Poses définitives après production des sprites (même principe que le §15 du pilote) ; positions ci-dessous en mètres, ancre des décors au coin sud-est de l'emprise.

```js
caravane_relais: {
  nom: 'La citerne qui respire', famille: 'caravane', prefixe: 'car_',
  terrains: ['piste'], biomes: ['desert'], poids: 1, duree: 1,              // +1 h si car_repare (§12.8)
  si: (etat, kase) => !etat.flags.monde_remedios_vue,                        // caravane unique (§12.1)
  arrivee: 'Un camp de caravane, au pied du talus. Une citerne penche, une marmite fume.',
  scene: { size: { w: 35, d: 26 },
    ground: { skin: 'g_rc_sable', tint: null, paint: [ /* bande g_rc_piste z 18-24 (tuiles à z 18 et 22) ; carré g_rc_lit x 8-16, z 12-16 ; variantes _b/_c semées */ ] },
    light: { /* celle du pilote, voile divisé par trois */ },
    buildings: [
      D('car_talus1', 'rc_ds_talus_b_3q', 0, 0, 10, 8.5, { solid: [{ x: 0, z: 5, w: 10, d: 3.5, couv: 1 }, { x: 0, z: 0, w: 10, d: 5, couv: 2 }] }),
      D('car_talus2', 'rc_ds_talus_a_3q', 10, 0, 10, 8.5, { solid: [{ x: 10, z: 5, w: 10, d: 3.5, couv: 1 }, { x: 10, z: 0, w: 10, d: 5, couv: 2 }] }),
      D('car_talus3', 'rc_ds_talus_b_3q', 20, 0, 10, 8.5, { solid: [{ x: 20, z: 5, w: 10, d: 3.5, couv: 1 }, { x: 20, z: 0, w: 10, d: 5, couv: 2 }] }),
      D('car_talus4', 'rc_ds_talus_fin_3q', 30, 0, 5, 8.5, { solid: [{ x: 30, z: 5, w: 5, d: 3.5, couv: 1 }, { x: 30, z: 0, w: 5, d: 5, couv: 2 }] }),
      D('car_relais', 'rc_ds_relais_ufsa_3q', 1, 9.5, 7, 5, { solid: [{ x: 1.3, z: 9.7, w: 6.6, d: 4, couv: 2 }, { x: 6.3, z: 14, w: 0.7, d: 0.5, couv: 1 }] }),
      D('car_ferraille', 'rc_car_ferraille_3q', 8.5, 10, 3, 2, { solid: [{ x: 8.5, z: 10, w: 3, d: 2, couv: 1 }] }),
      D('car_tracteur', 'rc_car_tracteur_3q', 14, 9.5, 7.5, 2.6, { solid: [{ x: 14, z: 9.5, w: 7.5, d: 2.6, couv: 2 }] }),
      D('car_tracteur_texte', 'rc_car_tracteur_3q_texte', 14, 9.5, 7.5, 2.6, { etage: 1 }),          // lettrage de la portière (calque normal, même ancre)
      D('car_remorque', 'rc_car_remorque_etal_3q', 22.5, 9.8, 6, 3.2, { solid: [{ x: 22.5, z: 9.8, w: 6, d: 2.5, couv: 2 }, { x: 22.5, z: 12.3, w: 6, d: 0.7, couv: 1 }] }),
      D('car_citerne', 'rc_car_citerne_3q', 29, 10.5, 5.5, 2.4, { solid: [{ x: 29, z: 10.5, w: 5.5, d: 2.4, couv: 2 }] }),
      D('car_puits', 'rc_ds_puits_3q', 12.5, 13, 2, 2, { solid: [{ x: 12.6, z: 13.1, w: 1.8, d: 1.8, couv: 1 }] }),
      D('car_bivouac', 'rc_car_bivouac_3q', 16, 13.5, 3, 3, { solid: [{ x: 17, z: 14.5, w: 1, d: 1, couv: 0 }] }),   // en buildings pour que son _neon (feu) soit posé
      D('car_bache', 'rc_emb_bache_cache_3q', 30, 14.5, 3.5, 3.5, { solid: [{ x: 30, z: 14.5, w: 3.5, d: 0.5, couv: 1 }, { x: 33, z: 15, w: 0.5, d: 3, couv: 1 }] }),
      D('car_traces', 'rc_car_traces_3q', 21, 13, 9, 5, { fond: true }) ],
    props: [ { sprite: 'rc_car_ballots_3q', x: 20.4, z: 12.4, w: 2, d: 1.2, solid: 1 }, { sprite: 'rc_car_ballots_b_3q', x: 12, z: 9.6, w: 2, d: 1.2, solid: 1 },
             { sprite: 'barrel', x: 11.7, z: 16.3, w: 0.6, d: 0.6, solid: 1 },
             { sprite: 'rc_ds_panneau_ufsa_3q', x: 1.2, z: 17, w: 0.6, d: 0.2, solid: [{ x: 1.4, z: 17, w: 0.2, d: 0.2, couv: 0 }] },
             { sprite: 'rc_ds_rochers_b_3q', x: 6, z: 24.4, w: 3, d: 1.5, solid: 1 }, { sprite: 'rc_ds_rochers_3q', x: 24, z: 24.3, w: 3, d: 1.5, solid: 1 } ],
    entree: { x: 1.5, z: 21, side: 'west' },
    sorties: [ { id: 'ouest', x: 0, z: 21, side: 'west', w: 6, effet: 'halte' },
               { id: 'est', x: 35, z: 21, side: 'east', w: 6, effet: 'reprise' } ] },
  declencheurs: [ { id: 'T1', zone: { x: 7, z: 9, w: 2, d: 15 }, si: '!car_salue', dialogue: 'rc_fierro' },
                  { id: 'pres_citerne', zone: { x: 28.5, z: 12.9, w: 6.5, d: 1.6 }, examen: 'rc_citerne' } ],
  pnj: [ { id: 'rc_fierro', name: 'Fierro', sprite: 'gen_rc_fierro', x: 13.2, z: 16.8, faceTo: [1.5, 21], dialogue: 'rc_fierro', si: '!car_vaincue' },
         { id: 'rc_remedios', name: 'Remedios', sprite: 'gen_rc_remedios', x: 25.5, z: 14.3, faceTo: [1.5, 21], dialogue: 'rc_remedios', si: '!car_vaincue' },
         { id: 'rc_ciro_dessous', name: 'Ciro', sprite: 'gen_rc_ciro_dessous', x: 31.83, z: 13.75, dialogue: 'rc_ciro', si: '!car_repare&!car_vaincue' },
         { id: 'rc_ciro', name: 'Ciro', sprite: 'gen_rc_ciro', x: 30, z: 14.2, faceTo: [25.5, 14.3], dialogue: 'rc_ciro:debout', si: 'car_repare&!car_vaincue' },
         { id: 'rc_lena', name: 'Lena', sprite: 'gen_rc_lena', x: 28.75, z: 14.2, faceTo: [1.5, 21], dialogue: 'rc_lena', si: 'car_vu_lena&!car_vaincue' } ],
  dialogues: { /* §6 : rc_fierro, rc_remedios, rc_ciro, rc_lena */ },
  fouilles: [ { id: 'rc_ferraille', x: 10, z: 12.6, si: 'car_q_lame&!inv:lame_ressort>=1&!car_repare', test: 'mecanique:4', alt: 'force:6', pass: 'give:lame_ressort', fail: 'Des lames trop étroites, des jantes, du sable.' },
              { id: 'rc_gourde', x: 13.5, z: 15.5, si: 'observation>=4', enter: 'give:water;flag:car_gourde' },
              { id: 'rc_coffre', x: 25.5, z: 13.4, si: 'car_vaincue', enter: 'gain:35;give:water:2;give:ration:2;give:pistolet' },   // pistolet seulement si !car_pistolet
              { id: 'rc_coffre_vol', x: 25.5, z: 13.4, si: '!car_regle', test: 'discretion:7', pass: 'gain:35;give:water:2;give:ration:2;flag:car_vole', fail: 'combat:caravane_relais' },
              { id: 'rc_bache', x: 29.8, z: 16.2, si: 'car_vaincue', enter: 'give:water:3' } ],
  examens: [ /* §3 : rc_relais, rc_panneau, rc_puits, rc_ferraille_vue, rc_portiere, rc_bivouac, rc_traces, rc_citerne (→ frapper), rc_bache_vue, rc_comptoir */ ],
  combat: { centre: { x: 22, z: 16.5 },
    ennemis: [ { id: 'fierro', nom: 'Fierro', sprite: 'gen_rc_fierro', x: 13.2, z: 16.8, pv: 16, pa: 7, initiative: 7, arme: 'fusil', competences: { melee: 35, armes: 60 } },
               { id: 'remedios', nom: 'Remedios', sprite: 'gen_rc_remedios', x: 25.5, z: 14.3, pv: 12, pa: 6, initiative: 4, arme: 'pistolet', competences: { melee: 20, armes: 40 }, rendSous: 0.5 },
               { id: 'ciro', nom: 'Ciro', sprite: 'gen_rc_ciro', x: 31, z: 14.2, pv: 12, pa: 6, initiative: 6, arme: 'barre', competences: { melee: 40, armes: 15 }, fuitTour: 2 } ],
    issues: { victoire: 'flag:car_regle;flag:car_vaincue;flag:monde_remedios_vaincue', fuite: 'rencontre:quitter',
              reddition: 'payMax:15;flag:car_regle', defaite: 'payMax:15;give:water;flag:car_regle;warp:rc_caravane_relais:1.5:21' },
    textes: { /* §8 */ } },
}
```
`monde_remedios_vue` est posé à l'arrivée dans la scène (par le gestionnaire, ou par un `enter` d'arrivée), en plus du journal de la case.

## 15. Table des poses pour Rivet (sprites produits le 2026-11-18)
Monde en mètres ; `x, z` = coin nord-ouest de l'emprise, ancre du sprite au coin sud-est au sol (`x + w`, `z + d`) ; `depth` = (x + w) + (z + d), la clé de tri du décor (plus grand = dessiné plus tard). Ordre : 0 sols peints, 1 décalque (`fond: true`), 10-13 talus, puis le décor par `depth` croissant ; les PNJ sont triés par le moteur avec le décor (pied du PNJ). Solides : (x ; z) w×d, `c` = couverture. Aucune hauteur (`y`), aucun `etage` sauf le lettrage du tracteur.

| Clé | x | z | w | d | Solides | Ordre | depth | Type et note |
|---|---|---|---|---|---|---|---|---|
| `rc_car_traces_3q` | 21 | 13 | 9 | 5 | — | 1 | 48 | buildings (fond: true) ; décalque, couche sol, sous tout le reste |
| `rc_ds_talus_b_3q` | 0 | 0 | 10 | 8.5 | (0 ; 5) 10×3.5 c1; (0 ; 0) 10×5 c2 | 10 | 18.5 | buildings ; réutilisé (pilote) |
| `rc_ds_talus_a_3q` | 10 | 0 | 10 | 8.5 | (10 ; 5) 10×3.5 c1; (10 ; 0) 10×5 c2 | 11 | 28.5 | buildings ; réutilisé |
| `rc_ds_talus_b_3q` | 20 | 0 | 10 | 8.5 | (20 ; 5) 10×3.5 c1; (20 ; 0) 10×5 c2 | 12 | 38.5 | buildings ; réutilisé |
| `rc_ds_talus_fin_3q` | 30 | 0 | 5 | 8.5 | (30 ; 5) 5×3.5 c1; (30 ; 0) 5×5 c2 | 13 | 43.5 | buildings ; réutilisé |
| `rc_ds_panneau_ufsa_3q` | 1.2 | 17 | 0.6 | 0.2 | (1.4 ; 17) 0.2×0.2 c0 | 20 | 19 | props ; réutilisé |
| `rc_ds_relais_ufsa_3q` | 1 | 9.5 | 7 | 5 | (1.3 ; 9.7) 6.6×4 c2; (6.3 ; 14) 0.7×0.5 c1 | 21 | 22.5 | buildings ; murs z 9,7-13,7 ; pompe (6,3-7 ; 14-14,5) ; banc non solide |
| `rc_car_ferraille_3q` | 8.5 | 10 | 3 | 2 | (8.5 ; 10) 3×2 c1 | 22 | 23.5 | buildings |
| `rc_car_ballots_b_3q` | 12 | 9.6 | 2 | 1.2 | (12 ; 9.6) 2×1.2 c1 | 23 | 24.8 | props |
| `barrel` | 11.7 | 16.3 | 0.6 | 0.6 | (11.7 ; 16.3) 0.6×0.6 c1 | 24 | 29.2 | props ; réutilisé (base) |
| `rc_ds_puits_3q` | 12.5 | 13 | 2 | 2 | (12.6 ; 13.1) 1.8×1.8 c1 | 25 | 29.5 | buildings |
| `rc_car_tracteur_3q` | 14 | 9.5 | 7.5 | 2.6 | (14 ; 9.5) 7.5×2.6 c2 | 26 | 33.6 | buildings ; cabine à l'ouest ; + rc_car_tracteur_3q_texte en etage: 1 sur la même emprise |
| `rc_ds_rochers_b_3q` | 6 | 24.4 | 3 | 1.5 | (6 ; 24.4) 3×1.5 c1 | 27 | 34.9 | props ; réutilisé |
| `rc_car_bivouac_3q` | 16 | 13.5 | 3 | 3 | (17 ; 14.5) 1×1 c0 | 28 | 35.5 | buildings ; en buildings (et non props) pour que le moteur pose son _neon ; seul le foyer est solide |
| `rc_car_ballots_3q` | 20.4 | 12.4 | 2 | 1.2 | (20.4 ; 12.4) 2×1.2 c1 | 29 | 36 | props |
| `rc_car_remorque_etal_3q` | 22.5 | 9.8 | 6 | 3.2 | (22.5 ; 9.8) 6×2.5 c2; (22.5 ; 12.3) 6×0.7 c1 | 30 | 41.5 | buildings ; comptoir z 12,3-13,0 (couv 1) ; perches de l’auvent en z 12,9-13,0 non solides |
| `rc_car_citerne_3q` | 29 | 10.5 | 5.5 | 2.4 | (29 ; 10.5) 5.5×2.4 c2 | 31 | 47.4 | buildings ; penchée vers l’est ; Ciro dessous au sud (31,5 ; 13,5) |
| `rc_emb_bache_cache_3q` | 30 | 14.5 | 3.5 | 3.5 | (30 ; 14.5) 3.5×0.5 c1; (33 ; 15) 0.5×3 c1 | 32 | 51.5 | buildings ; réutilisé (pilote) |
| `rc_ds_rochers_3q` | 24 | 24.3 | 3 | 1.5 | (24 ; 24.3) 3×1.5 c1 | 33 | 52.8 | props ; réutilisé |

**PNJ** (pivot 0 au milieu des pieds, `vue_dos` au manifeste, miroir horizontal pour l'autre côté) :

| Clé | Pose | Taille (px) | height_m | Dos |
|---|---|---|---|---|
| `gen_rc_fierro` | (13,2 ; 16,8), faceTo (1,5 ; 21) ; combat idem | 194 × 512 | 1,84 | `gen_rc_fierro_dos` |
| `gen_rc_remedios` | (25,5 ; 14,3), faceTo (1,5 ; 21) ; combat idem | 226 × 512 | 1,62 | `gen_rc_remedios_dos` |
| `gen_rc_ciro` | debout (30 ; 14,2), faceTo (25,5 ; 14,3) ; combat (31 ; 14,2) | 244 × 512 | 1,70 | `gen_rc_ciro_dos` |
| `gen_rc_ciro_dessous` | **(31,83 ; 13,75)** : point d'ancrage = bas du sprite ; talons en (31,5 ; 13,27), cuisses sous le châssis ; pas de faceTo, pas de miroir | 132 × 43 | 0.981 (= hauteur px / (50 × cos 28,8°), échelle exacte du décor) | aucun |
| `gen_rc_lena` | (28,75 ; 14,2), faceTo (1,5 ; 21), jamais en combat | 160 × 512 | 1,66 | `gen_rc_lena_dos` |

Portraits 192 × 192 : `portrait-gen_rc_remedios`, `portrait-gen_rc_fierro`, `portrait-gen_rc_ciro`, `portrait-gen_rc_lena`. Icône de `lame_ressort` : `rencontres/icone_lame_ressort_64.webp` (`icon`) et `_128.webp` (`icon128`), même format que `pirate_implant`.

**Calques** : `rc_car_bivouac_3q_neon` (additif, ≈ 35 px de flammes, orange (255,150,60), seule lumière de la scène ; vacillement lent conseillé par `loc.enseignes`) ; `rc_car_tracteur_3q_texte` (calque **normal**, non additif, jamais retourné) : le moteur ne lit `_texte` que sur les véhicules, d'où la pose en `etage: 1` sur l'emprise du tracteur.

**Écarts avec §3 et §10, assumés** : le décalque `rc_car_traces_3q` montre les arcs de pneus et le piétinement devant le comptoir, sans taches d'huile ; les trois trous de cric tombent sous la citerne, donc cachés (le texte d'examen les garde) ; le bivouac montre trois gamelles posées sur les caisses (le texte en compte quatre : la quatrième peut être dans la marmite) ; la citerne est penchée de 2,5° à l'écran (rotation rigide du repeint), assez pour se lire de près, discret de loin.
