// Généré par tools_steel.py : ne pas éditer à la main. v12-v14 Steel-Megalopolis (route + douane, Center-Town, Sous-Ville).
export const BUILDINGS_ROUTE = [{"id": "r_porte", "label": "Porte du sarcophage", "sprite": "b_st_porte2", "x": 17.0, "z": 0.0, "w": 30.0, "d": 8.0, "visitable": false, "cue": null}, {"id": "r_douane", "label": "Douane", "sprite": "b_st_poste", "x": 2.0, "z": 20.0, "w": 9.0, "d": 8.0, "visitable": true, "cue": "card"}, {"id": "r_service", "label": "Sortie de service", "sprite": "b_st_service", "x": 40.0, "z": 29.5, "w": 4.5, "d": 3.0, "visitable": false, "cue": null}];
export const PAINTED_DOORS_ROUTE = [{"id": "r_douane_door", "buildingId": "r_douane", "painted_px": [220, 540], "face": "s", "opening": [8.94, 28.0], "threshold": [8.94, 29.0]}];
export const BUILDINGS_SV1 = [{"id": "v_cab_a", "label": "Cabane", "sprite": "b_sv_cab0", "x": 2.0, "z": 3.0, "w": 5.0, "d": 4.0, "visitable": false, "cue": null}, {"id": "v_cab_b", "label": "Cabane", "sprite": "b_sv_cab1", "x": 9.0, "z": 2.5, "w": 5.0, "d": 4.0, "visitable": false, "cue": null}, {"id": "v_tripot", "label": "Le Tripot", "sprite": "b_sv_tripot", "x": 16.0, "z": 2.0, "w": 8.0, "d": 7.0, "visitable": true, "cue": "dice"}, {"id": "v_cab_c", "label": "Cabane", "sprite": "b_sv_cab2", "x": 27.0, "z": 3.0, "w": 5.0, "d": 4.0, "visitable": false, "cue": null}, {"id": "v_cab_d", "label": "Cabane", "sprite": "b_sv_cab3", "x": 3.0, "z": 20.0, "w": 5.0, "d": 4.5, "visitable": false, "cue": null}, {"id": "v_cab_e", "label": "Cabane", "sprite": "b_sv_cab1", "x": 22.0, "z": 21.0, "w": 5.0, "d": 4.0, "visitable": false, "cue": null}, {"id": "v_cab_f", "label": "Cabane", "sprite": "b_sv_cab0", "x": 30.0, "z": 20.5, "w": 5.0, "d": 4.0, "visitable": false, "cue": null}];
export const PAINTED_DOORS_SV1 = [{"id": "v_tripot_door", "buildingId": "v_tripot", "painted_px": [265, 350], "face": "s", "opening": [22.69, 9.0], "threshold": [22.69, 10.0]}];
export const BUILDINGS_SV2 = [{"id": "v_cab_g", "label": "Cabane", "sprite": "b_sv_cab2", "x": 2.0, "z": 3.0, "w": 5.0, "d": 4.0, "visitable": false, "cue": null}, {"id": "v_atelier", "label": "Atelier d'Elio", "sprite": "b_sv_atelier", "x": 10.0, "z": 2.5, "w": 6.5, "d": 5.5, "visitable": true, "cue": "key"}, {"id": "v_cab_h", "label": "Cabane", "sprite": "b_sv_cab3", "x": 19.0, "z": 2.0, "w": 5.0, "d": 4.5, "visitable": false, "cue": null}, {"id": "v_lift", "label": "Monte-charge", "sprite": "b_sv_lift", "x": 30.0, "z": 4.0, "w": 3.5, "d": 3.5, "visitable": false, "cue": null}, {"id": "v_cab_i", "label": "Cabane", "sprite": "b_sv_cab0", "x": 4.0, "z": 20.0, "w": 5.0, "d": 4.0, "visitable": false, "cue": null}, {"id": "v_cab_j", "label": "Cabane", "sprite": "b_sv_cab1", "x": 18.0, "z": 20.5, "w": 5.0, "d": 4.0, "visitable": false, "cue": null}];
export const PAINTED_DOORS_SV2 = [{"id": "v_atelier_door", "buildingId": "v_atelier", "painted_px": [160, 330], "face": "s", "opening": [14.68, 8.0], "threshold": [14.68, 9.0]}];
const B_CT = (id, label, sprite, x, z, w, d, extra = {}) => ({ id, label, sprite, x, z, w, d, visitable: false, cue: null, named: !!label, tint: '#ffffff', ...extra });
// Center-Town v2 (plan cible d'Ocre validé par Valentin le 11/11/2026 : 132 x 116 m, chaussée 20 m, tram au centre, trottoirs 8 m).
// Règle : aucun sprite étiré ni déformé (pas de b.k, pas de b.sy) ; chaque sprite v3 est posé à son échelle native et garde son emprise.
// Emplacements en attente d'un asset d'Ocre (aucun depuis le lot v4 ; mécanisme gardé pour les prochains) : champ attente { cle, h } (h = hauteur cible en m). Tant que la clé n'est pas dans un manifeste,
// le repli s'affiche (sprite v3 natif centré par b.ancre, ou silhouette neutre dessinée par le code : view.placeholder) ;
// dès qu'Ocre livre la clé, main.js la pose sur l'emprise réservée, sans autre changement de code (repliDe : élément de repli retiré à la livraison).
const SIL = (h, lumE = true) => ({ h, color: '#191c25', lights: [1.5, 4.5].map(x => ({ x, y: Math.min(h - 1, 2.2), w: 1.6, h: 0.7, c: '#e8a13a' })),
  lightsE: lumE ? [{ z: 2, y: Math.min(h - 1, 2.2), w: 1.6, h: 0.7, c: '#e8a13a' }] : [] });
