# Animando Estructuras de Datos: Stack y Queue

Proyecto del curso **Algoritmos y Estructuras de Datos**.

Es un video animado hecho con [Manim Community](https://www.manim.community/) que explica dos estructuras de datos lineales: el **stack** (pila) y la **queue** (cola). El video muestra paso a paso sus operaciones, compara las dos estructuras lado a lado, explica cómo se implementa una queue con un array circular y termina con una aplicación del stack: verificar si los paréntesis de una expresión están balanceados.

### Integrantes

- Tamara Iberico
- Maria Fernanda Carbajal

## Video demo

▶️ [Ver el video demo en YouTube](https://youtu.be/ldplMvxiCBc)

## Software requerido

| Software | Versión | Notas |
|---|---|---|
| Python | 3.10 a 3.13 | Probado con Python 3.13 |
| Manim Community | 0.21.0 | Se instala desde `requirements.txt` |
| FFmpeg | — | No hace falta instalarlo aparte: Manim (desde la v0.19) usa PyAV, que ya trae FFmpeg incluido |
| LaTeX | — | **No se necesita.** El proyecto usa solo `Text` y no usa `MathTex` ni `Tex` |

## Instalación en macOS

1. Instalar [Homebrew](https://brew.sh/) si no lo tienes:

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Instalar Python y las librerías de sistema que usa Manim (Cairo y Pango para dibujar el texto):

   ```bash
   brew install python cairo pango pkg-config
   ```

3. Clonar el repositorio y entrar a la carpeta:

   ```bash
   git clone https://github.com/waffles-gif/AED_proyecto.git
   cd AED_proyecto
   ```

4. Crear y activar un entorno virtual:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

5. Instalar las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

6. Comprobar que Manim quedó instalado:

   ```bash
   manim --version
   ```

## Cómo ejecutar

Los comandos se ejecutan desde la carpeta del proyecto y con el entorno virtual activado.

### Vista previa (baja calidad, rápida)

```bash
manim -pql main.py VideoCompleto
```

- `-p` abre el video al terminar de generarse.
- `-ql` usa calidad baja (480p, 15 fps) para que sea rápido.

El video queda en `media/videos/main/480p15/VideoCompleto.mp4`.

También se puede generar una sola sección para revisarla por separado. Las escenas disponibles son `Titulo`, `Stack`, `Queue`, `Comparacion`, `ArrayCircular`, `Parentesis` y `Creditos`. Por ejemplo:

```bash
manim -pql main.py Stack
```

### Render final (alta calidad)

```bash
manim -qh main.py VideoCompleto
```

- `-qh` usa calidad alta (1080p, 60 fps).

El video final queda en `media/videos/main/1080p60/VideoCompleto.mp4`.

## Estructuras de datos del video

### Stack (pila): LIFO

Un stack funciona con la regla **LIFO** (*Last In, First Out*): el último elemento que entra es el primero que sale, como una pila de platos. Solo se puede agregar y quitar por arriba (el *top*).

| Operación | Qué hace | Costo |
|---|---|---|
| `push(x)` | Agrega `x` en el top | O(1) |
| `pop()` | Saca el elemento del top | O(1) |
| `top()` | Devuelve el elemento del top sin sacarlo | O(1) |

Las tres operaciones son O(1) porque solo tocan el extremo superior. Nunca hace falta recorrer ni mover los demás elementos.

### Queue (cola): FIFO

Una queue funciona con la regla **FIFO** (*First In, First Out*): el primer elemento que entra es el primero que sale, como una fila de personas. Se entra por atrás (el *rear*) y se sale por adelante (el *front*).

| Operación | Qué hace | Costo |
|---|---|---|
| `enqueue(x)` | Agrega `x` en el rear | O(1) |
| `dequeue()` | Saca el elemento del front | O(1) |
| `front()` | Devuelve el elemento del front sin sacarlo | O(1) |

**Implementación con array circular.** Si la queue se guarda en un array y cada `dequeue` corriera todos los elementos una posición a la izquierda, sacar un elemento costaría O(n). Con un array circular los elementos no se mueven: lo que avanza son los índices `front` y `rear`, y cuando llegan al final del array vuelven al inicio usando el módulo:

```text
rear  = (rear + 1) % tamaño    # en enqueue
front = (front + 1) % tamaño   # en dequeue
```

Así se reutilizan las posiciones que quedaron libres al inicio del array, y tanto `enqueue` como `dequeue` son O(1).

## Estructura del repositorio

```text
AED_proyecto/
├── main.py            # Las 7 secciones del video y la escena VideoCompleto que las une
├── utilidades.py      # Colores, textos, datos del proyecto y clases visuales
│                      # (PilaVisual, ColaVisual, ArregloVisual)
├── requirements.txt   # Dependencias de Python
├── README.md
└── media/             # Salida de Manim (se genera al renderizar, no se sube al repo)
```

Secciones del video (en `main.py`):

1. **Título**: nombre del proyecto, curso e integrantes.
2. **Stack**: `push`, `pop`, puntero `top` y la regla LIFO.
3. **Queue**: `enqueue`, `dequeue`, punteros `front` y `rear` y la regla FIFO.
4. **Comparación**: stack y queue lado a lado con las mismas operaciones.
5. **Array circular**: cómo una queue reutiliza las posiciones libres de un array de tamaño fijo.
6. **Paréntesis balanceados**: aplicación del stack para validar `([]{})`.
7. **Créditos**.
