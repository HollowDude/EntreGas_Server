
## 🔐 AuthViewSet

> **Base URL:** `/v1/auth/`  
> **Autenticación:**
> 
> - `login` → **AllowAny**
>     
> - `logout`, `check_auth` → **IsAuthenticated**
>     
> - Usa _session cookies_ de Django, **ojo**: no es JWT.
>     

---

### 1. POST `/api/auth/login/`

- **Descripción:** Inicia sesión y crea sesión en servidor.
    
- **Request Body (JSON):**
    
    ```json
    {
      "username": "string",       // obligatorio
      "password": "string",       // obligatorio
      "recordar": true|false      // opcional, por defecto false
    }
    ```
    
- **Comportamiento:**
    
    - Valida credenciales con `authenticate()`.
        
    - Si `recordar: true`, la sesión expira en 30 días; si no, al cerrar el navegador.
        
    - Detecta si el usuario es Trabajador o Cliente y devuelve datos según modelo.
        
- **Respuestas exitosas (200 OK):**
    
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
        
    - **Otro (superusuario u otro caso):**
        
        ```json
        {
          "message": "Inicio de sesión exitoso"
        }
        ```
        
- **Error (400 Bad Request):**
    
    ```json
    { "error": "Credenciales inválidas" }
    ```
    

---

### 2. POST `/api/auth/logout/`

- **Descripción:** Cierra la sesión actual.
    
- **Headers:**
    
    - Debe enviar la cookie de sesión de Django.
        
- **Permisos:** `IsAuthenticated`
    
- **Response (200 OK):**
    
    ```json
    { "message": "Sesión cerrada" }
    ```
    

---

### 3. GET `/api/auth/check_auth/`

- **Descripción:** Verifica si la sesión está activa.
    
- **Headers:**
    
    - Debe enviar la cookie de sesión.
        
- **Permisos:** `IsAuthenticated`
    
- **Response (200 OK):**
    
    ```json
    { "username": "pepito" }
    ```
    
> **Nota:** Estas llamadas manejan _session cookies_. Asegúrate de que tu cliente (frontend o Postman) permita y reenvíe cookies.



---

## 🔑 PasswordResetViewSet

> **Base URL:** `/v1/password-reset/`  
> **Permisos:** `AllowAny` (no auth requerida)  
> **Métodos soportados:** `POST`, `GET`

---

### 📄 Serializadores

- **`PasswordResetRequestSerializer`**
    
    ```python
    class PasswordResetRequestSerializer(serializers.Serializer):
        email = serializers.EmailField()
    ```
    
- **`PasswordResetConfirmSerializer`**
    
    ```python
    class PasswordResetConfirmSerializer(serializers.Serializer):
        token = serializers.CharField()
        new_password = serializers.CharField(min_length=8)
    ```
    

---

### 1. Solicitar enlace de recuperación

- **Método:** `POST`
    
- **URL:** `/v1/password-reset/request_reset/`
    
- **Body (JSON):**
    
    ```json
    { "email": "usuario@uci.cu" }
    ```
    
- **Flujo:**
    
    1. Valida que el correo exista.
        
    2. Genera un **access token** JWT con vida de 5 horas.
        
    3. Construye link:
        
        ```
        http://localhost:5173/new-password/<token>
        ```
        
    4. Envía correo con asunto “Recuperación de contraseña” y cuerpo:
        
        ```
        Hola <username>,
        
        Para restablecer tu contraseña, haz click en el siguiente enlace:
        
        <link>
        
        El enlace expirará en 5 horas.
        ```
        
- **Respuestas:**
    
    - **200 OK:**
        
        ```json
        {
          "detail": "Se ha enviado un enlace de recuperación a tu correo uci.",
          "token": "<token>"
        }
        ```
        
    - **400 Bad Request:** errores de validación del serializer.
        
    - **404 Not Found:** `{ "detail": "No existe un usuario con este correo electrónico." }`
        

---

### 2. Validar token

- **Método:** `GET`
    
- **URL:** `/v1/password-reset/validate_token/`
    
- **Query Params:** `?token=<token>`
    
- **Descripción:** Verifica que el JWT esté bien formado y no expirado.
    
- **Respuestas:**
    
    - **200 OK:** `{ "detail": "Token válido." }`
        
    - **400 Bad Request:**
        
        - Si no se pasa `token`: `{ "detail": "Token no proporcionado." }`
            
        - Si es inválido o expirado: `{ "detail": "Token inválido o expirado." }`
            

