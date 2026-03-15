# Documentación de Implementación del Diseño Figma

## Resumen

Implementación del diseño de login de Lumen desde Figma usando HTML y Tailwind CSS con máxima fidelidad al diseño original.

---

## Tokens de Diseño Extraídos

### Colores

| Token            | Valor Hex | Uso                                                 |
| ---------------- | --------- | --------------------------------------------------- |
| `primary`        | `#6d5dfb` | Color principal (morado), usado en labels y botones |
| `primary-dark`   | `#362c77` | Color primario oscuro, usado en bordes de inputs    |
| `neutral-light`  | `#f7f7fb` | Fondo claro de inputs y contenedores                |
| `neutral-medium` | `#d4d4e0` | Color de placeholders                               |
| `neutral-dark`   | `#1f1f29` | Bordes del formulario principal                     |

### Espaciados

| Token     | Valor  | Uso                             |
| --------- | ------ | ------------------------------- |
| `spacers` | `8px`  | Padding pequeño                 |
| `spacerm` | `16px` | Padding medio estándar          |
| `gap-20`  | `20px` | Gap entre elementos principales |
| `gap-45`  | `45px` | Gap en el header entre logos    |

### Tipografía

- **Familia**: Inter (Extra Bold)
- **Peso**: 800 (Extra Bold)
- **Tamaño base**: 16px
- **Line height**: Normal

### Bordes

- **Border radius pequeño**: `8px` (inputs)
- **Border radius medio**: `16px` (contenedores)
- **Border radius pequeño (contenedor de logo)**: `6px`

### Sombras

- **Card shadow**: `0px 4px 4px 0px rgba(0, 0, 0, 0.25)`

---

## Medidas Exactas del Diseño

### Header con Logos

- **Ancho máximo**: 528px
- **Padding**: 16px
- **Border radius**: 16px
- **Gap entre elementos**: 45px
- **Sombra**: Card shadow estándar

#### Logo Escuela

- **Ancho**: 222px
- **Aspect ratio**: 222:114 (aprox. 1.95:1)
- **Background**: #f7f7fb
- **Padding**: 8px
- **Border radius**: 6px

#### Separador

- **Altura**: 76px
- **Ancho**: 0px (línea)
- **Rotación**: 90deg
- **Color**: #6d5dfb (primary)
- **Grosor**: 3px (aproximado)

#### Logo Hexagonal

- **Ancho**: 104px
- **Alto**: 123px
- **Color exterior**: #362c77 (primary-dark)
- **Color interior**: #6d5dfb (primary)

### Formulario de Login

- **Ancho máximo**: 440px
- **Alto**: 298px
- **Background**: #f7f7fb (neutral-light)
- **Border**: 2px solid #1f1f29 (neutral-dark)
- **Border radius**: 16px
- **Padding**: 16px
- **Display**: Flex column con `justify-between`

#### Labels

- **Fuente**: Inter Extra Bold
- **Tamaño**: 16px
- **Color**: #6d5dfb (primary)
- **Gap con input**: 16px

#### Inputs

- **Alto**: 66px
- **Ancho**: 100% del contenedor
- **Background**: #f7f7fb (neutral-light)
- **Border**: 1px solid #362c77 (primary-dark)
- **Border radius**: 8px
- **Padding horizontal**: 16px
- **Padding vertical**: 8px
- **Font**: Inter Extra Bold 16px
- **Placeholder color**: #d4d4e0 (neutral-medium)

---

## Decisiones de Implementación

### 1. **CDN de Tailwind CSS**

- Uso de CDN para prototipado rápido
- Configuración inline con `tailwind.config`
- **Recomendación**: Para producción, instalar Tailwind vía npm

### 2. **Fuente Inter**

- Cargada desde Google Fonts
- Pesos: 400 (regular) y 800 (extra bold)
- **Nota**: El diseño usa principalmente Extra Bold (800)

### 3. **Placeholders de Imágenes**

- Logo escuela: Placeholder con dimensiones correctas (222x114)
- Logo hexagonal: SVG generado con formas hexagonales
- **Acción requerida**: Reemplazar con assets reales

### 4. **Responsive Design**

- Mobile-first approach
- Máx. ancho de 528px para header
- Máx. ancho de 440px para formulario
- Padding lateral de 24px en móvil (`px-6`)

### 5. **Estados Interactivos**

- Focus en inputs: Ring de 2px en color primary
- Hover en botón: Cambio a primary-dark
- Transiciones suaves de 200ms

