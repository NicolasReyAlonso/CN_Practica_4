


🏗️ Arquitecturas
1️⃣ Arquitectura Acoplada (Crumblr-Back / Crumblr-Front)
Componentes:

Frontend: Aplicación web estática (HTML/CSS/JS) servida por Nginx en contenedor Docker
Backend: API REST monolítica en Python
Base de datos: PostgreSQL en RDS
Infraestructura: EC2 con contenedores Docker

Características:

Todo el código backend en un único servicio
Despliegue simple pero menos escalable
Ideal para desarrollo rápido y testing

Estructura:
Crumblr-Back/
├── db/                 # Capa de acceso a datos
│   ├── db.py          # Interfaz abstracta
│   ├── factory.py     # Factory pattern para DB
│   └── postgres_db.py # Implementación PostgreSQL
├── models/
│   └── crumb.py       # Modelo de datos
└── main.py            # API REST principal

Crumblr-Front/
├── index.html         # Interfaz de usuario
├── app.js            # Lógica del cliente
├── style.css         # Estilos
└── nginx.conf        # Configuración Nginx

2️⃣ Arquitectura Desacoplada (DESACOPLADO/)
Componentes:

Frontend: Mismo que en arquitectura acoplada
Backend: 5 Lambda functions independientes (CRUD)
API Gateway: Enrutamiento y gestión de APIs
Base de datos: PostgreSQL en RDS
ECR: Repositorios de imágenes Docker para cada Lambda

Características:

Escalabilidad automática por función
Pago por uso (solo cuando se ejecutan)
Alta disponibilidad y tolerancia a fallos
Implementación de principios de microservicios

Funciones Lambda:
FunciónMétodo HTTPRutaDescripcióncreate-crumbPOST/crumbsCrear nuevo crumbget-crumbsGET/crumbsListar todos los crumbsget-crumbGET/crumbs/{id}Obtener crumb específicoupdate-crumbPUT/crumbs/{id}Actualizar crumbdelete-crumbDELETE/crumbs/{id}Eliminar crumb
Estructura:
DESACOPLADO/
├── Crumblr-Back/
│   └── lambda/
│       ├── functions/
│       │   ├── create-crumb/
│       │   │   ├── app.py           # Handler Lambda
│       │   │   ├── dockerfile       # Imagen Docker
│       │   │   ├── buildandpush.sh  # Script deploy
│       │   │   └── shared/          # Código compartido
│       │   │       ├── db/
│       │   │       ├── models/
│       │   │       └── services/
│       │   ├── get-crumb/
│       │   ├── get-crumbs/
│       │   ├── update-crumb/
│       │   └── delete-crumb/
│       └── shared/                  # Código fuente original
└── main.yml                         # CloudFormation template

🚀 Despliegue
Arquitectura Acoplada
bash# 1. Desplegar base de datos
aws cloudformation create-stack \
  --stack-name crumblr-db \
  --template-body file://db_postgres.yml \
  --parameters ...

# 2. Construir y subir imágenes Docker
cd Crumblr-Back
./buildandpush.sh

cd ../Crumblr-Front
./buildandpush.sh

# 3. Desplegar EC2 con contenedores
aws cloudformation create-stack \
  --stack-name crumblr-monolith \
  --template-body file://main.yml \
  --parameters ...
Arquitectura Desacoplada
bash# 1. Desplegar base de datos
aws cloudformation create-stack \
  --stack-name crumblr-db \
  --template-body file://DESACOPLADO/db_postgres.yml \
  --parameters ...

# 2. Crear repositorios ECR para cada Lambda
cd DESACOPLADO/Crumblr-Back/lambda/functions/create-crumb
aws cloudformation create-stack \
  --stack-name create-crumb-ecr \
  --template-body file://ecr.yml

# Repetir para cada función...

# 3. Construir y subir imágenes Docker de todas las Lambdas
cd DESACOPLADO/Crumblr-Back
./BUILDANDPUSHALL.sh

# 4. Desplegar API Gateway + Lambdas
aws cloudformation create-stack \
  --stack-name crumblr-serverless \
  --template-body file://DESACOPLADO/main.yml \
  --parameters \
    ParameterKey=VpcId,ParameterValue=vpc-xxxxx \
    ParameterKey=SubnetIds,ParameterValue=subnet-xxx\\,subnet-yyy \
    ParameterKey=DBHost,ParameterValue=tu-db-endpoint.rds.amazonaws.com \
    ParameterKey=DBName,ParameterValue=crumblr_db \
    ParameterKey=DBUser,ParameterValue=postgres \
    ParameterKey=DBPass,ParameterValue=tu-password

