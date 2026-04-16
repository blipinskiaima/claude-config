---
name: seqera-cli-agent
description: Use the Seqera AI CLI as a subagent to answer questions about bioinformatics, Nextflow pipelines, Seqera Platform, and workflow management
triggers:
  - ask seqera
  - seqera agent
  - nextflow help
  - pipeline question
  - bioinformatics question
  - seqera platform help
allowed-tools: Bash(seqera:*)
metadata:
  service: seqera-cli
  audience: developers
  workflow: integration
  version: '1.4.0'
---

# Seqera AI CLI Subagent

Use the Seqera AI CLI in headless mode as a subagent to answer questions about:
- Nextflow pipelines and workflow development
- Seqera Platform configuration and usage
- Bioinformatics tools and best practices
- nf-core pipelines and community resources

## Workspace scoping — IMPORTANT

Boris ne s'intéresse **qu'au workspace `pipeline-prod` de l'organisation `aima-diagnostics`**. Le workspace `community` / `showcase` doit être **ignoré systématiquement**.

**Règle** : toute requête portant sur des runs, workflows, pipelines, compute environments, datasets, credentials, ou toute ressource Platform DOIT être explicitement scopée au workspace `pipeline-prod` (aima-diagnostics). Inclure cette contrainte dans le prompt passé à `seqera ai --headless`.

Template recommandé :
```bash
seqera ai --headless "Dans le workspace 'pipeline-prod' de l'organisation 'aima-diagnostics' UNIQUEMENT (ignore community/showcase) : <question>"
```

Les questions purement documentaires (syntaxe Nextflow, best practices, nf-core) n'ont pas besoin de ce scoping.

## Usage

### Basic Query (Headless Mode)

Run the CLI with a query in headless mode to get a response without the TUI:

```bash
seqera ai --headless "your question here"
```

### Example Queries

**Nextflow questions:**
```bash
seqera ai --headless "How do I configure resource limits in a Nextflow process?"
```

**Seqera Platform questions:**
```bash
seqera ai --headless "How do I set up a compute environment in Seqera Platform?"
```

**Pipeline development:**
```bash
seqera ai --headless "What's the best practice for handling input files in Nextflow?"
```

**nf-core questions:**
```bash
seqera ai --headless "How do I run the nf-core/rnaseq pipeline?"
```

## Headless Mode Options

| Flag | Description |
|------|-------------|
| `--headless` | Run without TUI, output to stdout |
| `--show-thinking` | Include reasoning/thinking in output |
| `--show-tools` | Show tool calls made by the agent |
| `--show-tool-results` | Show results of tool calls |
| `-c, --continue` | Continue the most recent session |
| `-s, --session <id>` | Continue a specific session |

### Verbose Output

For debugging or seeing the full agent response:
```bash
seqera ai --headless --show-thinking --show-tools "your question"
```

### Continue a Conversation

To continue a previous session:
```bash
seqera ai --headless --continue "follow-up question"
```

## When to Use This Skill

Use this skill when:
1. You need domain expertise about Nextflow, pipelines, or bioinformatics
2. You want to query the Seqera Platform API through natural language
3. You need help with pipeline development or debugging
4. You want to leverage Seqera AI's specialized knowledge

## Integration Pattern

When using as a subagent:

```bash
# Ask a question and capture the response
response=$(seqera ai --headless "How do I configure Nextflow to use AWS Batch?")
echo "$response"
```

## Authentication

The CLI requires authentication. If not already authenticated:
```bash
seqera login
```

Or set the access token directly:
```bash
export SEQERA_ACCESS_TOKEN=your-token
```

## Organization Selection

To work with a specific organization:
```bash
# List available organizations
seqera org

# Switch organization (interactive)
seqera org switch
```

**Note** : la CLI ne permet pas de changer d'org de façon non-interactive. Le scoping se fait donc dans le prompt envoyé à `seqera ai --headless` (voir section "Workspace scoping").
