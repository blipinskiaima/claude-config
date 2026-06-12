# Context — Bam2Beta — 2026-06-12

**Branche** : main
**Dernier commit** : 57b4deb — feat(bootstrap): bootstrap du score mVAF v1 (raima::bootstrap_model_v1)
**Status** : clean (seul dev/SCW/bacasable.sh untracked, sandbox exclu volontairement)

## Où j'en suis
Feature `bootstrap_model_v1` implémentée, validée bit-à-bit (Breast_10), commitée + pushée (57b4deb).
Vérification de non-régression S3 sur Colon_2 (HCL liquid) en cours : snapshot AVANT capturé,
reste à lancer le run rétrospectif puis l'inventaire APRÈS pour prouver que seul le CSV bootstrap est ajouté.

## Ce qui marche / ce qui foire
- ✓ bootstrap : 200 scores bit-à-bit identiques à la réf Florian (Breast_10), `max|Δ|=0`
- ✓ Image `raima:0.5.1` buildée (raima 0.5.1 + future + withr) ; `raima:latest` 0.5.0 intacte (id c69bfa42ec1a)
- ✓ Commit 57b4deb pushé ; MEMORY.md compactée 216→115 ; topic file bootstrap-model-v1.md
- ✓ Inventaire AVANT Colon_2 : 323 objets, 25,54 Go, digest `36c1e792…06ed33d4`, BOOTSTRAP/ absent (`processed/MRD/RetD/liquid/HCL/Colon_2/`)
- ⏳ Run rétrospectif Colon_2 + inventaire APRÈS : NON faits (à terminer)
- ⏳ Image 0.5.1 NON pushée sur Docker Hub (OK mono-nœud SCW ; push requis si multi-nœuds)

## Prochaine étape
Lancer le run rétrospectif Colon_2 (`--bootstrap true`, `grep -xE` pour cibler exact), puis régénérer
l'inventaire (`/tmp/inv_colon2.sh`) et `diff` vs AVANT → confirmer +1 objet (BOOTSTRAP/*.bootstrap_v1.tsv), 0 modifié, 0 supprimé.
