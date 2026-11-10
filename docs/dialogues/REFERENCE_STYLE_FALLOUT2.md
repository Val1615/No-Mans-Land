# Référence d'écriture : le style de Fallout 2

Statut : [référence] document de travail, rédigé par Régie le 2026-11-10 à la demande de Valentin.
Destinataire : Ocre, au moment de l'écriture des dialogues de No Man's Land.
Ce document ne fixe aucun canon. Il décrit des techniques de Fallout 2 et montre comment les transposer à NML. Les exemples marqués **[NML]** sont des exemples inventés pour illustrer, pas des textes validés.

## 1. Ce qui fait le ton de Fallout 2

- **Humour noir et sérieux mélangés, sans séparation.** Le jeu passe d'une scène grave à une blague grossière sans prévenir. La rétrospective de TechRaptor note que ce contraste entre maturité et bêtise est présent partout. Le monde est cruel, et les gens y survivent par l'ironie.
- **Le monde regarde le joueur.** Tim Cain explique que le code surveillait ce que faisait le joueur (dialogues, karma, réputation), et que tout cela a nourri les diapositives de fin : « ce jeu te regarde ». Chaque réplique peut savoir ce que le joueur a fait.
- **Des conséquences sans avertissement.** À Vault City, insulter un fonctionnaire fait expulser le joueur pour de bon, sans que le jeu l'annonce. Une autre piste existe toujours ailleurs. On ne prévient pas, mais on ne bloque jamais la partie.
- **Des personnages définis par leur façon de parler.** Sulik parle par phrases courtes, avec ses esprits. Myron est vaniteux et lourd. Torr parle un sabir. On reconnaît chacun en une ligne.
- **Le texte reste court.** Avellone rappelle qu'il y a une limite pratique à la quantité de texte qu'on montre au joueur. Les répliques de Fallout 2 tiennent souvent en une ou deux phrases.

## 2. Les types de dialogue

### 2.1 La description au regard (« Vous voyez... »)
Quand le joueur examine un PNJ ou un objet, une ligne de narration apparaît. Fallout 2 en écrit plusieurs par personnage : une pour le premier regard, puis des variantes qui tournent. Exemple réel, la fiche de Myron (fichier `NhMyron.msg`) : un adolescent au teint pâteux, aux cheveux gras, qui sent vaguement le formol. Les variantes suivantes le montrent qui regarde partout comme un furet, qui renifle, qui s'ennuie, qui bâille.
Règles :
- un détail physique concret et un détail d'attitude ;
- une pointe de jugement du narrateur, sèche ;
- des variantes qui changent selon le contexte (Myron a une description différente quand le joueur est une femme charismatique : il la reluque).

**[NML]** « Vous voyez un douanier en gilet réfléchissant. Son implant clignote orange, comme sa patience. »
**[NML]** « Vous voyez le douanier. Il compte les tickets d'une main et se gratte la nuque de l'autre. »

### 2.2 Les répliques flottantes (barks)
Des phrases au-dessus de la tête, sans fenêtre de dialogue. Fallout 2 les classe par situation : rencontre normale, joueur armé ou intrus, compagnon particulier dans l'équipe (Myron réagit au tribal, au mutant, à la goule), PNJ blessé, PNJ gravement blessé.
Règles :
- très court, cinq à dix mots ;
- plusieurs variantes par situation pour éviter la répétition ;
- réagir à la race, à l'équipement et aux compagnons du joueur.

**[NML]** Un vigile de Pulse Plaza, joueur Mutant : « Reste sur le trottoir, toi. » / « On t'a pas vu entrer. » / « Ça sent le désert ici. »
**[NML]** Le même, joueur Augmenté : « Bonne soirée, monsieur. »

