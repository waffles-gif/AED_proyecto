
from manim import *

from utilidades import *

# 1. Título
def seccion_titulo(escena: Scene) -> None:
    titulo = texto(TITULO, TAM_TITULO, weight=BOLD)
    subtitulo = texto(
        SUBTITULO, TAM_TITULO, weight=BOLD,
        t2c={"Stack": COLOR_STACK, "Queue": COLOR_QUEUE},
    )
    bloque_titulo = VGroup(titulo, subtitulo).arrange(DOWN, buff=0.25)

    linea = Line(LEFT * 4, RIGHT * 4, color=COLOR_ACENTO, stroke_width=3)
    curso = texto(CURSO, TAM_PEQUENO, COLOR_SECUNDARIO)
    autores = texto(", ".join(AUTORES), TAM_NORMAL)

    grupo = VGroup(bloque_titulo, linea, curso, autores).arrange(DOWN, buff=0.4)

    escena.play(Write(bloque_titulo), run_time=1.5)
    escena.play(GrowFromCenter(linea), FadeIn(curso, shift=UP * 0.2), run_time=0.8)
    escena.play(FadeIn(autores, shift=UP * 0.2), run_time=0.8)
    escena.wait(1.5)
    escena.play(FadeOut(grupo), run_time=0.6)


class Titulo(Scene):
    def construct(self):
        configurar_escena(self)
        seccion_titulo(self)

# 2. Stack

def seccion_stack(escena: Scene) -> None:
    titulo = encabezado("Stack (pila)", COLOR_STACK)
    pila = PilaVisual(posicion=LEFT * 3 + DOWN * 0.9, lado=1.1)
    escena.play(Write(titulo), Create(pila.contenedor), run_time=1.2)

    idea = texto("Solo se puede entrar y salir por arriba", TAM_NORMAL).move_to(PANEL_DERECHO + UP * 0.3)
    escena.play(FadeIn(idea, shift=UP * 0.2), run_time=0.8)
    escena.wait(2)
    escena.play(FadeOut(idea), run_time=0.4)

    op, descripcion, puntero_top = None, None, None
    for valor in (1, 2, 3):
        op = reemplazar(escena, op, codigo(f"push({valor})", COLOR_STACK).move_to(PANEL_DERECHO + UP * 1))
        caja, animacion = pila.push(valor)
        escena.play(animacion, run_time=0.8)
        if puntero_top is None:
            # La flecha "top" aparece con el primer elemento
            puntero_top = crear_puntero("top").next_to(caja, RIGHT, buff=0.35)
            descripcion = texto("agrega el elemento en el top", TAM_PEQUENO, COLOR_SECUNDARIO)
            descripcion.next_to(op, DOWN, buff=0.4)
            escena.play(FadeIn(puntero_top, shift=LEFT * 0.3), FadeIn(descripcion), run_time=0.6)
        else:
            escena.play(puntero_top.animate.next_to(caja, RIGHT, buff=0.35), run_time=0.5)
        escena.wait(1)

    op = reemplazar(escena, op, codigo("pop()", COLOR_STACK).move_to(op))
    descripcion = reemplazar(
        escena, descripcion,
        texto("saca el elemento del top", TAM_PEQUENO, COLOR_SECUNDARIO).move_to(descripcion),
    )
    caja = pila.pop()

    escena.play(caja[0].animate.set_color(COLOR_ERROR), run_time=0.6)
    escena.play(caja.animate.move_to([caja.get_x(), pila.contenedor.get_top()[1] + 0.8, 0]), run_time=0.8)

    sale = texto("sale el 3: el último que entró", TAM_NORMAL, t2c={"3": COLOR_ERROR})
    sale.next_to(descripcion, DOWN, buff=0.5)
    escena.play(
        FadeOut(caja, shift=RIGHT),
        puntero_top.animate.next_to(pila.top(), RIGHT, buff=0.35),
        FadeIn(sale, shift=UP * 0.2),
        run_time=0.8,
    )
    escena.wait(1.5)

    lifo = crear_insignia("LIFO", "Last In, First Out", COLOR_STACK).next_to(sale, DOWN, buff=0.4)
    escena.play(FadeIn(lifo, shift=UP * 0.2), run_time=1)
    costo = texto("push, pop y top: O(1)", TAM_PEQUENO).next_to(lifo, DOWN, buff=0.4)
    escena.play(FadeIn(costo), run_time=0.6)
    escena.wait(3)
    limpiar(escena)