---

### 3. Restablecer contraseña

- **Método:** `POST`
    
- **URL:** `/v1/password-reset/reset_password/`
    
- **Body (JSON):**
    
    ```json
    {
      "token": "<token>",
      "new_password": "nuevaContraseña123"
    }
    ```
    
- **Flujo:**
    
    1. Valida datos con `PasswordResetConfirmSerializer`.
        
    2. Decodifica el token; extrae `user_id`.
        
    3. Busca `User` y actualiza su contraseña.
        
- **Respuestas:**
    
    - **200 OK:** `{ "detail": "Contraseña actualizada correctamente." }`
        
    - **400 Bad Request:**
        
        - Errores de serializer.
            
        - Token inválido/expirado o usuario no existe:
            
            ```json
            { "detail": "Token inválido o expirado." }
            ```
            

---

> **Nota final:**
> 
> - Asegúrate de enviar correctamente el token en cada petición.
>     
> - La URL de frontend (`localhost:5173`) debe ajustarse a tu entorno de producción.
>     
> - El correo sale desde `settings.DEFAULT_FROM_EMAIL`.



---



## 🛢️ CilindroViewSet

> **Base URL:** `/v1/cilindros/`  
> **Permisos:**
> 
> - **IsAuthenticated**
>     
> - **CustomAccessPermission**
>     
> - Usa _session cookies_ o el esquema de autenticación que hayas configurado.
>     

---

### 1. Listar todos los cilindros

- **Método:** `GET`
    
- **URL:** `/v1/cilindros/`
    
- **Descripción:** Devuelve la lista completa de cilindros, incluyendo datos de asignación (`asign__user` con `select_related`).
    
- **Respuesta (200 OK):**
    
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
    

---

### 2. Recuperar un cilindro por ID

- **Método:** `GET`
    
- **URL:** `/v1/cilindros/{id}/`
    
- **Descripción:** Devuelve los datos del cilindro con el `id` especificado.
    
- **Respuesta (200 OK):**
    
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
    

---

### 3. Crear un nuevo cilindro

- **Método:** `POST`
    
- **URL:** `/v1/cilindros/`
    
- **Body (JSON):**
    
    ```json
    {
      "num": "XYZ789",           // opcional, puede ir vacío o null
      "fehca_llegada": "2025-05-10",
      "defectuoso": false,
      "lleno": true,
      "asign": 3                 // ID de Cliente al que se asigna (o null)
    }
    ```
    
- **Respuesta exitosa (201 Created):**
    
    ```json
    {
      "id": 12,
      "num": "XYZ789",
      "fehca_llegada": "2025-05-10",
      "defectuoso": false,
      "lleno": true,
      "asign": 3
    }
    ```
    
- **Error de validación (400 Bad Request):**
    
    ```json
    { "error": "…detalle del ValidationError…" }
    ```
    
- **Error inesperado (500):**
    
    ```json
    { "error": "Un error inesperado ha ocurrido …" }
    ```
    

---

### 4. Actualizar un cilindro (reemplazo total)

- **Método:** `PUT`
    
- **URL:** `/v1/cilindros/{id}/`
    
- **Body (JSON):** (mismos campos que en create)
    
- **Respuesta exitosa (200 OK):**
    
    ```json
    {
      "id": 12,
      "num": "XYZ789",
      "fehca_llegada": "2025-05-10",
      "defectuoso": false,
      "lleno": true,
      "asign": 4
    }
    ```
    
- **Error de validación (400):**
    
    ```json
    { "error": "…detalle del ValidationError…" }
    ```
    
- **Error inesperado (500):**
    
    ```json
    { "error inesperado": "Intenta again: …" }
    ```
    

---

### 5. Actualizar parcialmente un cilindro

- **Método:** `PATCH`
    
- **URL:** `/v1/cilindros/{id}/`
    
- **Body (JSON):** (solo los campos a cambiar)
    
    ```json
    { "defectuoso": true }
    ```
    
- **Respuesta exitosa (200 OK):**
    
    ```json
    {
      "id": 12,
      "num": "XYZ789",
      "fehca_llegada": "2025-05-10",
      "defectuoso": true,
      "lleno": true,
      "asign": 4
    }
    ```
    
