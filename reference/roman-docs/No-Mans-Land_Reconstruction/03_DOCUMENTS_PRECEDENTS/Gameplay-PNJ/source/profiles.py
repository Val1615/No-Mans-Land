"""Compléments de jeu proposés pour les personnes existantes."""
PROFILES={}
def npc(id,voix,motif,routine,reaction):
    PROFILES[id]=dict(voix=voix,motif=motif,routine=routine,reaction=reaction)

# Dusk et ferme
npc('mara','Pragmatique, préoccupée ; demande des quantités et une prochaine action.',
 'Maintenir la distribution sans promettre plus que la citerne ne contient.',
 'DT01 B01 à 06 h pour le niveau ; tournée des logements ; réunion à DT02 B05 après distribution. Repos à proximité de la pompe, garde prévenue.',
 'Observe les débits et reçoit les nouvelles des arrivages. En alerte, organise les cours refuges. Commente la décision hydraulique à partir de ses effets locaux.')
npc('vera','Questions brèves, consignes concrètes ; humour sec quand le patient peut l’entendre.',
 'Stabiliser les urgences et former Pía sans lui faire dépasser ses compétences.',
 'DT01 B02 : visite matinale, consultations, pansements et transmissions. Pause en relais avec Pía ; personne de garde indiquée la nuit.',
 'Ne quitte pas un patient pour une conversation. Met les autres à couvert en cas de tirs. Connaît ses diagnostics et stocks, pas les secrets du temple.')
npc('ezequiel','Amabilité commerciale ; se souvient des commandes et surveille les mains.',
 'Livrer une marchandise correcte, garder sa marge et rentrer avec son équipement.',
 'DT01 B05 les jours de marché ; chargement au dépôt DT03 B02. CR 01 vers Granja ; CR 02 seulement aux départs inscrits. Chambre louée quand il attend.',
 'Ferme l’étal s’il voyage ; une note donne le retour prévu. Replie sa toile en alerte. Ses nouvelles ont une étape et une date, jamais une précision omnisciente.')
npc('nilo','Se reprend, vérifie ce qu’il vient d’affirmer ; plus assuré devant un mécanisme.',
 'Réparer utilement sans revivre l’accident évité au monte-charge de son ancien poste.',
 'DT03 B01 puis pompe DT01 B01 et clinique B02 sur demande. Dort à DT03 B08. Recruté : retire sa présence locale et prépare une relève.',
 'Sécurise une machine avant de fuir. Suit les règles complètes du chapitre compagnons à terme. Sait ce qu’il a démonté ou lu ; un exosquelette ne garantit pas un ISIO.')
npc('inesguard','Rappel calme des usages ; observe avant de menacer.',
 'Garder les maisons tranquilles et repérer ceux qui suivent un convoi.',
 'DT01 B06 → hôtel B04 → pompe B01 → poste, avec arrêts de surveillance. Relève à 06 h et 18 h ; garde de nuit distincte, pas deux copies.',
 'En alerte, tient un passage et appelle la relève ; ne charge pas seule un groupe armé. Ignore l’intérieur des sous-sols scellés Human Corporation.')
npc('nadia','Accueillante mais attentive à la propreté ; ses plaisanteries viennent des factures.',
 'Nourrir le quartier en gardant des portions pour ceux qui ne peuvent pas faire la file.',
 'DT02 B01 dès 05 h ; réception à DT03 B02 sur rendez-vous ; service à DT02 B05 ; comptes après le repas et repos dans les logements proches.',
 'Montre le reçu réel de Dusk dans l’affaire de la citerne. Réduit un menu plutôt que d’inventer une réserve. En danger, ferme la cuisine après avoir coupé le feu.')
npc('abel','Parle quand il a fini le geste en cours ; peu enclin aux grands discours.',
 'Rendre les portes et fenêtres habitables avec le bois disponible.',
 'DT02 B03 : préparation ; chantier assigné dans les logements B02/B04/B06 ; retourne à l’atelier et range ses outils avant la nuit.',
 'Étaye une entrée si l’alerte le permet, puis rejoint la cour. Connaît les logements où il travaille ; aucune expertise automatique sur les blindages du Titan.')
npc('patient','Ardo plaisante sur sa convalescence, puis fatigue vite.',
 'Retrouver assez d’autonomie pour ne plus dépendre du brancard.',
 'DT01 B02, chambre ; marche au banc devant la clinique seulement après avis de Vera. Le soir, retour accompagné. Aucun circuit de travail pendant les soins.',
 'Une alerte interrompt la promenade ; Pía le reconduit. Témoigne de son traitement, pas du diagnostic des autres. Ne devient pas dément à cause d’un dialogue de travers.')
npc('paz','Pía annonce ce qu’elle sait faire et quand elle doit appeler Vera.',
 'Devenir une soignante fiable sans cacher une erreur.',
 'DT01 B02 : linge, accueil, pansements autorisés ; brève sortie vers la laverie DT02 B08 par le passage public. Repos en relais, garde affichée.',
 'Triage et stabilisation simples ; les cas graves vont à Vera. Sous les tirs, aide les personnes qui marchent mal. Ne révèle pas les dossiers médicaux aux curieux.')
npc('ines','Inés corrige d’abord le geste qui abîme un rang ; chaleureuse une fois le risque écarté.',
 'Sauver la récolte actuelle et garder de quoi recommencer.',
 'AN01 B07 irrigation à l’aube ; serres B01–B03 ; tri B04 ; repas et repos B06. Départs de récolte avec Iris au contrôle des semences.',
 'En manque d’eau, choisit les rangs à préserver et demande une aide chiffrée. Protège les gens avant les bacs sous une attaque. Connaît ses clients par leurs livraisons.')
npc('irisfarm','Précise sur l’hygiène ; soupçonne les semelles avant les intentions.',
 'Conserver un stock de graines sain au-delà de la prochaine récolte.',
 'AN01 B05 : inventaire à l’ouverture ; tournée des bacs avec Inés ; préparation des sachets au tri B04 ; stockage fermé le soir.',
 'Isole un lot suspect, fournit un échantillon et interdit sa vente jusqu’au contrôle. Ne confond pas radioactivité, maladie végétale et mutation d’un habitant.')

# Périmètre de Steel
npc('vidal','Formel, une vérification à la fois ; ne développe pas une doctrine politique.',
 'Éviter une admission irrégulière dont il porterait la signature.',
 'SM01 B01 contrôle ; passages à B08 administration et pauses au local personnel autorisé. Quitte le guichet à la relève, remplacé par un agent de service.',
 'Examine documents et statut individuel du compagnon. En alerte, ferme le sas civil et appelle le poste armé. Ne sait pas ce qu’Ada a dit sans dossier reçu.')
npc('luz','Fatiguée, phrases simples ; revient aux objets qu’elle a laissés au dortoir.',
 'Retrouver son lit et une solution pour son bras défaillant.',
 'Avant admission : attente SM01 B04. Après décision : trajet accompagné vers SM08 B08, puis soins à B07. Pas de double présence dans les deux plans.',
 'Évite un contrôle agressif et demande de l’aide avant une charge lourde. Connaît son ancien poste ; ne révèle pas Sine Vincula parce qu’elle vit dans la même travée.')
npc('mirek','Râle sur les délais avec des détails très matériels.',
 'Terminer la livraison avant que le client lui fasse payer l’attente.',
 'SM01 B02 avec le véhicule ; repos B07 après mise en sécurité ; contrôle puis départ vers l’aire de fret, jamais promenade dans une caserne.',
 'Peut montrer ses sacs ouverts et son ordre de transport. Un retard de formulaire ne l’amène pas à forcer une barrière militaire. Dernière position connue liée au départ.')