class Stack(Scene):
    def construct(self):
        configurar_escena(self)
        seccion_stack(self)


# 3. Queue

def seccion_queue(escena: Scene) -> None:
    titulo = encabezado("Queue (cola)", COLOR_QUEUE)
    cola = ColaVisual(posicion=UP * 0.9, lado=1.1)
    # Etiquetas en los extremos del tubo: por dónde se sale y por dónde se entra
    salida = texto("salida", TAM_PEQUENO, COLOR_SECUNDARIO).next_to(cola.contenedor, LEFT, buff=0.3)
    entrada = texto("entrada", TAM_PEQUENO, COLOR_SECUNDARIO).next_to(cola.contenedor, RIGHT, buff=0.3)
    escena.play(Write(titulo), Create(cola.contenedor), FadeIn(salida), FadeIn(entrada), run_time=1.2)

    idea = texto("Se entra por atrás y se sale por adelante", TAM_NORMAL).move_to(DOWN * 1.8)
    escena.play(FadeIn(idea, shift=UP * 0.2), run_time=0.8)
    escena.wait(2)
    escena.play(FadeOut(idea), run_time=0.4)

    op, descripcion = None, None
    puntero_front, puntero_rear = None, None
    for valor in (1, 2, 3):
        op = reemplazar(escena, op, codigo(f"enqueue({valor})", COLOR_QUEUE).move_to(DOWN * 1.8))
        caja, animacion = cola.enqueue(valor)
        escena.play(animacion, run_time=0.8)
        if puntero_front is None:
            # Con un solo elemento, front y rear apuntan a la misma caja
            puntero_front = crear_puntero("front", apunta=DOWN).next_to(caja, UP, buff=0.3)
            puntero_rear = crear_puntero("rear", apunta=UP).next_to(caja, DOWN, buff=0.3)
            descripcion = texto("agrega el elemento en el rear", TAM_PEQUENO, COLOR_SECUNDARIO)
            descripcion.next_to(op, DOWN, buff=0.4)
            escena.play(
                FadeIn(puntero_front, shift=DOWN * 0.3), FadeIn(puntero_rear, shift=UP * 0.3),
                FadeIn(descripcion), run_time=0.6,
            )
        else:
            escena.play(puntero_rear.animate.next_to(caja, DOWN, buff=0.3), run_time=0.5)
        escena.wait(1)

    op = reemplazar(escena, op, codigo("dequeue()", COLOR_QUEUE).move_to(op))
    descripcion = reemplazar(
        escena, descripcion,
        texto("saca el elemento del front", TAM_PEQUENO, COLOR_SECUNDARIO).move_to(descripcion),
    )
    caja = cola.dequeue()
    escena.play(caja[0].animate.set_color(COLOR_ERROR), run_time=0.6)
    escena.play(FadeOut(caja, shift=LEFT * 1.8), run_time=0.8)

    sale = texto("sale el 1: el primero que entró", TAM_NORMAL, t2c={"1": COLOR_ERROR})
    sale.next_to(descripcion, DOWN, buff=0.5)
    escena.play(
        *cola.reacomodar(),
        puntero_rear.animate.shift(LEFT * cola.lado),
        FadeIn(sale, shift=UP * 0.2),
        run_time=0.8,
    )
    escena.wait(1.5)

    fifo = crear_insignia("FIFO", "First In, First Out", COLOR_QUEUE)
    costo = texto("enqueue, dequeue y front: O(1)", TAM_PEQUENO)
    VGroup(fifo, costo).arrange(DOWN, buff=0.4).move_to(DOWN * 2.3)
    escena.play(FadeOut(VGroup(op, descripcion, sale)), run_time=0.4)
    escena.play(FadeIn(fifo, shift=UP * 0.2), run_time=1)
    escena.play(FadeIn(costo), run_time=0.6)
    escena.wait(3)
    limpiar(escena)


