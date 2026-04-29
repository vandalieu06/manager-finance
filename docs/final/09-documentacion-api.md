# 9. Documentación API

La documentación de API debe completarse tras revisar el backend real del proyecto. En la aplicación móvil revisada no se han identificado llamadas HTTP a una API propia para productos, facturas o estadísticas. La única integración externa funcional localizada en el frontend es Firebase Auth para el inicio de sesión.

El documento `mobile-app/docs/api.md` propone un patrón de API protegido por Firebase Auth, basado en rutas del usuario autenticado:

```http
GET /api/user/me
GET /api/user/me/stats
GET /api/user/me/products
```

El patrón consiste en enviar el token de Firebase en la cabecera `Authorization` y dejar que el backend obtenga el usuario real a partir del token, evitando rutas privadas basadas en identificadores manipulables como `/api/user/:id`.

Ejemplo de cabecera:

```http
Authorization: Bearer <firebase_id_token>
```

Este enfoque debe contrastarse con la implementación real del backend antes de presentarse como API definitiva.

## Endpoints a documentar tras revisar backend

La documentación final de API debería incluir:

- Autenticación y validación de tokens.
- Endpoints de usuario.
- Endpoints de productos o gastos.
- Endpoints de facturas.
- Endpoints de estadísticas.
- Endpoints de categorías.
- Endpoints de OCR/IA si existen como servicio independiente.
- Formato de peticiones.
- Formato de respuestas.
- Códigos de error.
- Ejemplos de uso.

[documentación endpoints backend]

[diagrama comunicación frontend-backend]