npc('north-agent','Rivas est directe, précise la pièce manquante sans tenir un discours.',
 'Faire passer les véhicules conformes tout en gardant une trace des scellés.',
 'SM02 B01 → B02 pour inspection litigieuse → B03 scellés. Contrôle continu par relais ; repos hors du guichet à heure annoncée.',
 'Compare nouvelle pesée et document avant de libérer Aro. En attaque, protège le sas puis transmet au poste nord. Ne décide pas seule de la politique d’Upper-Town.')
npc('reina','Fait déplacer les roues et couper le moteur ; ironie rare sur les certificats.',
 'Obtenir une mesure dont elle peut expliquer l’écart.',
 'SM02 aire de pesée et B07 atelier balances ; contrôle des masses au début du service, résultats remis à B03. Pause quand le plateau est libre.',
 'Suspend une mesure dangereuse, pas toute la douane. Donne tare, charge et heure séparément. Ne transforme pas un écart de poids en preuve de contrebande sans inspection.')
npc('east-agent','Paz garde le trafic en mouvement ; répond entre deux contrôles.',
 'Faire correspondre lot, propriétaire et autorisation.',
 'SM03 B01 puis B02 hall des lots ; litiges vers B03. Consignes de fermeture transmises au poste B06, repos après relève.',
 'Arrête le seul chargement litigieux. Une livraison Protectores est contrôlée, pas forcément saisie. Connaît les anomalies enregistrées, pas la totalité du marché noir.')
npc('dario','Darío prévient avant de faire signer ; connaît le prix d’une politesse mal placée.',
 'Livrer les lots sans hériter d’un supplément ou d’un destinataire fantôme.',
 'SM03 B02 emballage ; B03 litiges si le bon change ; B07 transport pour le départ. Rejoint l’équipe de fret après fermeture.',
 'Ne signe pas pour le joueur. En alerte, laisse le colis scellé sous garde. Ses liens Protectores n’impliquent pas la connaissance des contrats privés d’Alma.')
npc('avel','Compare référence et commande avant de répondre ; ton professionnel sans raideur forcée.',
 'Expédier le bon lot et faire reconnaître les délais de son service.',
 'SM04 B02 expéditions ; validation B07 ; réception des essais B03. Tour de chargement puis clôture des bons, pause B06 en relais.',
 'Gèle un lot au froid si l’alimentation tombe, appelle Delta et avertit le destinataire connu. Ne sait pas à qui le joueur remettra clandestinement une pièce après sortie.')
npc('delta','Énumère ses mesures ; coupe court quand on gêne le banc.',
 'Ne pas laisser partir une pompe qu’elle sait défaillante.',
 'SM04 B03 métrologie → B01 essai d’assemblage → B02 validation d’expédition. Coupe et consigne avant intervention ; repas B06.',
 'Refuse de cocher une valeur qu’elle n’a pas testée. Peut contester une référence de rebut avec un relevé. Sous attaque, sécurise d’abord l’essai en cours puis évacue.')
npc('north-officer','Sanz pose clairement la limite du service public.',
 'Garder la liaison accessible sans exposer le casernement.',
 'SM05 B01 accueil ; briefing B03 ; tour autorisé vers B07 avec garde. Remise des prestataires à l’accueil, pas à l’arsenal.',
 'Ordre d’alerte reçu par radio ; mission locale, escorte mesurée. Ne connaît pas les objectifs secrets des Dusk Forces et n’en donne pas la liste au premier visiteur.')
npc('pavel','Suspend sa réponse pour écouter un appel ; demande de répéter une fréquence.',
 'Savoir quel véhicule appelle et si l’information est encore utile.',
 'SM05 B03 communications ; contrôle des balises avec l’atelier B04 ; relève radio conservant le journal des messages.',
 'Un retard de balise reste un retard jusqu’à vérification. Communique l’heure de réception et le statut de détresse. Ne raconte pas un assaut auquel il n’a reçu aucun rapport.')
npc('east-officer','Baeza répond en regardant la carte des convois ; accepte une aide définie.',
 'Maintenir les capteurs de la route et éviter une patrouille envoyée à l’aveugle.',
 'SM06 B01 liaison → B02 radio → B08 antennes avec un technicien ; briefing au départ du convoi et retour au bureau.',
 'Détache une équipe seulement sur un incident confirmé. Les prestataires travaillent sur un appareil déterminé, sans accès libre aux autres secteurs militaires.')
npc('cielo','Explique ce qui attend quoi ; sarcasme concret sur les autorisations.',
 'Remettre le véhicule en état sans montage dangereux.',
 'SM06 B03 et B04 garages ; pièces à l’atelier B08 ; repos dans le secteur du personnel. Essai de roulage sur aire balisée.',
 'Attend la consignation du véhicule, puis peut montrer les références nécessaires. Alerte carburant : interrompt la réparation et rejoint le point prévu, outils laissés sûrs.')
npc('south-officer','Ferreyra donne une destination, une restriction et le prochain contact.',
 'Faire circuler le ravitaillement sud sans dégarnir le poste.',
 'SM07 B03 liaison ; contrôle parc B06 ; retour au poste avant chaque départ. Transmission de relève explicite.',
 'Annonce jusqu’où la route est confirmée. Ferme une aire touchée, pas tous les échanges régionaux. Un refus de mission n’est pas une désertion du joueur civil.')
npc('grisel','Brève quand les véhicules manœuvrent ; attentive aux départs difficiles.',
 'Faire rouler ce qui peut arriver à destination et immobiliser le reste.',
 'SM07 B06 parc → B02 atelier → B01 dépôt selon ordre de chargement. Clôture des départs avant repos.',
 'Donne état mécanique et heure de départ, pas une garantie absolue de route. En alerte, écarte les piétons des manœuvres et réserve un véhicule d’évacuation.')

# Steel intérieur
npc('salma','Sobre, laisse un silence lorsqu’un nom met quelqu’un en danger.',
 'Obtenir soins et eau pour ses collègues sans exposer tout son réseau.',
 'SM08 B01 atelier ; B04 cantine après relève ; B07 pour les cas médicaux. Rendez-vous clandestin bref, séparé du lieu de vie.',
 'Privilégie la mise à l’abri et la sauvegarde des preuves. Vérifie la source avant de citer un autre atelier. Ne présente pas chaque résident au réseau Sine Vincula.')
npc('inspector','H-6 demande référence et périmètre de contestation ; refuse les généralités.',
 'Maintenir un audit défendable et limiter ce qui circule hors de son service.',
 'SM08 arrivée par B10 monte-charge → B11 inspection → poste contrôlé. Aucune entrée par le passage clandestin B09.',
 'Saisit une copie seulement par une procédure ou une action visible. Un incident lui parvient par rapport. Ne sait pas qu’un document a été vendu avant confirmation.')
npc('enid','Écarte la mauvaise pièce du geste avant de l’expliquer.',
 'Désengorger le tri sans livrer du matériel réellement défectueux.',
 'SM08 B05 tri ; dépôt du relevé à B01 ; repas B04. Les lots refusés restent séparés et identifiés.',
 'Montre numéros et défaut observé. Ne détruit pas un lot pour gagner une dispute. Coupe la bande en cas d’accident et avertit Salma sans supposer un sabotage.')