class Queue(Scene):
    def construct(self):
        configurar_escena(self)
        seccion_queue(self)


# 4. Comparación lado a lado
def seccion_comparacion(escena: Scene) -> None:

    x_pila, x_cola = -3.5, 3.5
    pila = PilaVisual(capacidad=3, posicion=[x_pila, 0.9, 0], lado=1.0)
    cola = ColaVisual(capacidad=3, posicion=[x_cola, 0.9, 0], lado=1.0)
    nombre_pila = texto("Stack", TAM_SUBTITULO, COLOR_STACK, weight=BOLD).move_to([x_pila, 3.2, 0])
    nombre_cola = texto("Queue", TAM_SUBTITULO, COLOR_QUEUE, weight=BOLD).move_to([x_cola, 3.2, 0])
    divisor = DashedLine(UP * 3.5, DOWN * 3.7, color=COLOR_SECUNDARIO, stroke_opacity=0.5)
    escena.play(
        FadeIn(nombre_pila), FadeIn(nombre_cola), Create(divisor),
        Create(pila.contenedor), Create(cola.contenedor), run_time=1.2,
    )

    def codigo_en(contenido, color, x):
        return codigo(contenido, color, TAM_NORMAL + 4).move_to([x, -1.3, 0])

    op_pila, op_cola = None, None
    for valor in (1, 2, 3):
        nuevo_pila = codigo_en(f"push({valor})", COLOR_STACK, x_pila)
        nuevo_cola = codigo_en(f"enqueue({valor})", COLOR_QUEUE, x_cola)
        _, anim_pila = pila.push(valor)
        _, anim_cola = cola.enqueue(valor)
        escena.play(
            anim_pila, anim_cola,
            *anims_reemplazo(op_pila, nuevo_pila), *anims_reemplazo(op_cola, nuevo_cola),
            run_time=0.8,
        )
        op_pila, op_cola = nuevo_pila, nuevo_cola
        escena.wait(0.7)

    nuevo_pila = codigo_en("pop()", COLOR_STACK, x_pila)
    nuevo_cola = codigo_en("dequeue()", COLOR_QUEUE, x_cola)
    escena.play(*anims_reemplazo(op_pila, nuevo_pila), *anims_reemplazo(op_cola, nuevo_cola), run_time=0.5)
    op_pila, op_cola = nuevo_pila, nuevo_cola

    caja_pila, caja_cola = pila.pop(), cola.dequeue()
    escena.play(caja_pila[0].animate.set_color(COLOR_ERROR), caja_cola[0].animate.set_color(COLOR_ERROR), run_time=0.5)
    escena.play(FadeOut(caja_pila, shift=UP * 0.9), FadeOut(caja_cola, shift=LEFT * 1.5), run_time=0.8)
    escena.play(*cola.reacomodar(), run_time=0.6)

    sale_pila = texto("sale el 3", TAM_NORMAL, t2c={"3": COLOR_ERROR}).next_to(op_pila, DOWN, buff=0.3)
    sale_cola = texto("sale el 1", TAM_NORMAL, t2c={"1": COLOR_ERROR}).next_to(op_cola, DOWN, buff=0.3)
    escena.play(FadeIn(sale_pila, shift=UP * 0.2), FadeIn(sale_cola, shift=UP * 0.2), run_time=0.6)
    escena.wait(1.3)

