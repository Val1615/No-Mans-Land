# Écriture des dialogues de No Man’s Land

La Bible maîtresse de Sylvinia VN et Chroniques Alternatives V1.1 fournit les principes d’écriture de cette passe. Ses personnages, sa cosmologie et ses scènes ne sont pas transposés dans No Man’s Land. Le roman de No Man’s Land fournit les repères de la cité ; les quêtes et habitants de cette aventure de 2175 sont des créations dérivées.

## Principes appliqués

Un échange part d’une activité ou d’un problème présent. Le PNJ a une raison de répondre, de demander une précision, de faire attendre ou de refuser. Une information importante doit avoir une source, une date, une fiabilité et un intérêt dans la scène. Une réputation ou un drapeau global ne donne pas à chacun la connaissance du parcours du joueur.

Les gestes ne sont pas expliqués une seconde fois. Les silences et les interruptions peuvent déplacer l’échange. Les réponses du joueur portent sur une demande, une action ou une objection ; il ne diagnostique pas le caractère de son interlocuteur. L’humour dépend de la personne et de la situation. La formulation ne repose pas sur une suite de fausses oppositions, de slogans ou de métaphores professionnelles.

## Voix et connaissances

| Personnage | Manière de parler | Ce qui fonde ses informations |
| --- | --- | --- |
| Mara | Pragmatique, préoccupée par la distribution et les habitants | Diagnostic local, réserves, nouvelles reçues à Dusk-Town |
| Vera | Directe, protectrice, occupée ; humour sec ponctuel | Examens, soins, stocks de sa clinique |
| Nilo | Technique, hésitant à partir, se reprend dans l’action | Machines qu’il a réparées et documents de maintenance |
| Vidal | Formel, peu bavard, traite une vérification à la fois | Contrôle d’identité, documents de transit |
| Ada | Courtoise, précise sur les engagements, garde ses réserves | Dossiers IO qu’elle consulte ; pas les conversations privées du joueur |
| Luz | Fatiguée, concrète, phrases simples | Son ancien poste, son bras, son exclusion |
| Salma | Sobre, attentive au risque pour ses collègues | Quantités vues, relevés copiés et témoignages de l’atelier |
| Tomás | Méfiant, écoute avant de confier, souci des proches | Archives locales et messages de son réseau |
| Roque | Affable, adapte sa vente, escamote les défauts | Ses marchandises et les transactions du bazar |
| Alma | Froide, méthodique, oblige à préciser la contestation | Contrats, calculs et règlements |
| Otero | Excédé, concret, urgence du danger proche | Son installation autour du Titan |
| Ardo | Humour noir limité par sa fatigue | Son traitement et ses expériences personnelles |
| Cora | Lassée, économise ses mots, agit pour les locataires | État des logements et prélèvements transmis au recours |
| Eva | Précise, distingue la copie, l’absence et la preuve | Registre de son service et pièces apportées |
| Sen | Mesurée, clinique, insiste sur l’usage du matériel | Patients suivis, références et commandes médicales |
| Leal | Une question à la fois ; accepte un temps d’attente | Entrées de garde, rapprochement des heures et justificatifs |
| Rita | Sarcasme quotidien, attention aux passagers | Trajets, contrôles et clients de sa voiture |
| Elías | Patient et rassurant, attentif aux quais | État de sa ligne et confirmations des stations |
| Bérénice | Exigeante, juge l’entretien avant le prix | Coupe, tissus et équipement qu’elle vend |
| Maëlle | Calme, précise sans faire de discours politique | Plantes et lieux qu’elle entretient |
| Valen | Formel, limité à son service | Références de dossiers et consignes de l’atrium |

## Répartition du texte

- `dist/voices.js` : introductions situationnelles et échanges supplémentaires, avec de véritables relances.
- `dist/engine.js` : choix de quête existants, conditions et réponses aux actions. Les anciennes introductions redondantes ont été retirées.
- `dist/city-play.js` : dialogues des nouveaux habitants et résolution des affaires urbaines.
- `dist/city-data.js` : descriptions de lieux, documents et objets inspectables.

Mara possède quatre retours distincts après la décision hydraulique. Les variantes partent de ce qu’elle constate à Dusk-Town : remplissage, recensement, réserves encore limitées ou recherche d’un captage autonome.


## Passe 0.6 : habitants et affaires des secteurs agrandis

Les 45 nouveaux habitants ont un accueil lié à leur activité et un sujet personnel. Les descriptions physiques ne répètent pas leur dialogue. Les personnes qui tiennent les comptes (Nadia, Rocío, Sergio, Vesta) ne donnent pas une connaissance globale du monde : le joueur doit consulter leurs pièces sur place. Candela exige deux relevés avant le partage de la citerne ; Ramos examine les volumes et le titre de réquisition ; Alder attend la preuve d’un usage récent de l’atelier.

Esmé se concentre sur les patients et le transport. Vico décrit une panne et une pièce précise. Mila cherche une séance différente, Renzo travaille sur la machine. Silas réclame un lot complet et Noémi défend sa marge. Bruna défend un accès mesurable aux réserves. Les réponses restent attachées à ces préoccupations, avec des traits d’humour espacés ; aucune référence de pop culture n’est annoncée par un nom d’œuvre ou de personnage.

## Habitants de Dusk-Town — 0.7

Elvira parle des chambres et des réparations qu’elle doit gérer, avec une ironie sèche. Beto plaisante sur sa marchandise sans monopoliser la conversation. Elisa donne des consignes directes sur la vie des cours. Raúl n’invente aucune information sur le site qu’il garde. Ofelia raisonne en trajets et en bons de réception. Leurs répliques se rapportent aux objets et aux tâches présents dans leurs quartiers. Les informations du codex représentent le contexte de création ; elles ne deviennent pas automatiquement des connaissances des PNJ. Les dernières conversations sont datées dans le journal.
