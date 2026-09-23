"""
Utilidades compartidas por todas las escenas del video.

Aquí se definen la paleta de colores, los datos del proyecto y
funciones auxiliares (cajas con número, flechas, etiquetas) para
no repetir código en cada escena.
"""
from manim import *

# ---------------------------------------------------------------------------
# Datos del proyecto
# ---------------------------------------------------------------------------
TITULO = "Animando Estructuras de Datos"
SUBTITULO = "Stack y Queue"
CURSO = "Algoritmos y Estructuras de Datos"
AUTORES = ["Tamara Iberico", "Maria Fernanda Carbajal"]

# ---------------------------------------------------------------------------
# Paleta de colores (consistente en todo el video)
# ---------------------------------------------------------------------------
COLOR_FONDO = "#0F1117"      # fondo oscuro
COLOR_STACK = "#58C4DD"      # azul: todo lo relacionado con el stack
COLOR_QUEUE = "#F4A259"      # naranja: todo lo relacionado con la queue
COLOR_ACENTO = "#FFD166"     # amarillo: flechas y punteros
COLOR_OK = "#83C167"         # verde: resultados correctos
COLOR_ERROR = "#FC6255"      # rojo: errores / elemento que sale
COLOR_TEXTO = WHITE
COLOR_SECUNDARIO = "#9AA0A6"  # gris: texto secundario

# Tamaños de texto
TAM_TITULO = 48
TAM_SUBTITULO = 36
TAM_NORMAL = 28
TAM_PEQUENO = 22

# Lado de cada caja (celda) de las estructuras
LADO_CAJA = 0.9

# Centro del panel derecho donde se escriben las operaciones
PANEL_DERECHO = RIGHT * 2.8


def configurar_escena(escena: Scene) -> None:
    """Aplica el fondo oscuro común a una escena."""
    escena.camera.background_color = COLOR_FONDO


def texto(contenido: str, tam: int = TAM_NORMAL, color=COLOR_TEXTO, **kwargs) -> Text:
    """Crea un Text con los valores por defecto del proyecto."""
    return Text(contenido, font_size=tam, color=color, **kwargs)


def codigo(contenido: str, color=COLOR_TEXTO, tam: int = TAM_SUBTITULO) -> Text:
    """Texto con fuente monoespaciada para mostrar operaciones como push(1)."""
    return Text(contenido, font="Menlo", font_size=tam, color=color)


def encabezado(contenido: str, color) -> Text:
    """Título de sección, arriba de la pantalla."""
    return texto(contenido, TAM_SUBTITULO, color, weight=BOLD).to_edge(UP, buff=0.5)


def crear_caja(valor, color, lado: float = LADO_CAJA) -> VGroup:
    """Caja cuadrada con un número (o símbolo) centrado.

    Devuelve VGroup(cuadro, etiqueta): caja[0] es el cuadro y caja[1] el texto.
    """
    cuadro = Square(
        side_length=lado, color=color, stroke_width=4,
        fill_color=color, fill_opacity=0.25,
    )
    etiqueta = texto(str(valor), TAM_NORMAL + 4, weight=BOLD).move_to(cuadro)
    return VGroup(cuadro, etiqueta)


def crear_puntero(etiqueta: str, color=COLOR_ACENTO, apunta=LEFT, largo: float = 0.8) -> VGroup:
    """Flecha con nombre (por ejemplo "top", "front", "rear").

    `apunta` es la dirección hacia donde mira la flecha; el nombre queda
    en el extremo opuesto. Para colocarlo junto a un objeto usar:
        puntero.next_to(objeto, -apunta)
    """
    flecha = Arrow(
        start=-apunta * largo, end=ORIGIN, buff=0, color=color,
        stroke_width=5, max_tip_length_to_length_ratio=0.35,
    )
    nombre = texto(etiqueta, TAM_PEQUENO, color).next_to(flecha, -apunta, buff=0.1)
    return VGroup(flecha, nombre)


def anims_reemplazo(viejo, nuevo) -> list:
    """Animaciones para cambiar un texto por otro (viejo puede ser None)."""
    anims = [FadeIn(nuevo, shift=UP * 0.2)]
    if viejo is not None:
        anims.append(FadeOut(viejo, shift=UP * 0.2))
    return anims


def reemplazar(escena: Scene, viejo, nuevo, tiempo: float = 0.5):
    """Cambia un texto por otro con un desvanecido suave y devuelve el nuevo."""
    escena.play(*anims_reemplazo(viejo, nuevo), run_time=tiempo)
    return nuevo


def crear_insignia(sigla: str, significado: str, color) -> VGroup:
    """Recuadro con una sigla y su significado, por ejemplo LIFO / Last In, First Out."""
    contenido = VGroup(
        texto(sigla, TAM_SUBTITULO, color, weight=BOLD),
        texto(significado, TAM_PEQUENO, COLOR_SECUNDARIO),
    ).arrange(DOWN, buff=0.15)
    marco = SurroundingRectangle(contenido, color=color, buff=0.25, corner_radius=0.1)
    return VGroup(contenido, marco)


def limpiar(escena: Scene, tiempo: float = 0.6) -> None:
    """Desvanece todos los objetos que haya en pantalla."""
    if escena.mobjects:
        escena.play(*[FadeOut(m) for m in escena.mobjects], run_time=tiempo)


