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
  // clôture et portail IO du parvis (CENTER_TOWN.md §8G, §8I) : grille z46 x12-54 et x54 z4-46, sans trou ni chevauchement ;
  // portail recentré sur le milieu du pied d'escalier peint, projection 3/4 (même abscisse écran, x33,18 sur z46) :
  // emprise x29-37, solides sur les seuls piliers, passage libre 5,6 m (x30,2-35,8).
  // s1 17 m (x12-29) et s2 6 m (x37-43) d'Ocre, longueur réelle, aboutent le portail et s3 (x43-53,55) ; pas d'étirement.
  B_CT('c_arc_grille_s1', '', 'ct_arcadius_grille_s1_17m_v4_3q', 12, 45.7, 17, 0.6, { named: false }),
  B_CT('c_arc_portail_io', '', 'ct_arcadius_portail_io_v4_3q', 29, 45.4, 8, 1.2, { named: false, solid: [{ x: 29, z: 45.4, w: 1.2, d: 1.2 }, { x: 35.8, z: 45.4, w: 1.2, d: 1.2 }] }),
  B_CT('c_arc_grille_s2', '', 'ct_arcadius_grille_s2_6m_v4_3q', 37, 45.7, 6, 0.6, { named: false }),
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
  // porche et segment NE (§8L) : remplacent la pose ct_rempl1 (la clé ct_remplissage_8x8_a reste sur ct_rempl5)
  B_CT('ct_ne_seg0', '', 'ct_ne_segment_8x4_v4_3q', 92, 16, 8, 4, { named: false }),
  B_CT('ct_ne_porche0', 'Porche de la cour', 'ct_ne_porche_8x4_v4_3q', 92, 20, 8, 4, { named: false, solid: [{ x: 92, z: 20, w: 8, d: 0.4 }, { x: 92, z: 23.6, w: 8, d: 0.4 }] }),
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
  // tram v2 (§8K) : couloir N-S x72-76, tête au sud (z51,8), s'arrête avant le passage nord z52 ; taille native 2,65 × 33,8 m
  B_CT('ct_tram1', 'Tramway Center-Town', 'ct_veh_tram_avant_v4_3q', 72.68, 18, 2.65, 33.8, { named: false, solid: [{ x: 72.78, z: 18.3, w: 2.45, d: 33.2 }] }),
  B_CT('ct_echoppe0', 'Nouilles & Vapeur', 'ct_echoppe_vapeur_v3_3q', 36, 76, 4, 4, { named: false, solid: [{ x: 36.5, z: 77.5, w: 3.0, d: 2.1 }] }),
  B_CT('ct_kiosque0', 'Kiosque Presse & Médias', 'ct_kiosque_info_v3_3q', 84, 36, 4, 4, { named: false, solid: [{ x: 84.6, z: 37.5, w: 2.8, d: 2.1 }] }),
  B_CT('ct_lamp0', '', 'ct_lampadaire_io_v3_3q', 60, 40, 4, 4, { named: false, solid: [{ x: 61.5, z: 41.5, w: 1.0, d: 1.0 }] }),
  B_CT('ct_lamp1', '', 'ct_lampadaire_io_v3_3q', 84, 88, 4, 4, { named: false, solid: [{ x: 85.5, z: 89.5, w: 1.0, d: 1.0 }] }),
  B_CT('ct_bann0', '', 'ct_banniere_io_v3_3q', 40, 52, 4, 4, { named: false, solid: [{ x: 41.4, z: 53.4, w: 1.2, d: 1.2 }] }),
  B_CT('ct_bann1', '', 'ct_banniere_io_v3_3q', 60, 28, 4, 4, { named: false, solid: [{ x: 61.4, z: 29.4, w: 1.2, d: 1.2 }] }),
  B_CT('ct_ceris0', '', 'ct_cerisier_bac_v3_3q', 24, 76, 4, 4, { named: false, solid: [{ x: 25.0, z: 77.0, w: 2.0, d: 2.0 }] }),
  B_CT('ct_ceris1', '', 'ct_cerisier_bac_v3_3q', 108, 52, 4, 4, { named: false, solid: [{ x: 109.0, z: 53.0, w: 2.0, d: 2.0 }] }),

  // mobilier et signalétique du boulevard et du carrefour (CENTER_TOWN.md §8J) : trottoirs et parvis, hors chaussée 20 m, hors passages et sorties
  B_CT('ct_feu_no', '', 'ct_mob_feu_tricolore_v4_3q', 62.9, 54.9, 0.6, 0.6, { named: false, solid: [{ x: 63, z: 55, w: 0.4, d: 0.4 }] }),
  B_CT('ct_feu_ne', '', 'ct_mob_feu_tricolore_e_v4_3q', 84.5, 54.9, 0.6, 0.6, { named: false, solid: [{ x: 84.6, z: 55, w: 0.4, d: 0.4 }] }),
  B_CT('ct_feu_so', '', 'ct_mob_feu_tricolore_e_v4_3q', 62.9, 76.5, 0.6, 0.6, { named: false, solid: [{ x: 63, z: 76.6, w: 0.4, d: 0.4 }] }),
  B_CT('ct_feu_se', '', 'ct_mob_feu_tricolore_v4_3q', 84.5, 76.5, 0.6, 0.6, { named: false, solid: [{ x: 84.6, z: 76.6, w: 0.4, d: 0.4 }] }),
  B_CT('ct_fp_no', '', 'ct_mob_feu_pieton_e_v4_3q', 63.3, 51.2, 0.4, 0.4, { named: false, solid: [{ x: 63.4, z: 51.3, w: 0.25, d: 0.25 }] }),
  B_CT('ct_fp_ne', '', 'ct_mob_feu_pieton_v4_3q', 84.3, 51.2, 0.4, 0.4, { named: false, solid: [{ x: 84.4, z: 51.3, w: 0.25, d: 0.25 }] }),
  B_CT('ct_fp_so', '', 'ct_mob_feu_pieton_v4_3q', 63.3, 80.4, 0.4, 0.4, { named: false, solid: [{ x: 63.4, z: 80.5, w: 0.25, d: 0.25 }] }),
  B_CT('ct_fp_se', '', 'ct_mob_feu_pieton_e_v4_3q', 84.3, 80.4, 0.4, 0.4, { named: false, solid: [{ x: 84.4, z: 80.5, w: 0.25, d: 0.25 }] }),
  B_CT('ct_plots_no', '', 'ct_mob_plots_v4_3q', 56.6, 55.4, 1.2, 0.4, { named: false }),
  B_CT('ct_plots_ne', '', 'ct_mob_plots_v4_3q', 89.6, 55.4, 1.2, 0.4, { named: false }),
  B_CT('ct_plots_so', '', 'ct_mob_plots_v4_3q', 56.6, 76.3, 1.2, 0.4, { named: false }),
  B_CT('ct_plots_se', '', 'ct_mob_plots_v4_3q', 89.6, 76.3, 1.2, 0.4, { named: false }),
  B_CT('ct_gc_no', '', 'ct_mob_barriere_x_v4_3q', 57.8, 55.6, 2, 0.2, { named: false, solid: [{ x: 57.8, z: 55.6, w: 2, d: 0.2 }] }),
  B_CT('ct_gc_ne', '', 'ct_mob_barriere_x_v4_3q', 87.6, 55.6, 2, 0.2, { named: false, solid: [{ x: 87.6, z: 55.6, w: 2, d: 0.2 }] }),
  B_CT('ct_gc_so', '', 'ct_mob_barriere_x_v4_3q', 57.8, 76.2, 2, 0.2, { named: false, solid: [{ x: 57.8, z: 76.2, w: 2, d: 0.2 }] }),
  B_CT('ct_gc_se', '', 'ct_mob_barriere_x_v4_3q', 87.6, 76.2, 2, 0.2, { named: false, solid: [{ x: 87.6, z: 76.2, w: 2, d: 0.2 }] }),
  B_CT('ct_lampa0', '', 'ct_mob_lampadaire_ambre_v4_3q', 6.5, 54.5, 1, 1, { named: false, solid: [{ x: 6.7, z: 54.7, w: 0.6, d: 0.6 }] }),
  B_CT('ct_lampa1', '', 'ct_mob_lampadaire_ambre_v4_3q', 30.5, 54.5, 1, 1, { named: false, solid: [{ x: 30.7, z: 54.7, w: 0.6, d: 0.6 }] }),
  B_CT('ct_lampa2', '', 'ct_mob_lampadaire_ambre_v4_3q', 50.5, 54.5, 1, 1, { named: false, solid: [{ x: 50.7, z: 54.7, w: 0.6, d: 0.6 }] }),
  B_CT('ct_lampa3', '', 'ct_mob_lampadaire_ambre_v4_3q', 98.5, 54.5, 1, 1, { named: false, solid: [{ x: 98.7, z: 54.7, w: 0.6, d: 0.6 }] }),
  B_CT('ct_lampa4', '', 'ct_mob_lampadaire_ambre_v4_3q', 118.5, 54.5, 1, 1, { named: false, solid: [{ x: 118.7, z: 54.7, w: 0.6, d: 0.6 }] }),
  B_CT('ct_borne0', '', 'ct_mob_borne_info_v4_3q', 25, 53.4, 1, 0.5, { named: false, solid: [{ x: 25.1, z: 53.4, w: 0.8, d: 0.5 }] }),
  B_CT('ct_banc0', '', 'ct_mob_banc_x_v4_3q', 10, 54.6, 1.8, 0.6, { named: false, solid: [{ x: 10, z: 54.6, w: 1.8, d: 0.6 }] }),
  B_CT('ct_poub0', '', 'ct_mob_poubelles_x_v4_3q', 34, 54.6, 2.6, 0.6, { named: false, solid: [{ x: 34, z: 54.6, w: 2.6, d: 0.6 }] }),
  B_CT('ct_jard0', '', 'ct_mob_jardiniere_arbustes_v4_3q', 44.5, 54.2, 2.5, 1, { named: false, solid: [{ x: 44.5, z: 54.2, w: 2.5, d: 1 }] }),
  B_CT('ct_banc1', '', 'ct_mob_banc_x_v4_3q', 102, 54.6, 1.8, 0.6, { named: false, solid: [{ x: 102, z: 54.6, w: 1.8, d: 0.6 }] }),
  B_CT('ct_jarbre0', '', 'ct_mob_jardiniere_arbre_v4_3q', 114, 53.2, 2, 2, { named: false, solid: [{ x: 114, z: 53.2, w: 2, d: 2 }] }),
  B_CT('ct_poub1', '', 'ct_mob_poubelles_x_v4_3q', 124, 54.6, 2.6, 0.6, { named: false, solid: [{ x: 124, z: 54.6, w: 2.6, d: 0.6 }] }),
  B_CT('ct_distrib0', '', 'ct_mob_distributeurs_v4_3q', 115, 48.2, 2, 0.9, { named: false, solid: [{ x: 115, z: 48.2, w: 2, d: 0.9 }] }),
  B_CT('ct_stand0', '', 'ct_mob_stand_streetfood_v4_3q', 120.5, 49.2, 3, 2, { named: false, solid: [{ x: 120.8, z: 49.2, w: 2.7, d: 1.2 }] }),
  B_CT('ct_table0', '', 'ct_mob_table_haute_v4_3q', 118.6, 51.4, 1.4, 1.4, { named: false, solid: [{ x: 118.9, z: 51.7, w: 0.8, d: 0.8 }] }),
  B_CT('ct_holo_p0', '', 'ct_mob_panneau_holo_v4_3q', 104, 52.4, 3.5, 0.6, { named: false, solid: [{ x: 105.4, z: 52.5, w: 0.8, d: 0.5 }] }),
  B_CT('ct_lampa5', '', 'ct_mob_lampadaire_ambre_v4_3q', 8.5, 76.6, 1, 1, { named: false, solid: [{ x: 8.7, z: 76.8, w: 0.6, d: 0.6 }] }),
  B_CT('ct_lampa6', '', 'ct_mob_lampadaire_ambre_v4_3q', 46.5, 76.6, 1, 1, { named: false, solid: [{ x: 46.7, z: 76.8, w: 0.6, d: 0.6 }] }),
  B_CT('ct_lampa7', '', 'ct_mob_lampadaire_ambre_v4_3q', 98.5, 76.6, 1, 1, { named: false, solid: [{ x: 98.7, z: 76.8, w: 0.6, d: 0.6 }] }),
  B_CT('ct_lampa8', '', 'ct_mob_lampadaire_ambre_v4_3q', 122.5, 76.6, 1, 1, { named: false, solid: [{ x: 122.7, z: 76.8, w: 0.6, d: 0.6 }] }),
  B_CT('ct_banc2', '', 'ct_mob_banc_x_v4_3q', 14, 77.2, 1.8, 0.6, { named: false, solid: [{ x: 14, z: 77.2, w: 1.8, d: 0.6 }] }),
  B_CT('ct_jarbre1', '', 'ct_mob_jardiniere_arbre_v4_3q', 30, 76.6, 2, 2, { named: false, solid: [{ x: 30, z: 76.6, w: 2, d: 2 }] }),
  B_CT('ct_poub2', '', 'ct_mob_poubelles_x_v4_3q', 42, 77.2, 2.6, 0.6, { named: false, solid: [{ x: 42, z: 77.2, w: 2.6, d: 0.6 }] }),
  B_CT('ct_jard1', '', 'ct_mob_jardiniere_arbustes_v4_3q', 50, 77, 2.5, 1, { named: false, solid: [{ x: 50, z: 77, w: 2.5, d: 1 }] }),
  B_CT('ct_recharge0', '', 'ct_mob_bornes_recharge_v4_3q', 104, 76.6, 1.8, 0.6, { named: false, solid: [{ x: 104, z: 76.6, w: 1.8, d: 0.6 }] }),
  B_CT('ct_banc3', '', 'ct_mob_banc_x_v4_3q', 112, 77.2, 1.8, 0.6, { named: false, solid: [{ x: 112, z: 77.2, w: 1.8, d: 0.6 }] }),
  B_CT('ct_jard2', '', 'ct_mob_jardiniere_arbustes_v4_3q', 126, 77, 2.5, 1, { named: false, solid: [{ x: 126, z: 77, w: 2.5, d: 1 }] }),
  B_CT('ct_lampa9', '', 'ct_mob_lampadaire_ambre_v4_3q', 60.6, 10.5, 1, 1, { named: false, solid: [{ x: 60.8, z: 10.7, w: 0.6, d: 0.6 }] }),
  B_CT('ct_lampa10', '', 'ct_mob_lampadaire_ambre_v4_3q', 60.6, 94.5, 1, 1, { named: false, solid: [{ x: 60.8, z: 94.7, w: 0.6, d: 0.6 }] }),
  B_CT('ct_lampa11', '', 'ct_mob_lampadaire_ambre_v4_3q', 60.6, 108.5, 1, 1, { named: false, solid: [{ x: 60.8, z: 108.7, w: 0.6, d: 0.6 }] }),
  B_CT('ct_bancz0', '', 'ct_mob_banc_z_v4_3q', 62.6, 14, 0.6, 1.8, { named: false, solid: [{ x: 62.6, z: 14, w: 0.6, d: 1.8 }] }),
  B_CT('ct_poubz0', '', 'ct_mob_poubelles_z_v4_3q', 62.6, 20, 0.6, 2.6, { named: false, solid: [{ x: 62.6, z: 20, w: 0.6, d: 2.6 }] }),
  B_CT('ct_jarbre2', '', 'ct_mob_jardiniere_arbre_v4_3q', 61.4, 34.5, 2, 2, { named: false, solid: [{ x: 61.4, z: 34.5, w: 2, d: 2 }] }),
  B_CT('ct_bancz1', '', 'ct_mob_banc_z_v4_3q', 62.6, 98, 0.6, 1.8, { named: false, solid: [{ x: 62.6, z: 98, w: 0.6, d: 1.8 }] }),
  B_CT('ct_gbaz0', '', 'ct_mob_gba_z_v4_3q', 62.8, 112, 0.6, 2, { named: false, solid: [{ x: 62.8, z: 112, w: 0.6, d: 2 }] }),
  B_CT('ct_lampa12', '', 'ct_mob_lampadaire_ambre_v4_3q', 84.6, 6.5, 1, 1, { named: false, solid: [{ x: 84.8, z: 6.7, w: 0.6, d: 0.6 }] }),
  B_CT('ct_lampa13', '', 'ct_mob_lampadaire_ambre_v4_3q', 84.6, 103.5, 1, 1, { named: false, solid: [{ x: 84.8, z: 103.7, w: 0.6, d: 0.6 }] }),
  B_CT('ct_bancz2', '', 'ct_mob_banc_z_v4_3q', 84.8, 10, 0.6, 1.8, { named: false, solid: [{ x: 84.8, z: 10, w: 0.6, d: 1.8 }] }),
  B_CT('ct_poubz1', '', 'ct_mob_poubelles_z_v4_3q', 84.8, 14.5, 0.6, 2.6, { named: false, solid: [{ x: 84.8, z: 14.5, w: 0.6, d: 2.6 }] }),
  B_CT('ct_borne1', '', 'ct_mob_borne_info_v4_3q', 84.6, 41.4, 1, 0.5, { named: false, solid: [{ x: 84.7, z: 41.4, w: 0.8, d: 0.5 }] }),
  B_CT('ct_jarbre3', '', 'ct_mob_jardiniere_arbre_v4_3q', 84.6, 96, 2, 2, { named: false, solid: [{ x: 84.6, z: 96, w: 2, d: 2 }] }),
  B_CT('ct_poubz2', '', 'ct_mob_poubelles_z_v4_3q', 84.8, 108, 0.6, 2.6, { named: false, solid: [{ x: 84.8, z: 108, w: 0.6, d: 2.6 }] }),
  B_CT('ct_parv_jard0', '', 'ct_mob_jardiniere_arbustes_v4_3q', 13, 44.4, 2.5, 1, { named: false, solid: [{ x: 13, z: 44.4, w: 2.5, d: 1 }] }),
  B_CT('ct_parv_banc0', '', 'ct_mob_banc_x_v4_3q', 16.5, 44.6, 1.8, 0.6, { named: false, solid: [{ x: 16.5, z: 44.6, w: 1.8, d: 0.6 }] }),
  B_CT('ct_parv_jard1', '', 'ct_mob_jardiniere_arbustes_v4_3q', 39.5, 44.4, 2.5, 1, { named: false, solid: [{ x: 39.5, z: 44.4, w: 2.5, d: 1 }] }),
  B_CT('ct_parv_banc1', '', 'ct_mob_banc_x_v4_3q', 43, 44.6, 1.8, 0.6, { named: false, solid: [{ x: 43, z: 44.6, w: 1.8, d: 0.6 }] }),
  B_CT('ct_parv_arbre0', '', 'ct_mob_jardiniere_arbre_v4_3q', 48, 40, 2, 2, { named: false, solid: [{ x: 48, z: 40, w: 2, d: 2 }] }),
  B_CT('ct_parv_arbre1', '', 'ct_mob_jardiniere_arbre_v4_3q', 48, 28, 2, 2, { named: false, solid: [{ x: 48, z: 28, w: 2, d: 2 }] }),
  B_CT('ct_parv_arbre2', '', 'ct_mob_jardiniere_arbre_v4_3q', 48, 16, 2, 2, { named: false, solid: [{ x: 48, z: 16, w: 2, d: 2 }] }),
  // véhicules garés (§8K), le long des bordures de chaussée, taille native ; poses N-S en miroir (empreinte tournée)
  B_CT('ct_vtaxi0', '', 'ct_veh_taxi_avant_v4_3q', 40, 56.3, 5.4, 2, { named: false, solid: [{ x: 40.1, z: 56.4, w: 5.2, d: 1.8 }] }),
  B_CT('ct_vtaxi1', '', 'ct_veh_taxi_avant_v4_3q', 46.4, 56.3, 5.4, 2, { named: false, solid: [{ x: 46.5, z: 56.4, w: 5.2, d: 1.8 }] }),
  B_CT('ct_vmoto0', '', 'ct_veh_moto_avant_v4_3q', 52.5, 56.3, 2.3, 0.8, { named: false, solid: [{ x: 52.6, z: 56.4, w: 2.1, d: 0.6 }] }),
  B_CT('ct_vberl0', '', 'ct_veh_berline_dos_v4_3q', 30, 73.8, 4.8, 1.9, { named: false, solid: [{ x: 30.1, z: 73.9, w: 4.6, d: 1.7 }] }),
  B_CT('ct_vcomp0', '', 'ct_veh_compacte_dos_v4_3q', 36, 73.8, 4.3, 1.9, { named: false, solid: [{ x: 36.1, z: 73.9, w: 4.1, d: 1.7 }] }),
  B_CT('ct_vlivr0', '', 'ct_veh_motolivr_dos_v4_3q', 42, 74.8, 2.4, 0.9, { named: false, solid: [{ x: 42.1, z: 74.9, w: 2.2, d: 0.7 }] }),
  B_CT('ct_vutil0', '', 'ct_veh_utilitaire_avant_v4_3q', 96, 56.3, 5.8, 2.2, { named: false, solid: [{ x: 96.1, z: 56.4, w: 5.6, d: 2.0 }] }),
  B_CT('ct_vdep0', '', 'ct_veh_depanneuse_avant_v4_3q', 112, 56.3, 9, 2.6, { named: false, solid: [{ x: 112.1, z: 56.4, w: 8.8, d: 2.4 }] }),
  B_CT('ct_vbus0', '', 'ct_veh_bus_dos_v4_3q', 100, 73.15, 18, 2.55, { named: false, solid: [{ x: 100.1, z: 73.25, w: 17.8, d: 2.3 }] }),
  B_CT('ct_vlimo0', '', 'ct_veh_limo_dos_v4_3q', 121, 73.6, 6, 2.1, { named: false, solid: [{ x: 121.1, z: 73.7, w: 5.8, d: 1.9 }] }),
  B_CT('ct_vinter0', '', 'ct_veh_intercepteur_avant_v4_3q', 92, 73.6, 5, 2.1, { named: false, solid: [{ x: 92.1, z: 73.7, w: 4.8, d: 1.9 }] }),
  B_CT('ct_vtaxi2', '', 'ct_veh_taxi_avant_v4_3q', 64.3, 40, 2, 5.4, { named: false, miroir: true, solid: [{ x: 64.4, z: 40.1, w: 1.8, d: 5.2 }] }),  // axe N-S = miroir de la vue avant
  B_CT('ct_vberl1', '', 'ct_veh_berline_dos_v4_3q', 81.8, 86, 1.9, 4.8, { named: false, miroir: true, solid: [{ x: 81.9, z: 86.1, w: 1.7, d: 4.6 }] }),  // axe N-S = miroir de la vue dos
  B_CT('ct_vutil1', '', 'ct_veh_utilitaire_avant_v4_3q', 64.3, 90, 2.2, 5.8, { named: false, miroir: true, solid: [{ x: 64.4, z: 90.1, w: 2.0, d: 5.6 }] }),  // axe N-S = miroir de la vue avant

  // lot 2b §8M : ruelle-marché de nuit, coin SE (x100-132 z92-116), tout ≤ 6 m ; ruelle de raccord z92-95 devant les vitrines existantes
  B_CT('ct_p_se_kiosque_nouilles', '', 'ct_se_kiosque_nouilles_v4_3q', 100, 95, 6, 6, { named: false, solid: [{ x: 100, z: 95, w: 6, d: 5.3 }] }),
  B_CT('ct_p_se_echoppes_9x6', '', 'ct_se_echoppes_9x6_v4_3q', 115, 95, 9, 6, { named: false, solid: [{ x: 115, z: 95, w: 9, d: 6 }] }),
  B_CT('ct_p_se_maison_the', 'Maison de thé', 'ct_se_maison_the_v4_3q', 124, 95, 8, 6, { named: true, solid: [{ x: 124, z: 95, w: 8, d: 5.6 }] }),
  B_CT('ct_p_se_ateliers_12x10', '', 'ct_se_ateliers_12x10_v4_3q', 100, 106, 12, 10, { named: false, solid: [{ x: 100, z: 106, w: 12, d: 10 }] }),
  B_CT('ct_p_se_arriere_8x10', '', 'ct_se_arriere_8x10_v4_3q', 124, 106, 8, 10, { named: false, solid: [{ x: 124, z: 106, w: 8, d: 10 }] }),
  B_CT('ct_p_se_etals_couverts', '', 'ct_se_etals_couverts_v4_3q', 115, 111, 9, 5, { named: false, solid: [{ x: 115.3, z: 112, w: 8.4, d: 1.6 }] }),
  B_CT('ct_se_stand0', '', 'ct_mob_stand_streetfood_v4_3q', 106, 96.5, 3, 2, { named: false, solid: [{ x: 106.3, z: 96.5, w: 2.7, d: 1.2 }] }),
  B_CT('ct_se_stand1', '', 'ct_mob_stand_streetfood_v4_3q', 109, 96.5, 3, 2, { named: false, solid: [{ x: 109.3, z: 96.5, w: 2.7, d: 1.2 }] }),
  B_CT('ct_se_ceris0', '', 'ct_cerisier_bac_v3_3q', 115.5, 106.5, 4, 4, { named: false, solid: [{ x: 116.5, z: 107.5, w: 2, d: 2 }] }),
  B_CT('ct_se_ceris1', '', 'ct_cerisier_bac_v3_3q', 119.5, 106.5, 4, 4, { named: false, solid: [{ x: 120.5, z: 107.5, w: 2, d: 2 }] }),
  B_CT('ct_se_distrib0', '', 'ct_mob_distributeurs_v4_3q', 120, 101, 2, 0.9, { named: false, solid: [{ x: 120, z: 101, w: 2, d: 0.9 }] }),

  // lot 2c §8N : jardin du Dôme, coin SO (x0-44 z92-116) ; passage Dôme x44-56 z96-100 libre ; muret 4 m bout à bout
  B_CT('ct_so_kiosque0', 'Kiosque du jardin', 'ct_so_kiosque_jardin_v4_3q', 3, 107, 6, 6, { named: true, solid: [{ x: 3, z: 107, w: 0.4, d: 0.4 }, { x: 8.6, z: 107, w: 0.4, d: 0.4 }, { x: 3, z: 112.6, w: 0.4, d: 0.4 }, { x: 8.6, z: 112.6, w: 0.4, d: 0.4 }] }),
  B_CT('ct_so_fontaine0', '', 'ct_so_fontaine_v4_3q', 18, 101, 4, 4, { named: false, solid: [{ x: 18, z: 101, w: 4, d: 4 }] }),
  B_CT('ct_so_stand0', '', 'ct_so_stand_concert_v4_3q', 32.5, 101.5, 3, 2.5, { named: false, solid: [{ x: 32.5, z: 102.3, w: 3, d: 1.2 }] }),
  B_CT('ct_so_stand1', '', 'ct_so_stand_concert_v4_3q', 35.8, 101.5, 3, 2.5, { named: false, solid: [{ x: 35.8, z: 102.3, w: 3, d: 1.2 }] }),
  B_CT('ct_so_stand2', '', 'ct_so_stand_concert_v4_3q', 39.1, 101.5, 3, 2.5, { named: false, solid: [{ x: 39.1, z: 102.3, w: 3, d: 1.2 }] }),
  B_CT('ct_so_arbre0', '', 'ct_so_arbre_jardin_v4_3q', 4, 94.5, 3, 3, { named: false, solid: [{ x: 5.1, z: 95.6, w: 0.8, d: 0.8 }] }),
  B_CT('ct_so_arbre1', '', 'ct_so_arbre_jardin_v4_3q', 8.5, 98.5, 3, 3, { named: false, solid: [{ x: 9.6, z: 99.6, w: 0.8, d: 0.8 }] }),
  B_CT('ct_so_arbre2', '', 'ct_so_arbre_jardin_v4_3q', 18.5, 94.5, 3, 3, { named: false, solid: [{ x: 19.6, z: 95.6, w: 0.8, d: 0.8 }] }),
  B_CT('ct_so_arbre3', '', 'ct_so_arbre_jardin_v4_3q', 22.5, 110.5, 3, 3, { named: false, solid: [{ x: 23.6, z: 111.6, w: 0.8, d: 0.8 }] }),
  B_CT('ct_so_arbre4', '', 'ct_so_arbre_jardin_v4_3q', 5, 100.5, 3, 3, { named: false, solid: [{ x: 6.1, z: 101.6, w: 0.8, d: 0.8 }] }),
  B_CT('ct_so_ceris0', '', 'ct_cerisier_bac_v3_3q', 16, 110, 4, 4, { named: false, solid: [{ x: 17, z: 111, w: 2, d: 2 }] }),
  B_CT('ct_so_ceris1', '', 'ct_cerisier_bac_v3_3q', 24, 96.5, 4, 4, { named: false, solid: [{ x: 25, z: 97.5, w: 2, d: 2 }] }),
  B_CT('ct_so_table0', '', 'ct_mob_table_haute_v4_3q', 34, 105.4, 1.4, 1.4, { named: false, solid: [{ x: 34.3, z: 105.7, w: 0.8, d: 0.8 }] }),
  B_CT('ct_so_table1', '', 'ct_mob_table_haute_v4_3q', 38, 105.4, 1.4, 1.4, { named: false, solid: [{ x: 38.3, z: 105.7, w: 0.8, d: 0.8 }] }),
  B_CT('ct_so_banc0', '', 'ct_mob_banc_x_v4_3q', 18.6, 106.6, 1.8, 0.6, { named: false, solid: [{ x: 18.6, z: 106.6, w: 1.8, d: 0.6 }] }),
  B_CT('ct_so_bancz0', '', 'ct_mob_banc_z_v4_3q', 16.8, 101.6, 0.6, 1.8, { named: false, solid: [{ x: 16.8, z: 101.6, w: 0.6, d: 1.8 }] }),
  B_CT('ct_so_lampa0', '', 'ct_mob_lampadaire_ambre_v4_3q', 11, 100, 1, 1, { named: false, solid: [{ x: 11.2, z: 100.2, w: 0.6, d: 0.6 }] }),
  B_CT('ct_so_lampa1', '', 'ct_mob_lampadaire_ambre_v4_3q', 27, 104.6, 1, 1, { named: false, solid: [{ x: 27.2, z: 104.8, w: 0.6, d: 0.6 }] }),
  B_CT('ct_so_lampa2', '', 'ct_mob_lampadaire_ambre_v4_3q', 11, 112, 1, 1, { named: false, solid: [{ x: 11.2, z: 112.2, w: 0.6, d: 0.6 }] }),
  B_CT('ct_so_muret_s0', '', 'ct_so_muret_haie_x_v4_3q', 0, 115.4, 4, 0.6, { named: false, solid: [{ x: 0, z: 115.4, w: 4, d: 0.6 }] }),
  B_CT('ct_so_muret_s1', '', 'ct_so_muret_haie_x_v4_3q', 4, 115.4, 4, 0.6, { named: false, solid: [{ x: 4, z: 115.4, w: 4, d: 0.6 }] }),
  B_CT('ct_so_muret_s2', '', 'ct_so_muret_haie_x_v4_3q', 8, 115.4, 4, 0.6, { named: false, solid: [{ x: 8, z: 115.4, w: 4, d: 0.6 }] }),
  B_CT('ct_so_muret_s3', '', 'ct_so_muret_haie_x_v4_3q', 12, 115.4, 4, 0.6, { named: false, solid: [{ x: 12, z: 115.4, w: 4, d: 0.6 }] }),
  B_CT('ct_so_muret_s4', '', 'ct_so_muret_haie_x_v4_3q', 16, 115.4, 4, 0.6, { named: false, solid: [{ x: 16, z: 115.4, w: 4, d: 0.6 }] }),
  B_CT('ct_so_muret_s5', '', 'ct_so_muret_haie_x_v4_3q', 20, 115.4, 4, 0.6, { named: false, solid: [{ x: 20, z: 115.4, w: 4, d: 0.6 }] }),
  B_CT('ct_so_muret_s6', '', 'ct_so_muret_haie_x_v4_3q', 24, 115.4, 4, 0.6, { named: false, solid: [{ x: 24, z: 115.4, w: 4, d: 0.6 }] }),
  B_CT('ct_so_muret_s7', '', 'ct_so_muret_haie_x_v4_3q', 28, 115.4, 4, 0.6, { named: false, solid: [{ x: 28, z: 115.4, w: 4, d: 0.6 }] }),
  B_CT('ct_so_muret_s8', '', 'ct_so_muret_haie_x_v4_3q', 32, 115.4, 4, 0.6, { named: false, solid: [{ x: 32, z: 115.4, w: 4, d: 0.6 }] }),
  B_CT('ct_so_muret_s9', '', 'ct_so_muret_haie_x_v4_3q', 36, 115.4, 4, 0.6, { named: false, solid: [{ x: 36, z: 115.4, w: 4, d: 0.6 }] }),
  B_CT('ct_so_muret_s10', '', 'ct_so_muret_haie_x_v4_3q', 40, 115.4, 4, 0.6, { named: false, solid: [{ x: 40, z: 115.4, w: 4, d: 0.6 }] }),
  B_CT('ct_so_muret_o0', '', 'ct_so_muret_haie_z_v4_3q', 0, 94, 0.6, 4, { named: false, solid: [{ x: 0, z: 94, w: 0.6, d: 4 }] }),
  B_CT('ct_so_muret_o1', '', 'ct_so_muret_haie_z_v4_3q', 0, 98, 0.6, 4, { named: false, solid: [{ x: 0, z: 98, w: 0.6, d: 4 }] }),
  B_CT('ct_so_muret_o2', '', 'ct_so_muret_haie_z_v4_3q', 0, 102, 0.6, 4, { named: false, solid: [{ x: 0, z: 102, w: 0.6, d: 4 }] }),
  B_CT('ct_so_muret_o3', '', 'ct_so_muret_haie_z_v4_3q', 0, 106, 0.6, 4, { named: false, solid: [{ x: 0, z: 106, w: 0.6, d: 4 }] }),
  B_CT('ct_so_muret_o4', '', 'ct_so_muret_haie_z_v4_3q', 0, 110, 0.6, 4, { named: false, solid: [{ x: 0, z: 110, w: 0.6, d: 4 }] }),
  B_CT('ct_so_muret_o5', '', 'ct_so_muret_haie_z_v4_3q', 0, 111.4, 0.6, 4, { named: false, solid: [{ x: 0, z: 111.4, w: 0.6, d: 4 }] }),

  // lot 2d §8P : bureaux NE 12-18 m autour d'une cour (x100-132 z0-40) ; porche, segment et Nexus inchangés ; d/e1/f répétés selon la notice
  B_CT('ct_ne_bur_a1', '', 'ct_ne_bureaux_a1_8x6_v4_3q', 100, 0, 8, 6, { named: false, solid: [{ x: 100, z: 0, w: 8, d: 6 }] }),
  B_CT('ct_ne_bur_a2', '', 'ct_ne_bureaux_a2_8x6_v4_3q', 108, 0, 8, 6, { named: false, solid: [{ x: 108, z: 0, w: 8, d: 6 }] }),
  B_CT('ct_ne_bur_a3', '', 'ct_ne_bureaux_a3_8x6_v4_3q', 100, 6, 8, 6, { named: false, solid: [{ x: 100, z: 6, w: 8, d: 6 }] }),
  B_CT('ct_ne_bur_a4', '', 'ct_ne_bureaux_f_7x6_v4_3q', 108, 6, 7, 6, { named: false, solid: [{ x: 108, z: 6, w: 7, d: 6 }] }),
  B_CT('ct_ne_bur_b1', '', 'ct_ne_bureaux_b1_12x6_v4_3q', 120, 0, 12, 6, { named: false, solid: [{ x: 120, z: 0, w: 12, d: 6 }] }),
  B_CT('ct_ne_bur_b2', '', 'ct_ne_bureaux_b2_12x6_v4_3q', 120, 6, 12, 6, { named: false, solid: [{ x: 120, z: 6, w: 12, d: 6 }] }),
  B_CT('ct_ne_bur_c', '', 'ct_ne_bureaux_c_10x8_v4_3q', 100, 12, 10, 8, { named: false, solid: [{ x: 100, z: 12, w: 10, d: 8 }] }),
  B_CT('ct_ne_bur_d1', '', 'ct_ne_bureaux_d_10x6_v4_3q', 100, 28, 10, 6, { named: false, solid: [{ x: 100, z: 28, w: 10, d: 6 }] }),
  B_CT('ct_ne_bur_d2', '', 'ct_ne_bureaux_d_10x6_v4_3q', 100, 34, 10, 6, { named: false, solid: [{ x: 100, z: 34, w: 10, d: 6 }] }),
  B_CT('ct_ne_bur_e1', '', 'ct_ne_bureaux_e1_8x8_v4_3q', 124, 16, 8, 8, { named: false, solid: [{ x: 124, z: 16, w: 8, d: 8 }] }),
  B_CT('ct_ne_bur_e2', '', 'ct_ne_bureaux_e2_8x8_v4_3q', 124, 24, 8, 8, { named: false, solid: [{ x: 124, z: 24, w: 8, d: 8 }] }),
  B_CT('ct_ne_bur_e3', '', 'ct_ne_bureaux_e1_8x8_v4_3q', 124, 32, 8, 8, { named: false, solid: [{ x: 124, z: 32, w: 8, d: 8 }] }),
  B_CT('ct_ne_bur_f1', '', 'ct_ne_bureaux_f_7x6_v4_3q', 110, 34, 7, 6, { named: false, solid: [{ x: 110, z: 34, w: 7, d: 6 }] }),
  B_CT('ct_ne_bur_f2', '', 'ct_ne_bureaux_f_7x6_v4_3q', 117, 34, 7, 6, { named: false, solid: [{ x: 117, z: 34, w: 7, d: 6 }] }),
  B_CT('ct_ne_arbre0', '', 'ct_so_arbre_jardin_v4_3q', 111.5, 22, 3, 3, { named: false, solid: [{ x: 112.6, z: 23.1, w: 0.8, d: 0.8 }] }),
  B_CT('ct_ne_arbre1', '', 'ct_so_arbre_jardin_v4_3q', 119.5, 22, 3, 3, { named: false, solid: [{ x: 120.6, z: 23.1, w: 0.8, d: 0.8 }] }),
  B_CT('ct_ne_arbre2', '', 'ct_so_arbre_jardin_v4_3q', 115.5, 28.5, 3, 3, { named: false, solid: [{ x: 116.6, z: 29.6, w: 0.8, d: 0.8 }] }),
  B_CT('ct_ne_ceris0', '', 'ct_cerisier_bac_v3_3q', 115, 14.5, 4, 4, { named: false, solid: [{ x: 116, z: 15.5, w: 2, d: 2 }] }),
  B_CT('ct_ne_banc0', '', 'ct_mob_banc_x_v4_3q', 113, 26.2, 1.8, 0.6, { named: false, solid: [{ x: 113, z: 26.2, w: 1.8, d: 0.6 }] }),
  B_CT('ct_ne_banc1', '', 'ct_mob_banc_x_v4_3q', 118.6, 26.2, 1.8, 0.6, { named: false, solid: [{ x: 118.6, z: 26.2, w: 1.8, d: 0.6 }] }),
  B_CT('ct_ne_bancz0', '', 'ct_mob_banc_z_v4_3q', 122.6, 18, 0.6, 1.8, { named: false, solid: [{ x: 122.6, z: 18, w: 0.6, d: 1.8 }] }),
  B_CT('ct_ne_lampa0', '', 'ct_mob_lampadaire_ambre_v4_3q', 111, 17, 1, 1, { named: false, solid: [{ x: 111.2, z: 17.2, w: 0.6, d: 0.6 }] }),
  B_CT('ct_ne_lampa1', '', 'ct_mob_lampadaire_ambre_v4_3q', 122.5, 30, 1, 1, { named: false, solid: [{ x: 122.7, z: 30.2, w: 0.6, d: 0.6 }] }),
  B_CT('ct_ne_lampa2', '', 'ct_mob_lampadaire_ambre_v4_3q', 104, 22, 1, 1, { named: false, solid: [{ x: 104.2, z: 22.2, w: 0.6, d: 0.6 }] }),

];
export const PAINTED_DOORS_CENTER = [{ id: 'c_change_door', buildingId: 'c_change', painted_px: [441, 1873], face: 'e', opening: [8.0, 44.5], threshold: [9.0, 44.5] }];
