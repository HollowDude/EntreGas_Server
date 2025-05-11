https://entregas-server.onrender.com/v1/
## Table of Contents
- [🔐 AuthViewSet](#-authviewset)
- [🔑 PasswordResetViewSet](#-passwordresetviewset)
- [🛢️ CilindroViewSet](#️-cilindroviewset)
- [👷 TrabajadorViewSet](#-trabajadorviewset)
- [👥 ClienteViewSet](#-clienteviewset)
- [🚚 Comprobante_AbastecimientoViewSet](#-comprobante_abastecimientoviewset)
- [🚚 Comprobante_EntregaViewSet](#-comprobante_entregaviewset)
- [🔄 Reporte_DevolucionViewSet](#-reporte_devolucionviewset)

---

## 🔐 AuthViewSet

> **Base URL:** `/v1/auth/`  
> **Authentication:**
> - login → **AllowAny**
> - logout, check_auth → **IsAuthenticated**
> - Uses Django _session cookies_ (not JWT)

### Endpoints

<<<<<<< HEAD
### 1. POST /v1/auth/login/
=======
### 1. POST /api/auth/login/
>>>>>>> deefcce04c5c7979f71e91ac130616c92ea8e22f
- **Description:** Logs in and creates server session
- **Request Body (JSON):**
  ```json
  {
    "username": "string",       // required
    "password": "string",       // required
    "recordar": true|false      // optional, default false
  }
  ```
- **Behavior:**
  - Validates credentials with authenticate()
  - If recordar=true: session expires in 30 days; otherwise at browser close
  - Detects if user is Trabajador or Cliente and returns appropriate data
- **Successful Responses (200 OK):**
  - **Trabajador**:
    ```json
    {
      "message": "Inicio de sesión exitoso",
      "tipo_usuario": "trabajador",
      "puesto": "jefe de servicio",
      "username": "pepito"
    }
    ```
  - **Cliente**:
    ```json
    {
      "message": "Inicio de sesión exitoso",
      "tipo_usuario": "cliente",
      "tipo_cliente": "especial",
      "username": "juanito"
    }
    ```
  - **Other (superuser or other case)**:
    ```json
    {
      "message": "Inicio de sesión exitoso"
    }
    ```
- **Error (400 Bad Request):**
  ```json
  { "error": "Credenciales inválidas" }
  ```

<<<<<<< HEAD
### 2. POST /v1/auth/logout/
=======
### 2. POST /api/auth/logout/
>>>>>>> deefcce04c5c7979f71e91ac130616c92ea8e22f
- **Description:** Logs out current session
- **Headers:** Must send Django session cookie
- **Permissions:** IsAuthenticated
- **Response (200 OK):**
  ```json
  { "message": "Sesión cerrada" }
  ```

<<<<<<< HEAD
### 3. GET /v1/auth/check_auth/
=======
### 3. GET /api/auth/check_auth/
>>>>>>> deefcce04c5c7979f71e91ac130616c92ea8e22f
- **Description:** Checks if session is active
- **Headers:** Must send session cookie
- **Permissions:** IsAuthenticated
- **Response (200 OK):**
  ```json
  { "username": "pepito" }
  ```

> **Note:** These endpoints use _session cookies_. Ensure your client (frontend or Postman) allows and forwards cookies.

---

## 🔑 PasswordResetViewSet

> **Base URL:** `/v1/password-reset/`  
> **Permissions:** AllowAny (no auth required)  
> **Supported Methods:** POST, GET

### Serializers

- **PasswordResetRequestSerializer**
  ```python
  class PasswordResetRequestSerializer(serializers.Serializer):
      email = serializers.EmailField()
  ```

- **PasswordResetConfirmSerializer**
  ```python
  class PasswordResetConfirmSerializer(serializers.Serializer):
      token = serializers.CharField()
      new_password = serializers.CharField(min_length=8)
  ```

### Endpoints

### 1. Request Reset Link
- **Method:** POST
- **URL:** `/v1/password-reset/request_reset/`
- **Body (JSON):**
  ```json
  { "email": "usuario@uci.cu" }
  ```
- **Flow:**
  1. Validates email exists
  2. Generates JWT access token (5 hour lifespan)
  3. Builds link: `http://localhost:5173/new-password/<token>`
  4. Sends email with subject "Recuperación de contraseña" and body:
     ```
     Hola <username>,
     
     Para restablecer tu contraseña, haz click en el siguiente enlace:
     
     <link>
     
     El enlace expirará en 5 horas.
     ```
- **Responses:**
  - **200 OK:**
    ```json
    {
      "detail": "Se ha enviado un enlace de recuperación a tu correo uci.",
      "token": "<token>"
    }
    ```
  - **400 Bad Request:** serializer validation errors
  - **404 Not Found:** `{ "detail": "No existe un usuario con este correo electrónico." }`

### 2. Validate Token
- **Method:** GET
- **URL:** `/v1/password-reset/validate_token/`
- **Query Params:** `?token=<token>`
- **Description:** Verifies JWT is well-formed and not expired
- **Responses:**
  - **200 OK:** `{ "detail": "Token válido." }`
  - **400 Bad Request:**
    - If no token: `{ "detail": "Token no proporcionado." }`
    - If invalid/expired: `{ "detail": "Token inválido o expirado." }`

### 3. Reset Password
- **Method:** POST
- **URL:** `/v1/password-reset/reset_password/`
- **Body (JSON):**
  ```json
  {
    "token": "<token>",
    "new_password": "nuevaContraseña123"
  }
  ```
- **Flow:**
  1. Validates data with PasswordResetConfirmSerializer
  2. Decodes token; extracts user_id
  3. Finds User and updates password
- **Responses:**
  - **200 OK:** `{ "detail": "Contraseña actualizada correctamente." }`
  - **400 Bad Request:**
    - Serializer errors
    - Invalid/expired token or user doesn't exist:
      ```json
      { "detail": "Token inválido o expirado." }
      ```

> **Final Note:**
> - Ensure you send the token correctly in each request
> - The frontend URL (localhost:5173) should be adjusted for your production environment
> - Email is sent from settings.DEFAULT_FROM_EMAIL

---

## 🛢️ CilindroViewSet

> **Base URL:** `/v1/cilindros/`  
> **Permissions:**
> - **IsAuthenticated**
> - **CustomAccessPermission**
> - Uses _session cookies_ or your configured auth scheme

### Model
```python
class Cilindro(models.Model):
    num = CharField("Número de serie", blank=True, null=True, max_length=255)
    fehca_llegada = DateField(default=date.today)
    defectuoso = BooleanField(default=False)
    lleno = BooleanField(default=True)
    asign = ForeignKey(Cliente, on_delete=SET_NULL, null=True, blank=True)
```

### Endpoints

### 1. List All Cylinders
- **Method:** GET
- **URL:** `/v1/cilindros/`
- **Description:** Returns complete list of cylinders including assignment data
- **Response (200 OK):**
  ```json
  [
    {
      "id": 1,
      "num": "ABC123",
      "fehca_llegada": "2025-05-09",
      "defectuoso": false,
      "lleno": true,
      "asign": 5
    },
    { … }
  ]
  ```

### 2. Retrieve Cylinder by ID
- **Method:** GET
- **URL:** `/v1/cilindros/{id}/`
- **Response (200 OK):**
  ```json
  {
    "id": 1,
    "num": "ABC123",
    "fehca_llegada": "2025-05-09",
    "defectuoso": false,
    "lleno": true,
    "asign": 5
  }
  ```
- **Error (404 Not Found):**
  ```json
  { "detail": "Not found." }
  ```

### 3. Create New Cylinder
- **Method:** POST
- **URL:** `/v1/cilindros/`
- **Body (JSON):**
  ```json
  {
    "num": "XYZ789",           // optional, can be empty or null
    "fehca_llegada": "2025-05-10",
    "defectuoso": false,
    "lleno": true,
    "asign": 3                 // ID of assigned Client (or null)
  }
  ```
- **Success (201 Created):** Returns created cylinder
- **Validation Error (400):** `{ "error": "…ValidationError…" }`
- **Unexpected Error (500):** `{ "error": "Un error inesperado ha ocurrido …" }`

### 4. Update Cylinder (Full Replacement)
- **Method:** PUT
- **URL:** `/v1/cilindros/{id}/`
- **Body:** Same fields as create
- **Success (200 OK):** Returns updated cylinder
- **Errors:** Same as create

### 5. Partial Update
- **Method:** PATCH
- **URL:** `/v1/cilindros/{id}/`
- **Body:** Only fields to update
- **Success (200 OK):** Returns updated cylinder
- **Errors:** Same as PUT

### 6. Delete Cylinder
- **Method:** DELETE
- **URL:** `/v1/cilindros/{id}/`
- **Success (204 No Content):**
  ```json
  { "message": "Cilindro con id {id} eliminado" }
  ```
- **Errors:** Same as create

### 7. Cylinders Without Serial Number
- **Method:** GET
- **URL:** `/v1/cilindros/sin-numero/`
- **Description:** Returns cylinders where num is null or ""
- **Response (200 OK):**
  ```json
  [
    { "id": 3, "num": null, … },
    { "id": 7, "num": "", … }
  ]
  ```

### 8. Cylinders With Serial Number
- **Method:** GET
- **URL:** `/v1/cilindros/con-numero/`
- **Description:** Returns cylinders where num is not empty
- **Response (200 OK):**
  ```json
  [
    { "id": 1, "num": "ABC123", … },
    { "id": 2, "num": "DEF456", … }
  ]
  ```

> **Tip:** Ensure your client forwards session cookies and has correct auth headers configured.

---

## 👷 TrabajadorViewSet

> **Base URL:** `/v1/trabajador/`  
> **Permissions:**
> - **IsAuthenticated**
> - **CustomAccessPermission**
>   - **Superuser** or **Trabajador.puesto='administrador'**: full access
>   - **Jefe de servicio** and **Clientes**: no permissions for this endpoint

### Model
```python
class Trabajador(models.Model):
    user = OneToOneField(User, on_delete=CASCADE)
    puesto = CharField(
        choices=[
            ("tecnico", "Tecnico"),
            ("jefe de servicio", "Jefe de Servicio")
        ],
        max_length=255
    )
```

### Serializer
```python
class TrabajadorSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested

    class Meta:
        model = Trabajador
        fields = ['id', 'user', 'puesto']
```

### Endpoints

### 1. List Workers
- **Method:** GET
- **URL:** `/v1/trabajador/`
- **Permissions:** Administrators only
- **Response (200 OK):**
  ```json
  [
    {
      "id": 1,
      "user": {
        "id": 2,
        "username": "juan",
        "first_name": "Juan",
        "last_name": "Pérez",
        "email": "juan@uci.cu"
      },
      "puesto": "tecnico"
    },
    …
  ]
  ```

### 2. Retrieve Worker
- **Method:** GET
- **URL:** `/v1/trabajador/{id}/`
- **Permissions:** Administrators (or same worker via object permission)
- **Response (200 OK):** Same as list but single object
- **Error (404):** `{ "detail": "Not found." }`

### 3. Create Worker
- **Method:** POST
- **URL:** `/v1/trabajador/`
- **Body (JSON):**
  ```json
  {
    "user": {
      "username": "maria",
      "password": "secreto123",
      "first_name": "María",
      "last_name": "González",
      "email": "maria@uci.cu"
    },
    "puesto": "jefe de servicio"
  }
  ```
- **Responses:**
  - **201 Created:** Created Trabajador with nested user
  - **400 Bad Request:** `{ "error": "…ValidationError…" }`
  - **500 Internal Server Error:** `{ "error": "Un error inesperado ha ocurrido …" }`

### 4. Update Worker (Full Replacement)
- **Method:** PUT
- **URL:** `/v1/trabajador/{id}/`
- **Body:** Same fields as create
- **Permissions:** Administrators only
- **Responses:**
  - **200 OK:** Updated data
  - **400 / 500:** `{ "error": … }`

### 5. Partial Update
- **Method:** PATCH
- **URL:** `/v1/trabajador/{id}/`
- **Body:** Only fields to update
- **Permissions:** Administrators only
- **Responses:** Same as PUT, success → 200 OK

### 6. Delete Worker
- **Method:** DELETE
- **URL:** `/v1/trabajador/{id}/`
- **Permissions:** Administrators only
- **Responses:**
  - **204 No Content:**
    ```json
    { "message": "Trabajador con id {id} eliminado" }
    ```
  - **400 / 500:** `{ "error": … }`

> **Final Note:**
> - Ensure you forward session cookies or auth token in each request
> - Only administrators can manage workers; others will get **403 Forbidden**

---

## 👥 ClienteViewSet

> **Base URL:** `/v1/clientes/`  
> **Permissions:**
> - **IsAuthenticated**
> - **CustomAccessPermission**
>   - **Superuser** or **Trabajador.puesto='administrador'**: full access
>   - **Jefe de servicio**: list clients, cylinders; create receipts
>   - **Cliente**: list cylinders; create returns; view/edit own profile

### Serializer: ClienteSerializer
- **Fields:**
  - user (nested with @uci.cu email validation and password handling)
  - id
  - direccion
  - tipo (normal | especial)
  - fecha_UT (≤ today)
  - fecha_PC
- **create:** creates User + Cliente
- **update:** updates User and/or Cliente data

### Endpoints

### 1. List Clients
- **Method:** GET
- **URL:** `/v1/clientes/`
- **Description:** Returns all clients with user data

### 2. Retrieve Client by ID
- **Method:** GET
- **URL:** `/v1/clientes/{id}/`
- **Description:** Details of client {id}

### 3. Create Client
- **Method:** POST
- **URL:** `/v1/clientes/`
- **Body (JSON):**
  ```json
  {
    "user": {
      "username": "pepita",
      "password": "secreto123",
      "first_name": "Pepita",
      "last_name": "González",
      "email": "pepita@uci.cu"
    },
    "direccion": "Calle 123",
    "tipo": "normal",
    "fecha_UT": "2025-05-08",
    "fecha_PC": "2025-05-09"
  }
  ```
- **Responses:**
  - **201 Created:** Cliente object with nested user
  - **400 Bad Request:** `{ "error": "…ValidationError…" }`
  - **500 Internal Server Error:** `{ "error": "Un error inesperado ha ocurrido …" }`

### 4. Update Client (Full Replacement)
- **Method:** PUT
- **URL:** `/v1/clientes/{id}/`
- **Body:** Same fields as create
- **Responses:**
  - **200 OK:** Updated data
  - **400 / 500:** Same error structure as create

### 5. Partial Update
- **Method:** PATCH
- **URL:** `/v1/clientes/{id}/`
- **Body:** Only fields to update
- **Responses:** Same as PUT, but 200 OK for success

### 6. Delete Client
- **Method:** DELETE
- **URL:** `/v1/clientes/{id}/`
- **Responses:**
  - **204 No Content:** `{ "message": "Cliente con id {id} eliminado" }`
  - **400 / 500:** Details in `{ "error": … }`

> **Important:**
> - Ensure client sends/receives session cookies (or configured auth scheme)
> - Email validation only accepts @uci.cu and prevents duplicates
> - Only clients can modify their own resource (has_object_permission)

---

## 🚚 Comprobante_AbastecimientoViewSet

> **Base URL:** `/v1/comprobante_abastecimiento/`  
> **Permissions:**
> - IsAuthenticated
> - CustomAccessPermission
>   - Superuser / Trabajador administrador: full access
>   - Jefe de servicio: can **create** supply receipts and list them
>   - Clients: no access to this endpoint per permissions

### Model
```python
class Comprobante_Abastecimiento(models.Model):
    fecha = DateField()
    cant_cilindros = IntegerField()
    proveedor = CharField(max_length=50)
    trabajador_recivio = ForeignKey(Trabajador, on_delete=CASCADE)
```

### Serializer
```python
class Comprobante_AbastecimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comprobante_Abastecimiento
        fields = '__all__'
```

### Endpoints

### 1. List Receipts
- **Method:** GET
- **URL:** `/v1/comprobante_abastecimiento/`
- **Description:** Lists all receipts with trabajador_recivio__user data
- **Response (200 OK):**
  ```json
  [
    {
      "id": 1,
      "fecha": "2025-05-09",
      "cant_cilindros": 10,
      "proveedor": "GasCorp",
      "trabajador_recivio": 4
    },
    …
  ]
  ```

### 2. Retrieve Receipt
- **Method:** GET
- **URL:** `/v1/comprobante_abastecimiento/{id}/`
- **Description:** Details of receipt {id}
- **Response (200 OK):**
  ```json
  {
    "id": 1,
    "fecha": "2025-05-09",
    "cant_cilindros": 10,
    "proveedor": "GasCorp",
    "trabajador_recivio": 4
  }
  ```
- **Error (404):** `{ "detail": "Not found." }`

### 3. Create Receipt
- **Method:** POST
- **URL:** `/v1/comprobante_abastecimiento/`
- **Body (JSON):**
  ```json
  {
    "fecha": "2025-05-10",
    "cant_cilindros": 5,
    "proveedor": "GasProvider",
    "trabajador_recivio": 3      // Worker ID
  }
  ```
- **Additional Behavior:**  
  On creation, calls crear_cilindros_abastecimiento(fecha, cantidad) which:
  - Generates quantity cylinders with:
    - fehca_llegada = fecha
    - defectuoso = False
    - lleno = True
    - asign = null
  - Inserts them via bulk_create
- **Responses:**
  - **201 Created:** New receipt data
  - **400 Bad Request:** `{ "error": "…ValidationError…" }`
  - **500 Internal Server Error:** `{ "error": "Un error inesperado ha ocurrido: …" }`

### 4. Update Receipt
- **Method:** PUT
- **URL:** `/v1/comprobante_abastecimiento/{id}/`
- **Body:** Same fields as create
- **Responses:**
  - **200 OK:** Updated receipt
  - **400 / 500:** `{ "error": … }`

### 5. Partial Update
- **Method:** PATCH
- **URL:** `/v1/comprobante_abastecimiento/{id}/`
- **Body:** Only fields to update
- **Responses:** Same as PUT, but 200 OK for success

### 6. Delete Receipt
- **Method:** DELETE
- **URL:** `/v1/comprobante_abastecimiento/{id}/`
- **Responses:**
  - **204 No Content:**
    ```json
    { "message": "Comprobante_Abastecimiento con id {id} eliminado" }
    ```
  - **400 / 500:** `{ "error": … }`

## Key Utilities
- **crear_cilindros_abastecimiento(fecha: date, cantidad: int)**  
  Creates new unassigned cylinders for supply
- **calcular_fecha_proximo_cilindro(tipo: str) -> date**  
  Returns next refill date based on client type
- **procesar_entrega(comprobante)**  
  Assigns and rotates cylinders between client and stock, validating availability

> **Quick Tip:** Verify your client includes session cookies or auth token in each request; without them you'll get a 401.

---

## 🚚 Comprobante_EntregaViewSet

> **Base URL:** `/v1/comprobante_entrega/`  
> **Permissions:**
> - IsAuthenticated
> - CustomAccessPermission
>   - **Jefe de servicio**: can create/list deliveries
>   - **Cliente**: can create returns, but not deliveries—per permissions

### Model
```python
class Comprobante_Entrega(models.Model):
    fecha = DateField()
    cliente = ForeignKey(Cliente, on_delete=CASCADE)
    cilindroE = ForeignKey(Cilindro, on_delete=CASCADE, related_name='comprobantes_entrada')
    cilindroS = ForeignKey(Cilindro, on_delete=CASCADE, related_name='comprobantes_salida')
```

### Serializer
```python
class Comprobante_EntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comprobante_Entrega
        fields = '__all__'
```

### Endpoints

### 1. List Delivery Receipts
- **Method:** GET
- **URL:** `/v1/comprobante_entrega/`
- **Description:** Returns all deliveries with nested cliente__user data
- **Response (200 OK):**
  ```json
  [
    {
      "id": 1,
      "fecha": "2025-05-09",
      "cliente": 7,
      "cilindroE": 12,
      "cilindroS": 5
    },
    …
  ]
  ```

### 2. Retrieve Delivery
- **Method:** GET
- **URL:** `/v1/comprobante_entrega/{id}/`
- **Description:** Details of delivery {id}
- **Response (200 OK):**
  ```json
  {
    "id": 1,
    "fecha": "2025-05-09",
    "cliente": 7,
    "cilindroE": 12,
    "cilindroS": 5
  }
  ```
- **Error (404):** `{ "detail": "Not found." }`

### 3. Create Delivery Receipt
- **Method:** POST
- **URL:** `/v1/comprobante_entrega/`
- **Body (JSON):**
  ```json
  {
    "fecha": "2025-05-10",
    "cliente": 7,
    "cilindroE": 12,
    "cilindroS": 5
  }
  ```
- **Creation Flow:**
  1. Saves receipt
  2. Calls procesar_entrega(comprobante):
     - Finds available cylinder (unassigned, full, not defective)
     - Assigns cilindroE to client and removes cilindroS
     - Updates both cylinders (asign, lleno)
     - If no cylinders, returns 400 with `{ "error": "No hay cilindros disponibles para asignar." }`
  3. Updates **all** clients with same destination address:
     - fecha_UT = comprobante.fecha
     - fecha_PC based on type:
       - "normal" → today + 2 months
       - "especial" → today + 1 month
- **Responses:**
  - **201 Created:** Receipt data
  - **400 Bad Request:**
    - Initial validation: `{ "error": "…ValidationError…" }`
    - Error in procesar_entrega: `{ "error": "No hay cilindros disponibles para asignar." }`
  - **500 Internal Server Error:** `{ "error": "Un error inesperado ha ocurrido: …" }`

### 4. Update Delivery
- **Method:** PUT
- **URL:** `/v1/comprobante_entrega/{id}/`
- **Body:** Same fields as create
- **Responses:**
  - **200 OK:** Updated receipt
  - **400 / 500:** `{ "error": … }`

### 5. Partial Update
- **Method:** PATCH
- **URL:** `/v1/comprobante_entrega/{id}/`
- **Body:** Only fields to update
- **Responses:** Same as PUT, success → 200 OK

### 6. Delete Delivery
- **Method:** DELETE
- **URL:** `/v1/comprobante_entrega/{id}/`
- **Responses:**
  - **204 No Content:**
    ```json
    { "message": "Comprobante_Entrega con id {id} eliminado" }
    ```
  - **400 / 500:** `{ "error": … }`

## Key Utilities
- **procesar_entrega(comprobante)**  
  Assigns and rotates cylinders between stock and client; raises ValidationError if no cylinders available
- **calcular_fecha_proximo_cilindro(tipo: str) -> date**  
  Returns next refill date:
  - normal: today + 2 months
  - especial: today + 1 month

> **Tip:** Test first in Postman or your REST client, verify cookies/auth and observe grouping by address.

---

## 🔄 Reporte_DevolucionViewSet

> **Base URL:** `/v1/reporte_devolucion/`  
> **Permissions:**
> - IsAuthenticated
> - CustomAccessPermission
>   - **Superuser** / **Trabajador administrador**: full access (list, retrieve, create, etc.)
>   - **Jefe de servicio**: can **list** and **retrieve** return reports
>   - **Cliente**: can **create** their own return report

### Model
```python
class Reporte_Devolucion(models.Model):
    fecha = DateField()
    cliente = ForeignKey(Cliente, on_delete=CASCADE)
    cilindro = ForeignKey(Cilindro, on_delete=CASCADE)
    defecto = TextField(max_length=255)
```

### Serializer
```python
class Reporte_DevolucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte_Devolucion
        fields = '__all__'
        read_only_fields = ('cliente', 'cilindro', 'fecha')
```

### Endpoints

### 1. List Reports
- **Method:** GET
- **URL:** `/v1/reporte_devolucion/`
- **Access:** Superuser, Workers (any position) and Jefe de servicio
- **Description:** Returns all reports with cliente__user data
- **Response (200 OK):**
  ```json
  [
    {
      "id": 1,
      "fecha": "2025-05-10",
      "cliente": 7,
      "cilindro": 12,
      "defecto": "Fuga en la válvula"
    },
    …
  ]
  ```

### 2. Retrieve Report
- **Method:** GET
- **URL:** `/v1/reporte_devolucion/{id}/`
- **Access:** Same as List
- **Description:** Shows details of report {id}
- **Response (200 OK):**
  ```json
  {
    "id": 1,
    "fecha": "2025-05-10",
    "cliente": 7,
    "cilindro": 12,
    "defecto": "Fuga en la válvula"
  }
  ```
- **Error (404):** `{ "detail": "Not found." }`

### 3. Create Report
- **Method:** POST
- **URL:** `/v1/reporte_devolucion/`
- **Access:** Only authenticated **Clients**
- **Body (JSON):**
  ```json
  {
    "defecto": "Descripción del defecto (máx. 255 caracteres)"
  }
  ```
- **Creation Flow:**
  1. Validates defecto
  2. Finds cylinder assigned to client (get_object_or_404(Cilindro, asign=cliente))
  3. Creates Reporte_Devolucion with:
     - fecha = date.today()
     - cliente = authenticated user
     - cilindro = found cylinder
- **Responses:**
  - **201 Created:** Newly created Reporte_Devolucion
  - **400 Bad Request:** `{ "error": "…ValidationError…" }`
  - **500 Internal Server Error:** `{ "error": "Error inesperado: …" }`

### 4. Update (PUT) and Partial (PATCH)
- **Methods:** PUT and PATCH
- **URL:** `/v1/reporte_devolucion/{id}/`
- **Access:**
  - **Superuser** / **Workers**: yes
  - **Cliente**: only if it's **their own report** (has_object_permission)
- **Body:** Only defecto (other fields are read-only)
- **Responses:**
  - **200 OK:** Updated report
  - **400 / 500:** `{ "error": … }`

### 5. Delete Report
- **Method:** DELETE
- **URL:** `/v1/reporte_devolucion/{id}/`
- **Access:**
  - **Superuser** / **Workers**: yes
  - **Cliente**: only if it's **their own report**
- **Responses:**
  - **204 No Content:**
    ```json
    { "message": "Reporte_Devolucion con id {id} eliminado" }
    ```
  - **400 / 500:** `{ "error": … }`

> **Note:** Ensure your client forwards the session cookie or auth header in each request to avoid a **401 Unauthorized**.
