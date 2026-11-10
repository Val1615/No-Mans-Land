# Référence d'écriture : le style de Fallout 2

Statut : [référence] document de travail, rédigé par Régie le 2026-11-10 à la demande de Valentin.
Destinataire : Ocre, au moment de l'écriture des dialogues de No Man's Land.
Ce document ne fixe aucun canon. Les exemples complets sont en section 6. Il décrit des techniques de Fallout 2 et montre comment les transposer à NML. Les exemples marqués **[NML]** sont des exemples inventés pour illustrer, pas des textes validés.

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

## 6. Exemples

Deux sortes d'exemples dans cette section :
- **[FO2]** : de courtes citations de Fallout 2, en anglais d'origine avec une traduction de travail, tirées des sources de la section 4 ;
- **[NML]** : des scènes écrites dans l'esprit de Fallout 2 pour No Man's Land. Elles servent de modèle de ton. Ce n'est pas du canon : noms, quêtes et lieux sont à valider avant tout usage en jeu.

### 6.1 Description au regard

**[FO2]** Myron (`NhMyron.msg`) :
- *« You see Myron. He's looking around like a ferret. »* (Vous voyez Myron. Il regarde partout comme un furet.)
- *« You see Myron. He looks bored. »* (Vous voyez Myron. Il a l'air de s'ennuyer.)

**[NML]** Une vendeuse de nouilles de Pulse Plaza :
- Premier regard : « Vous voyez une femme d'une soixantaine d'années, tablier taché de sauce, bras de cyborg bas de gamme. Le bras est plus propre que le tablier. »
- Variante : « Vous voyez la vendeuse. Elle remue le bouillon sans le regarder. »
- Variante : « Vous voyez la vendeuse. Elle compte les clients qui ne paient pas. Elle n'a pas besoin de ses doigts. »
- Joueur Mutant : « Vous voyez la vendeuse. Elle vous suit des yeux et pose la main sur sa louche, comme on pose la main sur une arme. »

### 6.2 Répliques flottantes

