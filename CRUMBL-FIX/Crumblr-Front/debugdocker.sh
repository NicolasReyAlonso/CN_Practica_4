APIURI="https://w47srh1hxg.execute-api.us-east-1.amazonaws.com/prod/crumbs"
APIKEY="EluYjKzfgFaTanNU4dwi1alO2AnAjMxLCcxISg0j"
docker run -p 8080:80 \
  -e API_URL=${APIURI} \
  -e API_KEY=${APIKEY} \
  crumblr-gui