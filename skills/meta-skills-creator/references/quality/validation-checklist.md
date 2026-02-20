# Validation Checklist

## Before Validation Script

### SKILL.md
- [ ] `name` field is lowercase + hyphens
- [ ] `description` field lists specific triggers ("Use when...")
- [ ] Has `<objective>` XML tag
- [ ] Has `<workflow>` XML tag with numbered steps
- [ ] Navigation table links to ALL reference files
- [ ] Under 150 lines (max 500)
- [ ] No detailed content (extracted to references)

### Reference Files
- [ ] Each file covers exactly ONE topic
- [ ] Each file is under 200 lines
- [ ] Each file has at least one concrete example
- [ ] No duplicate content across files
- [ ] No general knowledge Claude already has
- [ ] File names are descriptive (not `file1.md`)
- [ ] All code blocks have syntax highlighting

### Structure
- [ ] Sub-folders organized by function (not arbitrary)
- [ ] No empty directories
- [ ] No leftover example files from init
- [ ] No scripts/ or assets/ if unused

### Content Quality
- [ ] Imperative mood ("Use X" not "You should use X")
- [ ] Bullet points over prose
- [ ] Tables for comparisons
- [ ] Anti-patterns or "don't" sections included
- [ ] Actionable content (not just descriptive)

## Run Validation Script

```bash
# Find the validator
VALIDATOR=$(find ~/.claude/plugins -name "quick_validate.py" -path "*/skill-creator/*" | head -1)

# Validate
python3 "$VALIDATOR" /path/to/skill
```

Expected output: `Skill is valid!`

## After Validation

### Delivery Checklist
- [ ] Show file tree to user
- [ ] Explain what each sub-folder covers
- [ ] List sources used for research
- [ ] Provide invocation command (`/skill-name`)
- [ ] Skill appears in available skills list

### Post-Delivery
- [ ] User can invoke with `/skill-name`
- [ ] Test with a representative task
- [ ] Iterate based on real usage

## Common Validation Failures

| Error | Cause | Fix |
|---|---|---|
| Missing name/description | Incomplete frontmatter | Add required YAML fields |
| Empty description | Default TODO text left | Write a real description |
| Invalid name | Uppercase or spaces | Use lowercase + hyphens |
| File not found | Broken reference link | Fix paths in navigation table |
