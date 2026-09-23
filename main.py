
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
    escena.wait(2.5)
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

    def sacar_top():
        # La caja del top se pone roja y sube; devuelve la caja y cómo se mueve la flecha top
        caja = pila.pop()
        escena.play(caja[0].animate.set_color(COLOR_ERROR), run_time=0.5)
        escena.play(caja.animate.move_to([caja.get_x(), pila.contenedor.get_top()[1] + 0.8, 0]), run_time=0.7)
        if pila.top() is not None:
            mover_top = puntero_top.animate.next_to(pila.top(), RIGHT, buff=0.35)
        else:
            mover_top = FadeOut(puntero_top)
        return caja, mover_top

    def cambiar_textos(nuevo_op, nueva_desc, nuevo_sale, *extra, tiempo=0.6):
        # Cambia a la vez la operación, la descripción y el resultado del panel derecho
        nonlocal op, descripcion, sale
        nuevo_op.move_to(op)
        nueva_desc.move_to(descripcion)
        nuevo_sale.move_to(sale)
        escena.play(
            *anims_reemplazo(op, nuevo_op), *anims_reemplazo(descripcion, nueva_desc),
            *anims_reemplazo(sale, nuevo_sale), *extra, run_time=tiempo,
        )
        op, descripcion, sale = nuevo_op, nueva_desc, nuevo_sale

    op = reemplazar(escena, op, codigo("pop()", COLOR_STACK).move_to(op))
    descripcion = reemplazar(
        escena, descripcion,
        texto("saca el elemento del top", TAM_PEQUENO, COLOR_SECUNDARIO).move_to(descripcion),
    )
    caja, mover_top = sacar_top()
    sale = texto("sale el 3: el último que entró", TAM_NORMAL, t2c={"3": COLOR_ERROR})
    sale.next_to(descripcion, DOWN, buff=0.5)
    escena.play(FadeOut(caja, shift=RIGHT), mover_top, FadeIn(sale, shift=UP * 0.2), run_time=0.8)
    escena.wait(1.5)

    # top(): mira el elemento de arriba sin sacarlo
    cambiar_textos(
        codigo("top()", COLOR_STACK),
        texto("consulta el top sin sacarlo", TAM_PEQUENO, COLOR_SECUNDARIO),
        texto("devuelve 2 y el 2 se queda", TAM_NORMAL, t2c={"2": COLOR_ACENTO}),
        Indicate(pila.top(), color=COLOR_ACENTO), tiempo=1,
    )
    escena.wait(1.5)

    # pop() hasta vaciar la pila
    for valor in (2, 1):
        cambiar_textos(
            codigo("pop()", COLOR_STACK),
            texto("saca el elemento del top", TAM_PEQUENO, COLOR_SECUNDARIO),
            texto(f"sale el {valor}", TAM_NORMAL, t2c={str(valor): COLOR_ERROR}),
            tiempo=0.4,
        )
        caja, mover_top = sacar_top()
        escena.play(FadeOut(caja, shift=RIGHT), mover_top, run_time=0.8)
        escena.wait(0.6)

    # isEmpty() y pop() sobre una pila vacía
    cambiar_textos(
        codigo("isEmpty()", COLOR_STACK),
        texto("¿la pila está vacía?", TAM_PEQUENO, COLOR_SECUNDARIO),
        texto("true: ya no quedan elementos", TAM_NORMAL, t2c={"true": COLOR_OK}),
    )
    escena.wait(1.5)
    cambiar_textos(
        codigo("pop()", COLOR_ERROR),
        texto("sacar de una pila vacía...", TAM_PEQUENO, COLOR_SECUNDARIO),
        texto("error: stack underflow", TAM_NORMAL, COLOR_ERROR),
        Wiggle(pila.contenedor), tiempo=1,
    )
    escena.wait(1.8)

    lifo = crear_insignia("LIFO", "Last In, First Out", COLOR_STACK).next_to(sale, DOWN, buff=0.4)
    escena.play(FadeIn(lifo, shift=UP * 0.2), run_time=1)
    costo = texto("push, pop, top e isEmpty: O(1)", TAM_PEQUENO).next_to(lifo, DOWN, buff=0.4)
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

    def sacar_front():
        # La caja del front se pone roja y sale por la izquierda
        caja = cola.dequeue()
        escena.play(caja[0].animate.set_color(COLOR_ERROR), run_time=0.5)
        escena.play(FadeOut(caja, shift=LEFT * 1.8), run_time=0.7)

    op = reemplazar(escena, op, codigo("dequeue()", COLOR_QUEUE).move_to(op))
    descripcion = reemplazar(
        escena, descripcion,
        texto("saca el elemento del front", TAM_PEQUENO, COLOR_SECUNDARIO).move_to(descripcion),
    )
    sacar_front()
    sale = texto("sale el 1: el primero que entró", TAM_NORMAL, t2c={"1": COLOR_ERROR})
    sale.next_to(descripcion, DOWN, buff=0.5)
    escena.play(
        *cola.reacomodar(),
        puntero_rear.animate.shift(LEFT * cola.lado),
        FadeIn(sale, shift=UP * 0.2),
        run_time=0.8,
    )
    escena.wait(1.5)

    # front(): mira el primero de la fila sin sacarlo
    nuevo_op = codigo("front()", COLOR_QUEUE).move_to(op)
    nueva_desc = texto("consulta el front sin sacarlo", TAM_PEQUENO, COLOR_SECUNDARIO).move_to(descripcion)
    nuevo_sale = texto("devuelve 2 y el 2 se queda", TAM_NORMAL, t2c={"2": COLOR_ACENTO}).move_to(sale)
    escena.play(
        *anims_reemplazo(op, nuevo_op), *anims_reemplazo(descripcion, nueva_desc),
        *anims_reemplazo(sale, nuevo_sale), Indicate(cola.front(), color=COLOR_ACENTO), run_time=1,
    )
    op, descripcion, sale = nuevo_op, nueva_desc, nuevo_sale
    escena.wait(1.5)

    # enqueue(4): entra por el rear
    nuevo_op = codigo("enqueue(4)", COLOR_QUEUE).move_to(op)
    nueva_desc = texto("agrega el elemento en el rear", TAM_PEQUENO, COLOR_SECUNDARIO).move_to(descripcion)
    escena.play(*anims_reemplazo(op, nuevo_op), *anims_reemplazo(descripcion, nueva_desc), FadeOut(sale), run_time=0.5)
    op, descripcion = nuevo_op, nueva_desc
    caja, animacion = cola.enqueue(4)
    escena.play(animacion, run_time=0.8)
    escena.play(puntero_rear.animate.next_to(caja, DOWN, buff=0.3), run_time=0.5)
    escena.wait(1)

    # dequeue() otra vez: ahora sale el 2
    nuevo_op = codigo("dequeue()", COLOR_QUEUE).move_to(op)
    nueva_desc = texto("saca el elemento del front", TAM_PEQUENO, COLOR_SECUNDARIO).move_to(descripcion)
    escena.play(*anims_reemplazo(op, nuevo_op), *anims_reemplazo(descripcion, nueva_desc), run_time=0.5)
    op, descripcion = nuevo_op, nueva_desc
    sacar_front()
    sale = texto("sale el 2: el primero de la fila", TAM_NORMAL, t2c={"2": COLOR_ERROR})
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

    # Sacar los tres elementos: se va armando el orden de salida de cada una
    sale_pila, sale_cola = None, None
    orden_pila, orden_cola = [], []
    for _ in range(3):
        caja_pila, caja_cola = pila.pop(), cola.dequeue()
        orden_pila.append(caja_pila[1].text)
        orden_cola.append(caja_cola[1].text)
        escena.play(caja_pila[0].animate.set_color(COLOR_ERROR), caja_cola[0].animate.set_color(COLOR_ERROR), run_time=0.4)
        escena.play(FadeOut(caja_pila, shift=UP * 0.9), FadeOut(caja_cola, shift=LEFT * 1.5), run_time=0.7)

        nuevo_pila = texto("salen: " + ", ".join(orden_pila), TAM_NORMAL).next_to(op_pila, DOWN, buff=0.3)
        nuevo_cola = texto("salen: " + ", ".join(orden_cola), TAM_NORMAL).next_to(op_cola, DOWN, buff=0.3)
        escena.play(
            *cola.reacomodar(),
            *anims_reemplazo(sale_pila, nuevo_pila), *anims_reemplazo(sale_cola, nuevo_cola),
            run_time=0.6,
        )
        sale_pila, sale_cola = nuevo_pila, nuevo_cola
        escena.wait(0.8)

    # El stack invierte el orden; la queue lo conserva
    escena.play(
        sale_pila.animate.set_color(COLOR_STACK).scale(1.15),
        sale_cola.animate.set_color(COLOR_QUEUE).scale(1.15),
        run_time=1,
    )
    escena.wait(1.3)

