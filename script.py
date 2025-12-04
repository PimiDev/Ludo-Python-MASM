import tkinter as tk
from tkinter import Canvas, PhotoImage
from ctypes import WinDLL, c_int, c_uint


dll = WinDLL("./LudoLibreria.dll")

tirarDado = dll.tirarDado
tirarDado.restype = c_int

getTurno = dll.getTurno
getTurno.restype = c_int

avanzarTurno = dll.avanzarTurno
avanzarTurno.restype = c_int

nueva_pos = dll.moverFicha
nueva_pos.argtypes = [c_int, c_int, c_int]  # posActual, pasos, jugador
nueva_pos.restype = c_int

# ----------------------------
# Globals / estado
# ----------------------------
accion_desde_pregunta = False
NOMBRES_JUGADORES = ["Rojo", "Verde", "Amarillo", "Azul"]

# Camino: incluye 0..51 (anillo) y luego zonas seguras por jugador (52+)
CAMINO = [
    #0-12 (1-13)
   (70, 210), (100, 210), (130, 210), (150, 210), (180, 210),
    (210, 180),(210, 150), (210, 120), (210, 100), (210, 70), (210, 40),
    (240, 40), (260, 40),

    #13-25 (14-26)
    (260, 70), (260, 100), (260, 120), (260, 150), (260, 180),
    (290, 210), (320, 210), (340, 210), (360, 210), (380, 210), (410, 210),
    (410, 210), (410, 260),

    #26-38 (27-39)
    (400, 260), (360, 260), (340, 260), (320, 260), (300, 260),
    (260, 270), (260, 290), (260, 310), (260, 340), (260, 360), (260, 380),
    (240, 380), (210, 380),

    #39-51 (40- 52)
   (210, 400), (210, 340), (210, 320), (210, 300), (210, 280),
   (260, 260), (220, 260), (200,260), (180,260), (150,260), (100,260),
    (70,230),(100,230),

    #zona segura roja 52-57 (53-58)
    (70,230),(100,230),(130,230),(150,230),(180,230),(210,230),

    #zona segura verde 58-63 (59-64)
    (240,70),(240,100),(240,120),(240,150),(240,180),(240,210),

    #zona segura amarillo 64-69 (65-70)
    (360,230),(340,230),(320,230),(290,230),(260,230),(210,230),

    #zona segura azul 70-75 (71-76)
    (240,360),(240,340),(240,320),(240,300),(240,280),(240,260),
]

estado_jugadores = {
    0: {"fuera": 0},
    1: {"fuera": 0},
    2: {"fuera": 0},
    3: {"fuera": 0}
}

ultimo_dado = 0

# Interfaz TK





root = tk.Tk()
root.title("Ludo con MASM + Python")

main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(padx=10, pady=10)

canvas = tk.Canvas(main_frame, width=800, height=500, highlightthickness=0)
canvas.grid(row=0, column=0)

# intenta cargar tablero; si falla, continúa (útil para pruebas)
try:
    tablero_img = PhotoImage(file="./tablero.png")
    canvas.create_image(250, 250, image=tablero_img)
except Exception:
    pass

# Casas iniciales por jugador
CASAS = {
    0: [(80, 80),  (140, 80),  (80, 140),  (140, 140)],   # Rojo
    1: [(390, 80), (330, 80), (390, 140), (330, 140)],    # verde
    2: [(390, 330), (330, 390), (390, 390), (330, 330)],  #amarillo
    3: [(80, 330), (140, 390), (80, 390), (140, 330)], # azul
}

fichas = {}
posiciones = {}
colores = ["red", "green", "yellow", "blue"]

for jugador in range(4):
    for f in range(4):
        x, y = CASAS[jugador][f]
        ficha = canvas.create_oval(x, y, x+30, y+30, fill=colores[jugador])
        fichas[(jugador, f)] = ficha
        posiciones[(jugador, f)] = -1  # En casa

# Panel derecho
panel = tk.Frame(main_frame, bg="#e6e6e6")
panel.grid(row=0, column=1, sticky="n", padx=20)

tk.Button(panel, text="Tirar Dado", command=lambda: lanzar_dado()).pack(pady=5)
resultado_label = tk.Label(panel, text="Dado: ")
resultado_label.pack()
turno_label = tk.Label(panel, text="Turno actual: ")
turno_label.pack()
fichas_label = tk.Label(panel, text="")
fichas_label.pack(pady=5)


# FUNCIONES
def mostrar_turno():
    turno = getTurno()
    # mostramos nombres en lugar de 0..3
    nombre = NOMBRES_JUGADORES[turno]
    turno_label.config(text=f"Turno actual: {nombre}")


def preguntar_accion(jugador):
    global accion_desde_pregunta
    accion_desde_pregunta = True

    ventana = tk.Toplevel(root)
    ventana.title("Elige acción")
    tk.Label(ventana, text=f"Turno: {NOMBRES_JUGADORES[jugador]}").pack(pady=6)
    tk.Label(ventana, text="¿Qué deseas hacer?").pack(pady=10)

    if estado_jugadores[jugador]["fuera"] < 4:
        tk.Button(
            ventana,
            text="Sacar ficha",
            command=lambda: (sacar_ficha(jugador), ventana.destroy())
        ).pack(pady=5)

    if estado_jugadores[jugador]["fuera"] > 0:
        tk.Button(
            ventana,
            text="Mover ficha",
            command=lambda: (mover_ficha(jugador), ventana.destroy())
        ).pack(pady=5)


