
APIURI="https://rz7bkepbwj.execute-api.us-east-1.amazonaws.com/prod/crumbs"
APIKEY="WyUFVGjQSj7EfA9GCc1Lj7v1abUKrpbGusFN5lr5"

curl -X POST "${APIURI}" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${APIKEY}" \
  -d '{"content":"Hello World!","image_url":"https://example.com/image.jpg"}'
# Listar todos los crumbs
curl -X GET "${APIURI}" \
  -H "x-api-key: ${APIKEY}"
# Obtener un crumb específico
curl -X GET "${APIURI}/{id}" \
  -H "x-api-key: ${APIKEY}"
# Actualizar un crumb
curl -X PUT "${APIURI}/{id}" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${APIKEY}" \
  -d '{"content":"Updated content"}'
# Eliminar un crumb
curl -X DELETE "${APIURI}/{id}" \
  -H "x-api-key: ${APIKEY}"