npc('ada','Courtoise ; distingue ce qu’elle signe, transmet et ne peut pas modifier.',
 'Obtenir un contrat applicable et conserver la confiance professionnelle de son service.',
 'SM09 B01 bureau ; rendez-vous au Forum ; consultations programmées à SM18 B02 seulement si le dossier le justifie. Repas discret puis départ annoncé.',
 'Vérifie les données reçues. Réagit à une allocation par les bénéficiaires et obligations du contrat. Aucun savoir sur les échanges privés avec Tomás sans document ou rapport.')
npc('security','Rappelle la circulation avant les sanctions ; une consigne claire suffit souvent.',
 'Maintenir le Forum praticable et éviter l’escalade inutile.',
 'SM09 ronde B07 station → B01 service municipal → galerie B02 ; relais au point de sûreté. N’entre pas dans les logements sans motif.',
 'Arme braquée : couverture, sommation et appel SMPD. Danger majeur : renfort adapté. Ne prend pas en chasse un citoyen pour avoir demandé une direction.')
npc('astor','Se perd dans un intitulé de quai, puis trouve lui-même le détail qui l’explique.',
 'Livrer et faire signer avant de reprendre une autre commande.',
 'SM09 B10 réserve → B07 quai → destinataire de galerie B02. Trajets de fret par bande prévue, pause chariot stationné.',
 'Ne bloque pas une sortie avec son chariot. Raconte les changements de quai vus, pas les secrets des destinataires. En alerte, se range et protège seulement son lot transportable.')
npc('rita','Sarcasme du quotidien ; surveille d’abord les passagers et la chaussée.',
 'Garder sa clientèle et un trajet qu’elle accepte de refaire demain.',
 'SM10 stationnement près du quai ; courses vers SM13 B07 selon contrat ; retour à la maison du thé B01 ou résidence B03. Une course l’absente réellement.',
 'Refuse une destination inaccessible à un passager. Peut décrire un contrôle vécu, pas une arrestation dans un autre secteur. Se retire des tirs avec les occupants, sans charge héroïque.')
npc('lin','Technique et patient quand on laisse les contacts tranquilles.',
 'Réparer correctement et être payé sans reprendre trois fois le même montage.',
 'SM10 B02 atelier ; achats d’un lot au point de livraison ; repas bref près de B08. Ferme la réserve et reste dans le quartier après service.',
 'Aide Elías avec le pont de commande existant. Ne pirate pas spontanément toutes les puces ISIO. Alerte locale : coupe son banc et abrite les clients derrière le comptoir.')
npc('yu','Continue de nouer le fil ; ton désabusé qui ne devient pas un discours.',
 'Protéger son atelier et finir les réparations payées.',
 'SM10 B09 eaux pour vérifier les filets ; travail sur quai autorisé ; rangement en résidence B03, sans traverser le lac.',
 'Peut reconnaître une coupe franche et son dernier client, pas identifier un saboteur invisible. Si menacée par le réseau, demande un témoin avant d’accuser publiquement.')
npc('leda','Son inquiétude coupe ses phrases ; elle revient à l’heure et à la veste de Sami.',
 'Faire rentrer son frère tout en tenant le stand qui les nourrit.',
 'SM11 B02 service, repas préparé à proximité ; logement B05 après fermeture. Si Sami est retenu, reste joignable par le stand et une voisine.',
 'Réagit à une confirmation de libération, puis au retour réel. Ne traverse pas seule une préfecture pour maintenir le scénario. En alerte, rejoint le logement avec Sami s’il est là.')
npc('hassan','Serviable, range par usage et rappelle une commande oubliée.',
 'Servir le quartier sans perdre les stocks déjà promis.',
 'SM11 B03 cantine et comptoir ; réserve desservie par B09 quai ; remise des bols à Nour en fin de service ; repos en logement local.',
 'Garde une commande payée à part. Partage une nouvelle reçue d’un livreur avec sa date. En pénurie, annonce les produits manquants avant de prendre l’argent.')
npc('sami','Prudent depuis sa retenue ; vérifie parfois sa carte sans en faire une tirade.',
 'Reprendre sa place au marché avec des justificatifs qu’il peut montrer.',
 'Avant libération : absent du marché, dossier de garde SM16. Après sortie : retour à SM11 B05 puis B02 aux heures de travail.',
 'Un contrôle le fait hésiter ; il demande à Leda où laisser le stand. Raconte seulement sa propre retenue. La copie du reçu ne lui donne pas une immunité policière.')
npc('nour','Pratique, humour de service après les premières commandes.',
 'Servir la nuit sans récupérer tout le nettoyage du jour.',
 'SM11 B08 préparation à 18 h ; service tardif vers B03 ; rangement et comptage des bols ; repos B05 le matin.',
 'Indique sa vraie prochaine ouverture. Garde un bouillon pour une urgence locale si le stock le permet. N’est pas disponible en permanence parce que le quartier reste dans la nuit.')
npc('cora','Lassée mais organisée ; demande une preuve utile plutôt qu’une promesse.',
 'Conserver les logements habités et faire entretenir les accès.',
 'SM12 B01 bureau de bloc ; passage laverie B05 et ascenseurs B06 ; réunion des locataires le soir, repos au bloc.',
 'Après recours, prévient les résidents et conserve la décision. Une nouvelle panne n’annule pas le jugement. En alerte, connaît les personnes à aider à descendre.')
npc('elias','Patient, reformule un quai et attend la confirmation avant d’annoncer la reprise.',
 'Faire fonctionner sa ligne et rendre les correspondances prévisibles.',
 'SM12 B09 station ; diagnostic B06 réseau ; contact avec SM13 B07 par le service, déplacement si intervention réelle. Relève en fin de cycle.',
 'Valide la réparation sur trois confirmations. En panne, affiche l’itinéraire de marche. En danger, arrête l’embarquement au lieu de laisser une rame traverser une zone de tir.')
npc('tala','Ramasse un jouet avant de parler ; répartie dirigée vers une absurdité précise.',
 'Garder une cour utilisable pour les habitants et les enfants.',
 'SM12 cour du B01, salle d’étude B08 puis rangement ; courses brèves à B07. Dort au bloc, remplacée par la garde locale la nuit.',
 'Rassemble les enfants dans une pièce connue en alerte. N’affronte pas un drone avec un trousseau. Ne connaît que les accès et foyers de sa cour.')
npc('berenice','Exigeante sur la coupe ; reconnaît un vêtement qui a bien tenu.',
 'Vendre du matériel ajusté sans dégrader la réputation de son atelier.',
 'SM13 B05 boutique ; prises de mesures, atelier puis comptoir. Achats livrés par l’arrière desserte ; fermeture avec rendez-vous possible le lendemain.',
 'Refuse une retouche dangereuse sur une plaque armée. Ses remarques portent sur le vêtement observable, pas sur la moralité du joueur. Réserve les commandes nominatives.')
npc('central-host','Accueil clair ; demande la destination exacte avant de diriger.',
 'Envoyer les visiteurs au bon service sans promettre une admission.',
 'SM13 B08 accueil ; contrôle des affichages B06 ; relais au déjeuner et à la fermeture de l’information publique.',
 'Signale un service fermé et un accès alternatif. Une alerte suit le circuit d’évacuation public. Ne donne pas le plan des locaux réservés d’Arcadius.')
npc('odette','Parle en poursuivant un travail compatible ; ironie lasse sur les habitués.',
 'Finir sa section sans incident ni heures supplémentaires invisibles.',
 'SM13 galerie B06 → abords B08 → station B07 ; signalisation posée avant lavage. Remise de la machine au local d’entretien après service.',
 'Peut se rappeler une heure et un vêtement vus pendant sa tournée. Aucun accès automatique aux bureaux des tours. En alerte, coupe la machine et libère la voie.')