#LIFO vs FIFO
    lifo = crear_insignia("LIFO", "Last In, First Out", COLOR_STACK).next_to(sale_pila, DOWN, buff=0.35)
    fifo = crear_insignia("FIFO", "First In, First Out", COLOR_QUEUE).next_to(sale_cola, DOWN, buff=0.35)
    escena.play(FadeIn(lifo, shift=UP * 0.2), FadeIn(fifo, shift=UP * 0.2), run_time=1)
    escena.wait(3)
    limpiar(escena)


class Comparacion(Scene):
    def construct(self):
        configurar_escena(self)
        seccion_comparacion(self)



# 5. Queue con array circular
def seccion_array_circular(escena: Scene) -> None:
    TAMANO = 5
    titulo = encabezado("Queue con array circular", COLOR_QUEUE)
    arreglo = ArregloVisual(TAMANO, posicion=UP * 0.8, lado=1.1)
    tamano_fijo = texto(f"tamaño fijo: {TAMANO}", TAM_PEQUENO, COLOR_SECUNDARIO)
    tamano_fijo.next_to(arreglo.celdas, RIGHT, buff=0.5)
    escena.play(Write(titulo), Create(arreglo.celdas), FadeIn(arreglo.indices), FadeIn(tamano_fijo), run_time=1.2)

    front, rear = 0, -1
    puntero_front = crear_puntero("front", apunta=DOWN).next_to(arreglo.celdas[front], UP, buff=0.15)
    escena.play(FadeIn(puntero_front, shift=DOWN * 0.3), run_time=0.4)
    puntero_rear = None

    def lugar_rear(i):
        return arreglo.indices[i].get_bottom() + DOWN * 0.1

    def linea_op(contenido):
        return codigo(contenido, COLOR_QUEUE, TAM_NORMAL + 4).move_to(DOWN * 2.6)

    def linea_formula(contenido, color=COLOR_SECUNDARIO):
        return codigo(contenido, color, TAM_PEQUENO + 2).move_to(DOWN * 3.3)

    op = None
    formula = linea_formula("rear = (rear + 1) % 5")
    for valor in (1, 2, 3, 4):
        rear = (rear + 1) % TAMANO
        nuevo_op = linea_op(f"enqueue({valor})")
        caja, anim = arreglo.poner(rear, valor)
        if puntero_rear is None:
            puntero_rear = crear_puntero("rear", apunta=UP)
            puntero_rear.next_to(lugar_rear(rear), DOWN, buff=0)
            mover_rear = FadeIn(puntero_rear, shift=UP * 0.3)
            extra = [FadeIn(formula)]
        else:
            mover_rear = puntero_rear.animate.next_to(lugar_rear(rear), DOWN, buff=0)
            extra = []
        escena.play(anim, mover_rear, *anims_reemplazo(op, nuevo_op), *extra, run_time=0.6)
        op = nuevo_op
        escena.wait(0.4)

    formula = reemplazar(escena, formula, linea_formula("front = (front + 1) % 5"), tiempo=0.4)
    for _ in range(2):
        op = reemplazar(escena, op, linea_op("dequeue()"), tiempo=0.3)
        caja = arreglo.quitar(front)
        escena.play(caja[0].animate.set_color(COLOR_ERROR), run_time=0.3)
        front = (front + 1) % TAMANO
        escena.play(
            FadeOut(caja, shift=UP * 0.6),
            puntero_front.animate.next_to(arreglo.celdas[front], UP, buff=0.15),
            run_time=0.6,
        )

    libres = texto("las posiciones 0 y 1 quedaron libres", TAM_NORMAL, t2c={"0 y 1": COLOR_OK}).move_to(op)
    escena.play(
        arreglo.celdas[0].animate.set_stroke(COLOR_OK, width=5),
        arreglo.celdas[1].animate.set_stroke(COLOR_OK, width=5),
        *anims_reemplazo(op, libres), FadeOut(formula), run_time=0.6,
    )
    op = libres
    escena.wait(1.2)

    rear = (rear + 1) % TAMANO
    caja, anim = arreglo.poner(rear, 5)
    nuevo_op = linea_op("enqueue(5)")
    formula = linea_formula("rear = (3 + 1) % 5 = 4")
    escena.play(*anims_reemplazo(op, nuevo_op), FadeIn(formula), run_time=0.4)
    op = nuevo_op
    escena.play(anim, puntero_rear.animate.next_to(lugar_rear(rear), DOWN, buff=0), run_time=0.6)
    escena.wait(0.6)

    anterior = rear
    rear = (rear + 1) % TAMANO
    nuevo_op = linea_op("enqueue(6)")
    nueva_formula = linea_formula(f"rear = ({anterior} + 1) % 5 = {rear}", COLOR_ACENTO)
    escena.play(*anims_reemplazo(op, nuevo_op), *anims_reemplazo(formula, nueva_formula), run_time=0.4)
    op, formula = nuevo_op, nueva_formula

    vuelta = CurvedArrow(
        puntero_rear.get_bottom() + DOWN * 0.3,
        [arreglo.celdas[rear].get_x(), puntero_rear.get_bottom()[1] - 0.3, 0],
        angle=-PI / 3, color=COLOR_ACENTO, stroke_width=4,
    )
    escena.play(Create(vuelta), puntero_rear.animate.next_to(lugar_rear(rear), DOWN, buff=0), run_time=1)
    caja, anim = arreglo.poner(rear, 6)
    escena.play(anim, arreglo.celdas[0].animate.set_stroke(COLOR_SECUNDARIO, width=3), run_time=0.6)
    escena.wait(1.2)

    #conclusión
    mensaje = VGroup(
        texto("Se reutilizan las posiciones libres sin mover elementos", TAM_NORMAL),
        texto("enqueue y dequeue: O(1)", TAM_NORMAL, COLOR_QUEUE),
    ).arrange(DOWN, buff=0.3).move_to(DOWN * 2.9)
    escena.play(FadeOut(VGroup(op, formula, vuelta)), run_time=0.4)
    escena.play(FadeIn(mensaje, shift=UP * 0.2), run_time=0.6)
    escena.wait(3)
    limpiar(escena)