- **Errores:** mismos que en PUT.
    

---

### 6. Eliminar un cilindro

- **Método:** `DELETE`
    
- **URL:** `/v1/cilindros/{id}/`
    
- **Respuesta exitosa (204 No Content):**
    
    ```json
    { "message": "Cilindro con id {id} eliminado" }
    ```
    
- **Error de validación (400):**
    
    ```json
    { "error": "…detalle del ValidationError…" }
    ```
    
- **Error inesperado (500):**
    
    ```json
    { "error inesperado": "Intenta again: …" }
    ```
    

---

### 7. Cilindros sin número de serie

- **Método:** `GET`
    
- **URL:** `/v1/cilindros/sin-numero/`
    
- **Descripción:** Devuelve todos los cilindros donde `num` es `null` o `""`.
    
- **Respuesta (200 OK):**
    
    ```json
    [
      { "id": 3, "num": null, … },
      { "id": 7, "num": "", … }
    ]
    ```
    

---

### 8. Cilindros con número de serie

- **Método:** `GET`
    
- **URL:** `/v1/cilindros/con-numero/`
    
- **Descripción:** Devuelve todos los cilindros donde `num` no está vacío.
    
- **Respuesta (200 OK):**
    
    ```json
    [
      { "id": 1, "num": "ABC123", … },
      { "id": 2, "num": "DEF456", … }
    ]
    ```
    

---

### 📋 Modelo `Cilindro`

```python
class Cilindro(models.Model):
    num           = CharField("Número de serie", blank=True, null=True, max_length=255)
    fehca_llegada = DateField(default=date.today)
    defectuoso    = BooleanField(default=False)
    lleno         = BooleanField(default=True)
    asign         = ForeignKey(Cliente, on_delete=SET_NULL, null=True, blank=True)
```

---

> **Tip:** Asegúrate de que tu cliente reenvíe las cookies de sesión y tenga configurados los headers de autenticación correctamente.



---

## 👷 TrabajadorViewSet

> **Base URL:** `/v1/trabajador/`  
> **Permisos:**
> 
> - **IsAuthenticated**
>     
> - **CustomAccessPermission**
>     
>     - **Superusuario** o **Trabajador.puesto='administrador'**: acceso total.
>         
>     - **Jefe de servicio** y **Clientes**: **no** tienen permisos para este endpoint (salvo ver su propio recurso si el permiso de objeto lo permite).
>         

---

### 📦 Modelo `Trabajador`

```python
class Trabajador(models.Model):
    user  = OneToOneField(User, on_delete=CASCADE)
    puesto = CharField(
        choices=[
            ("tecnico", "Tecnico"),
            ("jefe de servicio", "Jefe de Servicio")
        ],
        max_length=255
    )
```

---

### 🔄 Serializador

```python
class TrabajadorSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested

    class Meta:
        model  = Trabajador
        fields = ['id', 'user', 'puesto']
```

- **`UserSerializer`** maneja:
    
    - Campos: `id`, `username`, `password` (write-only), `first_name`, `last_name`, `email`
        
    - Valida dominio `@uci.cu` y unicidad de email.
        
    - Crea/actualiza el `User` con manejo de password.
        

---

### 1. Listar trabajadores

- **Método:** `GET`
    
- **URL:** `/v1/trabajador/`
    
- **Permisos:** Solo administradores.
    
- **Descripción:** Lista todos los trabajadores con datos de usuario (`select_related('user')`).
    
- **Respuesta (200 OK):**
    
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
    

---

### 2. Recuperar un trabajador

- **Método:** `GET`
    
- **URL:** `/v1/trabajador/{id}/`
    
- **Permisos:** Solo administradores (o el mismo trabajador por permiso de objeto).
    
- **Descripción:** Detalles del trabajador `{id}`.
    
- **Respuesta (200 OK):** igual a la de **Listar**, pero un solo objeto.
    
- **Error (404):** `{ "detail": "Not found." }`
    

---

### 3. Crear trabajador

- **Método:** `POST`
    
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
    
- **Respuestas:**
    
    - **201 Created:** objeto `Trabajador` creado con usuario anidado.
        
    - **400 Bad Request:** `{ "error": "…ValidationError…" }`
        
    - **500 Internal Server Error:** `{ "error": "Un error inesperado ha ocurrido …" }`
        

---

### 4. Actualizar trabajador (reemplazo total)