npc('broker','Chirurgien K-12 : devis précis et limites matérielles explicites.',
 'Pratiquer une intervention compatible avec le modèle et le suivi acheté.',
 'SM14 B01 consultation ; B03 intervention sur rendez-vous ; suivi remis à B02. Pas d’opération complète instantanée au milieu de la place.',
 'Avant implant, confirme coût, effets sur l’Aura et statut ; pas de réversibilité inventée. En alerte, protège la salle d’opération et suspend les consultations ordinaires.')
npc('sen','Mesurée, clinique ; explique l’usage concret d’une pièce.',
 'Suivre les patients sans accepter que les contrats remplacent tous les soins urgents.',
 'SM14 B02 rééducation et consultations ; B07 réception des modules ; B06 admission pour les urgences. Passe les consignes avant repos.',
 'Vérifie sceau et température des lots reçus. Peut stabiliser sans identité, mais n’obtient pas des pièces illimitées. Ne révèle pas les patients à un démarcheur.')
npc('yuna','Technicienne de rééducation ; consignes patiemment répétées, ton différent de Yuna Marin.',
 'Permettre aux patients d’utiliser ce qu’ils ont réellement sous contrat.',
 'SM14 B02 exercices ; pharmacie B05 pour matériel autorisé ; comptes rendus puis nettoyage de la salle. Le soir, pas de suivi sans personne de garde.',
 'Observe la mobilité et appelle Sen si la douleur change. Ne pose pas une puce ISIO seule. Ne connaît aucun trafic du nœud maritime par homonymie.')
npc('eva','Petites précisions datées ; distingue absence d’une preuve et preuve d’une absence.',
 'Traiter un recours qui puisse être retrouvé et exécuté.',
 'SM15 B01 guichet ; B02 vérification d’archives ; B03 recours. Pause transmise à un collègue, rendez-vous de dossier pour son retour.',
 'Demande référence et copie avant décision. Peut délivrer une convocation prévue, pas ouvrir la présidence. Une alerte ferme les originaux et laisse les visiteurs sortir.')
npc('ivo','Propose le guichet déjà essayé ; autodérision contenue.',
 'Faire corriger son adresse sans perdre une autre journée de salaire.',
 'SM15 salle d’attente B01 puis B03 à l’appel ; repart en logement à la fermeture. Reçoit un prochain rendez-vous s’il reste une pièce à fournir.',
 'Montre son ticket et son dossier personnel, pas celui du voisin. S’écarte en alerte. Une journée passée n’efface pas la preuve qu’il a déjà déposée.')
npc('leal','Une question à la fois ; laisse un silence avant de répondre à une accusation.',
 'Résoudre une incohérence de garde sans falsifier l’entrée de son service.',
 'SM16 B02 bureau des retenues ; liaison interne au B03 ; accueil B01 pour remise de documents. Service continu par relais nommé.',
 'Compare heure du reçu et relevé de contrôle ; applique la libération existante. Ne raconte pas toutes les autres retenues. Alerte armée : protège les personnes dans le hall.')
npc('aural','Exige le ticket exact ; humour sec sur les descriptions approximatives.',
 'Rendre les bonnes armes à leur propriétaire, sans échange opportuniste.',
 'SM16 B08 vestiaire public ; transmission inventoriée à la relève ; déplacements courts vers B05 scellés uniquement pour un dépôt autorisé.',
 'Refuse une restitution sans preuve, propose la procédure correspondante. Une arme confiée ne se duplique pas dans le sac du joueur et le casier. Met les clients à couvert en alerte.')
npc('maelle','Calme, part d’une plante précise ; n’explique pas toute la société par le jardin.',
 'Maintenir les arbres vivants sur plusieurs saisons artificielles.',
 'SM17 B06 matériel ; tournée orangerie B04 et allées ; rapports au pavillon B01. Se repose après transmission à l’équipe d’entretien.',
 'Guide les visiteurs vers les bancs et respecte leurs accréditations. Connaît besoins et horaires d’entretien, pas les réunions privées des résidents cyborgs.')
npc('eilin','Plus piquante que Maëlle ; rappelle ce qui est compté.',
 'Obtenir une marge de travail sans faire perdre le stock végétal.',
 'SM17 B06 préparation → B04 contrôle des fruits → relevés d’eau ; ne pénètre pas dans B07 machinerie du ciel sans intervention autorisée.',
 'Un manque d’eau produit un relevé et une alerte technique, pas une accusation universelle. Fait fermer une allée si une branche menace ; rejoint son abri en cas de tirs.')
npc('valen','Formel, peu de gestes ; renvoie à la référence plutôt qu’à une formule intimidante.',
 'Recevoir les observations autorisées sans exposer le siège.',
 'SM18 B02 consultations ; B03 recherche de document ouvert ; relais d’accueil B04. Le pilier B01 n’est pas un passage public vers tous les étages.',
 'Connaît consignes et dossiers qu’il a consultés. Refuse calmement un accès non couvert, puis appelle la sûreté si l’intrusion continue. N’est pas présenté comme dirigeant d’IO.')
npc('sem','Donne une règle puis son état réel d’application ; ironie administrative espacée.',
 'Retrouver les documents consultables et ne pas perdre les demandes.',
 'SM18 B03 archives de consultation → B02 remise au comptoir ; inventaire avant fermeture ; dossiers sensibles laissés dans leur service.',
 'Donne une liste datée avec sa limite. Ne devient pas dépositaire de tous les secrets du Grand Exode. En alerte, ferme les rayonnages et laisse un registre d’évacuation.')

# Junk-Burgh
npc('roque','Affable, teste le besoin et la capacité à payer ; élude avant de concéder.',
 'Faire circuler les lots et conserver son ascendant sur les petits vendeurs.',
 'JB01 B02 comptoir ; rendez-vous aux comptes JB02 B03 ; retour à la réserve puis fermeture. Un déplacement annoncé le rend indisponible au bazar.',
 'Appelle un garde pour une menace, un médiateur pour un litige encore rentable. Connaît ses lots et contrats ; ne sait pas quel nom le joueur a livré à l’UFSA.')
npc('alma','Froide et méthodique ; une contestation doit viser une ligne.',
 'Faire payer les engagements et garder les preuves de ce qui a été réglé.',
 'JB02 B03 comptabilité ; vérification B04 lots retenus ; audience B08 contrats sur rendez-vous. Registre enfermé après service, copie de consultation séparée.',
 'Une dette payée reste close. Une fraude prouvée lui coûte un calcul, pas une conversion morale. En attaque, protège les livres et fait verrouiller son office.')
npc('debtor','Diego parle bas près des gardes, plus librement une fois sorti.',
 'Quitter le bazar et rejoindre sa cousine aux serres.',
 'Avant règlement : JB03 B07 et passage public près du médiateur. Après : rassemble son sac, demande le prochain départ sûr puis trajet vers Granja ; pas de disparition instantanée.',
 'Ne provoque pas ses créanciers. Connaît ses frais, les personnes qui l’ont gardé et son projet de départ. Le joueur n’obtient pas toute l’organisation Protectores par son récit.')
npc('scrapper','Sœur Ferraille impose le canon vers le mur ; préfère une pièce à une histoire de victimes.',
 'Vendre des armes réparables et ne pas recevoir une explosion sur l’établi.',
 'JB04 B02 armurerie ; démontage B01 quand une commande le demande ; pause B06 ; réserve d’armes verrouillée hors service.',
 'Refuse une manipulation chargée ; prend couvert et défend l’atelier si attaqué. Les nouvelles de lots viennent des réceptionnaires. Ne recharge pas gratuitement les armes du compagnon.')
