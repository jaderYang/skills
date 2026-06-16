#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
SKILLS_DIR="$REPO_DIR/skills"
TARGET="${1:-.claude/skills}"

echo "Linking skills to $TARGET ..."

mkdir -p "$TARGET"

find "$SKILLS_DIR" -mindepth 2 -maxdepth 2 -name "SKILL.md" | while read -r skill_file; do
  skill_dir="$(dirname "$skill_file")"
  skill_name="$(basename "$skill_dir")"
  category="$(basename "$(dirname "$skill_dir")")"

  [ "$category" = "deprecated" ] && continue
  [ "$category" = "in-progress" ] && continue

  ln -sfn "$skill_dir" "$TARGET/$skill_name"
  echo "  linked: $category/$skill_name"
done

echo "Done."