### 6. **Accesibilidad**

- Labels asociados correctamente con inputs
- Placeholders descriptivos
- Alto contraste en textos
- Elementos focusables claramente visibles

---

## Assets Necesarios

### Imágenes Requeridas

1. **Logo Jaume Viladoms Centre Educatiu**

   - Dimensiones recomendadas: 222x114px (o múltiplo)
   - Formato: PNG con fondo transparente o JPG
   - Ubicación sugerida: `/assets/logo-escuela.png`

2. **Logo TaskGener (Hexágono)**
   - Dimensiones: 104x123px
   - Formato: SVG (vector) o PNG de alta resolución
   - Ubicación sugerida: `/assets/logo-taskgener.svg`

### Reemplazar Placeholders

```html
<!-- Logo Escuela -->
<img
	src="./assets/logo-escuela.png"
	alt="Logo Jaume Viladoms" />

<!-- Logo Hexagonal -->
<img
	src="./assets/logo-taskgener.svg"
	alt="TaskGener" />
```

---

## Valores que Difieren del Diseño

| Elemento     | Diseño Figma | Implementación       | Razón                           |
| ------------ | ------------ | -------------------- | ------------------------------- |
| Separador    | Línea rotada | Border con rotate    | Aproximación visual equivalente |
| Font weight  | Extra Bold   | font-extrabold (800) | Clase de Tailwind más cercana   |
| Altura input | 66px         | h-[66px]             | Valor arbitrario exacto         |
| Gap header   | 45px         | gap-[45px]           | Valor arbitrario exacto         |

---

## Mejoras y Sugerencias

### Funcionalidad

1. **Validación de formulario**

   - Validación en tiempo real
   - Mensajes de error específicos por campo
   - Indicadores visuales de validación

2. **Botón de "Mostrar contraseña"**

   - Toggle para ver/ocultar contraseña
   - Icono de ojo (usar lucide-react o similar)

3. **Recordar usuario**

   - Checkbox "Recordar credenciales"
   - Implementar con localStorage

4. **Enlace "Olvidé mi contraseña"**
   - Añadir debajo del formulario
   - Flujo de recuperación de contraseña

### Accesibilidad

1. **ARIA labels**

   - Añadir aria-describedby para mensajes de error
   - aria-invalid cuando hay errores

2. **Navegación por teclado**
   - Orden de tabulación lógico
   - Submit con Enter

### Performance

1. **Optimización de imágenes**

   - Usar WebP para mejor compresión
   - Lazy loading si hay múltiples imágenes

2. **Build de Tailwind**
   - Instalar Tailwind localmente
   - Purgar clases no utilizadas
   - Minificar CSS final

### Responsive

1. **Breakpoints adicionales**

   - Tablet: Ajustar espaciados
   - Desktop grande: Mantener tamaño máximo centrado

2. **Orientación**
   - Landscape en móvil: Reducir padding vertical

---

## Código de Instalación (Producción)

Si deseas usar Tailwind en producción en lugar del CDN:

```bash
# Instalar dependencias
npm install -D tailwindcss postcss autoprefixer

# Inicializar Tailwind
npx tailwindcss init

# Crear archivo CSS de entrada
# src/input.css
@tailwind base;
@tailwind components;
@tailwind utilities;

# Build CSS
npx tailwindcss -i ./src/input.css -o ./dist/output.css --watch
```

Luego en el HTML:

```html
<link
	href="./dist/output.css"
	rel="stylesheet" />
```

---

## Testing Checklist

- [ ] Verificar diseño en Chrome, Firefox, Safari
- [ ] Probar en móvil (iOS y Android)
- [ ] Validar accesibilidad con screen reader
- [ ] Comprobar contraste de colores (WCAG AA)
- [ ] Probar navegación por teclado
- [ ] Verificar estados hover/focus/active
- [ ] Probar con diferentes tamaños de fuente del navegador
- [ ] Validar HTML (W3C Validator)

---

## Referencias

- **Diseño Figma**: [TaskGener Design](https://www.figma.com/design/zAulmgBMEDtZdLUihnyfiM/TaskGener?node-id=20-2)
- **Tailwind CSS**: https://tailwindcss.com/docs
- **Google Fonts (Inter)**: https://fonts.google.com/specimen/Inter
- **Accesibilidad**: https://www.w3.org/WAI/WCAG21/quickref/

---

**Fecha de implementación**: 11 de diciembre de 2025  
**Versión**: 1.0