- **Método:** `PUT`
    
- **URL:** `/v1/trabajador/{id}/`
    
- **Body:** mismos campos que en **create**.
    
- **Permisos:** Solo administradores.
    
- **Respuestas:**
    
    - **200 OK:** datos actualizados.
        
    - **400 / 500:** `{ "error": … }`
        

---

### 5. Actualizar parcialmente

- **Método:** `PATCH`
    
- **URL:** `/v1/trabajador/{id}/`
    
- **Body:** solo los campos a modificar, por ejemplo:
    
    ```json
    { "puesto": "tecnico" }
    ```
    
- **Permisos:** Solo administradores.
    
- **Respuestas:** mismas que en **PUT**, éxito → 200 OK.
    

---

### 6. Eliminar trabajador

- **Método:** `DELETE`
    
- **URL:** `/v1/trabajador/{id}/`
    
- **Permisos:** Solo administradores.
    
- **Respuestas:**
    
    - **204 No Content:**
        
        ```json
        { "message": "Trabajador con id {id} eliminado" }
        ```
        
    - **400 / 500:** `{ "error": … }`
        

---

> **Nota final:**
> 
> - Asegúrate de reenviar cookies de sesión o token de autenticación en cada petición.
>     
> - Solo los administradores pueden gestionar trabajadores; el resto recibirá **403 Forbidden**.
>


---

## 👥 ClienteViewSet

> **Base URL:** `/v1/clientes/`  
> **Permisos:**
> 
> - **IsAuthenticated**
>     
> - **CustomAccessPermission**
>     
>     - **Superuser** o **Trabajador.puesto='administrador'**: acceso total.
>         
>     - **Jefe de servicio**: listar clientes, cilindros; crear comprobantes.
>         
>     - **Cliente**: listar cilindros; crear devoluciones; ver/editar su propio perfil.
>         

---

### 📒 Serializador: `ClienteSerializer`

- **Campos:**
    
    - `user` (anidado con validación de correo `@uci.cu` y manejo de password)
        
    - `id`
        
    - `direccion`
        
    - `tipo` (`normal` | `especial`)
        
    - `fecha_UT` (≤ hoy)
        
    - `fecha_PC`
        
- **create:** crea `User` + `Cliente`.
    
- **update:** actualiza datos de `User` y/o `Cliente`.
    

---

### 1. Listar clientes

- **Método:** `GET`
    
- **URL:** `/v1/clientes/`
    
- **Descripción:** Devuelve todos los clientes con datos de usuario (`select_related('user')`).
    

---

### 2. Recuperar cliente por ID

- **Método:** `GET`
    
- **URL:** `/v1/clientes/{id}/`
    
- **Descripción:** Detalles del cliente `{id}`.
    

---

### 3. Crear cliente

- **Método:** `POST`
    
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
    
- **Respuestas:**
    
    - **201 Created:** objeto `Cliente` con `user` anidado.
        
    - **400 Bad Request:** `{ "error": "…ValidationError…" }`
        
    - **500 Internal Server Error:** `{ "error": "Un error inesperado ha ocurrido …" }`
        

---

### 4. Actualizar cliente (reemplazo total)

- **Método:** `PUT`
    
- **URL:** `/v1/clientes/{id}/`
    
- **Body:** mismos campos que en **create**.
    
- **Respuestas:**
    
    - **200 OK:** datos actualizados.
        
    - **400 / 500:** estructura de error igual a **create**.
        

---

### 5. Actualizar parcialmente cliente

- **Método:** `PATCH`
    
- **URL:** `/v1/clientes/{id}/`
    
- **Body:** solo campos a modificar.
    
- **Respuestas:** mismas que en **PUT**, pero 200 OK para éxito.
    

---

### 6. Eliminar cliente

- **Método:** `DELETE`
    
- **URL:** `/v1/clientes/{id}/`
    
- **Respuestas:**
    
    - **204 No Content:** `{ "message": "Cliente con id {id} eliminado" }`
        
    - **400 / 500:** detalles en `{ "error": … }`
        

---

> **Importante:**
> 
> - Asegura que el cliente envíe y reciba cookies de sesión (o el esquema auth configurado).
>     
> - La validación de `email` sólo acepta `@uci.cu` y evita duplicados.
>     
> - Sólo los clientes pueden modificar su propio recurso (`has_object_permission`).




---

