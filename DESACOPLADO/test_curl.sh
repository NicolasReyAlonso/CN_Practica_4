APIURI="https://0lqziua1y9.execute-api.us-east-1.amazonaws.com/prod/crumbs"
APIKEY="McAPKEIMdV1s6P4C5IVvr4sxz5jE9CQa7JcjqMlR"
curl -X GET "${APIURI}" \
     -H "x-api-key: ${APIKEY}"

curl -X POST "${APIURI}" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${APIKEY}" \
  -d '{
    "content": "Mi primer crumb de prueba",
    "image_url": "https://example.com/image.jpg"
  }'

curl -X POST "${APIURI}" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${APIKEY}" \
  -d '{
    "content": "Mi primer crumb de prueba",
    "image_url": "https://example.com/image.jpg"
  }'