#LIFO vs FIFO
    lifo = crear_insignia("LIFO", "Last In, First Out", COLOR_STACK).next_to(sale_pila, DOWN, buff=0.35)
    fifo = crear_insignia("FIFO", "First In, First Out", COLOR_QUEUE).next_to(sale_cola, DOWN, buff=0.35)
    escena.play(FadeIn(lifo, shift=UP * 0.2), FadeIn(fifo, shift=UP * 0.2), run_time=1)
    escena.wait(4)
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

    # Contador de elementos: permite saber si la cola está vacía o llena
    size = 0

    def texto_size(n, color=COLOR_TEXTO):
        return texto(f"size = {n}", TAM_PEQUENO, color).next_to(tamano_fijo, DOWN, aligned_edge=LEFT, buff=0.25)

    contador = texto_size(0)
    escena.play(
        Write(titulo), Create(arreglo.celdas), FadeIn(arreglo.indices),
        FadeIn(tamano_fijo), FadeIn(contador), run_time=1.2,
    )

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
        size += 1
        nuevo_contador = texto_size(size)
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
        escena.play(
            anim, mover_rear, *anims_reemplazo(op, nuevo_op),
            *anims_reemplazo(contador, nuevo_contador), *extra, run_time=0.6,
        )
        op, contador = nuevo_op, nuevo_contador
        escena.wait(0.4)

    formula = reemplazar(escena, formula, linea_formula("front = (front + 1) % 5"), tiempo=0.4)
    for _ in range(2):
        op = reemplazar(escena, op, linea_op("dequeue()"), tiempo=0.3)
        caja = arreglo.quitar(front)
        escena.play(caja[0].animate.set_color(COLOR_ERROR), run_time=0.3)
        front = (front + 1) % TAMANO
        size -= 1
        nuevo_contador = texto_size(size)
        escena.play(
            FadeOut(caja, shift=UP * 0.6),
            puntero_front.animate.next_to(arreglo.celdas[front], UP, buff=0.15),
            *anims_reemplazo(contador, nuevo_contador),
            run_time=0.6,
        )
        contador = nuevo_contador

    libres = texto("las posiciones 0 y 1 quedaron libres", TAM_NORMAL, t2c={"0 y 1": COLOR_OK}).move_to(op)
    escena.play(
        arreglo.celdas[0].animate.set_stroke(COLOR_OK, width=5),
        arreglo.celdas[1].animate.set_stroke(COLOR_OK, width=5),
        *anims_reemplazo(op, libres), FadeOut(formula), run_time=0.6,
    )
    op = libres
    escena.wait(1.2)

    rear = (rear + 1) % TAMANO
    size += 1
    nuevo_contador = texto_size(size)
    caja, anim = arreglo.poner(rear, 5)
    nuevo_op = linea_op("enqueue(5)")
    formula = linea_formula("rear = (3 + 1) % 5 = 4")
    escena.play(*anims_reemplazo(op, nuevo_op), FadeIn(formula), run_time=0.4)
    op = nuevo_op
    escena.play(
        anim, puntero_rear.animate.next_to(lugar_rear(rear), DOWN, buff=0),
        *anims_reemplazo(contador, nuevo_contador), run_time=0.6,
    )
    contador = nuevo_contador
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
    size += 1
    nuevo_contador = texto_size(size)
    caja, anim = arreglo.poner(rear, 6)
    escena.play(
        anim, arreglo.celdas[0].animate.set_stroke(COLOR_SECUNDARIO, width=3),
        *anims_reemplazo(contador, nuevo_contador), run_time=0.6,
    )
    contador = nuevo_contador
    escena.wait(1.2)

    # enqueue(7): ocupa la última posición libre (la 1)
    anterior = rear
    rear = (rear + 1) % TAMANO
    size += 1
    nuevo_contador = texto_size(size)
    nuevo_op = linea_op("enqueue(7)")
    nueva_formula = linea_formula(f"rear = ({anterior} + 1) % 5 = {rear}")
    escena.play(
        FadeOut(vuelta), *anims_reemplazo(op, nuevo_op), *anims_reemplazo(formula, nueva_formula),
        run_time=0.4,
    )
    op, formula = nuevo_op, nueva_formula
    caja, anim = arreglo.poner(rear, 7)
    escena.play(
        anim, puntero_rear.animate.next_to(lugar_rear(rear), DOWN, buff=0),
        arreglo.celdas[1].animate.set_stroke(COLOR_SECUNDARIO, width=3),
        *anims_reemplazo(contador, nuevo_contador), run_time=0.6,
    )
    contador = nuevo_contador
    escena.wait(1)

    # Cola llena: size == capacidad, ya no se puede insertar
    nuevo_op = codigo("enqueue(8) ?", COLOR_ERROR, TAM_NORMAL + 4).move_to(op)
    nueva_formula = linea_formula("size == 5  →  cola llena", COLOR_ERROR)
    nuevo_contador = texto_size(size, COLOR_ERROR)
    escena.play(
        *anims_reemplazo(op, nuevo_op), *anims_reemplazo(formula, nueva_formula),
        *anims_reemplazo(contador, nuevo_contador),
        arreglo.celdas.animate.set_stroke(COLOR_ERROR, width=5), run_time=0.6,
    )
    op, formula, contador = nuevo_op, nueva_formula, nuevo_contador
    escena.play(Wiggle(arreglo.celdas), run_time=1)
    escena.wait(2)

    #conclusión
    mensaje = VGroup(
        texto("Se reutilizan las posiciones libres sin mover elementos", TAM_NORMAL),
        texto("enqueue y dequeue: O(1)", TAM_NORMAL, COLOR_QUEUE),
    ).arrange(DOWN, buff=0.3).move_to(DOWN * 2.9)
    escena.play(
        FadeOut(VGroup(op, formula)),
        arreglo.celdas.animate.set_stroke(COLOR_SECUNDARIO, width=3), run_time=0.4,
    )
    escena.play(FadeIn(mensaje, shift=UP * 0.2), run_time=0.6)
    escena.wait(4)
    limpiar(escena)


