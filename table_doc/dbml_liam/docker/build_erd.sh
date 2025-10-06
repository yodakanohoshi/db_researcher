#!/usr/bin/env bash
set -euo pipefail

DBML_PATH="${1:-schema.dbml}"          # 入力DBML
SQL_PATH="${4:-schema.postgres.sql}"   # 中間SQL

echo "1) DBML → PostgreSQL SQL 変換"
dbml2sql "$DBML_PATH" --postgres -o "$SQL_PATH"

echo "2) liam erd serve"
npx -y @liam-hq/cli erd build \
  --input "$SQL_PATH" \
  --format postgres \
  --output-dir out