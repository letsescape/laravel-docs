#!/bin/bash
# Sync translated documents from laravel-docs-source repository
# Usage: ./scripts/sync-docs.sh [source_repo_url] [versions...]
#
# This script clones the translation source repository and copies
# Korean translated docs and origin documentation into the versioned_docs directory.

set -euo pipefail

SOURCE_REPO="${1:-https://github.com/kimchanhyung98/laravel-docs-source.git}"
shift || true
if [ $# -gt 0 ]; then
  VERSIONS=("$@")
else
  VERSIONS=(8.x 9.x 10.x 11.x 12.x)
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMP_DIR=$(mktemp -d)

cleanup() {
  rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

echo "Cloning source repository: $SOURCE_REPO"
git clone --depth 1 "$SOURCE_REPO" "$TEMP_DIR/laravel-docs-source"

for VERSION in "${VERSIONS[@]}"; do
  SOURCE_KO="$TEMP_DIR/laravel-docs-source/$VERSION/ko"
  SOURCE_ORIGIN="$TEMP_DIR/laravel-docs-source/$VERSION/origin"
  TARGET_DIR="$PROJECT_ROOT/versioned_docs/version-$VERSION"

  if [ ! -d "$SOURCE_KO" ]; then
    echo "Warning: Source directory not found for version $VERSION (ko), skipping."
    continue
  fi

  echo "Syncing version $VERSION..."

  # Ensure target directories exist
  mkdir -p "$TARGET_DIR/origin"

  # Copy Korean translated docs
  find "$SOURCE_KO" -maxdepth 1 -name "*.md" -exec cp {} "$TARGET_DIR/" \;

  # Copy origin documentation.md for sidebar generation
  if [ -f "$SOURCE_ORIGIN/documentation.md" ]; then
    cp "$SOURCE_ORIGIN/documentation.md" "$TARGET_DIR/origin/documentation.md"
  fi

  echo "  Done: version $VERSION"
done

echo "Document sync complete!"
