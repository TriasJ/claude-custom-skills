#!/usr/bin/env bash
# install.sh - Install Claude custom skills to ~/.claude/skills/
set -euo pipefail

SKILLS_DIR="$HOME/.claude/skills"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing Claude custom skills..."
echo "Source:      $SCRIPT_DIR"
echo "Destination: $SKILLS_DIR"
echo ""

mkdir -p "$SKILLS_DIR"

INSTALLED=0
SKIPPED=0

for skill_dir in "$SCRIPT_DIR"/*/; do
    skill_name="$(basename "$skill_dir")"

    # Skip non-skill directories
    [[ "$skill_name" == ".git" ]] && continue
    [[ "$skill_name" == "node_modules" ]] && continue

    # Check if SKILL.md exists (valid skill)
    if [[ ! -f "$skill_dir/SKILL.md" ]]; then
        echo "  SKIP  $skill_name (no SKILL.md found)"
        ((SKIPPED++))
        continue
    fi

    if [[ -d "$SKILLS_DIR/$skill_name" ]]; then
        echo "  UPDATE  $skill_name"
    else
        echo "  NEW     $skill_name"
    fi

    cp -r "$skill_dir" "$SKILLS_DIR/$skill_name"
    ((INSTALLED++))
done

echo ""
echo "Done! Installed $INSTALLED skills ($SKIPPED skipped)."
echo ""

# Remind about .env files
if [[ -f "$SKILLS_DIR/fetch-media/.env.example" ]] && [[ ! -f "$SKILLS_DIR/fetch-media/.env" ]]; then
    echo "REMINDER: Set up API keys for fetch-media:"
    echo "  cp $SKILLS_DIR/fetch-media/.env.example $SKILLS_DIR/fetch-media/.env"
    echo ""
fi

if [[ -f "$SKILLS_DIR/image-generation/.env.example" ]] && [[ ! -f "$SKILLS_DIR/image-generation/.env" ]]; then
    echo "REMINDER: Set up API key for image-generation:"
    echo "  cp $SKILLS_DIR/image-generation/.env.example $SKILLS_DIR/image-generation/.env"
    echo ""
fi
