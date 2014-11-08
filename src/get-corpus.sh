#!/bin/bash
#
# FILENAME
#   get-corpus.sh
#
# USAGE
#   Just execute ./get-corpus.sh
#
# AUTHOR
#   Jonathan D. Jones
#
# CHANGELOG
#   2014-10-19: Initial version
#

# Download pitchfork's album reviews sitemap
SITEMAP_URL='http://pitchfork.com/sitemap-album-reviews.xml'
SITEMAP_FILE='p4k-sitemap-album-reviews.xml'
wget $SITEMAP_URL -O $SITEMAP_FILE

# TODO: Compare with old sitemap?

# Extract URLs from sitemap
URLS=$(sed -r -e s:'<url>'\|'<loc>'\|'<lastmod>'\|'<changefreq>'\|' '::g -e s:'</loc>'\|'</lastmod>'\|'</changefreq>':'\t':g -e s:'</url>':'\n':g <$SITEMAP_FILE | mawk '/pitchfork/ {print $1}')

# Download the corpus
CORPUS_DIR='p4k-reviews/'
mkdir $CORPUS_DIR
while read line; do
    OUT_FILE=$(echo $line | sed -r s~'http://pitchfork.com/reviews/albums/'\|'/'~~g)
    printf "%s\t%s\n" "$line" "$OUT_FILE"
    wget $line -O "$CORPUS_DIR""$OUT_FILE"".xml"
done <<< "$URLS"