class ArrayCircular(Scene):
    def construct(self):
        configurar_escena(self)
        seccion_array_circular(self)


# 6. Aplicación del stack: paréntesis balanceados
def seccion_parentesis(escena: Scene) -> None:

    PAREJA = {")": "(", "]": "[", "}": "{"}  # cada cierre con su apertura
    x_texto = 1.8  # columna derecha donde van la cadena y las explicaciones

    titulo = encabezado("Aplicación: paréntesis balanceados", COLOR_STACK)
    pila = PilaVisual(capacidad=3, posicion=[-4, -0.6, 0], lado=0.9)
    nombre_pila = texto("stack", TAM_PEQUENO, COLOR_STACK).next_to(pila.contenedor, DOWN, buff=0.2)
    escena.play(Write(titulo), Create(pila.contenedor), FadeIn(nombre_pila), run_time=1.2)

    regla = texto("abre → push     cierra → pop y comparar", TAM_PEQUENO, COLOR_SECUNDARIO)
    regla.move_to([x_texto, 0.5, 0])

    def validar(cadena):
        # Recorre la cadena animando el stack.
        # Devuelve (es_valida, simbolos, restos): restos son los textos a borrar después.
        simbolos = VGroup(*[codigo(c, COLOR_TEXTO, 56) for c in cadena]).arrange(RIGHT, buff=0.5)
        simbolos.move_to([x_texto, 1.6, 0])
        escena.play(FadeIn(simbolos, shift=DOWN * 0.2), run_time=0.6)

        cursor, accion, comparacion = None, None, None
        abiertos = []  # índices de los símbolos que siguen abiertos
        for i, c in enumerate(cadena):
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
                continue

            nueva = codigo("pop()", COLOR_STACK, TAM_NORMAL + 4).move_to([x_texto, -0.8, 0])
            escena.play(mover_cursor, *anims_reemplazo(accion, nueva), *quitar, run_time=0.5)
            accion = nueva
            caja = pila.pop()
            j = abiertos.pop()
            coincide = cadena[j] == PAREJA[c]
            color = COLOR_OK if coincide else COLOR_ERROR
            mensaje = "coinciden ✓" if coincide else "no coinciden ✗"
            comparacion = texto(f"{cadena[j]}  con  {c}  {mensaje}", TAM_NORMAL, color)
            comparacion.next_to(accion, DOWN, buff=0.4)
            escena.play(
                caja[0].animate.set_color(color),
                simbolos[i].animate.set_color(color),
                simbolos[j].animate.set_color(color),
                FadeIn(comparacion, shift=UP * 0.2),
                run_time=0.5,
            )
            escena.play(FadeOut(caja, shift=UP * 0.8), run_time=0.5)
            escena.wait(0.4 if coincide else 1.2)
            if not coincide:
                return False, simbolos, VGroup(cursor, accion, comparacion)

        # Si quedó algo abierto en el stack, la cadena tampoco es válida
        return not abiertos, simbolos, VGroup(cursor, accion, comparacion)

    # --- Ejemplo 1: ( [ ] { } ) es válida ---
    escena.play(FadeIn(regla), run_time=0.5)
    escena.wait(0.8)
    _, simbolos, restos = validar("([]{})")

    #Resultado;; el stack terminó vacío, la cadena es válida
    resultado = VGroup(
        texto("Stack vacío al final", TAM_NORMAL),
        texto("la cadena es válida ✓", TAM_NORMAL + 4, COLOR_OK, weight=BOLD),
    ).arrange(DOWN, buff=0.25).move_to([x_texto, -1.3, 0])
    escena.play(FadeOut(restos), run_time=0.4)
    escena.play(
        FadeIn(resultado, shift=UP * 0.2),
        pila.contenedor.animate.set_color(COLOR_OK),
        run_time=0.8,
    )
    escena.wait(2.2)

    # --- Ejemplo 2: ( [ ) ] no es válida ---
    escena.play(
        FadeOut(simbolos), FadeOut(resultado),
        pila.contenedor.animate.set_color(COLOR_SECUNDARIO), run_time=0.6,
    )
    _, simbolos, restos = validar("([)]")

    resultado = VGroup(
        texto("El top no coincide con el cierre", TAM_NORMAL),
        texto("la cadena es inválida ✗", TAM_NORMAL + 4, COLOR_ERROR, weight=BOLD),
    ).arrange(DOWN, buff=0.25).move_to([x_texto, -1.3, 0])
    escena.play(FadeOut(restos), run_time=0.4)
    escena.play(
        FadeIn(resultado, shift=UP * 0.2),
        pila.contenedor.animate.set_color(COLOR_ERROR),
        run_time=0.8,
    )
    escena.wait(3.5)
    limpiar(escena)


