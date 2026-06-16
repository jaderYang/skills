#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
SKILLS_DIR="$REPO_DIR/skills"

for category_dir in "$SKILLS_DIR"/*/; do
  category="$(basename "$category_dir")"
  [ -d "$category_dir" ] || continue

  echo "## $category"
  echo ""

  for skill_dir in "$category_dir"*/; do
    [ -f "$skill_dir/SKILL.md" ] || continue
    skill_name="$(basename "$skill_dir")"
    description="$(grep -m1 '^description:' "$skill_dir/SKILL.md" | sed 's/^description: *//')"
    echo "  $skill_name — $description"
  done

  echo ""
done
