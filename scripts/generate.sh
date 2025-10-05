#!/usr/bin/env bash
#set -euo pipefail

DBML="${1:-shema.dbml}"
TMP_DIR="tmp"
OUT_DIR="out"

mkdir -p "${OUT_DIR}" "${TMP_DIR}"

echo "[1/2] DBML -> YAML変換"
python3 scripts/dbml_to_yaml.py --input-file "${DBML}" --output-file "${TMP_DIR}/schema.yaml"

echo "[2/2] DBML -> SQLファイル変換"
#dbml2sql "${DBML}" -o "${TMP_DIR}/schema.sql" --postgres

echo "[3/3] Liam ERD 生成（静的サイト）"
#npx --yes @liam-hq/cli erd build \
# --input "${TMP_DIR}/schema.sql" \
# --format postgres \
# --output-dir "${TMP_DIR}/erd"

#echo "[4/3] カラム説明とER図を結合してドキュメントに出力"
#python3 scripts/generate_docs.py --input-erd "${TMP_DIR}/erd.html" --output-html "${OUT_DIR}/index.html"
#--input-yaml "${TMP_DIR}/schema.yaml"

echo "[5/3] Viteで単一HTMLファイル化"
# Viteプロジェクトは作業ディレクトリ直下に作成
if [ ! -d "erd-singlefile" ]; then
  CI=true npm create vite@latest erd-singlefile -- --template vanilla -y <<EOF
No
EOF
fi
cd erd-singlefile
npm install
npm install vite-plugin-singlefile --save-dev --legacy-peer-deps
cat <<'EOF' > vite.config.js
import { defineConfig } from 'vite';
import singleFile from 'vite-plugin-singlefile';

export default defineConfig({
  plugins: [singleFile()]
});
EOF
mkdir -p public
cp -r ../${TMP_DIR}/erd/* public/
npm run build
cd ..
cp erd-singlefile/dist/index.html ${OUT_DIR}/singlefile.html