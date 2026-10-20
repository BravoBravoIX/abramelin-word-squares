#!/usr/bin/env bash
# Rerun the whole study from the fetched sources.
# Usage: code/run_all.sh SOURCE_DIR [WORK_DIR]    (SOURCE_DIR filled by scripts/fetch_sources.sh;
#        WORK_DIR, default work/, holds Kollatsch's squares as parsed; git ignores it)
# Needs pdftotext (poppler) and uv, which supplies Python 3.13 with numpy 2.5.4 and scipy 1.18.1,
# the versions the results were made with (set PYTHON to use another interpreter with both).
# CPU only; the three analysis runs go in parallel under nice -n 19, about 5 minutes in all.
set -euo pipefail
SRC="$(cd "$1" && pwd)"
HERE="$(cd "$(dirname "$0")" && pwd)"
WORK="${2:-$HERE/../work}"
mkdir -p "$WORK/logs"
WORK="$(cd "$WORK" && pwd)"
read -r -a PY <<< "${PYTHON:-uv run --no-project --python 3.13 --with numpy==2.5.4 --with scipy==1.18.1 python}"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$HERE"

# W1: Kollatsch's figures, parsed into WORK only (CC BY-NC-ND 4.0: no derivative goes into git)
pdftotext -bbox "$SRC/kollatsch/buchstabenquadrate.pdf" "$WORK/w1_bbox.html"
"${PY[@]}" parse_w1.py "$WORK/w1_bbox.html" "$WORK/w1_squares.json" > "$WORK/logs/parse_w1.log"
# M: Mathers 1900, parsed into data/m_squares.json (public domain; git shows any change)
pdftotext -bbox "$SRC/mathers/Abramelin_3.pdf" "$WORK/m3_bbox.html"
"${PY[@]}" parse_mathers.py "$WORK/m3_bbox.html" ../data/m_squares.json > "$WORK/logs/parse_mathers.log"
# Tests A, B and C: primary (pre-registered), no i/j u/v folding (pre-registered secondary),
# and I/T folded (post hoc)
for opt in "" --nofold --fold-it; do
  nice -n 19 "${PY[@]}" analyse.py "$WORK/w1_squares.json" $opt > "$WORK/logs/analyse${opt}.log" 2>&1 &
done
wait
for tag in "" _nofold _foldit; do
  "${PY[@]}" summary.py ../results "$tag" > "$WORK/logs/summary${tag}.log"
done
echo "done; logs in $WORK/logs"
