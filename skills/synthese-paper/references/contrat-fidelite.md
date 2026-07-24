# Contrat de fidélité avec Aima-Tower

La synthèse produite doit être **identique** à celle de la page `/survey` d'Aima-Tower.
Ce fichier documente ce qui garantit cette identité — et ce qui la romprait.

## Ce que fait Tower exactement

`SurveyService.generate_article_synthesis` (`~/Pipeline/Aima-Tower/src/survey_service.py`) :

```python
content = (
    f"PMID : {article.pmid}\n"
    f"Date : {article.date}\n"
    f"Priorité : {article.priority.upper()}\n"
    f"Rubriques : {', '.join(article.categories)}\n"
    f"Journal : {article.journal}\n"
    f"Auteurs : {article.authors}\n"
    f"Titre : {article.title}\n\n"
    f"Résumé :\n{article.abstract}"
)
text = call_claude(content, SURVEY_ARTICLE_SYNTHESIS_SYSTEM_PROMPT)
```

Puis `call_claude` (`~/Pipeline/Aima-Tower/src/claude_cli.py`) :

| Paramètre | Valeur |
|---|---|
| Modèle | **`claude-sonnet-4-6`** — ⚠ pas Haiku, contrairement au scoring d'Aima-Survey |
| Timeout | 240 s |
| System prompt | `SURVEY_ARTICLE_SYNTHESIS_SYSTEM_PROMPT` **+** `<pipeline_context>…</pipeline_context>` |
| `pipeline_context` | concaténation de **tous** les `~/Pipeline/*/CLAUDE.md`, chargée au démarrage |
| Flags | `-p --output-format text --disable-slash-commands --tools "" --no-session-persistence --permission-mode bypassPermissions --setting-sources ""` |
| Entrée | `content` via stdin |

Le `pipeline_context` n'est pas un détail : c'est lui qui donne au modèle la connaissance de
l'écosystème AIMA, et donc la pertinence de la section « Implications AIMA ».

## Comment la fidélité est garantie

`scripts/synthese_paper.py` **importe** depuis Tower plutôt que de recopier :

```python
sys.path.insert(0, "/home/blipinski/Pipeline/Aima-Tower/src")
from claude_cli import call_claude
from prompts.survey_synthesis import SURVEY_ARTICLE_SYNTHESIS_SYSTEM_PROMPT
```

Conséquence : toute modification du prompt ou du modèle côté Tower est **automatiquement
répercutée**. Aucune dérive possible.

Si Aima-Tower est introuvable, le script **s'arrête** au lieu de produire une synthèse
approximative. C'est délibéré.

## Ce qui romprait le contrat

| Action | Effet |
|---|---|
| Recopier le prompt dans le skill | dérive silencieuse dès que Tower évolue |
| Utiliser l'API Anthropic au lieu du CLI | facturation, et `pipeline_context` perdu |
| Changer le modèle | Sonnet 4.6 ≠ Haiku : sorties nettement différentes |
| Omettre un champ de `content` | le prompt attend ces métadonnées, y compris `Rubriques` |
| Utiliser le texte intégral (`--fulltext`) | ⚠ le prompt impose « base-toi uniquement sur le titre, le résumé et les métadonnées » |

## Le cas `--fulltext`

L'option existe parce qu'un PDF contient plus qu'un résumé. Mais elle **contredit une contrainte
explicite du prompt**. À n'utiliser que si l'utilisateur le demande, en signalant l'écart.

Par défaut, même pour un PDF, seul le résumé est extrait — pour rester fidèle.

## Vérifier le contrat après une évolution de Tower

```bash
grep -n "^MODEL" ~/Pipeline/Aima-Tower/src/claude_cli.py
grep -c "" ~/Pipeline/Aima-Tower/src/prompts/survey_synthesis.py
```

Si le modèle ou le prompt changent, ce fichier de référence doit être mis à jour — le script,
lui, suit tout seul.