# 5. Obtener API Key
./getapikey.sh

# 6. Desplegar Frontend
cd DESACOPLADO/Crumblr-Front
# Actualizar app.js con el API endpoint y key
./buildandpush.sh

🔑 Obtener credenciales del API
bash# Obtener el endpoint del API
aws cloudformation describe-stacks \
  --stack-name crumblr-serverless \
  --query 'Stacks[0].Outputs[?OutputKey==`APIEndpoint`].OutputValue' \
  --output text

# Obtener la API Key
aws cloudformation describe-stacks \
  --stack-name crumblr-serverless \
  --query 'Stacks[0].Outputs[?OutputKey==`APIKeyId`].OutputValue' \
  --output text

# Luego obtener el valor de la key
aws apigateway get-api-key \
  --api-key <API_KEY_ID> \
  --include-value \
  --query 'value' \
  --output text

🧪 Testing con curl
Crear un crumb
bashcurl -X POST https://API_ID.execute-api.REGION.amazonaws.com/prod/crumbs \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{"content":"Hello World!","image_url":"https://example.com/image.jpg"}'
Listar todos los crumbs
bashcurl -X GET https://API_ID.execute-api.REGION.amazonaws.com/prod/crumbs \
  -H "x-api-key: YOUR_API_KEY"
Obtener un crumb específico
bashcurl -X GET https://API_ID.execute-api.REGION.amazonaws.com/prod/crumbs/{id} \
  -H "x-api-key: YOUR_API_KEY"
Actualizar un crumb
bashcurl -X PUT https://API_ID.execute-api.REGION.amazonaws.com/prod/crumbs/{id} \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{"content":"Updated content"}'
Eliminar un crumb
bashcurl -X DELETE https://API_ID.execute-api.REGION.amazonaws.com/prod/crumbs/{id} \
  -H "x-api-key: YOUR_API_KEY"

📦 Tecnologías Utilizadas
Backend

Python 3.11: Lenguaje principal
psycopg2: Driver PostgreSQL
pydantic: Validación de datos
AWS Lambda: Funciones serverless (desacoplado)
FastAPI/Flask: Framework web (acoplado)

Frontend

HTML5/CSS3/JavaScript: Stack web clásico
Nginx: Servidor web
Docker: Containerización

Infraestructura AWS

Lambda: Compute serverless
API Gateway: REST API management
RDS PostgreSQL: Base de datos relacional
ECR: Repositorio de imágenes Docker
EC2: Máquinas virtuales (acoplado)
CloudFormation: Infrastructure as Code
CloudWatch: Logs y monitoreo


