// Référentiel spatial commun. 1 unité monde = 1 mètre. Toute dimension en mètres.
export const UNITS = {
  cell: 0.5,              // pas de la grille de navigation et de collision
  character: { height: 1.8, radius: 0.3 },
  door: { width: 1.0, height: 2.2, thresholdDepth: 1.0 }, // seuil = case devant l'ouverture
  storey: 3.0,            // hauteur d'étage
  wall: 0.2,              // épaisseur de mur
  street: { minWidth: 6.0, sidewalk: 1.5 },
  plotModule: 4.0,        // les parcelles sont des multiples de 4 m
  camera: { yawDeg: 45, pitchDeg: 35.264, pxPerMeterDesktop: 30, pxPerMeterMobile: 24 },
  companion: { followDistance: 1.5, maxDoorDistance: 6.0 },
  walkSpeed: 3.0          // m/s
};