### 2.3 Le dialogue principal à options
Le PNJ parle, le joueur choisit une ligne. Le manuel de Fallout 2 précise que les options dépendent surtout de l'Intelligence, parfois des compétences, et de ce que le joueur a déjà fait ou appris. Une réplique stupide ou déplacée peut fâcher le PNJ ou lancer un combat.
Structure qu'Avellone appelle les points de passage (chokepoints) : un nœud central avec plusieurs questions, chacune revient au nœud, jusqu'à ce que le joueur parte. Cela garde l'arbre lisible pour le joueur et pour l'auteur.
Règles d'Avellone pour chaque PNJ (PC Gamer) :
1. le dialogue a un but (un marchand vend, et vite) ;
2. il connaît l'histoire locale et l'histoire générale (le marchand dit de se dépêcher parce que l'ennemi arrive) ;
3. il connaît les actes du joueur (après la victoire, le marchand fait moitié prix). Sa méthode : une liste de contrôle par personnage, « si, alors, sinon ».

**[NML]** Le kiosquier de Pulse Plaza, avant et après que le joueur a fait tomber l'écran du Feed :
« Des piles, des chips, des faux billets pour le Dôme. Choisis vite, la patrouille passe. »
« C'est toi qui as coupé le Feed ? Prends ce que tu veux. Enfin, presque. »

### 2.4 Les tests de compétence dans le dialogue
Certaines options demandent un jet, le plus souvent la Parole (mentir, convaincre), parfois une autre compétence ou un attribut. Une compétence technique ouvre aussi des réponses spécialisées : un joueur fort en Science obtient plus d'un scientifique.
Chez NML, le format existe déjà avec Ah-Lam (`docs/dialogues/AH_LAM_BARRAGE.md`) : étiquette à crochets, réussite, résultat partiel, échec avec conséquence.
Règles :
- l'option à crochets montre ce que le joueur tente, pas la réussite ;
- l'échec coûte quelque chose (prix plus haut, PNJ méfiant, porte fermée) mais n'arrête pas la partie ;
- le PNJ se souvient de l'essai.

### 2.5 Le dialogue à faible Intelligence
Avec 3 ou moins en Intelligence, le joueur ne fait que grogner et les PNJ ont du mal à le comprendre (manuel). Les PNJ le remarquent, souvent avec cruauté. Sulik conseille au joueur d'aller voir le chaman pour se faire percer un trou dans la tête, un grand trou.
L'exception célèbre est Torr, l'idiot de Klamath : il parle un sabir, avec la traduction claire entre parenthèses. Seul un joueur peu intelligent peut tenir une vraie conversation avec lui et obtenir une quête en plus. Le gag : les deux se comprennent parfaitement.
Règles :
- écrire une branche « faible Intelligence » pour chaque PNJ important, au moins l'accueil et l'adieu ;
- ne pas tout fermer au joueur peu intelligent : lui donner au moins un PNJ et une quête qui lui sont propres ;
- l'humour vise la situation, pas seulement le joueur.

**[NML]** Joueur à faible Intelligence devant le portique de la Mega-Line : « Ticket ? Bip ? » Le portique : « IMPLANT NON DÉTECTÉ. » Le joueur : « Bip pas. »

### 2.6 Les compagnons
Les compagnons ont leurs propres répliques flottantes : en combat, blessés, quand on les laisse attendre, quand ils s'ennuient. Myron se plaint sans arrêt, rate ses répliques, rit quand un ennemi le manque, et supplie qu'on ne le laisse pas seul. Ses phrases servent de commentaire permanent sur le joueur.
Règles :
- une voix immédiatement reconnaissable ;
- des répliques qui jugent les choix du joueur ;
- une réaction quand on le laisse en arrière.

### 2.7 La réputation et les titres
Karma général, réputation par ville et titres gagnés par les actes (Champion, Childkiller, Slaver, Made Man, Gigolo). D'après le wiki Fallout, la première réaction d'un PNJ dépend du Charisme comparé, de la réputation locale et des titres. Les personnages mauvais réagissent à l'envers : ils aiment les titres mauvais.
**[NML]** Équivalents possibles, à décider : réputation par quartier (Center-Town, Lower-Town, Asia-Ground), titres liés aux actes (« Celui qui a coupé le Feed », « Balance de la SMPD »). Les PNJ de Human Corp et ceux de la Sous-Ville réagissent dans des sens opposés.

### 2.8 Les diapositives de fin
Chaque lieu et chaque compagnon important a une diapositive de fin qui raconte ce que les actes du joueur ont produit. Le ton est sec, parfois cruel. Exemple réel : si Myron est encore en vie, il meurt poignardé par un drogué au Jet, moins d'un an plus tard, et personne ne se souvient de son nom.
Règles : quelques phrases au passé, factuelles, avec une chute ironique quand le personnage l'a méritée.

## 3. Règles de rédaction pour NML (synthèse)

1. Une à deux phrases par réplique de PNJ, trois au maximum.
2. Chaque PNJ a une manière de parler qu'on peut résumer en une ligne dans sa fiche (vocabulaire, longueur, tic).
3. Pour chaque PNJ, la liste de contrôle « si, alors, sinon » : race du joueur, quêtes faites, réputation du quartier, compagnons présents, Intelligence.
4. Écrire les descriptions au regard et les répliques flottantes en même temps que le dialogue, pas après.
5. L'humour noir est permis partout, mais une scène grave reste grave dans ses répliques importantes.
6. Les conséquences arrivent sans prévenir, et il existe toujours une autre piste.
7. Pas de vrai nom de Groovy Vibes, jamais.

## 4. Sources consultées

- [Manuel de Fallout 2](https://images.fallout.wiki/7/74/Fallout_2_manual.pdf) (écran de dialogue, Intelligence, tests de Parole).
- [Experimenting With Low Intelligence Dialogue](https://www.gamedeveloper.com/business/experimenting-with-low-intelligence-dialogue), Game Developer (Torr).
- [The future of dialogue in games](https://www.pcgamer.com/the-future-of-dialogue-in-games/), PC Gamer (les trois règles d'Avellone, les points de passage).
- [Chris Avellone on writing game stories](https://80.lv/articles/chris-avellone-on-writing-making-game-stories-engaging), 80.lv.
- [Tim Cain on Fallout reactivity](https://gameworldobserver.com/2022/11/18/tim-cain-fallout-inverview-reactivity-rpg-system-professional-limits), Game World Observer.
- [Design Lesson 101 : Fallout/Fallout 2](https://www.gamedeveloper.com/design/design-lesson-101---em-fallout-fallout-2-em-), Game Developer (Vault City).
- [Fallout 2 Turns 20](https://techraptor.net/gaming/features/fallout-2-turns-20), TechRaptor (humour noir).
- [Myron](https://fallout.wiki/wiki/Myron) et [NhMyron.msg](https://fallout.wiki/wiki/NhMyron.msg), The Fallout Wiki (descriptions, répliques flottantes classées).
- [Reaction](https://www.fallout.wiki/wiki/Reaction), The Fallout Wiki (réaction initiale, titres).
- [Funny Moments in Fallout 2](https://tvtropes.org/pmwiki/pmwiki.php/Funny/Fallout2), TV Tropes (Sulik, Torr).

## 5. Pistes à creuser plus tard
Les fichiers `.msg` complets d'autres PNJ sur The Fallout Wiki (Sulik, Marcus, Vic, l'Ancienne d'Arroyo, les fonctionnaires de Vault City, les familles de New Reno, Frank Horrigan) donnent des modèles pour chaque type de voix : tribal, mafieux, bureaucrate, militaire.