class ArrayCircular(Scene):
    def construct(self):
        configurar_escena(self)
        seccion_array_circular(self)


# 6. Aplicación del stack: paréntesis balanceados
def seccion_parentesis(escena: Scene) -> None:

    CADENA = "([]{})"
    PAREJA = {")": "(", "]": "[", "}": "{"}  # cada cierre con su apertura
    x_texto = 1.8  # columna derecha donde van la cadena y las explicaciones

    titulo = encabezado("Aplicación: paréntesis balanceados", COLOR_STACK)
    simbolos = VGroup(*[codigo(c, COLOR_TEXTO, 56) for c in CADENA]).arrange(RIGHT, buff=0.5)
    simbolos.move_to([x_texto, 1.6, 0])
    pila = PilaVisual(capacidad=3, posicion=[-4, -0.6, 0], lado=0.9)
    nombre_pila = texto("stack", TAM_PEQUENO, COLOR_STACK).next_to(pila.contenedor, DOWN, buff=0.2)
    escena.play(Write(titulo), FadeIn(simbolos), Create(pila.contenedor), FadeIn(nombre_pila), run_time=1.2)

    regla = texto("abre → push     cierra → pop y comparar", TAM_PEQUENO, COLOR_SECUNDARIO)
    regla.move_to([x_texto, 0.5, 0])
    escena.play(FadeIn(regla), run_time=0.5)
    escena.wait(0.8)

    cursor, accion, comparacion = None, None, None
    abiertos = []
    for i, c in enumerate(CADENA):
        if cursor is None:
            cursor = SurroundingRectangle(simbolos[i], color=COLOR_ACENTO, buff=0.15)
            mover_cursor = Create(cursor)
        else:
            mover_cursor = cursor.animate.move_to(simbolos[i])
        quitar = [FadeOut(comparacion)] if comparacion is not None else []
        comparacion = None

        if c in "([{":
            nueva = codigo(f"push('{c}')", COLOR_STACK, TAM_NORMAL + 4).move_to([x_texto, -0.8, 0])
            escena.play(mover_cursor, *anims_reemplazo(accion, nueva), *quitar, run_time=0.5)
            accion = nueva
            _, anim = pila.push(c)
            abiertos.append(i)
            escena.play(anim, run_time=0.6)
            escena.wait(0.3)
        else:
            nueva = codigo("pop()", COLOR_STACK, TAM_NORMAL + 4).move_to([x_texto, -0.8, 0])
            escena.play(mover_cursor, *anims_reemplazo(accion, nueva), *quitar, run_time=0.5)
            accion = nueva
            caja = pila.pop()
            j = abiertos.pop()
            comparacion = texto(f"{PAREJA[c]}  con  {c}  coinciden ✓", TAM_NORMAL, COLOR_OK)
            comparacion.next_to(accion, DOWN, buff=0.4)
            escena.play(
                caja[0].animate.set_color(COLOR_OK),
                simbolos[i].animate.set_color(COLOR_OK),
                simbolos[j].animate.set_color(COLOR_OK),
                FadeIn(comparacion, shift=UP * 0.2),
                run_time=0.5,
            )
            escena.play(FadeOut(caja, shift=UP * 0.8), run_time=0.5)
            escena.wait(0.4)

    #Resultado;; el stack terminó vacío, la cadena es válida
    resultado = VGroup(
        texto("Stack vacío al final", TAM_NORMAL),
        texto("la cadena es válida ✓", TAM_NORMAL + 4, COLOR_OK, weight=BOLD),
    ).arrange(DOWN, buff=0.25).move_to([x_texto, -1.3, 0])
    escena.play(FadeOut(VGroup(cursor, accion, comparacion)), run_time=0.4)
    escena.play(
        FadeIn(resultado, shift=UP * 0.2),
        pila.contenedor.animate.set_color(COLOR_OK),
        run_time=0.8,
    )
    escena.wait(2.2)
    limpiar(escena)


