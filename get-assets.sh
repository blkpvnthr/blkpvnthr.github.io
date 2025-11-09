#!/bin/bash
# =========================================
# Fetch local CSS/JS assets for portfolio
# =========================================

set -e

# Disable custom CA temporarily if not set up
unset SSL_CERT_FILE REQUESTS_CA_BUNDLE PIP_CERT

echo "📂 Ensuring directories..."
mkdir -p css fonts includes vendor/bootstrap-5.3.7-dist/css

# --- Animate.css ---
echo "⬇️ Downloading Animate.css..."
curl -L https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css -o css/animate.min.css

# --- Bootstrap Icons CSS + fonts ---
echo "⬇️ Downloading Bootstrap Icons..."
curl -L https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css -o css/bootstrap-icons.css
curl -L https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/fonts/bootstrap-icons.woff2 -o fonts/bootstrap-icons.woff2
curl -L https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/fonts/bootstrap-icons.woff -o fonts/bootstrap-icons.woff

# Fix CSS font paths so they work locally
sed -i.bak 's|url(./fonts/|url(../fonts/|g' css/bootstrap-icons.css
rm -f css/bootstrap-icons.css.bak

# --- jQuery ---
echo "⬇️ Downloading jQuery..."
curl -L https://code.jquery.com/jquery-3.6.0.min.js -o includes/jquery-3.6.0.min.js

# --- Bootstrap (optional: CSS only since you already have vendor folder) ---
echo "⬇️ Downloading Bootstrap CSS..."
curl -L https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css -o vendor/bootstrap-5.3.7-dist/css/bootstrap.min.css

# --- CA bundle (so curl, pip, requests work everywhere) ---
echo "⬇️ Downloading Mozilla CA bundle..."
curl -L https://curl.se/ca/cacert.pem -o ~/Documents/cacert-bundle.crt

echo "✅ All assets downloaded and ready!"
