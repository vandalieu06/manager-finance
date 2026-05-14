# Contexto para la siguiente sesión

## Objetivo actual

Se está construyendo un sistema de maquetación para que ChatGPT genere en Figma la memoria formal de Lumen usando los copies de `final/*.md`.

El archivo principal es:

- `DESIGNLAYOUT.md`

La memoria debe generarse como páginas A4 verticales en Figma, siguiendo una rejilla estricta y el estilo visual de la app móvil Lumen.

## Archivos importantes

- `DESIGNLAYOUT.md`: sistema actual de maquetación. Es la fuente principal.
- `final/00-indice.md`: índice obligatorio de la memoria.
- `final/*.md`: copies finales que se deben usar para rellenar la memoria.
- `DESIGN.md`: solo se usa como referencia de estructura documental, no de estética.
- `/home/adri/dev/github/manager-finance-repos/mobile-app`: app móvil usada como fuente visual principal.

## Referencias Figma

Archivo Figma principal:

- `https://www.figma.com/design/JbBnf8LdpmtQavzNqcRlmu/Manager-Finance`

Nodos relevantes:

- `369:28` — `A4 - 3`: referencia base positiva para página interior.
- `381:2` — ejemplo rechazado. No respeta bien la rejilla.
- `389:23` — referencia útil para tabla/listado limpio.
- `389:82` — referencia útil para cards de recursos/tecnologías.
- `390:2` — referencia positiva para texto + foto/placeholder lateral.
- `390:23` — referencia útil para pasos/listado estructurado.

Regla importante: si se usa ChatGPT/Figma, siempre hay que pasar link de Figma, pestaña/página destino y nodo de referencia. Si no, el resultado falla o se coloca en la pestaña equivocada.

## Decisiones cerradas

- La memoria se maqueta en A4 vertical: `595 x 842`.
- El marco principal es `x=10, y=20, w=575, h=802`.
- El contenido principal solo puede ir entre `y=137` y `y=705`.
- Los decoradores inferiores no se usan como zona de contenido.
- La fuente visual viene de la app móvil, no de `DESIGN.md`.
- Estilo: Red Hat Mono, blanco, negro, turquesa `#4ECDC4`, naranja `#F76132`.
- Bordes negros de `3px`.
- Sombras duras `4px 4px`, solo en cards, fotos, capturas, placeholders o bloques destacados.
- Los textos normales, H3/H4 simples y captions no deben llevar sombra.
- Las fotos/capturas pendientes son placeholders naranjas.
- Si hay dos o más capturas en una página, usar plantilla de capturas, no `Texto + Imagen Lateral`.
- La portada es única y no se trata como plantilla reutilizable.
- No repetir plantillas por comodidad. Hay que cuidar el ritmo editorial.
- Las cards solo se usan cuando aportan claridad: stacks, tecnologías, datos clave, avisos, resúmenes o agrupaciones reales.
- Si se añaden logos de tecnologías, deben ir dentro del sistema visual y no romper la paleta.

## Rejilla y texto

Regla nueva importante:

- Los bloques de texto deben empezar en una fila de rejilla.
- Deben ocupar al menos dos filas completas.
- No pueden ocupar `1.5` filas, `2.5` filas ni empezar/terminar a media fila.
- Si sobra espacio, se deja aire dentro del bloque.
- Si el texto no cabe, se amplía a la siguiente fila completa o se mueve el bloque completo a la página siguiente.
- H3/H4 y captions también deben alinearse a fila de rejilla.

## Jerarquía Markdown

Los archivos de `final/` marcan bien la jerarquía.

La intención es mapear:

- `#`: capítulo/cabecera principal.
- `##`: subtítulo principal de página.
- `###`: título simple con decorador ligero.
- `####`: título aún más discreto.
- Listas y tablas: estructuras limpias, sin convertir todo en cards.
- Imágenes/capturas: placeholder naranja si falta recurso final.

Pendiente de mejorar más:

- Definir con precisión el decorador de H3 y H4.
- Aclarar cuándo usar línea turquesa, barra naranja lateral o solo tipografía.
- Reforzar que H3/H4 no deben convertirse en cards.

## Plantillas actuales

`DESIGNLAYOUT.md` contiene 7 plantillas:

1. Texto + Imagen Lateral.
2. Card Protagonista.
3. Bloque de Acento Naranja.
4. Tabla Brutalista.
5. Esquema Técnico.
6. Capturas / Prototipo.
7. Anexos / Contenido Denso.

Regla de ritmo:

- Elegir plantilla por contenido y por ritmo visual.
- Si dos plantillas son válidas, elegir la que evite repetición.
- Si un capítulo tiene más de tres páginas, debe combinar al menos dos tipos de página cuando el contenido lo permita.

## Problemas detectados

- ChatGPT tiende a repetir plantillas demasiado.
- Si no se le pasa link Figma y pestaña/nodo destino, no acierta bien.
- Tiende a colocar elementos “a ojo” si no se le obliga a respetar coordenadas.
- Puede crear páginas visualmente aceptables pero que no respetan la rejilla.
- Puede abusar de cards.
- Puede usar bloques de texto con alturas intermedias, como una fila y media.

## Qué hacer en la siguiente sesión

Si el usuario pide seguir mejorando `DESIGNLAYOUT.md`, revisar primero el archivo actual y continuar desde ahí.

Mejoras probables:

- Añadir reglas explícitas de H3/H4 y decoradores simples.
- Añadir una tabla Markdown -> Figma.
- Añadir ejemplos positivos/negativos por jerarquía.
- Reforzar qué elementos pueden tener sombra.
- Crear un prompt maestro final para generar capítulos completos.
- Crear un prompt específico para auditar páginas ya generadas en Figma.

Si el usuario pide generar Figma:

1. Cargar primero la skill `figma-use`.
2. Pedir o confirmar:
   - link completo de Figma;
   - pestaña/página destino;
   - nodo base o referencia;
   - capítulo o archivo `final/*.md`;
   - estado de página anterior.
3. No crear nada si falta contexto Figma.

## Prompt breve para retomar

```text
Estamos trabajando en DESIGNLAYOUT.md, el sistema para maquetar en Figma la memoria formal de Lumen usando final/*.md.
Lee CONTEXTO_SIGUIENTE_SESION.md y DESIGNLAYOUT.md.
Continúa desde el estado actual, respetando las reglas de rejilla, ritmo editorial, placeholders naranjas, jerarquía Markdown y contexto Figma obligatorio.
```
