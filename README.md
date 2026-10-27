# **Inmobiliaria** - Prototipo Arquitectónico Cloud

Este prototipo demuestra la viabilidad técnica y la aplicación de patrones de diseño en la nube para la modernización de la plataforma.

## Patrones Evidenciados
1. **Cache-Aside Pattern:** Consulta rápida en capa de caché antes de acceder a la base de datos transaccional (`GET /inmuebles`).
2. **Desacoplamiento / Tareas Asíncronas:** Respuesta inmediata al cliente delegando la optimización multimedia a un worker en segundo plano (`POST /inmuebles/publicar`).

## Endpoints
* `GET /`: Estado de salud de la API.
* `GET /inmuebles`: Catálogo con resolución de caché.
* `POST /inmuebles/publicar`: Registro con procesamiento desacoplado.


**Sergio Fuentes**