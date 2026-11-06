// Généré par tools_steel.py : ne pas éditer à la main. v12-v14 Steel-Megalopolis (route + douane, Center-Town, Sous-Ville).
export const BUILDINGS_ROUTE = [{"id": "r_porte", "label": "Porte du sarcophage", "sprite": "b_st_porte2", "x": 17.0, "z": 0.0, "w": 30.0, "d": 8.0, "visitable": false, "cue": null}, {"id": "r_douane", "label": "Douane", "sprite": "b_st_poste", "x": 2.0, "z": 20.0, "w": 9.0, "d": 8.0, "visitable": true, "cue": "card"}, {"id": "r_service", "label": "Sortie de service", "sprite": "b_st_service", "x": 40.0, "z": 29.5, "w": 4.5, "d": 3.0, "visitable": false, "cue": null}];
export const PAINTED_DOORS_ROUTE = [{"id": "r_douane_door", "buildingId": "r_douane", "painted_px": [220, 540], "face": "s", "opening": [8.94, 28.0], "threshold": [8.94, 29.0]}];
export const BUILDINGS_SV1 = [{"id": "v_cab_a", "label": "Cabane", "sprite": "b_sv_cab0", "x": 2.0, "z": 3.0, "w": 5.0, "d": 4.0, "visitable": false, "cue": null}, {"id": "v_cab_b", "label": "Cabane", "sprite": "b_sv_cab1", "x": 9.0, "z": 2.5, "w": 5.0, "d": 4.0, "visitable": false, "cue": null}, {"id": "v_tripot", "label": "Le Tripot", "sprite": "b_sv_tripot", "x": 16.0, "z": 2.0, "w": 8.0, "d": 7.0, "visitable": true, "cue": "dice"}, {"id": "v_cab_c", "label": "Cabane", "sprite": "b_sv_cab2", "x": 27.0, "z": 3.0, "w": 5.0, "d": 4.0, "visitable": false, "cue": null}, {"id": "v_cab_d", "label": "Cabane", "sprite": "b_sv_cab3", "x": 3.0, "z": 20.0, "w": 5.0, "d": 4.5, "visitable": false, "cue": null}, {"id": "v_cab_e", "label": "Cabane", "sprite": "b_sv_cab1", "x": 22.0, "z": 21.0, "w": 5.0, "d": 4.0, "visitable": false, "cue": null}, {"id": "v_cab_f", "label": "Cabane", "sprite": "b_sv_cab0", "x": 30.0, "z": 20.5, "w": 5.0, "d": 4.0, "visitable": false, "cue": null}];
export const PAINTED_DOORS_SV1 = [{"id": "v_tripot_door", "buildingId": "v_tripot", "painted_px": [265, 350], "face": "s", "opening": [22.69, 9.0], "threshold": [22.69, 10.0]}];
export const BUILDINGS_SV2 = [{"id": "v_cab_g", "label": "Cabane", "sprite": "b_sv_cab2", "x": 2.0, "z": 3.0, "w": 5.0, "d": 4.0, "visitable": false, "cue": null}, {"id": "v_atelier", "label": "Atelier d'Elio", "sprite": "b_sv_atelier", "x": 10.0, "z": 2.5, "w": 6.5, "d": 5.5, "visitable": true, "cue": "key"}, {"id": "v_cab_h", "label": "Cabane", "sprite": "b_sv_cab3", "x": 19.0, "z": 2.0, "w": 5.0, "d": 4.5, "visitable": false, "cue": null}, {"id": "v_lift", "label": "Monte-charge", "sprite": "b_sv_lift", "x": 30.0, "z": 4.0, "w": 3.5, "d": 3.5, "visitable": false, "cue": null}, {"id": "v_cab_i", "label": "Cabane", "sprite": "b_sv_cab0", "x": 4.0, "z": 20.0, "w": 5.0, "d": 4.0, "visitable": false, "cue": null}, {"id": "v_cab_j", "label": "Cabane", "sprite": "b_sv_cab1", "x": 18.0, "z": 20.5, "w": 5.0, "d": 4.0, "visitable": false, "cue": null}];
export const PAINTED_DOORS_SV2 = [{"id": "v_atelier_door", "buildingId": "v_atelier", "painted_px": [160, 330], "face": "s", "opening": [14.68, 8.0], "threshold": [14.68, 9.0]}];
const B_CT = (id, label, sprite, x, z, w, d, extra = {}) => ({ id, label, sprite, x, z, w, d, visitable: false, cue: null, named: !!label, tint: '#ffffff', ...extra });
export const BUILDINGS_CENTER = [
  // Monuments et tours à publicités du Carrefour Arcadius (CENTER_TOWN.md §2.A, 0 clone)
  B_CT('c_arcadius', 'Arcadius Center', 'ct_arcadius_qg_3q', 36, 0, 12, 12),
  B_CT('c_tour', 'Le Dôme Fréquence', 'ct_dome_frequence_3q', 16, 0, 12, 12, { visitable: true }),
  B_CT('c_blanc', 'Bureau des permis', 'ct_bureau_permis_3q', 40, 28, 8, 8),
  B_CT('c_change', 'Change de Teng', 'ct_tour_teng_v2_3q', 4, 4, 8, 8, { visitable: true, cue: 'coin' }),
  B_CT('ct_archeon', 'Tour Archeon Industries', 'ct_tour_archeon_v2_3q', -8, 4, 8, 8),
  B_CT('ct_orc', 'Tour Orc Énergie', 'ct_tour_orc_v2_3q', 48, 2, 8, 8),
  B_CT('ct_humancorp', 'Tour Human Corp', 'ct_tour_humancorp_v2_3q', 4, -8, 8, 8),
  B_CT('ct_nexus', 'Tour Nexus', 'ct_tour_nexus_v2_3q', 20, -8, 8, 8),
  // Bordure sud basse (CENTER_TOWN.md §2.B)
  B_CT('c_immeuble', 'Immeuble Nexus Transit', 'ct_bord_sud_a_3q', 0, 32, 8, 4),
  B_CT('c_galerie', 'Galerie du Carrefour', 'ct_bord_sud_b_3q', 8, 32, 8, 4),
  B_CT('c_neon', 'Guichets Human Corp', 'ct_bord_sud_c_3q', 20, 28, 4, 8),
  // Transports, hologramme suspendu et mobilier urbain (CENTER_TOWN.md §2.C, emprises >= 4 m, sous-rectangles solid)
  B_CT('ct_mono_v0', '', 'ct_monorail_viaduc_3q', 0, 0, 4, 12, { cover: true, named: false, solid: [{ x: 0.4, z: 0.4, w: 2.0, d: 2.0 }, { x: 0.4, z: 9.8, w: 2.0, d: 2.0 }] }),
  B_CT('ct_mono_r0', 'Viaduc Mega-Line', 'ct_monorail_rame_3q', 0, 12, 4, 12, { cover: true, named: false, solid: [{ x: 0.4, z: 12.4, w: 2.0, d: 2.0 }, { x: 0.4, z: 21.8, w: 2.0, d: 2.0 }] }),
  B_CT('ct_holo0', '', 'ct_holo_suspendu_3q', 24, 12, 4, 12, { cover: true, named: false, solid: [{ x: 24.6, z: 12.6, w: 1.4, d: 1.4 }, { x: 24.6, z: 22.0, w: 1.4, d: 1.4 }] }),
  B_CT('ct_arret0', 'Arrêt Tram Central', 'ct_arret_tram_3q', 4, 12, 8, 4, { named: false, solid: [{ x: 4.5, z: 12.3, w: 7.0, d: 1.4 }] }),
  B_CT('ct_tram0', 'Tramway Center-Town', 'ct_tram_3q', 28, 22, 4, 12, { named: false, solid: [{ x: 28.8, z: 22.8, w: 2.4, d: 10.4 }] }),
  B_CT('ct_taxi1', '', 'ct_taxi_v2_3q', 13.5, 17.1, 4.5, 1.8, { named: false }),
  B_CT('ct_taxi0', '', 'ct_taxi_v2_3q', 41.5, 17.1, 4.5, 1.8, { named: false }),
  B_CT('ct_echoppe0', 'Nouilles & Vapeur', 'ct_echoppe_vapeur_3q', 4, 20, 4, 4, { named: false, solid: [{ x: 4.5, z: 21.5, w: 3.0, d: 2.1 }] }),
  B_CT('ct_kiosque0', 'Kiosque Presse & Médias', 'ct_kiosque_info_3q', 12, 20, 4, 4, { named: false, solid: [{ x: 12.6, z: 21.5, w: 2.8, d: 2.1 }] }),
  B_CT('ct_lamp0', '', 'ct_lampadaire_io_3q', 16, 12, 4, 4, { named: false, solid: [{ x: 17.5, z: 13.5, w: 1.0, d: 1.0 }] }),
  B_CT('ct_lamp1', '', 'ct_lampadaire_io_3q', 36, 20, 4, 4, { named: false, solid: [{ x: 37.5, z: 21.5, w: 1.0, d: 1.0 }] }),
  B_CT('ct_bann0', '', 'ct_banniere_io_3q', 36, 12, 4, 4, { named: false, solid: [{ x: 37.4, z: 13.4, w: 1.2, d: 1.2 }] }),
  B_CT('ct_bann1', '', 'ct_banniere_io_3q', 44, 12, 4, 4, { named: false, solid: [{ x: 45.4, z: 13.4, w: 1.2, d: 1.2 }] }),
  B_CT('ct_ceris0', '', 'ct_cerisier_bac_v2_3q', 12, 12, 4, 4, { named: false, solid: [{ x: 13.0, z: 13.0, w: 2.0, d: 2.0 }] }),
  B_CT('ct_ceris1', '', 'ct_cerisier_bac_v2_3q', 36, 24, 4, 4, { named: false, solid: [{ x: 37.0, z: 25.0, w: 2.0, d: 2.0 }] }),
];
export const PAINTED_DOORS_CENTER = [{ id: 'c_change_door', buildingId: 'c_change', painted_px: [430, 1792], face: 'e', opening: [12.0, 8.5], threshold: [13.0, 8.5] }];