npc('silas','Ironie contrariée ; recompte en montrant les pièces.',
 'Recevoir le lot promis sans sacrifier son prochain chantier.',
 'JB02 passage public près de B06 ; B03 pour sa réclamation ; après résolution, chargement au bureau de transport JB01 B09 et départ annoncé.',
 'Reste hors du stock armé. Utilise le livre de Sergio comme preuve, sans savoir ce qui a circulé après la signature. Une compensation règle son lot, pas toutes les fraudes du bazar.')
npc('noemi','Escroc souriante ; laisse la phrase du client préciser ce qu’il achète.',
 'Vendre la bonne référence au prix qui lui convient.',
 'JB02 B06 comptoir ; vérification en B01 fournitures ; inventaire avant fermeture. Reste disponible pour un retour signé le jour même selon contrat.',
 'Admet une erreur montrée sur pièce, défend un défaut de preuve. N’agresse pas un client qui compare les prix. Ses réserves finies viennent du lot effectivement acheté.')
npc('beltra','Beltrán réduit une affaire à une couleur, un numéro et une signature.',
 'Que le colis parte avec le bon statut, sans devenir responsable d’un impayé.',
 'JB02 B04 lots retenus ↔ B03 comptabilité ; transporte une étiquette ou une copie, pas le registre maître. Fin de service après rapprochement.',
 'Ne réétiquette qu’après instruction vérifiable. Une alerte ferme la cage et interrompt les manipulations. Peut attester une étiquette vue, pas l’origine lointaine de la marchandise.')

# Buenos Aires
npc('tomas','Méfiant à l’arrivée ; diction posée, souci concret des absents.',
 'Défendre les habitants sans confier trop vite leurs noms et leurs routes.',
 'BA03 B04 maison des délégués ; consultation B01 archives ; réception de courrier avec Celia. Visites aux Patios prévues, pas présence simultanée.',
 'Attend le dossier ou une nouvelle de Lucero. En alerte, organise liaison et abri plutôt que commander chaque combattant. Son origine mutante ne résume pas ses opinions.')
npc('celia','Précise sur le sceau, la dose et le retour ; peu de goût pour l’improvisation.',
 'Faire arriver des produits utilisables et répartir les réserves.',
 'BA03 point de distribution près de B04 ; réception BA01 B04 ; visite au dispensaire BA02 B01 selon bordereau ; stock fermé la nuit.',
 'Écarte un lot compromis et fournit une alternative annoncée. Connaît ses fournisseurs et commandes, pas les cellules clandestines qui les soutiennent. Protège le matériel médical en alerte.')
npc('vesta','Demande la recherche avant qu’on touche aux boîtes ; calme, parfois lasse.',
 'Préserver des preuves utilisables malgré l’état du bâtiment.',
 'BA03 B01 archives ; copies B05 imprimerie ; rangement et fermeture des salles fragiles. Les originaux ne sortent pas pour suivre le joueur.',
 'Distingue un ancien titre de l’usage récent d’un atelier. Alerte : évacuation des visiteurs puis mise à l’abri des pièces transportables, sans sauver tous les rayonnages au prix de sa vie.')
npc('candela','Tient les bons visibles ; colère dirigée vers l’écart entre promesse et charge.',
 'Faire respecter une livraison destinée aux habitants.',
 'BA01 B02 poste des citernes ; vérification B07 réservoir ; repos B06 après relève. L’affaire de Mauro la retient au barrage jusqu’à décision.',
 'Exige pesées et reçu avant partage ; libère réellement le passage après accord. En danger, fait abriter les conducteurs. Ne présume pas que Dusk ment parce qu’elle manque aussi d’eau.')
npc('mauro','Las mais concret ; protège la frontière entre conduire et garantir la vente.',
 'Décharger selon un accord qu’il puisse prouver puis reprendre la route.',
 'BA01 B02 avec la citerne ; repos B03 chauffeurs ; après accord, livraison au dépôt nommé puis retour, avec fret déduit une seule fois.',
 'Ne roule pas dans une ligne de tir pour tenir un délai. Connaît son chargement et ses ordres, pas l’identité du vendeur caché. Soutient un contrôle de volume transparent.')
npc('isma','Avertit du toit avant de répondre ; humour résigné sur les anciens horaires.',
 'Laisser les voyageurs dormir à un endroit qui ne s’effondre pas.',
 'BA01 B01 gare ; contrôle des arches et B10 garde voyageurs ; repos en relais à B06. Les voies servent de chemin, pas de départ ferroviaire actif.',
 'Ferme une travée instable et désigne l’abri disponible. Sait qui est arrivé quand il était de veille, pas tous les voyageurs de la nuit précédente.')
npc('esme','Priorité à la personne devant elle ; ne transforme pas une visite en cours de politique.',
 'Soigner et rendre le dispensaire accessible sans épuiser les porteurs.',
 'BA02 B01 consultations ; contrôle du treuil avec Vico quand il est arrêté ; transmissions aux aides avant repos. Un accueil de garde reste indiqué.',
 'Après réparation, organise de vraies montées. Peut demander un créneau prioritaire sans nier les besoins de l’atelier. Renseignements médicaux réservés aux personnes concernées.')
npc('mila','Enthousiasme encore actif sous la lassitude ; se moque du programme qu’elle recolle.',
 'Rassembler des habitants pour une soirée qui les change du bulletin répété.',
 'BA02 B05 foyer du cinéma ; affichage près de B02 ; préparation l’après-midi et accueil le soir ; démontage puis repos aux logements.',
 'Une panne fait modifier la séance ou reporter, pas oublier la bobine trouvée. En alerte, compte les sorties et aide le public à se ranger. Ne promet pas de courant infini.')
npc('gaspar','Direct, chaleureux par les actes ; plaisanteries sur ce qui revient trop souvent à la table.',
 'Servir tous ceux qui passent avec les apports du jour.',
 'BA02 B02 cuisine dès le matin ; réception d’eau et légumes ; service, nettoyage puis repos dans les logements. Menu du soir affiché selon stock.',
 'Adaptation des portions et appel à contribution en pénurie. Sous les tirs, coupe le feu et abrite la file. Connaît ses livraisons, pas les archives d’IO.')
npc('teo','Demande un nom précis ; respecte le contenu fermé d’un courrier.',
 'Remettre les lettres aux bonnes personnes et rentrer avec les accusés nécessaires.',
 'BA02 petite école B06 comme départ ; tournée des patios ; liaison BA03 B04 pour messages adressés ; retour au foyer avant la nuit.',
 'Détourne sa tournée si une rue est dangereuse et prévient le destinataire par relais. Ne lit pas un pli pour fournir une quête. Un message important possède expéditeur et réception datés.')
npc('vico','Fait arrêter l’alimentation avant toute explication ; précision rassurante.',
 'Réparer le frein de façon vérifiable et remettre l’usage aux équipes.',
 'BA04 B01 remise puis B02 treuil ; essai à vide, essai chargé et consignation. Pause B09, repos B06. Visite BA02 seulement pour contrôle convenu.',
 'Refuse un essai avec patient avant validation. Ne remet pas un chemin de fer entier en marche avec le frein récupéré. En alerte, consigne puis se replie.')
