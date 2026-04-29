# 1. Definición del proyecto

## 1.1. Introducción

Lumen es una aplicación móvil orientada a la gestión de finanzas personales. Su objetivo principal es ayudar al usuario a registrar, consultar y comprender mejor sus gastos cotidianos, ofreciendo una visión clara sobre cómo se distribuye su dinero y en qué tipo de productos concentra una mayor parte de su consumo.

La idea del proyecto nace de una necesidad habitual: muchas personas no tienen una visión ordenada de sus gastos porque el registro manual resulta lento, repetitivo o poco cómodo. Lumen propone una solución centrada en el móvil, con una interfaz sencilla y visual, para que el usuario pueda consultar su información financiera de forma rápida.

El proyecto contempla dos vías de registro de información. Por un lado, el usuario puede introducir productos de forma manual. Por otro, se plantea el procesamiento de tickets o facturas mediante reconocimiento óptico de caracteres e inteligencia artificial, con el objetivo de extraer productos, importes y comercios de forma automatizada. En el prototipo móvil revisado, este flujo aparece representado mediante servicios simulados que permiten validar la experiencia de usuario antes de integrarlo con servicios reales de backend, OCR e IA.

[captura pantalla login]

[captura pantalla home]

## 1.1.1. Explicación de qué trata

La aplicación se estructura como una herramienta de apoyo para la economía personal. Permite al usuario acceder a un resumen de su actividad, consultar productos, filtrar gastos, revisar facturas y configurar preferencias básicas de la aplicación.

En el estado actual del frontend móvil, Lumen cuenta con las siguientes áreas principales:

- Inicio, donde se muestran tarjetas resumen y accesos a estadísticas.
- Productos, donde se listan gastos o productos de demostración con filtros por categoría, marca, precio y búsqueda textual.
- Scan, donde se simula el flujo de captura de una factura y se permite añadir productos manualmente.
- Configuración, donde se agrupan opciones de perfil, preferencias, permisos y otras secciones de la aplicación.

El proyecto no se limita únicamente a la interfaz, sino que plantea una arquitectura más amplia formada por frontend móvil, backend, base de datos y servicios de procesamiento de tickets. No obstante, esta memoria diferencia entre lo que está implementado en el prototipo móvil y lo que queda como integración o mejora futura.

## 1.1.2. Propósitos y objetivos que se quieren alcanzar

El propósito general del proyecto es desarrollar una aplicación móvil que ayude a mejorar la gestión de gastos personales mediante una experiencia clara, visual y fácil de utilizar.

Los objetivos principales son:

- Diseñar una interfaz móvil sencilla y comprensible para consultar información financiera.
- Permitir el registro y consulta de productos o gastos cotidianos.
- Clasificar los gastos en categorías para facilitar su interpretación.
- Ofrecer filtros y búsquedas que permitan localizar productos concretos.
- Representar el flujo de escaneo de facturas como base para una futura integración con OCR e IA.
- Permitir la revisión de facturas y productos detectados o introducidos manualmente.
- Aplicar una identidad visual coherente basada en el concepto de Lumen como herramienta que aporta claridad sobre el dinero.
- Utilizar tecnologías actuales de desarrollo móvil, como React Native y Expo.
- Documentar el proyecto de forma que pueda ser entendido, mantenido y ampliado.

Como objetivo formativo, el proyecto permite aplicar conocimientos de desarrollo de interfaces, diseño de software, organización de proyectos, documentación técnica, control de versiones y análisis de requisitos.
