#!/bin/sh
# Builds the standalone, installable index.html from app.html
# (adds the web-app manifest and uses the bundled three.js so it works offline).
cd "$(dirname "$0")/.." || exit 1
{
cat <<'HEAD'
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#3550f0">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Elements">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="icons/icon-180.png">
<script src="vendor/peerjs.min.js"></script>
</head>
<body>
HEAD
sed 's#https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js#vendor/three.min.js#' app.html
printf '\n</body>\n</html>\n'
} > index.html
echo "index.html built"