npc('rocio','Demande d’enlever ce qui dépasse ; relit la colonne juste sans flatter.',
 'Donner une mesure qui reste valable après le départ du client.',
 'BA04 B03 pesées ; étalonnage avant ouverture ; remise des copies au comptoir et rapprochement avec B04. Repas en relève.',
 'Fournit la preuve de tare dans l’affaire de la citerne. Garde les originaux et date une correction. Une pression armée peut suspendre le service, pas rendre la fausse valeur vraie.')
npc('sergio','Concis, tient à son exemplaire ; peut rire de sa mémoire avec retenue.',
 'Conserver la chaîne des entrées et sorties pour ne plus payer les pertes d’autrui.',
 'BA04 B04 livre des lots ; inspection des arrivages côté B08 ; remise d’une copie signée puis retour au bureau. Livre rangé avant fermeture.',
 'Ne permet pas d’emporter le registre. Une entrée prouve un passage, pas le motif caché de l’expéditeur. En alerte, prend le livre s’il est à portée, puis rejoint l’abri.')
npc('lian','Parle en surveillant la radio ; défend des logements précis plutôt qu’un slogan.',
 'Protéger les familles et l’atelier sans déclencher un tir évitable.',
 'BA05 B03 poste ; observation du passage ; liaison courte avec BA03 sur rendez-vous après accord. Relève maintenue pour ne pas déserter le front.',
 'N’agit sur un registre que lorsqu’il est reçu. Peut faire cesser les tirs de son équipe, pas de toute la région. Si repli, garde une route pour les civils.')
npc('alder','Formel et borné au mandat ; peut reconnaître une preuve qui modifie son ordre.',
 'Récupérer le matériel déclaré vacant sans perdre son détachement.',
 'BA05 B02 liaison et B08 technique IO ; observation de B01 atelier contesté. Les soldats restent en poste pendant l’entretien.',
 'Transmet le registre récent avant retrait. Ne devient pas allié universel après cessez-le-feu. Repli ou poursuite dépend d’un objectif local et d’un ordre reçu.')
npc('renzo','Fait écouter une panne puis attend ; se plaint de la machine avec précision.',
 'Projeter jusqu’à la fin sans user une bobine irremplaçable.',
 'BA02 B05 régie ; entretien le jour, essai avant séance, projection le soir. La scène cinéma actuelle sera rattachée au même ensemble, sans second Renzo.',
 'Coupe l’appareil si ça chauffe ; préfère reporter qu’abîmer le film. L’alerte le conduit à allumer la sortie et ouvrir le public, pas à finir une projection coûte que coûte.')

# Routes et sud actuellement accessibles
npc('otero','Excédé par le danger proche ; montre l’objet dont il parle.',
 'Vendre des pièces auxiliaires et conserver l’abri qui lui permet de travailler.',
 'AN03 B06 abri ; contrôle au B07 treuil ; entrée par B01 bras droit pour une récupération précise ; retour avant mauvaise visibilité.',
 'Abandonne une plaque si elle menace de tomber. Connaît ses passages sûrs, pas tous les systèmes du Titan. N’ouvre pas le cœur et ne proclame pas son réacteur éteint.')
npc('pilar','Question de vanne avant la conversation ; distingue usage et titre de propriété.',
 'Entretenir les filtres sans laisser une querelle administrative vider la réserve.',
 'AN04 B03 maintenance → B02 filtres → B04 pompes ; carnet sur sa desserte, pause dans le local de service. Accès B01 selon autorisation.',
 'Montre les prélèvements anciens effectivement notés. En panne, isole une section et prévient ses usagers connus. N’annule pas seule le choix hydraulique du joueur.')
npc('veiled','Réponses rares, exercices précis ; le mystère ne justifie pas des énigmes à chaque phrase.',
 'Garder un espace d’apprentissage sans promettre un pouvoir accessible à tous.',
 'AN05 B02 salle ; retrait en cellules B04 à heures annoncées par Senda. Accueil des voyageurs à B01 sans présence partout à la fois.',
 'Ne donne aucune vérité définitive sur les Érudits. Son refus d’enseigner à un implanté suit la limite du jeu ; ne vend pas un rituel qui la contourne. Violence : retrait protégé, sans combat de boss improvisé.')
npc('senda','Accueille en travaillant ; humour domestique qui ne lui prête pas une autorité mystique.',
 'Rendre les marches et la salle communes sûres pour les voyageurs.',
 'AN05 B03 cuisine → terrasses → B01 accueil ; réserve vérifiée avant la nuit ; repos dans une cellule autorisée.',
 'Donne horaires et consignes, pas une interprétation universelle de l’Aura. En danger, guide vers B05 abri. Ne révèle pas l’identité de la Veilleuse à partir d’une familiarité banale.')
npc('marin','Yuna Marin observe les caméras et choisit ses mots ; ton distinct de la soignante Yuna.',
 'Acheminer un module de liaison sans exposer les équipes qui l’utiliseront.',
 'AN06 B01 manutention ; B02 contrôle d’équipe ; pause B05. Remise discrète brève, sur une zone où elle est autorisée à travailler.',
 'Ne raconte que sa partie du transfert. En contrôle, suit les documents visibles ; aucune fuite de tout le réseau. Réagit à la dénonciation par une conséquence reçue, pas par télépathie.')
npc('deserter','Esteban hésite sur ce qu’il ignore ; parle d’un ordre qu’il a quitté.',
 'Trouver un refuge et décider s’il peut encore aider sans obéir aveuglément.',
 'Avant issue : AN06 B05 à l’écart du contrôle. Après asile : trajet discret convenu vers Dusk, repos DT01 B04 ; recrutement seulement après récupération.',
 'Évite UFSA et les contrôles où il serait identifié. Ne connaît pas la fin de l’opération après son départ. Son ancienne appartenance ne lui ouvre pas automatiquement les portes de la garnison.')
npc('celso','Interrompt la conversation si la charge bouge ; se moque peu quand elle est au-dessus.',
 'Changer le frein avant qu’une tolérance de gestion provoque un accident.',
 'AN06 B03 atelier → grue à l’arrêt → essais balisés ; compte rendu au responsable du quai puis repos B05.',
 'Interdit le passage sous charge, choisit un repli sûr en alerte. Connaît matériel et départs de son poste. Les colis radio ne font pas de lui un initié de Sine Vincula.')
npc('ortiz','Vocabulaire de territoire et de service ; répond à la situation de sa garnison.',
 'Garder ses effectifs et maintenir une administration qui reste obéie.',
 'NC02 B01 liaison ; B03 rapport radio ; inspection programmée de l’intendance B06. Pas de libre circulation du visiteur dans B02 casernement.',
 'Le cas Esteban la concerne après signalement. Une réserve civile contestée se traite avec Ramos et pièces, pas une attaque générale sans ordre. Ne connaît pas chaque transaction du nord.')
npc('quartermaster','Compte réellement avant de confirmer ; ton sobre, remarque sèche si quelqu’un se sert.',
 'Faire correspondre sorties, reçus et ce qui reste dans l’étagère.',
 'NC02 B06 intendance ; réception au portail B07 ; stock commercial distinct de B04 arsenal ; inventaire à la relève.',
 'Une livraison modifie seulement la catégorie reçue. En alerte, ferme les munitions et prépare une sortie autorisée. Aucune vente de l’arsenal entier au premier client solvable.')
