# Quête test : « La porte d'acier » (Dusk-Town, 2175)

Statut : **proposition** à relire avec Valentin, sauf les points marqués [canon].
Fin imposée par Valentin : le joueur force l'accès scellé du labo, une voix étrange se fait entendre, un homme coincé derrière la porte demande d'aller à Steel-Megalopolis. **La porte ne s'ouvre pas.**

## Canon relu (roman, Ch. I) et ce qu'on en garde
| Fait | Source | Usage |
|---|---|---|
| Un ancien labo Human Corporation est sous Dusk-Town, l'accès est verrouillé, beaucoup tentent de forcer les portes scellées, en vain | Ch. I §75 | [canon] cœur de la quête |
| Quand des bandes de récupérateurs se croisent : bains de sang | Ch. I §77 | [canon] Ezequiel en parle |
| Labo = centre de cryogénisation expérimental ; liaison avec les serveurs HC coupée ; messages préenregistrés « Attention… confinement… » ; générateur faible | Prélude | [canon] : seul l'écho d'un message de confinement grésillant est repris, **rien d'autre n'est révélé** (pas de mot « cryogénie », pas de date, pas de nombre de sujets) |
| En 2202 (roman) Luis Flores sort seul, toutes les autres capsules sont vides | Prélude, §288 | Compatibilité : en 2175 un homme répond encore ; en 2202 il n'y a plus personne. Rien ne contredit. |
| Soldats du Service Militarisé de Steel-Megalopolis passent par Dusk-Town | Ch. I §61-69 | [canon] patrouille à éviter |
| Steel-Megalopolis capitale d'IO, crédit ; dollar ailleurs | CANON_ARBITRAGES §8-9 | [canon] tout se paie en $ |

## Propositions (non canon)
- L'homme derrière la porte : **non nommé** (« Ça n'a plus d'importance, mon nom »). Ni son rôle (personnel ou sujet), ni comment il a tenu ne sont dits. [proposition]
- Une grille d'interphone au-dessus de la porte ; le battant gauche bouge d'un doigt au cric ; quand la porte bouge, sa ventilation s'arrête. [proposition]
- Il envoie le joueur à Steel-Megalopolis « où l'on sait ouvrir ce qui est fermé ». Il ne dit pas à qui s'adresser. [proposition]
- Le cric d'Anselme, le signal au miroir de Teo, la vraie version d'Ezequiel. [proposition]

## Déroulé
Prérequis existant (v7) : Teo, au guet du Transit, vend pour 5 $ le chemin de l'atelier (Ezequiel).

1. **Ceux qui ont tenté la porte** (Ezequiel, l'atelier, Le Scellé). Nouvelle option : « Ceux qui ont tenté la porte, tu les connais ? ». Il raconte, puis comment il a essayé lui-même.
   - Si le joueur connaît déjà le secret de sa jambe (drapeau `ezequiel_toit`), il dit la vérité : la grille du toit est un leurre, seul le bas du battant gauche bouge → drapeau `q_battant` (ligne en plus dans la scène finale).
   - Sinon il ment (« au cric, à sept, une bande est arrivée »), mais l'information utile est la même.
   - Il envoie chez Anselme (cric) et chez Teo (le moment). → `q_start`.
2. **De quoi forcer** (Anselme, l'épicerie, La Pompe). **Choix** :
   - payer 15 $ → `q_cric`;
   - mentir (« c'est pour la pompe de Mara ») → 5 $, `q_cric` + `q_menti_anselme`. Conséquence visible : Anselme accueille ensuite le joueur autrement (« Mara n'a jamais entendu parler de mon cric… ») ;
   - refuser.
3. **Le bon moment** (Teo, le guet, Le Transit). **Choix** :
   - payer 5 $ → `q_signal` ;
   - si on connaît le secret d'Ezequiel : le vendre à Teo à la place → `q_signal` + `q_trahi`. Conséquence visible : Ezequiel accueille ensuite le joueur autrement (Teo imite un chat qui tombe quand il passe) ;
   - plus tard.
4. **La porte d'acier** (Le Scellé). Tap sur l'accès HC :
   - sans la quête : texte v7 (marques de pied-de-biche) ;
   - quête lancée mais pas prêt : « Pas à mains nues, et pas sans savoir où sont les camions. » ;
   - cric + signal : le joueur marche jusqu'au pied de la porte, scène finale (ci-dessous). Fin → `q_fin`.
5. **Aller à Steel-Megalopolis** : objectif ajouté, marqué « hors de portée pour l'instant : la route n'existe pas encore ». Non atteignable.

## Scène finale (textes)
- « Au loin, un seul éclat de miroir : la route est vide. Le cric tient tout juste sous le bas du battant. »
- Pomper : « Le cric grince. Le battant gémit, bouge d'un doigt, puis plus rien. »
- Pomper encore : « Un claquement sec à l'intérieur. Puis un grésillement, au-dessus de la porte, dans une grille que tu avais prise pour de la rouille. Une voix coupée en morceaux : « …ttention… confinement… ». Le message boucle, se tord, s'arrête. »
- (Frapper : trois coups répondent, plus faibles, puis quelqu'un respire dans la grille.)
- La voix : « Ne tire plus sur la porte. S'il te plaît. Chaque fois qu'elle bouge, l'air s'arrête. » … « Tu es vivant, toi ? Vraiment vivant ? »
- « Ça n'a plus d'importance, mon nom. Ça a mal tourné, ici. Très mal. On attendait quelqu'un d'en haut. Personne n'est descendu. »
- « Je suis le seul à répondre. Les autres sont là, je les vois d'ici. Ils ne réclament plus rien. C'est la seule qualité qui leur reste. »
- « Non. Pas avec ça. Cette porte s'ouvre d'ici, et d'ici je n'ai plus la main. » … « Steel-Megalopolis. Va à Steel-Megalopolis. Là-bas ils savent ouvrir ce qui est fermé. Dis-leur que quelqu'un répond encore sous Dusk-Town. »
- Fin : « Le grésillement se coupe. Le cric glisse, le battant retombe à sa place. La porte reste fermée. »

## Système
- Drapeaux dans `state.flags` (état partagé du jeu) ; conditions d'options `a&!b`, variantes de texte `alt`, actions multiples `a;b`, `pay:N`.
- Journal (J) : section « Quêtes » avec étapes cochées, objectif courant ; objectif courant rappelé sous le nom du lieu (HUD).