class Parentesis(Scene):
    def construct(self):
        configurar_escena(self)
        seccion_parentesis(self)

# 7. Créditos
def seccion_creditos(escena: Scene) -> None:
    """Autores, curso y herramienta usada (~5 s)."""
    import manim  # solo para leer la versión instalada

    titulo = texto("Créditos", TAM_TITULO, COLOR_ACENTO, weight=BOLD)
    autores = VGroup(*[texto(nombre, TAM_SUBTITULO) for nombre in AUTORES]).arrange(DOWN, buff=0.2)
    curso = texto(CURSO, TAM_NORMAL, COLOR_SECUNDARIO)
    herramienta = texto(
        f"Hecho con Manim Community v{manim.__version__}", TAM_PEQUENO,
        t2c={"Manim Community": COLOR_STACK},
    )
    grupo = VGroup(titulo, autores, curso, herramienta).arrange(DOWN, buff=0.5)

    escena.play(Write(titulo), run_time=0.8)
    escena.play(FadeIn(autores, shift=UP * 0.2), run_time=0.8)
    escena.play(FadeIn(curso, shift=UP * 0.2), FadeIn(herramienta, shift=UP * 0.2), run_time=0.6)
    escena.wait(2.2)
    escena.play(FadeOut(grupo), run_time=0.8)


class Creditos(Scene):
    def construct(self):
        configurar_escena(self)
        seccion_creditos(self)



# Video completo
SECCIONES = [
    seccion_titulo,
    seccion_stack,
    seccion_queue,
    seccion_comparacion,
    seccion_array_circular,
    seccion_parentesis,
    seccion_creditos,
]


class VideoCompleto(Scene):
    def construct(self):
        configurar_escena(self)
        for seccion in SECCIONES:
            seccion(self)
            self.wait(0.3)  #pequeña pausa entre secciones