## 🚚 Comprobante_AbastecimientoViewSet

> **Base URL:** `/v1/comprobante_abastecimiento/`  
> **Permisos:**
> 
> - `IsAuthenticated`
>     
> - `CustomAccessPermission`
>     
>     - Superusuario / Trabajador administrador: acceso completo.
>         
>     - Jefe de servicio: puede **crear** comprobantes de abastecimiento y listarlos.
>         
>     - Clientes: no tienen acceso a este endpoint según permisos.
>         

---

### 📦 Modelo `Comprobante_Abastecimiento`

```python
class Comprobante_Abastecimiento(models.Model):
    fecha             = DateField()
    cant_cilindros    = IntegerField()
    proveedor         = CharField(max_length=50)
    trabajador_recivio = ForeignKey(Trabajador, on_delete=CASCADE)
```

---

### 🔄 Serializador

```python
class Comprobante_AbastecimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Comprobante_Abastecimiento
        fields = '__all__'
```

---

### 1. Listar comprobantes

- **Método:** `GET`
    
- **URL:** `/v1/comprobante_abastecimiento/`
    
- **Descripción:** Lista todos los comprobantes, incluye datos de `trabajador_recivio__user` gracias a `select_related`.
    
- **Respuesta (200 OK):**
    
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
    

---

### 2. Recuperar un comprobante

- **Método:** `GET`
    
- **URL:** `/v1/comprobante_abastecimiento/{id}/`
    
- **Descripción:** Detalles del comprobante `{id}`.
    
- **Respuesta (200 OK):**
    
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
    

---

### 3. Crear comprobante

- **Método:** `POST`
    
- **URL:** `/v1/comprobante_abastecimiento/`
    
- **Body (JSON):**
    
    ```json
    {
      "fecha": "2025-05-10",
      "cant_cilindros": 5,
      "proveedor": "GasProvider",
      "trabajador_recivio": 3      // ID de Trabajador
    }
    ```
    
- **Comportamiento adicional:**  
    Al crearse, invoca `crear_cilindros_abastecimiento(fecha, cantidad)` que:
    
    - Genera `cantidad` cilindros con:
        
        - `fehca_llegada = fecha`
            
        - `defectuoso = False`
            
        - `lleno = True`
            
        - `asign = null`
            
    - Los inserta vía `bulk_create`.
        
- **Respuestas:**
    
    - **201 Created:** datos del nuevo comprobante.
        
    - **400 Bad Request:** `{ "error": "…ValidationError…" }`
        
    - **500 Internal Server Error:** `{ "error": "Un error inesperado ha ocurrido: …" }`
        

---

### 4. Actualizar comprobante

- **Método:** `PUT`
    
- **URL:** `/v1/comprobante_abastecimiento/{id}/`
    
- **Body:** mismos campos que en **create**.
    
- **Respuestas:**
    
    - **200 OK:** comprobante actualizado.
        
    - **400 / 500:** `{ "error": … }`
        

---

### 5. Actualizar parcialmente

- **Método:** `PATCH`
    
- **URL:** `/v1/comprobante_abastecimiento/{id}/`
    
- **Body:** solo campos a modificar, e.g.
    
    ```json
    { "proveedor": "NuevoProveedor" }
    ```
    
- **Respuestas:** idénticas a **PUT**, pero 200 OK para éxito.
    

---

### 6. Eliminar comprobante

- **Método:** `DELETE`
    
- **URL:** `/v1/comprobante_abastecimiento/{id}/`
    
- **Respuestas:**
    
    - **204 No Content:**
        
        ```json
        { "message": "Comprobante_Abastecimiento con id {id} eliminado" }
        ```
        
    - **400 / 500:** `{ "error": … }`
        

---

## 🛠️ Utilidades disponibles

- **`crear_cilindros_abastecimiento(fecha: date, cantidad: int)`**  
    Crea cilindros nuevos sin asignar para abastecimiento.
    
- **`calcular_fecha_proximo_cilindro(tipo: str) -> date`**  
    Retorna fecha de próxima recarga según tipo de cliente (`normal` +2 meses, `especial` +1 mes).
    
- **`procesar_entrega(comprobante)`**  
    Asigna y rota cilindros entre cliente y stock, validando disponibilidad.
    

---

> **Tip rápido:** Verifica que tu cliente incluya cookies de sesión o token de autenticación en cada petición; sin ellas, recibirás un 401.