const RES = (id, cle, x, z, w, d, h) => B_CT(id, '', cle, x, z, w, d, { named: false, attente: { cle, h }, ph: SIL(h) });
export const BUILDINGS_CENTER = [
  // Monuments (CENTER_TOWN.md §2.A, §8)
  // Arcadius v4 d'Ocre (socle 32x32x16, tour 16x16x60, 50 px/m, échelle native) : 3 sprites d'emprise sans chevauchement, triés arrière -> aile est -> façade ;
  // l'escalier (x22-34, z36-42,6) est peint dans la façade hors emprise, praticable (CENTER_TOWN.md §8). Solides = les 3 emprises (socle complet).
  B_CT('c_arcadius_n', '', 'ct_arcadius_arriere_v4_3q', 12, 4, 24, 22, { named: false }),
  B_CT('c_arcadius_e', '', 'ct_arcadius_aile_est_v4_3q', 36, 4, 8, 22, { named: false }),
  B_CT('c_arcadius', 'Arcadius Center', 'ct_arcadius_facade_v4_3q', 12, 26, 32, 10),
  // clôture et portail IO du parvis (CENTER_TOWN.md §8G) : grille z46 x12-54 et x54 z4-46 ;
  // portail recentré sur le milieu du pied d'escalier peint, projection 3/4 (même abscisse écran, x33,18 sur z46) :
  // emprise x29-37, solides sur les seuls piliers, passage libre 5,6 m (x30,2-35,8). s1 inchangé (12 m, x12-24).
  // s2 à x37-48 ; s3 reste à x43-53,55 (chevauchement 5 m, segments à largeur fixe, sans étirement).
  // Trou visuel x24-29 (5 m) : aucun segment de 5 m livré, on n'étire pas s1 ; à combler quand Ocre livrera la pièce.
  B_CT('c_arc_grille_s1', '', 'ct_arcadius_grille_s1_v4_3q', 12, 45.7, 12, 0.6, { named: false }),
  B_CT('c_arc_portail_io', '', 'ct_arcadius_portail_io_v4_3q', 29, 45.4, 8, 1.2, { named: false, solid: [{ x: 29, z: 45.4, w: 1.2, d: 1.2 }, { x: 35.8, z: 45.4, w: 1.2, d: 1.2 }] }),
  B_CT('c_arc_grille_s2', '', 'ct_arcadius_grille_s2_v4_3q', 37, 45.7, 11, 0.6, { named: false, solid: [{ x: 37, z: 45.7, w: 6, d: 0.6 }] }),
  B_CT('c_arc_grille_s3', '', 'ct_arcadius_grille_s3_v4_3q', 43, 45.7, 10.55, 0.6, { named: false }),
  B_CT('c_arc_grille_e1', '', 'ct_arcadius_grille_e1_v4_3q', 53.7, 4, 0.6, 14, { named: false }),
  B_CT('c_arc_grille_e2', '', 'ct_arcadius_grille_e2_v4_3q', 53.7, 18, 0.6, 14, { named: false }),
  B_CT('c_arc_grille_e3', '', 'ct_arcadius_grille_e3_v4_3q', 53.55, 32, 0.9, 14.45, { named: false }),
  B_CT('c_tour', 'Le Dôme Fréquence', 'ct_dome_frequence_v3_3q', 44, 84, 12, 12, { visitable: true }),
  B_CT('c_blanc', 'Bureau des permis', 'ct_bureau_permis_v3_3q', 92, 40, 8, 8),
  // 5 tours v4 d'Ocre (8 x 8 m, 50 px/m, échelle 1 ; CENTER_TOWN.md §8E) : Teng 39, Archeon 43, Orc 45, Nexus 46, Human Corp 48 m
  B_CT('c_change', 'Change de Teng', 'ct_tour_teng_v4_3q', 0, 40, 8, 8, { visitable: true, cue: 'coin' }),
  B_CT('ct_archeon', 'Tour Archeon Industries', 'ct_tour_archeon_v4_3q', 16, 84, 8, 8),
  B_CT('ct_orc', 'Tour Orc Énergie', 'ct_tour_orc_v4_3q', 92, 8, 8, 8),
  B_CT('ct_humancorp', 'Tour Human Corp', 'ct_tour_humancorp_v4_3q', 104, 40, 8, 8),
  B_CT('ct_nexus', 'Tour Nexus', 'ct_tour_nexus_v4_3q', 92, 24, 8, 8),
  // Bâti bas (CENTER_TOWN.md §2.B)
  B_CT('c_immeuble', 'Immeuble Nexus Transit', 'ct_bord_sud_a_v3_3q', 28, 84, 8, 4),
  B_CT('c_galerie', 'Galerie du Carrefour', 'ct_bord_sud_b_v3_3q', 100, 84, 8, 4),
  B_CT('c_neon', 'Guichets Human Corp', 'ct_bord_sud_c_v3_3q', 92, 84, 4, 8),
  // Façades continues de remplissage (plan v2) : sprites v4 d'Ocre à 50 px/m, échelle 1, ancre au coin avant (CENTER_TOWN.md §8C) ; hauteur cible en commentaire
  B_CT('ct_rempl0', '', 'ct_remplissage_8x8_c', 92, 0, 8, 8, { named: false }), // h 20 m
  B_CT('ct_rempl1', '', 'ct_remplissage_8x8_a', 92, 16, 8, 8, { named: false }), // h 12 m
  B_CT('ct_rempl2', '', 'ct_remplissage_8x8_b', 92, 32, 8, 8, { named: false }), // h 16 m
  B_CT('ct_rempl3', '', 'ct_remplissage_16x8_b', 112, 40, 16, 8, { named: false }), // h 18 m
  B_CT('ct_rempl4', '', 'ct_remplissage_16x8_a', 0, 84, 16, 8, { named: false }), // h 14 m
  B_CT('ct_rempl5', '', 'ct_remplissage_8x8_a', 36, 84, 8, 8, { named: false }), // h 12 m
  B_CT('ct_rempl6', '', 'ct_remplissage_8x16_bas_b', 48, 100, 8, 16, { named: false }), // h 6 m
  B_CT('ct_rempl7', '', 'ct_remplissage_16x8_bas_a', 108, 84, 16, 8, { named: false }), // h 6 m
  B_CT('ct_rempl8', '', 'ct_remplissage_8x8_bas_a', 124, 84, 8, 8, { named: false }), // h 5 m
  B_CT('ct_rempl9', '', 'ct_remplissage_8x16_bas_a', 92, 92, 8, 16, { named: false }), // h 6 m
  B_CT('ct_rempl10', '', 'ct_remplissage_8x8_bas_b', 92, 108, 8, 8, { named: false }), // h 6 m
  // Transports, hologramme suspendu et mobilier urbain (bandes de mobilier des trottoirs ; sous-rectangles solid recalés avec la pose)
  B_CT('ct_mono_v0', '', 'ct_monorail_viaduc_v3_3q', 0, 16, 4, 12, { cover: true, named: false, solid: [{ x: 0.4, z: 16.4, w: 2.0, d: 2.0 }, { x: 0.4, z: 25.8, w: 2.0, d: 2.0 }] }),
  B_CT('ct_mono_r0', 'Viaduc Mega-Line', 'ct_monorail_rame_v3_3q', 0, 28, 4, 12, { cover: true, named: false, solid: [{ x: 0.4, z: 28.4, w: 2.0, d: 2.0 }, { x: 0.4, z: 37.8, w: 2.0, d: 2.0 }] }),
  B_CT('ct_holo0', '', 'ct_holo_suspendu_v3_3q', 84, 20, 4, 12, { cover: true, named: false, solid: [{ x: 84.6, z: 20.6, w: 1.4, d: 1.4 }, { x: 85.1, z: 30.5, w: 1.4, d: 1.4 }] }),
  B_CT('ct_arret0', 'Arrêt Tram Central', 'ct_arret_tram_v3_3q', 16, 52, 8, 4, { named: false, solid: [{ x: 16.5, z: 52.3, w: 7.0, d: 1.4 }] }),
  // tram : sprite orienté z, à l'arrêt sur la voie tram de l'avenue N-S (x72-76) ; les taxis roulent (steel.js, vehicules)
  B_CT('ct_tram0', 'Tramway Center-Town', 'ct_tram_v3_3q', 72, 20, 4, 12, { named: false, solid: [{ x: 72.8, z: 20.8, w: 2.4, d: 10.4 }] }),
  B_CT('ct_echoppe0', 'Nouilles & Vapeur', 'ct_echoppe_vapeur_v3_3q', 36, 76, 4, 4, { named: false, solid: [{ x: 36.5, z: 77.5, w: 3.0, d: 2.1 }] }),
  B_CT('ct_kiosque0', 'Kiosque Presse & Médias', 'ct_kiosque_info_v3_3q', 84, 36, 4, 4, { named: false, solid: [{ x: 84.6, z: 37.5, w: 2.8, d: 2.1 }] }),
  B_CT('ct_lamp0', '', 'ct_lampadaire_io_v3_3q', 60, 40, 4, 4, { named: false, solid: [{ x: 61.5, z: 41.5, w: 1.0, d: 1.0 }] }),
  B_CT('ct_lamp1', '', 'ct_lampadaire_io_v3_3q', 84, 88, 4, 4, { named: false, solid: [{ x: 85.5, z: 89.5, w: 1.0, d: 1.0 }] }),
  B_CT('ct_bann0', '', 'ct_banniere_io_v3_3q', 40, 52, 4, 4, { named: false, solid: [{ x: 41.4, z: 53.4, w: 1.2, d: 1.2 }] }),
  B_CT('ct_bann1', '', 'ct_banniere_io_v3_3q', 60, 28, 4, 4, { named: false, solid: [{ x: 61.4, z: 29.4, w: 1.2, d: 1.2 }] }),
  B_CT('ct_ceris0', '', 'ct_cerisier_bac_v3_3q', 24, 76, 4, 4, { named: false, solid: [{ x: 25.0, z: 77.0, w: 2.0, d: 2.0 }] }),
  B_CT('ct_ceris1', '', 'ct_cerisier_bac_v3_3q', 108, 52, 4, 4, { named: false, solid: [{ x: 109.0, z: 53.0, w: 2.0, d: 2.0 }] }),
];
export const PAINTED_DOORS_CENTER = [{ id: 'c_change_door', buildingId: 'c_change', painted_px: [441, 1873], face: 'e', opening: [8.0, 44.5], threshold: [9.0, 44.5] }];