npc('ramos','S’en tient aux volumes et à l’inventaire ; écoute un relevé contradictoire.',
 'Assurer ses réserves sans perdre la maîtrise du dépôt.',
 'NC03 B02 bureau ; vérification B01 cuve et B03 entrepôt ; remise des heures de retrait. Rapports à NC02 par liaison, pas présence dupliquée.',
 'Applique la répartition convenue une fois. Un détournement constaté ferme le retrait concerné et lance une enquête locale. Il ne connaît pas le coupable sans témoin ou trace.')
npc('bruna','Directe et combative ; humour contre une priorité arbitraire, pas contre les autres demandeurs.',
 'Faire obtenir aux trois campements un accès mesurable à l’eau.',
 'NC01 B02 requêtes puis NC03 B04 file civile pendant négociation ; B02 bureau Ramos sur invitation ; retour place et camp après livraison.',
 'Annonce un accord seulement après signature et premier créneau. En alerte, écarte la file de la cuve. Ne transforme pas tous les civils en partisans d’un soulèvement armé.')
npc('courier','Lucero masque sa fatigue par une remarque courte, puis vérifie le paquet.',
 'Faire parvenir le dossier et signaler qu’elle est encore vivante.',
 'AN07 B01 ancienne station en attente de soins ; retour progressif vers Buenos Aires avec relais identifié ; courrier BA03 puis repos BA02. Pas de retour instantané.',
 'La radio hors service limite ses nouvelles. Compagnon futur seulement après remise et relève. Ne conduit pas volontairement une équipe mutante vers un poste de contrôle IO légal.')
npc('leoncoast','León jauge une épave avant de plaisanter ; bon sens du rivage.',
 'Récupérer des filets sans se faire reprendre par la marée.',
 'AN07 B02 abri → zone de collecte sûre → B01 station ; départ selon marée annoncée. Nuit à l’abri, jamais sous une coque instable.',
 'Montre les passages qu’il a vus récemment et admet qu’un autre a pu se refermer. Évite les tirs et rejoint le signal B03 si le chemin est libre. Ne vend pas une sortie maritime garantie.')

# Ancienne définition hors scène
npc('prospector','Le Doseur mesure avant d’évaluer le risque.',
 'Ancien rôle de prospecteur conservé dans les données, sans implantation actuelle.',
 'RETRAIT À CONSERVER : aucun poste ni routine à Big Larry. Réemploi éventuel uniquement sur une piste extérieure, après proposition distincte.',
 'Ne pas le réintroduire comme résident de l’impact pour remplir le plan. Sa définition et ses anciens textes ne prouvent aucune présence jouable en v0.6.')

ROAD_PROFILES=[
 dict(id='road-trader',name='Sora',present='Rencontre caravane ; identifiant créé par case, pas membre d’un circuit mobile.',
      voice='Marchande de route, prix annoncés sans sermon.',
      routine='Stock vendable actuel limité à 5 achats d’eau ou d’antirad. Proposition : relier une seule Sora à CR 02, avec étape, réserve personnelle invendable et retour daté.',
      react='Se met à couvert et cherche le véhicule plutôt que poursuivre un voleur à travers la région. Ne se duplique pas sur plusieurs cases ; les anciens exemplaires de sauvegarde exigent une migration explicite.'),
 dict(id='road-injured',name='Maïra',present='Rencontre de récupératrice blessée ; résolution et coût des soins persistants par case.',
      voice='Gênée par l’accident, plaisante sur le geste qui l’a blessée.',
      routine='Actuellement soignable sur place. Proposition : une instance nommée unique, attente à l’abri puis départ avec une caravane reçue ; confirmation d’arrivée au prochain dépôt.',
      react='Soin par trousse ou tissus et compétence, comme aujourd’hui. Après aide, marche limitée et repos ; pas de marchandage infini de gratitude ni de nouvelle blessure identique pour reprendre la récompense.')
]

