#!/usr/bin/env bash
# Download the public sources this study is built from, into SOURCE_DIR, and check them against
# the SHA-256 sums of the copies used for the published results (sources/SHA256SUMS).
# None of these files is redistributed here; each stays under its own terms (README, Licensing).
# Every download uses HTTPS with the certificate verified (curl's default).
# Needs bash, curl and sha256sum.
# Usage: scripts/fetch_sources.sh SOURCE_DIR
#        WITH_L_IMAGES=1 scripts/fetch_sources.sh SOURCE_DIR   (also the Leipzig page images, 99 MB)
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
SUMS="$HERE/sources/SHA256SUMS"
OUT="$1"
mkdir -p "$OUT"/kollatsch "$OUT"/mathers
UA="abramelin-word-squares source fetch (one request at a time)"
get() { [ -s "$2" ] || { curl -fsSL --proto '=https' --retry 3 -A "$UA" -o "$2.part" "$1" && mv "$2.part" "$2"; sleep 1; }; }

# 1. Rick-Arne Kollatsch (2021), Figures of the 257 magical letter squares (witness W1,
#    Cod. Guelf. 47.13 Aug. 4°, as edited), KCWorks doi:10.17613/3hfq-9a74, CC BY-NC-ND 4.0.
#    Read locally only; never redistributed, and nothing derived from it is written into git.
#    The KCWorks records API answers the file request with a signed storage URL, fetched next.
K="$OUT/kollatsch/buchstabenquadrate.pdf"
if [ ! -s "$K" ]; then
  curl -fsSL --proto '=https' --retry 3 -A "$UA" -o "$K.part" \
    "https://works.hcommons.org/api/records/xep4n-asx54/files/buchstabenquadrate.pdf/content"
  if head -c 8 "$K.part" | grep -q '^https://'; then
    url="$(tr -d '\r\n' < "$K.part")"
    curl -fsSL --proto '=https' --retry 3 -A "$UA" -o "$K.part" "$url"
  fi
  mv "$K.part" "$K"
  sleep 1
fi

# 2. S. L. MacGregor Mathers, The Book of the Sacred Magic of Abra-Melin the Mage, 2nd ed. (1900),
#    Book III, as typeset in a 1999 digital edition; archive.org item sacred-magic-abramelin
#    (Public Domain Mark).
get https://archive.org/download/sacred-magic-abramelin/Abramelin_3.pdf "$OUT/mathers/Abramelin_3.pdf"

# 3. Optional: the page images of the squares section of Leipzig UB Cod. mag. 15 (witness L),
#    from the archive.org mirror of the UB Leipzig digitisation (Public Domain Mark), JPEG 2000,
#    91 images. Image _00NN is page pNNN in data/L_read.json. Not needed to rerun the analysis;
#    only to check the transcription against the manuscript.
if [ "${WITH_L_IMAGES:-0}" = 1 ]; then
  mkdir -p "$OUT/leipzig"
  get "https://archive.org/download/Abramelin-CabalaMysticaAegyptiorum-CarrMagiques-1750_232/CabalaMysticaAegyptiorumEtPatriarcharumDasIstDasBuchDerWahrenAltenUndGttlichenMagiaGeschriebenVonAbrahamDenSohnSimonis-CarrMagiques-1750_jp2.zip" \
      "$OUT/leipzig/Cod_mag_15_squares_jp2.zip"
fi

# Check every file present against the sums of the copies used for the published results.
status=0
cd "$OUT"
while read -r sum path; do
  [ -e "$path" ] || continue
  if [ "$(sha256sum "$path" | cut -d' ' -f1)" = "$sum" ]; then
    echo "OK       $path"
  else
    echo "CHANGED  $path (differs from the copy the results were made from; results may differ)" >&2
    status=1
  fi
done < "$SUMS"
exit $status
