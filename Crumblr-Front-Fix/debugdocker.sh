APIURI="https://cnvsinwx5g.execute-api.us-east-1.amazonaws.com/prod/crumbs"
APIKEY="NgBOHyxHY11a7KmqZDlNq8TZWt22xOi92Fba3oWW"
docker run -p 8080:80 \
  -e API_URL=${APIURI} \
  -e API_KEY=${APIKEY} \
  crumblr-gui