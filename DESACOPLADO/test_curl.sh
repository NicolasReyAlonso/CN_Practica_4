APIURI="https://r3qwoyw0bj.execute-api.us-east-1.amazonaws.com/prod/crumbs"
APIKEY="SQW8kZ2XRxaMe7jyCHwdB8lMgvqTma5l4nG917On"
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