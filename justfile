set shell := ["bash", "-euo", "pipefail", "-c"]
set allow-duplicate-recipes

# The devkit's shared recipes (uprd, pr, stack, issue-*, ...), from the tree `nix develop` links.
import? '.devkit/devkit.just'

default:
    @just --list

# Rebuild data/index.json and docs/4-reference_index.md from GitHub (needs GH_TOKEN).
refresh:
    python3 scripts/refresh.py

# Every gate CI runs.
quality:
    #!/usr/bin/env bash
    set -euo pipefail
    for tool in ruff actionlint agents-check docs-lint; do command -v "$tool" >/dev/null || { echo "quality: $tool not installed — run inside 'nix develop'" >&2; exit 1; }; done
    ruff check .
    ruff format --check .
    python3 scripts/refresh.py --self-test
    for f in data/*.json; do python3 -m json.tool "$f" > /dev/null; done
    actionlint
    agents-check
    docs-lint

# The devkit hooks' contract: fast checks at commit, the full gate at push.
precommit:
    ruff check .
    agents-check

prepush:
    just quality