def lanzar_dado():
    global ultimo_dado
    jugador = getTurno()
    mostrar_turno()

    valor = tirarDado()
    ultimo_dado = valor
    resultado_label.config(text=f"Dado: {valor}")

    # ======= CASO 6 =======
    if valor == 6:
        # Si no tiene fichas fuera -> sacar obligatoria
        if estado_jugadores[jugador]["fuera"] == 0:
            fichas_label.config(text="Sacaste 6, primera ficha obligatoria")
            sacar_ficha(jugador)
            return

        # Si tiene fichas fuera -> preguntar (sacar o mover)
        fichas_label.config(text="¡Sacaste 6!")
        preguntar_accion(jugador)
        return

    # ======= CASO NO 6 =======
    # Si no tiene fichas fuera -> turno perdido
    if estado_jugadores[jugador]["fuera"] == 0:
        fichas_label.config(text="No tienes fichas fuera. Turno perdido.")
        terminar_accion()
        return

    # Si hay fichas fuera -> mover (auto o interactivo; ahora mueve primera disponible)
    mover_ficha(jugador)


def avanzar_turno_btn():
    avanzarTurno()
    mostrar_turno()


def mover_ficha(jugador):
    global accion_desde_pregunta

    # Verificar que haya fichas fuera
    if estado_jugadores[jugador]["fuera"] == 0:
        fichas_label.config(text="No tienes fichas fuera.")
        terminar_accion()
        return

    # Buscar fichas fuera
    fichas_fuera = []
    for f in range(4):
        pos = posiciones[(jugador, f)]
        if pos != -1 and pos < 1000:
            fichas_fuera.append(f)

    if not fichas_fuera:
        fichas_label.config(text="Todas tus fichas están en casa o meta.")
        terminar_accion()
        return

    # Si solo hay una ficha → moverla directamente
    if len(fichas_fuera) == 1:
        mover_ficha_seleccionada(jugador, fichas_fuera[0])
        return

    # Si hay varias → abrir selector
    seleccionar_ficha(jugador, fichas_fuera, lambda f: mover_ficha_seleccionada(jugador, f))



def sacar_ficha(jugador):
    global accion_desde_pregunta

    for f in range(4):
        if posiciones[(jugador, f)] == -1:
            # posiciones de salida por jugador
            pos_inicial = [0, 13, 26, 39][jugador]

            posiciones[(jugador, f)] = pos_inicial
            # si CAMINO no tiene esa casilla, proteger
            if 0 <= pos_inicial < len(CAMINO):
                x, y = CAMINO[pos_inicial]
                canvas.coords(fichas[(jugador, f)], x, y, x + 30, y + 30)
            else:
                canvas.coords(fichas[(jugador, f)], -100, -100, -100, -100)

            estado_jugadores[jugador]["fuera"] += 1
            fichas_label.config(text=f"{NOMBRES_JUGADORES[jugador]} sacó ficha {f + 1}")

            # si venía de pregunta: solo limpiar flag y no avanzar turno
            if accion_desde_pregunta:
                accion_desde_pregunta = False
                return True

            terminar_accion()
            return True

    fichas_label.config(text="No tienes fichas en casa.")
    return False


def terminar_accion():
    global ultimo_dado
    # Turno extra por 6: limpiamos dado y mantenemos turno actual
    if ultimo_dado == 6:
        ultimo_dado = 0
        mostrar_turno()
        return

    # Cambiar turno normal
    ultimo_dado = 0
    avanzarTurno()
    mostrar_turno()

def seleccionar_ficha(jugador, fichas_fuera, callback):
    ventana = tk.Toplevel(root)
    ventana.title("Elige qué ficha mover")

    tk.Label(ventana, text=f"Jugador {jugador + 1}: elige una ficha").pack(pady=8)

    for f in fichas_fuera:
        tk.Button(
            ventana,
            text=f"Ficha {f + 1}",
            width=15,
            bg=colores[jugador],
            fg="white",
            command=lambda ficha=f: (callback(ficha), ventana.destroy())
        ).pack(pady=5)

def mover_ficha_seleccionada(jugador, ficha):
    global accion_desde_pregunta

    pos = posiciones[(jugador, ficha)]

    try:
        nueva = nueva_pos(pos, ultimo_dado, jugador)
    except Exception as e:
        fichas_label.config(text=f"Error al calcular nueva posición: {e}")
        terminar_accion()
        return

    posiciones[(jugador, ficha)] = nueva

    # Meta o fuera de CAMINO
    if nueva >= len(CAMINO) or nueva < 0:
        fichas_label.config(text=f"¡Ficha {ficha + 1} llegó a la meta ({nueva})!")
        canvas.coords(fichas[(jugador, ficha)], -100, -100, -100, -100)
        estado_jugadores[jugador]["fuera"] -= 1
    else:
        x, y = CAMINO[nueva]
        canvas.coords(fichas[(jugador, ficha)], x, y, x + 30, y + 30)
        fichas_label.config(text=f"Ficha {ficha + 1} movida a pos {nueva}")

    # Si viene de pregunta → NO avanzar turno
    if accion_desde_pregunta:
        accion_desde_pregunta = False
        return

    terminar_accion()





root.resizable(False, False)
mostrar_turno()
root.mainloop()