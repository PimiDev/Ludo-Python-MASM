import tkinter as tk
from tkinter import Canvas, PhotoImage
from ctypes import WinDLL, c_int


dll = WinDLL("./LudoLibreria.dll")

tirarDado = dll.tirarDado
tirarDado.restype = c_int

getTurno = dll.getTurno
getTurno.restype = c_int

avanzarTurno = dll.avanzarTurno
avanzarTurno.restype = c_int

puedeSacarFicha = dll.puedeSacarFicha
puedeSacarFicha.argtypes = [c_int]
puedeSacarFicha.restype = c_int

nueva_pos = dll.moverFicha
nueva_pos.argtypes = [c_int, c_int]
nueva_pos.restype = c_int


# Camino de 52 casillas (prueba)
CAMINO = [
    (250, 10), (250, 40), (250, 70), (250, 100), (250, 130), (250, 160),
    (250, 190), (250, 220), (250, 250), (250, 280), (250, 310), (250, 340),
    (250, 370), (250, 400), (250, 430), (250, 460),  # derecha

    (220, 460), (190, 460), (160, 460), (130, 460), (100, 460), (70, 460),
    (40, 460), (10, 460),   # abajo

    (10, 430), (10, 400), (10, 370), (10, 340), (10, 310), (10, 280),
    (10, 250), (10, 220), (10, 190), (10, 160), (10, 130), (10, 100),
    (10, 70), (10, 40), (10, 10),  # izquierda

    (40, 10), (70, 10), (100, 10), (130, 10), (160, 10),
    (190, 10), (220, 10)  # arriba
]

estado_jugadores = {
    0: {"fuera": 0},
    1: {"fuera": 0},
    2: {"fuera": 0},
    3: {"fuera": 0},
}

ultimo_dado = 0

# Interfaz TK

root = tk.Tk()
root.title("Ludo con MASM + Python")

main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(padx=10, pady=10)

# Canvas para tablero
canvas = tk.Canvas(main_frame, width=800, height=500, highlightthickness=0)
canvas.grid(row=0, column=0)  # A la izquierda

# Cargar imagen del tablero
tablero_img = PhotoImage(file="./tablero.png")
canvas.create_image(250, 250, image=tablero_img)




# Casas iniciales por jugador
CASAS = {
    0: [(80, 80),  (140, 80),  (80, 140),  (140, 140)],   # Rojo
    1: [(390, 80), (330, 80), (390, 140), (330, 140)],    # verde
    2: [(80, 330), (140, 390), (80, 390), (140, 330)],    # azul
    3: [(390, 330), (330, 390), (390, 390), (330, 330)],     # Amarillo
}



# prueba de fichas, posiblemente la cambie despues
fichas = {}
posiciones = {}

colores = ["red", "green", "blue", "yellow"]

for jugador in range(4):
    for f in range(4):
        x, y = CASAS[jugador][f]
        ficha = canvas.create_oval(
            x, y, x+30, y+30,
            fill=colores[jugador]
        )
        fichas[(jugador, f)] = ficha
        posiciones[(jugador, f)] = -1  # En casa




# Funciones del juego

def preguntar_accion(jugador):
    ventana = tk.Toplevel(root)
    ventana.title("Elige acción")

    tk.Label(ventana, text="¿Qué deseas hacer?").pack(pady=10)

    tk.Button(
        ventana,
        text="Sacar ficha",
        command=lambda: (sacar_ficha(jugador), ventana.destroy())
    ).pack(pady=5)

    tk.Button(
        ventana,
        text="Mover ficha",
        command=lambda: (mover_ficha(jugador), ventana.destroy())
    ).pack(pady=5)

def lanzar_dado():
    global ultimo_dado

    jugador = getTurno()
    valor = tirarDado()
    ultimo_dado = valor

    resultado_label.config(text=f"Dado: {valor}")

    # 1. ¿Puede sacar ficha?
    if puedeSacarFicha(valor):
        # Si no tiene fichas fuera, debe sacarla
        if estado_jugadores[jugador]["fuera"] == 0:
            fichas_label.config(text="Primer movimiento: ficha obligatoria")
            sacar_ficha(jugador)
        else:
            # Preguntar al usuario qué quiere hacer
            preguntar_accion(jugador)
    else:
        mover_ficha(jugador)

def mostrar_turno():
    turno = getTurno()
    turno_label.config(text=f"Turno actual: Jugador {turno + 1}")

def avanzar_turno_btn():
    avanzarTurno()
    mostrar_turno()


def mover_ficha(jugador):
    # Elegir ficha a mover (solo fuera de casa)
    for f in range(4):
        if posiciones[(jugador, f)] != -1:
            ficha = f
            break
    else:
        fichas_label.config(text="No tienes fichas fuera")
        return

    pos_actual = posiciones[(jugador, ficha)]
    nueva = nueva_pos(pos_actual, ultimo_dado)

    posiciones[(jugador, ficha)] = nueva
    x, y = CAMINO[nueva]
    canvas.coords(fichas[(jugador, ficha)], x, y, x + 30, y + 30)

    fichas_label.config(text=f"Ficha {ficha + 1} movida a casilla {nueva}")

def sacar_ficha(jugador):
    # Buscar una ficha que esté en casa (-1)
    for f in range(4):
        if posiciones[(jugador, f)] == -1:
            posiciones[(jugador, f)] = 0

            x, y = CAMINO[0]
            canvas.coords(fichas[(jugador, f)], x, y, x + 30, y + 30)

            estado_jugadores[jugador]["fuera"] += 1
            fichas_label.config(text=f"Jugador {jugador + 1} sacó la ficha {f + 1}")
            return True

    fichas_label.config(text="No tiene fichas para sacar")
    return False


#botones panel
panel = tk.Frame(main_frame, bg="#e6e6e6")
panel.grid(row=0, column=1, sticky="n", padx=20)


tk.Button(panel, text="Tirar Dado", command=lanzar_dado).pack(pady=5)
resultado_label = tk.Label(panel, text="Dado: ")
resultado_label.pack()

tk.Button(panel, text="Mostrar Turno", command=mostrar_turno).pack(pady=5)
turno_label = tk.Label(panel, text="Turno actual: ")
turno_label.pack()

tk.Button(panel, text="Avanzar Turno", command=avanzar_turno_btn).pack(pady=5)




fichas_label = tk.Label(panel, text="")
fichas_label.pack(pady=5)



root.resizable(False, False)  # evita que el usuario le cambie el tamaño

root.mainloop()
