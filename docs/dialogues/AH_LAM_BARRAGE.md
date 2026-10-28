# Ah-Lam, le Barrage (a_sud, Asia-Ground vers China Lake)

Statut : [proposition] à relire. Ne modifie pas `src/`. Le développeur intègre.
Seuils fixés par la production le 2026-10-28.

## Personnage
Garde du Barrage, assis sur ses caisses. Il encaisse pour China Lake et le sait. Il fait de l'ironie sèche et parle peu. Il ne se bat pas pour vingt crédits, mais il n'aime pas qu'on le prenne pour un idiot. Il connaît la ruelle de Lower-Town et le dit volontiers : ceux qui ne paient pas font le tour (repris de sa réplique « non » existante).

## Texte

**Accueil (remplace `start`)**
Ah-Lam : Vingt crédits pour passer. Le marché, faut bien l'entretenir.

Options du joueur :
- Payer 20 cr.
- [Discours] Je viens dépenser là-dedans. Si tu me ruines à l'entrée, c'est Zhou qui y perd.
- [Intimider] Regarde-moi bien. Tu veux vraiment compter mes pièces ?
- Et si je ne paie pas ?
- Au revoir.

**[Discours] réussite (4 ou plus)**
Ah-Lam : ... T'as pas tort. Passe. Et fais pas d'histoires.

**[Discours] résultat partiel (3 exactement)**
Ah-Lam : Bon. Dix, et on n'en parle plus.
Options : Payer 10 cr. / Au revoir.

**[Discours] échec (prix inchangé, 20 cr)**
Ah-Lam : Zhou a pas besoin de toi pour compter. Vingt.
Options : Payer 20 cr. / Au revoir.

**[Intimider] réussite (contre Volonté 4)**
Ah-Lam : Ça va, ça va... Entre. J'ai rien vu.

**[Intimider] échec (le prix passe à 30 cr)**
Ah-Lam : Joli numéro. Maintenant c'est trente.
Ah-Lam : Ou la ruelle, par Lower-Town. Personne la garde.
Options : Payer 30 cr. / Au revoir.

**Retour après échec d'intimidation**
Ah-Lam : Toujours trente. J'ai bonne mémoire.

**Pas assez de crédits (30)**
Ah-Lam : Trente. Pas vingt-neuf. Reviens.

Répliques existantes conservées : `paye`, `deja`, `non`, `pauvre`.

## Snippet (format de `src/data/asia_ground.js`, `DIALOGUES_ASIA.ag_ahlam`)

Points à trancher par le développeur :
- Le dépôt n'a pas encore de libellé à crochets ; la compétence s'appelle `parole` (character.js), « Discours » est l'étiquette affichée demandée.
- `test` ne gère aujourd'hui que pass/fail. Le palier à 3 demande un champ nouveau, proposé ici `partial` (+ `partialAt: 3`).
- L'intimidation est un jet opposé à la Volonté 4 d'Ah-Lam : proposé `test: 'intimider:4', opposed: 'volonte'`, à adapter au moteur.
- Nouveaux drapeaux : `cl_barrage_10`, `cl_barrage_30`, `ahlam_tente` (un seul essai de Discours ou d'Intimider).

```js
  ag_ahlam: { start: { text: 'Vingt crédits pour passer. Le march\u00e9, faut bien l\u2019entretenir.', options: [
      { label: 'Payer 20 cr.', action: 'paycr:20;flag:cl_barrage', next: 'paye', if: '!cl_barrage' },
      { label: '[Discours] Je viens d\u00e9penser l\u00e0-dedans. Si tu me ruines \u00e0 l\u2019entr\u00e9e, c\u2019est Zhou qui y perd.', if: '!cl_barrage', action: 'flag:ahlam_tente',
        test: 'parole:4', partial: 'dix', partialAt: 3, pass: 'parle_ok', fail: 'parle_rate' },
      { label: '[Intimider] Regarde-moi bien. Tu veux vraiment compter mes pi\u00e8ces ?', if: '!cl_barrage', action: 'flag:ahlam_tente',
        test: 'intimider:4', opposed: 'volonte', pass: 'peur_ok', fail: 'trente' },
      { label: 'Et si je ne paie pas ?', next: 'non', if: '!cl_barrage' },
      { label: 'Je repasse.', next: 'deja', if: 'cl_barrage' }, { label: 'Au revoir.', next: 'end' } ] },
    // NB : masquer Discours/Intimider si ahlam_tente ; si cl_barrage_30, ouvrir sur 'trente_retour'.
    parle_ok: { text: '\u2026 T\u2019as pas tort. Passe. Et fais pas d\u2019histoires.', options: [ { label: 'Au revoir.', action: 'flag:cl_barrage', next: 'end' } ] },
    dix: { text: 'Bon. Dix, et on n\u2019en parle plus.', options: [
      { label: 'Payer 10 cr.', action: 'paycr:10;flag:cl_barrage', next: 'paye' }, { label: 'Au revoir.', action: 'flag:cl_barrage_10', next: 'end' } ] },
    parle_rate: { text: 'Zhou a pas besoin de toi pour compter. Vingt.', options: [
      { label: 'Payer 20 cr.', action: 'paycr:20;flag:cl_barrage', next: 'paye' }, { label: 'Au revoir.', next: 'end' } ] },
    peur_ok: { text: '\u00c7a va, \u00e7a va\u2026 Entre. J\u2019ai rien vu.', options: [ { label: 'Au revoir.', action: 'flag:cl_barrage', next: 'end' } ] },
    trente: { text: 'Joli num\u00e9ro. Maintenant c\u2019est trente. Ou la ruelle, par Lower-Town. Personne la garde.', options: [
      { label: 'Payer 30 cr.', action: 'paycr:30;flag:cl_barrage', next: 'paye' }, { label: 'Au revoir.', action: 'flag:cl_barrage_30', next: 'end' } ] },
    trente_retour: { text: 'Toujours trente. J\u2019ai bonne m\u00e9moire.', options: [
      { label: 'Payer 30 cr.', action: 'paycr:30;flag:cl_barrage', next: 'paye' }, { label: 'Au revoir.', next: 'end' } ] },
    pauvre30: { text: 'Trente. Pas vingt-neuf. Reviens.', options: [ { label: 'Au revoir.', next: 'end' } ] },
    // paye, deja, non, pauvre : inchangés.
```
