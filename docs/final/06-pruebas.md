# 6. Pruebas

Las pruebas del proyecto deben cubrir tanto la experiencia de usuario como la calidad técnica del código. En el estado actual, la aplicación móvil dispone de configuración de lint mediante Expo, pero no se han localizado pruebas unitarias o de integración definidas en `package.json`.

Por este motivo, este apartado diferencia entre comprobaciones disponibles, pruebas propuestas y pruebas que deben ejecutarse formalmente antes de presentar resultados finales.

## 6.1. Pruebas de usabilidad

Las pruebas de usabilidad deben comprobar si el usuario entiende los flujos principales de la aplicación sin explicación externa. Los flujos recomendados para evaluar son:

- Iniciar sesión.
- Interpretar la pantalla Home.
- Buscar productos.
- Filtrar productos por categoría, marca o precio.
- Abrir el detalle de un producto.
- Acceder a la pestaña Scan.
- Simular la subida de una factura.
- Añadir manualmente un producto a una factura.
- Revisar, validar o denegar una factura.
- Cambiar idioma o moneda desde preferencias.

[tabla resultados pruebas usabilidad]

Para cerrar esta sección en la memoria final, se recomienda realizar sesiones con usuarios y recoger observaciones como tiempo necesario para completar tareas, errores cometidos y dudas durante el uso.

## 6.2. Pruebas de accesibilidad

El código ya incorpora algunas propiedades de accesibilidad en elementos interactivos, como `accessibilityRole`, `accessibilityLabel` y `accessibilityState`. Estas propiedades aparecen en botones, enlaces, pestañas, switches y acciones principales.

Esta base ayuda a que los elementos sean más comprensibles para tecnologías de asistencia, pero todavía sería necesario realizar una revisión completa.

Aspectos a comprobar:

- Contraste entre texto y fondo.
- Tamaño mínimo de áreas táctiles.
- Lectura correcta con lector de pantalla.
- Descripción clara de botones e iconos.
- Navegación coherente entre pantallas.
- Comprensión de estados activos, seleccionados o deshabilitados.

[tabla revisión accesibilidad]

## 6.3. Pruebas unitarias, de integración y de sistema

El proyecto móvil dispone de los siguientes comandos de ejecución y verificación:

```bash
npm run start
npm run android
npm run ios
npm run web
npm run lint
```

El comando más relevante para revisión estática es:

```bash
npm run lint
```

Resultado obtenido en la revisión del proyecto móvil:

```bash
> lumen@1.0.0 lint
> expo lint
```

El comando finalizó sin mostrar errores en la salida de consola.

No se han localizado pruebas unitarias automatizadas. En una versión más completa del proyecto, se recomienda añadir pruebas para:

- Funciones de filtrado de productos.
- Formateo de precios y fechas.
- Servicio mock de facturas.
- Componentes reutilizables.
- Flujos de navegación principales.
- Validaciones de formularios.

[tabla pruebas técnicas]
