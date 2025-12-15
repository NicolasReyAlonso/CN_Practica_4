#!/bin/sh
set -e

# Reemplaza las variables en el template y genera app.js
envsubst '${API_URL} ${API_KEY}' < /usr/share/nginx/html/app.js.template > /usr/share/nginx/html/app.js

# Inicia nginx
exec nginx -g 'daemon off;'