---

## 🚚 Comprobante_EntregaViewSet

> **Base URL:** `/v1/comprobante_entrega/`  
> **Permisos:**
> 
> - `IsAuthenticated`
>     
> - `CustomAccessPermission`
>     
>     - **Jefe de servicio**: puede crear/listar entregas.
>         
>     - **Cliente**: puede crear devoluciones, pero no entregas—según permisos.
>         

---

### 📦 Modelo `Comprobante_Entrega`

```python
class Comprobante_Entrega(models.Model):
    fecha      = DateField()
    cliente    = ForeignKey(Cliente, on_delete=CASCADE)
    cilindroE  = ForeignKey(Cilindro, on_delete=CASCADE, related_name='comprobantes_entrada')
    cilindroS  = ForeignKey(Cilindro, on_delete=CASCADE, related_name='comprobantes_salida')
```

---

### 🔄 Serializador

```python
class Comprobante_EntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Comprobante_Entrega
        fields = '__all__'
```

---

### 1. Listar comprobantes de entrega

- **Método:** `GET`
    
- **URL:** `/v1/comprobante_entrega/`
    
- **Descripción:** Devuelve todas las entregas, con datos anidados de `cliente__user`.
    
- **Respuesta (200 OK):**
    
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
    

---

### 2. Recuperar una entrega

- **Método:** `GET`
    
- **URL:** `/v1/comprobante_entrega/{id}/`
    
- **Descripción:** Detalles de la entrega `{id}`.
    
- **Respuesta (200 OK):**
    
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
    

---

### 3. Crear comprobante de entrega

- **Método:** `POST`
    
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
    
- **Flujo de creación:**
    
    1. Guarda el comprobante.
        
    2. Llama a `procesar_entrega(comprobante)`:
        
        - Busca un cilindro disponible (no asignado, lleno, no defectuoso).
            
        - Asigna `cilindroE` al cliente y retira `cilindroS`.
            
        - Actualiza ambos cilindros (`asign`, `lleno`).
            
        - Si no hay cilindros, devuelve 400 con `{ "error": "No hay cilindros disponibles para asignar." }`.
            
    3. Actualiza **todos** los clientes con la misma `direccion` del destinatario:
        
        - `fecha_UT = comprobante.fecha`
            
        - `fecha_PC` según tipo:
            
            - `"normal"` → hoy + 2 meses
                
            - `"especial"` → hoy + 1 mes
                
- **Respuestas:**
    
    - **201 Created:** datos del comprobante.
        
    - **400 Bad Request:**
        
        - Validación inicial: `{ "error": "…ValidationError…" }`
            
        - Error en `procesar_entrega`: `{ "error": "No hay cilindros disponibles para asignar." }`
            
    - **500 Internal Server Error:** `{ "error": "Un error inesperado ha ocurrido: …" }`
        

---

### 4. Actualizar entrega

- **Método:** `PUT`
    
- **URL:** `/v1/comprobante_entrega/{id}/`
    
- **Body:** mismos campos que en **create**.
    
- **Respuestas:**
    
    - **200 OK:** comprobante actualizado.
        
    - **400 / 500:** `{ "error": … }`
        

---

### 5. Actualizar parcialmente

- **Método:** `PATCH`
    
- **URL:** `/v1/comprobante_entrega/{id}/`
    
- **Body:** solo los campos a modificar.
    
- **Respuestas:** idénticas a **PUT**, éxito → 200 OK.
    

---

### 6. Eliminar entrega

- **Método:** `DELETE`
    
- **URL:** `/v1/comprobante_entrega/{id}/`
    
- **Respuestas:**
    
    - **204 No Content:**
        
        ```json
        { "message": "Comprobante_Entrega con id {id} eliminado" }
        ```
        
    - **400 / 500:** `{ "error": … }`
        

---

## 🛠️ Utilidades clave

- **`procesar_entrega(comprobante)`**  
    Asigna y rota cilindros entre stock y cliente; lanza `ValidationError` si no hay cilindros disponibles.
    
- **`calcular_fecha_proximo_cilindro(tipo: str) -> date`**  
    Devuelve fecha de próxima recarga:
    
    - `normal`: hoy + 2 meses
        
    - `especial`: hoy + 1 mes
        

---

> **Consejo:** Prueba primero en Postman o tu cliente REST, verifica cookies/autenticación y observa la agrupación por `direccion`.