# ---------------------------------------------------------------------------
# Representación visual de un stack
# ---------------------------------------------------------------------------
class PilaVisual:
    """Stack dibujado como un contenedor vertical abierto por arriba.

    Guarda las cajas en una lista: el último elemento de la lista es el top.
    Los métodos devuelven animaciones (en lugar de reproducirlas) para poder
    combinarlas con otras en un mismo `play`, por ejemplo en la comparación.
    """

    def __init__(self, capacidad: int = 4, color=COLOR_STACK, posicion=ORIGIN, lado: float = LADO_CAJA):
        self.color = color
        self.lado = lado
        self.cajas = []
        ancho = lado + 0.3
        alto = capacidad * lado + 0.3
        # Contenedor en forma de "U": paredes laterales y fondo
        self.contenedor = VMobject(color=COLOR_SECUNDARIO, stroke_width=4)
        self.contenedor.set_points_as_corners([
            [-ancho / 2, alto, 0], [-ancho / 2, 0, 0],
            [ancho / 2, 0, 0], [ancho / 2, alto, 0],
        ])
        self.contenedor.move_to(posicion)

    def posicion(self, i: int):
        """Centro de la ranura i (0 = fondo de la pila)."""
        return self.contenedor.get_bottom() + UP * (0.15 + self.lado * (i + 0.5))

    def push(self, valor):
        """Crea la caja en el top; devuelve (caja, animación de caída desde arriba)."""
        caja = crear_caja(valor, self.color, self.lado * 0.9)
        caja.move_to(self.posicion(len(self.cajas)))
        self.cajas.append(caja)
        return caja, FadeIn(caja, shift=DOWN * 1.5)

    def pop(self):
        """Quita la caja del top de la lista y la devuelve (la animación la decide la escena)."""
        return self.cajas.pop()

    def top(self):
        """Caja que está en el top (o None si la pila está vacía)."""
        return self.cajas[-1] if self.cajas else None


# ---------------------------------------------------------------------------
# Representación visual de una queue
# ---------------------------------------------------------------------------
class ColaVisual:
    """Queue dibujada como un tubo horizontal abierto en ambos extremos.

    Los elementos entran por la derecha (rear) y salen por la izquierda
    (front), como una fila de personas. cajas[0] es el front y cajas[-1]
    el rear.
    """

    def __init__(self, capacidad: int = 5, color=COLOR_QUEUE, posicion=ORIGIN, lado: float = LADO_CAJA):
        self.color = color
        self.lado = lado
        self.cajas = []
        largo = capacidad * lado + 0.3
        alto = lado + 0.3
        # Dos líneas paralelas: pared superior e inferior del tubo
        superior = Line([-largo / 2, alto / 2, 0], [largo / 2, alto / 2, 0])
        inferior = Line([-largo / 2, -alto / 2, 0], [largo / 2, -alto / 2, 0])
        self.contenedor = VGroup(superior, inferior).set_stroke(COLOR_SECUNDARIO, width=4)
        self.contenedor.move_to(posicion)

    def posicion(self, i: int):
        """Centro de la ranura i (0 = front, a la izquierda)."""
        return self.contenedor.get_left() + RIGHT * (0.15 + self.lado * (i + 0.5))

    def enqueue(self, valor):
        """Crea la caja al final; devuelve (caja, animación de entrada desde la derecha)."""
        caja = crear_caja(valor, self.color, self.lado * 0.9)
        caja.move_to(self.posicion(len(self.cajas)))
        self.cajas.append(caja)
        return caja, FadeIn(caja, shift=LEFT * 1.5)

    def dequeue(self):
        """Quita la caja del front de la lista y la devuelve."""
        return self.cajas.pop(0)

    def reacomodar(self):
        """Animaciones para que los elementos restantes avancen una posición."""
        return [caja.animate.move_to(self.posicion(i)) for i, caja in enumerate(self.cajas)]

    def front(self):
        return self.cajas[0] if self.cajas else None

    def rear(self):
        return self.cajas[-1] if self.cajas else None


# ---------------------------------------------------------------------------
# Representación visual de un array de tamaño fijo (para la cola circular)
# ---------------------------------------------------------------------------
class ArregloVisual:
    """Fila de celdas vacías con su índice debajo.

    A diferencia de ColaVisual, aquí los elementos NO se mueven: cada valor
    se queda en su celda y lo que avanza son los índices front y rear.
    """

    def __init__(self, tamano: int = 5, color=COLOR_QUEUE, posicion=ORIGIN, lado: float = LADO_CAJA):
        self.color = color
        self.lado = lado
        self.celdas = VGroup(*[
            Square(side_length=lado, color=COLOR_SECUNDARIO, stroke_width=3) for _ in range(tamano)
        ]).arrange(RIGHT, buff=0).move_to(posicion)
        self.indices = VGroup(*[
            texto(str(i), TAM_PEQUENO, COLOR_SECUNDARIO).next_to(celda, DOWN, buff=0.15)
            for i, celda in enumerate(self.celdas)
        ])
        self.valores = [None] * tamano  # caja guardada en cada posición

    def poner(self, i: int, valor):
        """Coloca un valor en la celda i; devuelve (caja, animación)."""
        caja = crear_caja(valor, self.color, self.lado * 0.9).move_to(self.celdas[i])
        self.valores[i] = caja
        return caja, FadeIn(caja, shift=DOWN * 0.5)

    def quitar(self, i: int):
        """Vacía la celda i y devuelve la caja que estaba ahí."""
        caja, self.valores[i] = self.valores[i], None
        return caja
