#!/bin/bash
# Download Inter font .woff2 files locally
mkdir -p fonts/inter

echo "⬇️ Downloading Inter fonts..."

curl -L -o fonts/inter/inter-regular.woff2 https://fonts.gstatic.com/s/inter/v12/UcC73FwrK3iLTeHuS_fvQtMwCp50KnMa.woff2
curl -L -o fonts/inter/inter-600.woff2    https://fonts.gstatic.com/s/inter/v12/UcC73FwrK3iLTeHuS_fvQtMwCp50KnMa.woff2
curl -L -o fonts/inter/inter-700.woff2    https://fonts.gstatic.com/s/inter/v12/UcC73FwrK3iLTeHuS_fvQtMwCp50KnMa.woff2

echo "✅ Fonts saved to fonts/inter/"

