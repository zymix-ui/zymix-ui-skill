#!/usr/bin/env bash
# 打包 ZymixUI 原型技能 → zymix-ui-prototype.skill
# 用法: bash scripts/pack.sh
#
# 固化两条容易踩的规则:
#   1) 用默认压缩,禁用 zip -0 —— store 会让包体积虚增约 3 倍
#   2) 排除 tokens/(真源,使用者只需 references/tokens.css)与产物/本地配置
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT="$(pwd)"
OUT="$ROOT/zymix-ui-prototype.skill"
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

mkdir -p "$STAGE/zymix-ui-prototype"
rsync -a \
  --exclude='.DS_Store' \
  SKILL.md README.md DESIGN.md TOKENS-GUIDE.md PROTOTYPE-GUIDE.md .gitignore \
  references scripts assets \
  "$STAGE/zymix-ui-prototype/"

rm -f "$OUT"
( cd "$STAGE" && zip -r -X -q "$OUT" zymix-ui-prototype )

echo "written $OUT ($(wc -c < "$OUT" | tr -d ' ') bytes, $(unzip -l "$OUT" | tail -1 | awk '{print $2}') files)"
unzip -t "$OUT" > /dev/null && echo "zip 完整性 OK"
