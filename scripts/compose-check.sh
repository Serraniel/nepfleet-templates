#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# Parses every template's compose file with `docker compose config`, using
# placeholder values for its variables.
set -euo pipefail
cd "$(dirname "$0")/.."
failed=0
for dir in system/*/ apps/*/; do
  dir=${dir%/}
  envs=()
  for v in $(grep -oE '\$\{[A-Z_][A-Z0-9_]*' "$dir/compose.yaml" | cut -c3- | sort -u); do
    case $v in
      *PORT) val=1234 ;;
      BIND_ADDR) val=127.0.0.1 ;;
      *PATH) val=/tmp ;;
      *) val=placeholder ;;
    esac
    envs+=("$v=$val")
  done
  if out=$(cd "$dir" && env "${envs[@]}" docker compose -f compose.yaml config -q 2>&1); then
    echo "ok   $dir"
  else
    echo "FAIL $dir: $out"
    failed=1
  fi
done
exit $failed