NEW_PROFILES=[
 ('Conductrice Aro','SM02','Contrat civil de fret, origine à définir.', 'Finir sa tournée sans payer les erreurs de tare.', 'B04 attente → pesée et B02 fouille → départ validé. Dort au repos chauffeurs si contrôle retardé.', 'Parle du véhicule et du temps perdu. Refuse un départ avec frein défectueux ; connaît son manifeste et sa dernière étape, pas les dossiers IO.'),
 ('Noa','SM03','Augmentée proposée ; technicienne de fret, candidate compagnon.', 'Obtenir une mission extérieure reconnue par son emploi.', 'B07 transport → B02 lots → B08 diagnostic autorisé ; repos hors zone de transit. Absence locale durant son contrat de compagnie.', 'Précise, un peu impatiente devant un faux diagnostic. Refuse de falsifier un dépistage dangereux. Ses accès ne valent que pour ses appareils de fret.'),
 ('Soignante Dena','SM08','Résidente de travée, statut biologique à définir.', 'Maintenir une infirmerie de proximité sans exposer ses patients.', 'B07 accueil et soins ; B04 pour les personnes incapables de se déplacer ; repos derrière le rideau en relais.', 'Douce avec les malades, ferme sur ses limites. Aide Luz, appelle une expertise si nécessaire ; aucune affiliation clandestine déduite de son voisinage.'),
 ('Rafi','SM10','Intermédiaire proposé du réseau local ; origine non arrêtée.', 'Faire respecter ses prélèvements en gardant les ateliers ouverts.', 'B06 bureau du réseau → B05 entrepôt → B01 rendez-vous ; ne stationne pas partout autour du lac.', 'Affable avec les témoins, plus direct en privé. Peut négocier un montant ou perdre un péage. Ne commande pas la SMPD ni toutes les familles de China Lake.'),
 ('Mina','SM11','Commerçante de tissus proposée ; résidente enregistrée à préciser.', 'Conserver une clientèle qui revient pour la bonne matière.', 'B01 halle → B09 réception de livraison → B05 logement. Prix visibles et échantillon disponible au comptoir.', 'Parle de texture et d’usage, sans transformer cela en métaphore constante. Ferme sa réserve en alerte ; ne vend pas soudain des armes militaires.'),
 ('Voisine Elisa','DT02','Habitante humaine proposée ; pas une représentante universelle du quartier.', 'Garder sa maison sèche et préserver un peu d’intimité.', 'B06 logement → B08 laverie → B01 cuisine ; porte ouverte sur invitation, fermée au repos.', 'Peut être piquante envers les visiteurs indiscrets. Témoigne d’une scène vue dans sa cour. Refuse que le joueur fouille une chambre sous prétexte de quête.'),
 ('Contrôleuse Ana','JB01','Protectores, contrôle commercial ; origine à définir.', 'Faire appliquer droits de passage et consignes d’armes.', 'B01 porte → B03 pesées pour litige → B08 poste à la relève. Poste tenu par une autre personne quand elle se repose.', 'Vérifie la transaction avant de menacer. Un client pauvre peut entrer si les règles le permettent ; un client armé menaçant appelle le renfort local.'),
 ('Hôtelière Cira Lobo','JB03','Exploitante proposée du motel ; indépendante sous règles Protectores.', 'Louer ses chambres et ne pas payer les dégâts des courtiers.', 'B01 accueil, chambre visitable après location ; B06 linge ; repos en logement du personnel B05.', 'Énonce tarif et suppléments avant la clé. Peut facturer une réparation prouvée, sans piège comptable identique à chaque client. En alerte, guide ses locataires.'),
 ('Tenancier Iago','JB03','Tenancier proposé du bar ; affiliation contractuelle à définir.', 'Faire revenir les clients sans transformer chaque querelle en fusillade.', 'B02 comptoir et petite scène ; réception B06 le matin ; fermeture, comptes et repos B05.', 'Moqueur avec ses habitués, prudent avec un inconnu armé. Connaît les propos entendus dans sa salle, pas leur vérité ni le contenu des chambres.'),
 ('Chirurgienne Sol','JB03','Praticienne commerciale proposée ; accès et origine à préciser.', 'Être payée pour du matériel qu’elle peut réellement remplacer.', 'B03 examen, devis puis intervention ; stock séparé ; repos sous garde de la clinique.', 'Parle prix sans feindre la bienveillance de Vera. Stabilisation et pièce prothétique sont deux prestations distinctes. Aucun miracle gratuit, aucune opération imposée au joueur.'),
 ('Mécanicienne Alba','JB04','Travailleuse de récupération proposée ; pas membre automatique des courtiers.', 'Sortir des moteurs fiables à partir de lots inégaux.', 'B03 moteurs → B01 démontage → B07 essai de roues ; repas et repos B06.', 'Montre un défaut, propose une réparation et un coût. Une visite n’autorise pas à prendre les pièces des autres. En incendie, isole le carburant avant repli si possible.'),
 ('Acheteur Damián','JB04','Acheteur proposé de lots sensibles ; origine et liens à garder circonscrits.', 'Acheter une provenance vérifiable à son échelle et garder sa marge.', 'Rendez-vous B04 enclos ; pesée au point autorisé ; signature B05 ; départ sans accès aux comptes privés d’Alma.', 'Poli, questions précises sur la chaîne de possession. Peut refuser un lot compromis. Ne révèle pas tous ses clients pour une simple hausse d’Éloquence.'),
 ('Soignant Salo','NC01','Praticien civil proposé, matériel limité.', 'Conserver un dispensaire ouvert malgré les priorités militaires.', 'B03 consultations ; déplacement accompagné vers un camp sur appel précis ; repos et garde transmis.', 'Explique ce qu’il peut stabiliser et ce qui demande transfert. Oriente vers Numa ou une structure connue seulement si une route fonctionne. Pas de bioprothèse IO en réserve gratuite.'),
 ('Marchande Elva','NC01','Commerçante civile proposée.', 'Garder l’équipe de manutention et livrer les commandes du marché.', 'B01 comptoir ; B09 transport pour un bon ; réception le matin puis maison B05.', 'Rapide, volontairement précise sur le poids. Conteste une réquisition avec un reçu et un témoin. Ne commande pas Bruna ni les habitants qui refusent de la suivre.'),
 ('Opératrice Lina','NC02','Militaire UFSA proposée, radio.', 'Transmettre le bon message au bon destinataire sans perdre son heure.', 'B03 radio ; B08 atelier pour panne consignée ; relève avec journal, repos B02.', 'Répète l’heure et la provenance. Ne divulgue pas les fréquences réservées à un civil. Une rumeur entendue sur un canal ouvert reste indiquée comme telle.'),
 ('Lieutenante Tessa Vela','PU01','Militaire UFSA proposée, liaison du port futur.', 'Maintenir le quai exploitable et son ordre de priorité.', 'B02 contrôle → B04 capitainerie → B01 réception ; pas d’autorité sur tous les navires lointains.', 'Ferme, admet un risque de grue établi par Neri. Peut signer une modification de lot. Aucun rôle de dirigeante du pays ; ne remplace pas Mara de Dusk.'),
 ('Grutier Daro','PU01','Opérateur civil proposé.', 'Poser la charge et rentrer avec ses bras intacts.', 'Grue balisée et B03 atelier ; essai à vide avec Neri ; repos hors d’une zone sous charge.', 'Ne parle longuement qu’une fois la commande sûre. Arrête une opération dangereuse, même si Tessa presse. Connaît son quai, pas le manifeste complet du port.'),
 ('Mécanicienne Neri','PU01','Technicienne civile proposée.', 'Remettre le frein en service sans laisser partir un essai douteux.', 'B03 atelier → grue consignée → B07 seulement sur autorisation de pièces ; repos après essai validé.', 'Diagnostic concret, impatience devant une fausse urgence administrative. Propose plusieurs coûts de réparation. N’a pas accès à un arsenal pour fournir un simple roulement.'),
 ('Elsa Voss','PU02','Marchande de pêche proposée ; aucun lien familial établi avec Ada Voss.', 'Vendre une prise saine et faire supporter le mauvais lot à son fournisseur.', 'B01 marché → aire de tri → B02 réunion des travailleurs sur rendez-vous ; logement local après fermeture.', 'Réservée avec les inconnus, vive sur une taxe incohérente. Le soignant lui transmet un avis sur le lot examiné ; elle ne diagnostique pas tous les poissons au regard.'),
 ('Charpentier Ulmo','PU02','Artisan de coques proposé.', 'Finir une réparation qui tiendra au prochain trajet.', 'B03 chantier → réserve de bois du chantier → B02 accord de travail ; pause à l’auberge B04.', 'Examine les assemblages avant de répondre au devis. Refuse un embarquement qu’il sait dangereux. Ne promet pas un bateau joueur navigable avant conception d’un tel système.'),
 ('Secrétaire D. Salvat','SU01','Agent administratif proposé ; aucun statut de dirigeant canonique.', 'Faire exécuter les décisions de son service et éviter deux ordres incompatibles.', 'B01 bureaux → B08 réunion autorisée → B02 pétitions pour remise datée ; passage public filtré.', 'Courtois, défensif si sa signature manque. Peut arbitrer une annexe locale, pas expliquer toute la constitution UFSA ou annoncer la reconquête du continent.'),
 ('Greffière Orel','SU01','Employée civile proposée.', 'Faire appeler les personnes dans l’ordre et conserver les pièces reçues.', 'B02 pétitions → B03 dépôt d’archives → comptoir ; pauses en relais et rendez-vous de retour.', 'Précise, évite les promesses vagues. Vérifie date et destinataire des deux listes. Ne détruit pas une réclamation parce que le joueur a été impoli.'),
 ('Intendante Joana','SU02','Intendante civile proposée ; ne commande pas la garnison.', 'Répartir les ressources de service et obtenir un convoi de chauffage.', 'B06 entrepôt → B01 marché → B08 courrier ; réunion SU01 seulement après convocation.', 'Compte les besoins avec Numa, annonce les manques. Un retard de route produit un arbitrage local ; elle ne détourne pas spontanément tous les stocks militaires.'),
 ('Technicien Farel','SU02','Technicien du chauffage proposé.', 'Réparer le réseau avec une pièce compatible et des essais sûrs.', 'B04 atelier → B03 dispensaire sur intervention → retour aux outils ; logements de service hors garde.', 'Parle panne, température et temps de pose. Connaît le relevé qu’il a fait, pas un complot tiré d’un simple échangeur absent. Coupe la section avant réparation.'),
 ('Soignante Numa','SU02','Praticienne civile proposée.', 'Préserver les patients et faire reconnaître le besoin de chauffage.', 'B03 soins ; coordination B06 par messager quand un patient ne peut être laissé ; relève annoncée avant repos.', 'Reste douce sans tout accepter. Donne un besoin mesuré et anonymisé. Aucun patient ne meurt uniquement parce que le joueur ouvre le journal de quête.'),
 ('Aubergiste Oso','SU02','Aubergiste proposé du foyer des voyageurs.', 'Garder des lits secs et être remboursé des chambres réquisitionnées.', 'B05 accueil → B01 courses → rangement du foyer ; garde de nuit au comptoir, chambre privée fermée.', 'Hospitalité prudente et humour de facture impayée. Donne les départs annoncés au foyer, pas la position exacte de chaque convoi hors de sa vue.')
]
