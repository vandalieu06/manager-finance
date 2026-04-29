# 7. Manual de instalación y configuración

Este manual describe la instalación y ejecución de la aplicación móvil revisada. La instalación del backend, base de datos, OCR e IA debe completarse tras revisar los servicios correspondientes.

## Requisitos previos

Para ejecutar la aplicación móvil es necesario disponer de:

- Node.js instalado.
- npm como gestor de paquetes.
- Git para clonar o actualizar el repositorio.
- Expo Go, emulador Android, simulador iOS o navegador web.

## Instalación de dependencias

Desde la carpeta del proyecto móvil:

```bash
cd /home/adri/dev/github/manager-finance-repos/mobile-app
npm install
```

## Ejecución en desarrollo

Para iniciar el servidor de desarrollo de Expo:

```bash
npm run start
```

Para abrir la aplicación en Android:

```bash
npm run android
```

Para abrir la aplicación en iOS:

```bash
npm run ios
```

Para ejecutar la aplicación en web:

```bash
npm run web
```

## Comprobación de calidad

Para ejecutar la revisión de lint:

```bash
npm run lint
```

Resultado obtenido:

```bash
> lumen@1.0.0 lint
> expo lint
```

El comando finalizó sin mostrar errores en la salida de consola.

## Configuración de Firebase

La aplicación inicializa Firebase desde el archivo `src/services/firebase.ts`. En el estado actual, la configuración está incluida directamente en el código y se utiliza para obtener el objeto `auth`, que se consume en la pantalla de login.

En una versión productiva, esta configuración debería gestionarse mediante variables de entorno o mecanismos seguros de configuración.

## Configuración de backend a completar tras revisión

La configuración completa de backend debe documentarse cuando se revise el servicio real. Este apartado deberá incluir:

- Variables de entorno.
- Base de datos.
- Migraciones.
- Endpoints disponibles.
- Autenticación entre frontend y backend.
- Servicio OCR/IA.
- Despliegue en servidor.

[manual instalación backend]