class Parentesis(Scene):
    def construct(self):
        configurar_escena(self)
        seccion_parentesis(self)

# Resumen: tabla Stack vs Queue
def seccion_resumen(escena: Scene) -> None:
    titulo = encabezado("Resumen", COLOR_ACENTO)
    filas = [
        ("", "Stack", "Queue"),
        ("Orden", "LIFO", "FIFO"),
        ("Insertar", "push", "enqueue"),
        ("Sacar", "pop", "dequeue"),
        ("Consultar", "top", "front"),
        ("Costo", "O(1)", "O(1)"),
        ("Usos", "deshacer (Ctrl+Z),\nllamadas a funciones", "turnos, impresora,\nrecorrido BFS"),
    ]
    # Cada fila: etiqueta en gris, columna del stack en azul y de la queue en naranja
    celdas = []
    for k, (etiqueta, de_pila, de_cola) in enumerate(filas):
        peso = BOLD if k == 0 else NORMAL
        celdas += [
            texto(etiqueta, TAM_NORMAL, COLOR_SECUNDARIO),
            texto(de_pila, TAM_NORMAL, COLOR_STACK, weight=peso),
            texto(de_cola, TAM_NORMAL, COLOR_QUEUE, weight=peso),
        ]
    tabla = VGroup(*celdas).arrange_in_grid(rows=len(filas), cols=3, buff=(1.2, 0.35), col_alignments="lcc")
    tabla.next_to(titulo, DOWN, buff=0.5)
    filas_mob = [VGroup(*celdas[3 * k:3 * k + 3]) for k in range(len(filas))]
    linea = Line(tabla.get_left(), tabla.get_right(), color=COLOR_SECUNDARIO, stroke_width=2)
    linea.next_to(filas_mob[0], DOWN, buff=0.18).set_x(tabla.get_x())

    escena.play(Write(titulo), run_time=0.8)
    escena.play(FadeIn(filas_mob[0], shift=DOWN * 0.2), Create(linea), run_time=0.7)
    for fila in filas_mob[1:]:
        escena.play(FadeIn(fila, shift=UP * 0.2), run_time=0.6)
        escena.wait(0.8)
    escena.wait(5)
    limpiar(escena)


class Resumen(Scene):
    def construct(self):
        configurar_escena(self)
        seccion_resumen(self)


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
    escena.wait(3.2)
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
    seccion_resumen,
    seccion_creditos,
]


class VideoCompleto(Scene):
    def construct(self):
        configurar_escena(self)
        for seccion in SECCIONES:
            seccion(self)
            self.wait(0.3)  #pequeña pausa entre secciones