🗂️ Modelo de Datos
Crumb
python{
    "crumb_id": "uuid-string",
    "content": "string",
    "image_url": "string (opcional)",
    "created_at": "datetime (ISO 8601)"
}
Esquema PostgreSQL
sqlCREATE TABLE crumbs (
    crumb_id VARCHAR(36) PRIMARY KEY,
    content TEXT NOT NULL,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

🔧 Configuración de Variables de Entorno
Lambda Functions
bashDB_TYPE=postgres
DB_HOST=your-db-endpoint.rds.amazonaws.com
DB_NAME=crumblr_db
DB_USER=postgres
DB_PASS=your-password
DB_DYNAMONAME=crumbs  # Si se usa DynamoDB

📊 Comparación de Arquitecturas
CaracterísticaAcopladaDesacopladaEscalabilidadVertical (EC2 más grande)Horizontal automáticaCostoFijo (EC2 siempre corriendo)Por uso (pay-per-request)ComplejidadBajaMedia-AltaTiempo de deployMás lentoMás rápido (por función)MantenimientoUn servicioMúltiples funcionesDisponibilidadDepende de EC2Multi-AZ automáticoCold startsNo aplicaSí (primeras ejecuciones)

🛠️ Troubleshooting
Lambda: "No module named 'db'"

Causa: Falta __init__.py en carpetas o imports incorrectos
Solución: Agregar __init__.py en shared/, shared/db/, shared/models/, shared/services/

Lambda: "datetime is not JSON serializable"

Causa: El objeto datetime no se puede serializar directamente
Solución: Usar .isoformat() en los handlers

API Gateway: "Missing Authentication Token"

Causa: Falta el header x-api-key
Solución: Incluir -H "x-api-key: YOUR_KEY" en las peticiones

CloudFormation: "CloudWatch Logs role ARN must be set"

Causa: Cuenta sin rol de CloudWatch configurado
Solución: Eliminar MethodSettings del Stage o configurar el rol


📝 Scripts Útiles
BUILDANDPUSHALL.sh
Construye y sube todas las imágenes Lambda a ECR
buildandpush.sh (individual)
Construye y sube una imagen específica
reload_lambda.sh
Fuerza la actualización de las funciones Lambda con las nuevas imágenes
getapikey.sh
Obtiene la API Key del stack de CloudFormation
test_curl.sh
Suite de pruebas curl para validar el API

👥 Autores
Proyecto desarrollado como práctica de Computación en la Nube - ULPGC

📄 Licencia
Este proyecto es material educativo para la asignatura de Computación en la Nube.



# Practica Entregable: CRUMBLR
## Descripción de la aplicación
Crumblr es una página web sucesora espiritual de tumblr en la que es posible hacer microblogging con capacidad de estilo de html. En el proyecto se encuentras dos implementaciones, la primera es la que se encuentra en la carpeta raíz, que es la acoplada, y en mi opinión, la más correcta para el volumen de la aplicación.

Por otra parte se encuentra la versión Desacoplada en ["DESACOPLADO"](./DESACOPLADO/). Esta versión para el modelo de negocio de mi aplicación supone más que una mejora de escalabilidad, un problema de encarecimiento ya que el uso de lambdas dispara el coste del lanzamiento con que la usen un par de miles de usuarios.

- **Arquitectura "Acoplada":** 
  - Monolito tradicional con ECS Fargate + API Gateway
  - Frontend que utiliza el mismo ECS Fargate
- **Arquitectura Desacoplada:** 
  - Microservicios con Lambda + API Gateway
  - Frontend separado en un ECS Fargate


## Bases de datos:
- Postgres
Utilicé postgres porque es la base de datos con la que estoy más familiarizado y porque encaja bien con el tipo de aplicación que estoy creando.

### Diagrama de arquitectura
#### Arquitectura "Acoplada": 
![Diagrama de la práctica](Diagram.png)

#### Arquitectura Desacoplada:


### Componentes principales **ACOPLADO**

- **API Gateway (REST)**: expone los recursos `crumbs` y `crum` y enruta al backend vía VPC Link. Protegido con API Key.
- **VPC Link + NLB**: el VPC Link conecta API Gateway con un Network Load Balancer interno que apunta al servicio de ECS.
- **ECS Fargate 1**: ejecuta el contenedor de la app Flask definido en `/Crumblr-Front/Dockerfile` y `/Crumblr-Front/mainFront.yml`.
- **ECS Fargate 2**: ejecuta el contenedor del frontend `Dockerfile` y `main.yml`.
- **Bases de datos**:
  - **PostgreSQL (Amazon RDS)** en el VPC, con SG de acceso al puerto 5432.
  - **Amazon DynamoDB** como alternativa NoSQL de tabla única.
- **Amazon ECR**: repositorio para la imagen del contenedor.

### Componentes principales **ACOPLADO**

- **API Gateway (REST)**: expone los recursos `crumbs` y `crum` y enruta al backend vía VPC Link. Protegido con API Key.
- **VPC Link + NLB**: el VPC Link conecta API Gateway con un Network Load Balancer interno que apunta al servicio de ECS.
- **ECS Fargate**: ejecuta el contenedor de la app Flask definido en `Dockerfile` y `main.yml`.
- **Bases de datos**:
  - **PostgreSQL (Amazon RDS)** en el VPC, con SG de acceso al puerto 5432.
  - **Amazon DynamoDB** como alternativa NoSQL de tabla única.
- **Amazon ECR**: repositorio para la imagen del contenedor.

### Estructura del proyecto

- `app/main.py`: aplicación Flask con endpoints y CORS.
- `app/models/ticket.py`: modelo `Ticket` con validación Pydantic.
- `app/db/db.py`: interfaz abstracta de base de datos.
- `app/db/postgres_db.py`: implementación PostgreSQL.
- `app/db/dynamodb_db.py`: implementación DynamoDB.
- `app/db/factory.py`: selecciona la implementación según `DB_TYPE`.
- `Dockerfile`: imagen de la aplicación.
- `requirements.txt`: dependencias Python.
- `main.yml`: plantilla CloudFormation para API Gateway + VPC Link + NLB + ECS Fargate.
- `db_postgres.yml`: plantilla para RDS PostgreSQL.
- `db_dynamodb.yml`: plantilla para la tabla DynamoDB mínima.
- `ecr.yml`: plantilla para el repositorio ECR.
- `postgres.sql`: script SQL equivalente para crear la tabla localmente.
- `frontend.html`: HTML básico para probar la API vía API Gateway.

### API

- **POST** `/items`: crea un ticket.
- **GET** `/items`: lista de tickets.
- **GET** `/items/{ticket_id}`: obtiene un ticket.
- **PUT** `/items/{ticket_id}`: actualiza un ticket.
- **DELETE** `/items/{ticket_id}`: borra un ticket.
- **GET** `/health`: comprobación de vida.

Las respuestas de error gestionan validación (`pydantic`), integridad/operación de PostgreSQL y errores de DynamoDB.

### Variables de entorno

- **DB_TYPE**: `postgres` (por defecto) o `dynamodb`.
- Si `DB_TYPE=postgres`:
  - **DB_HOST**, **DB_NAME**, **DB_USER**, **DB_PASS**.
- Si `DB_TYPE=dynamodb`:
  - **DB_DYNAMONAME**: nombre de la tabla (por defecto `tickets`).

### Ejecución local (opcional)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Ejemplo usando PostgreSQL local
export DB_TYPE=postgres DB_HOST=localhost DB_NAME=ticketsdb DB_USER=postgres DB_PASS=postgres
python app/main.py
# La API quedará en http://localhost:8080
```

### Contenedor

```bash
# Construir
docker build -t tickets-app:latest .
# Ejecutar
docker run --rm -p 8080:8080 \
  -e DB_TYPE=postgres \
  -e DB_HOST=host.docker.internal -e DB_NAME=ticketsdb -e DB_USER=postgres -e DB_PASS=postgres \
  tickets-app:latest
```

### Despliegue en AWS (CloudFormation)

Orden recomendado de plantillas:

1. `ecr.yml` → crea el repositorio y subir la imagen.
2. `db_postgres.yml` o `db_dynamodb.yml` → crea la base de datos elegida.
3. `main.yml` → despliega VPC Link, NLB, ECS Fargate, API Gateway y enlaza la imagen y variables.

Parámetros clave de `main.yml`:

- **ImageName**: `<repo>:<tag>` en ECR.
- **VpcId**, **SubnetIds**: VPC y subredes existentes.
- **DBType**: `postgres` o `dynamodb`.
- Campos de DB correspondientes: `DBHost`, `DBName`, `DBUser`, `DBPass` o `DBDynamoName`.

### Probar con `frontend.html`

`frontend.html` es una página estática que consume los endpoints del API Gateway usando `fetch` y la cabecera `x-api-key`.

Uso rápido:

1. Abrir el archivo `frontend.html` en el navegador (doble clic o `file:///...`).
2. En el modal de configuración inicial, introducir:
   - **API URL**: la URL del Stage (por ejemplo, `https://<rest-api-id>.execute-api.us-east-1.amazonaws.com/prod`).
   - **API Key**: el valor de la API Key creada por `main.yml`.
3. Pulsar “Conectar”.
4. Crear/editar/mover tickets en el tablero. Las operaciones llaman a `POST /items`, `GET /items`, `PUT /items/{id}` y `DELETE /items/{id}` del API Gateway.

Notas:

- La configuración (URL y API Key) se guarda en `localStorage` del navegador.
- Si la API Key no es válida o el CORS falla, la app mostrará un mensaje de error.

### Notas

- La región de las prácticas es `us-east-1`.
- El contenedor expone el puerto 8080 y el NLB escucha en el mismo puerto.
- Se deja tanto el grupo de seguridad de la tarea de ECS como de la BBDD abierto para que los alumnos puedan acceder desde fuera para validar su trabajo. Permitiéndoles debuggear de forma sencilla.
