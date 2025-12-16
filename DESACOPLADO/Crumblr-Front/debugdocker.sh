APIURI="https://r3qwoyw0bj.execute-api.us-east-1.amazonaws.com/prod/crumbs"
APIKEY="SQW8kZ2XRxaMe7jyCHwdB8lMgvqTma5l4nG917On"
docker run -p 8080:80 \
  -e API_URL=${APIURI} \
  -e API_KEY=${APIKEY} \
  crumblr-gui