**[FO2]** Myron selon la situation :
- Normale : *« Thought I smelled something… »* (Il me semblait bien que ça sentait quelque chose…)
- Blessé : *« Is this my blood? »* (C'est mon sang, ça ?) / *« Medic! »* (Médecin !)

**[NML]** Un agent de la SMPD à Center-Town :
- Normale : « Circulez. » / « Implant visible, s'il vous plaît. » / « Belle soirée pour un contrôle. »
- Joueur armé : « Tu ranges ça ou je te le range. »
- Joueur Mutant : « Toi, tu n'as rien à faire ici. » / « On a des cages pour ta taille. »
- Joueur avec le titre « Celui qui a coupé le Feed » : « C'est lui. Appelle le central. »
- Blessé : « Agent à terre ! » / « Ça, c'est dans le rapport. »

### 6.3 Dialogue principal avec nœud central

**[NML]** Le kiosquier de Pulse Plaza.

> Kiosquier : Piles, chips, plans de la Mega-Line. Tout est neuf, sauf ce qui ne l'est pas.
> 1. Qu'est-ce que tu vends, au juste ?
> 2. Il se passe quoi sur la place ?
> 3. Tu connais un moyen de prendre la Mega-Line sans implant ?
> 4. Au revoir.

> (1) Kiosquier : Ce qui se vend. Aujourd'hui, c'est les écouteurs contre le Feed. Demain, ce sera le Feed contre les écouteurs. *(Retour au nœud.)*

> (2) Kiosquier : Concert au Dôme ce soir. Groovy Crew. La moitié de la ville va pleurer devant un écran, l'autre moitié va leur vendre des mouchoirs. *(Retour au nœud.)*

> (3) Kiosquier : Sans implant ? T'es Humain, toi. Ça se voit à ta façon d'avoir l'air perdu. Il y a des gens qui bricolent des puces dans la Sous-Ville. Moi, je t'ai rien dit. *(Drapeau : piste du piratage. Retour au nœud.)*

> (4) Kiosquier : Reviens quand t'auras des crédits. Ou des questions moins chères.

Points à remarquer : le nœud revient après chaque question, une réponse fait avancer une quête, et la réplique (3) change selon la race du joueur.

Variante (3) pour un joueur Augmenté :
> Kiosquier : T'as un implant et tu me demandes comment t'en passer ? Ou bien t'es flic, ou bien t'es pire.

### 6.4 Test de compétence

**[NML]** Le portier du Dôme Fréquence, soir de concert.

> Portier : Liste fermée. Si ton nom n'y est pas, t'existes pas.
> 1. [Parole] Je suis de l'équipe technique. Tron m'attend pour les retours.
> 2. [Intimider] Regarde-moi. Tu veux vraiment que mon nom y soit ?
> 3. [Volonté] *(Attendre sans rien dire, le regarder en face.)*
> 4. Tant pis.

> [Parole] réussite : Portier : L'équipe technique… T'as pas de badge, mais t'as la tête de quelqu'un qui a oublié son badge. Entre.
> [Parole] échec : Portier : Tron n'attend personne. Tron fait attendre. Dégage.
> [Intimider] réussite : Portier : … Ça va. Entrée de service, à gauche. Je t'ai pas vu.
> [Intimider] échec : Portier : Mignon. Les gars, on a un comique. *(Deux vigiles arrivent. Entrée fermée pour la soirée.)*
> [Volonté] réussite : Portier *(après un long silence)* : … T'es bizarre, toi. Entre avant que je change d'avis.
> Retour après échec : Portier : Encore toi ? J'ai une excellente mémoire des visages. Surtout des moches.

### 6.5 Faible Intelligence

**[FO2]** Torr, à Klamath. Il parle un sabir et le sens clair vient entre parenthèses :
> Torr : *Me Torr* (Je suis Torr. Je peux t'aider ?)
> Joueur : *You Torr* (Bonjour Torr. J'ai quelques questions.)

**[FO2]** Sulik, devant un joueur peu intelligent, en substance : la plupart des gens ont de mauvais esprits, toi tu as des esprits stupides, va voir le chaman pour te faire un trou dans la tête, un très grand trou.

**[NML]** Le même kiosquier, avec un joueur à faible Intelligence :
> Kiosquier : Piles, chips, plans de la Mega-Line.
> 1. Chips !
> 2. Train ? *(Montrer la rame du doigt.)*
> 3. *(Partir.)*

> (1) Kiosquier : Bon choix. Le seul que t'aies fait aujourd'hui, j'imagine. *(Vente simple.)*
> (2) Kiosquier : Oui. Train. Tchou-tchou. Il faut un implant. Im-plant. *(Il tapote sa nuque.)* T'en as un ? Non. Bien sûr que non.

**[NML]** Un PNJ qui comprend le joueur peu intelligent, dans l'esprit de Torr : un vieux robot de nettoyage de la Mega-Line, qui ne parle que par codes d'erreur, traduits entre parenthèses.
> Robot : BZZT. ERR-404. *(Je ne trouve pas mon chef. Personne ne me trouve. Tant mieux.)*
> Joueur : Toi perdu ?
> Robot : ERR-200. OK. *(Pas perdu. Oublié. C'est différent, et c'est mieux.)*
> Joueur : Train ? Pas implant.
> Robot : ERR-403… *(Interdit. Mais la porte du local technique ne ferme plus depuis 2091. Je ne l'ai jamais signalé.)*

Seul un joueur à faible Intelligence obtient cette piste. Un joueur normal reçoit seulement les codes d'erreur.

### 6.6 Compagnon

**[NML]** Fusible, si on l'emmène :
- Il s'ennuie : « On fait quelque chose, ou on regarde les néons jusqu'à ce qu'ils grillent ? »
- En combat, coup raté contre lui : « Raté ! Raté ! Fais-le encore pour voir… non, en fait, non. »
- Blessé : « J'ai une fuite. Une fuite de moi. »
- On le laisse attendre : « Ici ? Tout seul ? Près des poubelles ? Super. Je vais me faire des amis. »
- Le joueur ment à un PNJ : « T'as menti tellement bien que j'y ai cru, et j'étais là. »

### 6.7 Réputation et titres

**[NML]** Le même vigile de Human Corp, selon la réputation du joueur à Center-Town :
- Réputation haute : « Ah, vous. La direction parle de vous. En bien. Ça m'inquiète un peu. »
- Neutre : « Badge. »
- Basse : « Ton visage est sur notre liste. Pas la bonne liste. »
- Titre « Balance de la SMPD », PNJ de la Sous-Ville : « Les murs ont des oreilles. Toi, t'es une oreille avec des jambes. »

### 6.8 Diapositive de fin

**[FO2]** Myron, en substance : poignardé par un drogué au Jet dans un bar du Den, moins d'un an après la chute de l'Enclave ; sa découverte est vite oubliée, et personne ne se souvient de son nom.

**[NML]** Deux fins pour le kiosquier de Pulse Plaza :
- Si le joueur a coupé le Feed : « Sans le Feed, Pulse Plaza a découvert le silence. Le kiosquier a vendu des écouteurs pour ne pas l'entendre. Il a fait fortune en trois semaines, puis le Feed est revenu. »
- Sinon : « Le kiosquier a continué de vendre des piles, des chips et des plans de la Mega-Line. Il n'a jamais pris la ligne. Il disait qu'il connaissait déjà le terminus. »
