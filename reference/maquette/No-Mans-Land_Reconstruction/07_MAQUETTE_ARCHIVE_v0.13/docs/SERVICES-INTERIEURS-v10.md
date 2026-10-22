# Services et intérieurs — version 0.10

21 intérieurs accessibles, dont 17 nouveaux. Ils appartiennent à des bâtiments dessinés et leurs accès sont ancrés aux façades. Les emprises et les meubles sont placés explicitement, sans remplissage aléatoire.

| Intérieur | Zone | Personnel | Accès |
|---|---|---|---|
| Clinique de Dusk-Town | Dusk-Town | Ardo Funes, Dr Vera Solis, Pía | Porte libre |
| L’arrière-salle des comptes | Junk-Burgh | Beltrán | Serrure : crochetage ou force |
| Coursives du Striker Oméga | Le Titan échoué | Sans personnel permanent | Porte libre |
| Cinéma des Patios | Patios habités | Renzo | Porte libre |
| Hôtel des Volets | Dusk-Town | Elvira | Porte libre |
| Bar du Passage | Dusk-Town | Beto | Porte libre |
| Épicerie de la pompe | Dusk-Town | Olga Ferreyra | Porte libre |
| Atelier de Nilo | Ateliers et veille | Lidia Soto | Porte libre |
| Bazar de Roque | Junk-Burgh | Zoé Mena | Porte libre |
| Clinique du comptant | Junk-Burgh | Simón Lagos | Porte libre |
| Agence de services du Forum | Forum de Lower-Town | Iris Dorn | Porte libre |
| Électronique Lin | China Lake | Wei Sanz, Lin Qiao | Porte libre |
| Consultations K-12 | Pôle des augmentations | Daria Velez, Dr Célian Rusk, Dr Iman Sen | Porte libre |
| Hall du registre civique | Registre civique | Noé Ferrer, Eva Serra | Porte libre |
| Bureau de garde SMPD | Préfecture SMPD | Aubin Rey, Agent Leal | Porte libre |
| Salle de lecture des archives | Buenos Aires | Maia Funes | Porte libre |
| Dispensaire des Patios | Patios habités | Inesa Cruz | Porte libre |
| Intendance de Novo Córdoba | Novo Córdoba | Beltrán Cobo | Porte libre |
| Infirmerie de campagne UFSA | Novo Córdoba | Ruth Vidal | Porte libre |
| Capitainerie du nœud maritime | Nœud maritime IO | Inara Silva | Porte libre |
| Salle de conduite 07 | Station de répartition | Lázaro Gil | Porte libre |

## Services effectifs

- Marchandises : stock réel, déduction du prix et ajout au sac. Les nouveaux comptoirs complètent les marchands ambulants.
- Soins : 18 $, ou 28 $ chez Lagos, restauration des PV et 30 minutes de soins. Décontamination : 35 $, −30 RAD, une heure. Les actions refusent un solde insuffisant.
- Hôtel : chambre à 8 $ pour huit heures ; fatigue annulée, récupération de 60 % des PV maximum. Elvira reçoit à l’intérieur.
- Bar : repas à 6 $, +8 PV et −12 points nets de fatigue, 30 minutes. Beto travaille derrière le comptoir.
- Ateliers : fabrication et démontage utilisent tout objet de type établi, à deux cases au maximum. Les recettes et leurs coûts existants sont conservés.
- K-12 : Sen et le chirurgien des augmentations reçoivent dans la clinique. Lin travaille dans son atelier ; Eva et Leal dans leurs halls. Vera reçoit dans la clinique de Dusk-Town.
- Nilo suit le joueur dans les intérieurs et revient par la porte sans duplication. Les sauvegardes conservent le lieu, les biens et les routines. Les anciennes positions de Vera, Elvira et Beto restent importables.

## Nœud maritime IO — AN06

Implantation reprise à partir du dossier : halle au nord-ouest, capitainerie et contrôle au nord, atelier des grues au sud-ouest, réserve sensible au sud-est, repos et inspection sanitaire de part et d’autre de la route. Un bassin maritime continu borde la côte est. Deux grues sont sur le quai ; un cargo fonctionnel remplace les épaves décoratives. La cour de manutention et la route ne traversent pas les bâtiments ni les conteneurs. La capitainerie est visitable. Les autres hangars du port ne possèdent pas encore tous un intérieur ; leurs portes ne présentent pas d’action d’entrée fictive.

## Station 07 et temple

La station suit AN04 : commande, filtration et maintenance au nord, stockage, accès et pompes aval au sud, deux bassins techniques et une cour de manœuvre. Les conduites principales sont enterrées ; les regards, collecteurs et segments visibles sont regroupés près des équipements. Les coudes de tuyaux isolés et les anciennes lignes plates ont été retirés de ce site. La salle de conduite est visitable ; le terminal extérieur conserve les décisions de la quête principale. Les arches du temple utilisent un modèle en pierre complet et reposent sur la terrasse.

## Rendu et assets

20 nouveaux sprites raster : 12 mobiliers et équipements, 6 éléments propres aux intérieurs IO, un cargo et un parquet. Sources PNG, prompts du mode image_gen intégré et manifests dans art-source. Les WebP préservent leur alpha. Les murs réels ont des finitions texturées adaptées au lieu. Lorsqu’une façade masque le joueur, seule une petite fenêtre autour de lui devient transparente ; le reste du bâtiment reste opaque.

## Vérification et limites

56 scènes fixes. Tests des parcours vers les portes, entrée et retour, services, prix, fabrication, compagnon, sauvegardes et migrations des routines. Rendus Canvas de production inspectés hors navigateur. Le rendu et les gestes sur téléphone restent à vérifier dans un navigateur réel. Les logements privés et les accès scellés ne sont pas ouverts par cette mise à jour. Human Corporation reste condamnée en 2175.
