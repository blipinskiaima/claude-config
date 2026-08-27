# Context — Aima-Survey — 2026-08-27

**Branche** : main (poussé, origin/main = d302c20)
**Dernier commit** : d302c20 — refonte(biodesix): dossier repris sur documents
primaires + route 8-K EX-99.1
**Status** : clean

## Où j'en suis
Session terminée. Le dossier Biodesix a été entièrement refait — il était le plus
faible des huit, il est maintenant le premier sur les quatre mesures de densité.
Deux acquis dépassent Biodesix : la route 8-K EX-99.1 dans le collecteur, et
l'audit du profil AIMA retourné contre nous.

## Ce qui marche / ce qui foire
- ✓ P1 1730 l. / 218 marqueurs, P2 1390 / 236, contre 344/45 et 291/47 avant.
  534 constats, 548 affirmations réfutées (490 confirmées, 48 trompeuses,
  10 inexactes). PDF régénéré 19 → 77 pages.
- ✓ Route **8-K EX-99.1** (item 2.02) : 53 communiqués de résultats étaient en
  base sans corps, tous concurrents confondus. Rattrapés, 80/83, moy. 19 385 car.
  263 tests (+8).
- ✓ `AIMA-POSITIONING.md` audité : 7 corrections, 5 ajouts, **3 passes** de
  vérification adversariale contre le PDF SD-02. Tous les chiffres `[EXIS]`
  confirmés exacts dans les deux sens.
- ✗ **GlobeNewswire est mort pour nous** : PR Newswire 76/76 corps, GlobeNewswire
  0/24. `http=000`, rc 92, curl et WebFetch. Ce n'est PAS `_ZONES` — la coupure
  est par hôte. L'EX-99.1 est la route de secours.
- ✗ **Mail parasite envoyé le 27/08 à 08:01** : mon rattrapage avec `--days 2400`
  a collecté 93 dépôts SEC historiques 2020-2025 jamais vus, qui sont entrés dans
  la file de notification. `events_pending_email` n'a aucun filtre de date. J'ai
  voulu les marquer notifiés sans envoi, le classifieur a bloqué l'écriture, et le
  cron est parti avant. File à zéro depuis.
- ⚠ Les 3 passes ont trouvé 8, puis 5, puis 5 défauts graves, tous de moi. Le même
  réflexe **quatre fois** : correction appliquée à un seul des deux endroits où
  l'affirmation vivait. La boucle n'est pas sèche — j'ai arrêté sur jugement, la
  gravité décroissant nettement.

## Prochaine étape
Rien de bloquant. Trois candidats si on reprend : une 4ᵉ passe de vérification du
profil AIMA avant de le considérer opposable ; borner `--days` ou filtrer
`events_pending_email` par date pour qu'un rattrapage ne puisse plus déclencher
un mail d'archives ; et toujours l'alerte d'échec de cron, ouverte depuis le 28/07.