---

## 🔄 Reporte_DevolucionViewSet

> **Base URL:** `/v1/reporte_devolucion/`  
> **Permisos:**
> 
> - `IsAuthenticated`
>     
> - `CustomAccessPermission`
>     
>     - **Superuser** / **Trabajador administrador**: acceso total (list, retrieve, create, etc.).
>         
>     - **Jefe de servicio**: puede **listar** y **recuperar** reportes de devolución.
>         
>     - **Cliente**: puede **crear** su propio reporte de devolución.
>         

---

### 📦 Modelo `Reporte_Devolucion`

```python
class Reporte_Devolucion(models.Model):
    fecha    = DateField()
    cliente  = ForeignKey(Cliente, on_delete=CASCADE)
    cilindro = ForeignKey(Cilindro, on_delete=CASCADE)
    defecto  = TextField(max_length=255)
```

---

### 🔄 Serializador

```python
class Reporte_DevolucionSerializer(serializers.ModelSerializer):
    class Meta:
        model            = Reporte_Devolucion
        fields           = '__all__'
        read_only_fields = ('cliente', 'cilindro', 'fecha')
```

- **Campos de solo lectura:**
    
    - `fecha` (se asigna `date.today()`)
        
    - `cliente` (que hace la petición)
        
    - `cilindro` (el asignado al cliente)
        

---

### 1. Listar reportes

- **Método:** `GET`
    
- **URL:** `/v1/reporte_devolucion/`
    
- **Acceso:** Superusuario, Trabajadores (cualquier puesto) y Jefe de servicio.
    
- **Descripción:** Devuelve todos los reportes con datos de `cliente__user`.
    
- **Respuesta (200 OK):**
    
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
    

---

### 2. Recuperar un reporte

- **Método:** `GET`
    
- **URL:** `/v1/reporte_devolucion/{id}/`
    
- **Acceso:** Igual que **Listar**.
    
- **Descripción:** Muestra detalle del reporte `{id}`.
    
- **Respuesta (200 OK):**
    
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
    

---

### 3. Crear reporte

- **Método:** `POST`
    
- **URL:** `/v1/reporte_devolucion/`
    
- **Acceso:** Sólo **Clientes** autenticados.
    
- **Body (JSON):**
    
    ```json
    {
      "defecto": "Descripción del defecto (máx. 255 caracteres)"
    }
    ```
    
- **Flujo de creación:**
    
    1. Valida `defecto`.
        
    2. Busca el cilindro asignado al cliente (`get_object_or_404(Cilindro, asign=cliente)`).
        
    3. Crea `Reporte_Devolucion` con:
        
        - `fecha = date.today()`
            
        - `cliente` = usuario autenticado
            
        - `cilindro` = cilindro encontrado
            
- **Respuestas:**
    
    - **201 Created:** objeto `Reporte_Devolucion` recién creado.
        
    - **400 Bad Request:** `{ "error": "…ValidationError…" }`
        
    - **500 Internal Server Error:** `{ "error": "Error inesperado: …" }`
        

---

### 4. Actualizar (PUT) y parcial (PATCH)

- **Métodos:** `PUT` y `PATCH`
    
- **URL:** `/v1/reporte_devolucion/{id}/`
    
- **Acceso:**
    
    - **Superuser** / **Trabajadores**: sí
        
    - **Cliente**: sólo si es **su propio reporte** (`has_object_permission`).
        
- **Body:** sólo `defecto` (los demás campos son de solo lectura).
    
- **Respuestas:**
    
    - **200 OK:** reporte actualizado.
        
    - **400 / 500:** `{ "error": … }`
        

---

### 5. Eliminar reporte

- **Método:** `DELETE`
    
- **URL:** `/v1/reporte_devolucion/{id}/`
    
- **Acceso:**
    
    - **Superuser** / **Trabajadores**: sí
        
    - **Cliente**: sólo si es **su propio reporte**.
        
- **Respuestas:**
    
    - **204 No Content:**
        
        ```json
        { "message": "Reporte_Devolucion con id {id} eliminado" }
        ```
        
    - **400 / 500:** `{ "error": … }`
        

---

> **Nota:** Asegúrate de que tu cliente reenvíe la cookie de sesión o cabecera de autenticación en cada petición para evitar un **401 Unauthorized**.


