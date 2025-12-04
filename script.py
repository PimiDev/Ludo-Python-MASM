import tkinter as tk
from tkinter import PhotoImage
from ctypes import WinDLL, c_int


dll = WinDLL("./LudoLibreria.dll")
tirarDado = dll.tirarDado; tirarDado.restype = c_int
getTurno = dll.getTurno; getTurno.restype = c_int
avanzarTurno = dll.avanzarTurno; avanzarTurno.restype = c_int
puedeSacarFicha = dll.puedeSacarFicha; puedeSacarFicha.argtypes = [c_int]; puedeSacarFicha.restype = c_int
nueva_pos = dll.moverFicha; nueva_pos.argtypes = [c_int, c_int]; nueva_pos.restype = c_int


TABLERO_SIZE = 416
FILAS, COLS = 15, 15
CELDA = TABLERO_SIZE / FILAS
MATRIZ = [[(c*CELDA, f*CELDA) for c in range(COLS)] for f in range(FILAS)]


SALIDAS = {
    0: (6,1),   # Rojo
    1: (1,8),   # Verde
    2: (13,6),  # Azul
    3: (8,13)   # Amarillo
}


def generar_borde():
    borde = []
    # Arriba
    for c in range(1,14):
        borde.append((0,c))
    # Derecha
    for f in range(1,14):
        borde.append((f,14))
    # Abajo
    for c in range(13,0,-1):
        borde.append((14,c))
    # Izquierda
    for f in range(13,0,-1):
        borde.append((f,0))
    return borde
BORDE = generar_borde()

#
def construir_camino(salida):
    fila_salida, col_salida = salida
    # Encuentra el índice más cercano en borde
    index = min(range(len(BORDE)), key=lambda i: abs(BORDE[i][0]-fila_salida)+abs(BORDE[i][1]-col_salida))
    camino = BORDE[index:] + BORDE[:index]
    camino = camino[:52]

    # Zona de meta según esquina
    if salida == (6,1):        # Rojo, arriba izquierda
        meta = [(7,1),(7,2),(7,3),(7,4),(7,5)]
    elif salida == (1,8):      # Verde, arriba derecha
        meta = [(1,7),(2,7),(3,7),(4,7),(5,7)]
    elif salida == (13,6):     # Azul, abajo izquierda
        meta = [(13,7),(12,7),(11,7),(10,7),(9,7)]
    elif salida == (8,13):     # Amarillo, abajo derecha
        meta = [(7,13),(7,12),(7,11),(7,10),(7,9)]
    camino.extend(meta)
    return camino

CAMINOS = {j: construir_camino(SALIDAS[j]) for j in range(4)}


estado_jugadores = {0: {"fuera":0},1: {"fuera":0},2: {"fuera":0},3: {"fuera":0}}
ultimo_dado = 0


root = tk.Tk()
root.title("Ludo 15x15 + MASM")

main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(padx=10,pady=10)

canvas = tk.Canvas(main_frame, width=TABLERO_SIZE, height=TABLERO_SIZE, highlightthickness=0)
canvas.grid(row=0,column=0)

tablero_img = PhotoImage(file="./tablero.png")
canvas.create_image(TABLERO_SIZE//2, TABLERO_SIZE//2, image=tablero_img)


CASAS = {
    0:[(0,0),(0,1),(1,0),(1,1)],       # Rojo
    1:[(0,13),(0,14),(1,13),(1,14)],   # Verde
    2:[(13,0),(13,1),(14,0),(14,1)],   # Azul
    3:[(13,13),(13,14),(14,13),(14,14)]# Amarillo
}

fichas = {}
posiciones = {}
colores = ["red","green","blue","yellow"]

for j in range(4):
    for f in range(4):
        fila,col = CASAS[j][f]
        x,y = MATRIZ[fila][col]
        ficha = canvas.create_oval(x,y,x+CELDA,y+CELDA,fill=colores[j])
        fichas[(j,f)] = ficha
        posiciones[(j,f)] = -1


def mover_ficha(jugador):
    global ultimo_dado
    camino = CAMINOS[jugador]
    for f in range(4):
        if posiciones[(jugador,f)] != -1:
            pos_actual = posiciones[(jugador,f)]
            nueva = nueva_pos(pos_actual, ultimo_dado)
            posiciones[(jugador,f)] = nueva
            fila, col = camino[nueva]
            x, y = MATRIZ[fila][col]
            canvas.coords(fichas[(jugador,f)], x, y, x+CELDA, y+CELDA)
            fichas_label.config(text=f"Ficha {f+1} movida a casilla {nueva}")
            break
    else:
        fichas_label.config(text="No hay fichas para mover")
    if ultimo_dado != 6:
        avanzar_turno_btn()

def sacar_ficha(jugador):
    global ultimo_dado
    camino = CAMINOS[jugador]
    for f in range(4):
        if posiciones[(jugador,f)] == -1:
            posiciones[(jugador,f)] = 0
            fila, col = camino[0]
            x, y = MATRIZ[fila][col]
            canvas.coords(fichas[(jugador,f)], x, y, x+CELDA, y+CELDA)
            estado_jugadores[jugador]["fuera"] += 1
            fichas_label.config(text=f"Jugador {jugador+1} sacó ficha {f+1}")
            if ultimo_dado != 6:
                avanzar_turno_btn()
            return
    fichas_label.config(text="No hay fichas para sacar")
    avanzar_turno_btn()

def lanzar_dado():
    global ultimo_dado
    jugador = getTurno()
    valor = tirarDado()
    ultimo_dado = valor
    resultado_label.config(text=f"Dado: {valor}")

    if valor == 6 and estado_jugadores[jugador]["fuera"]==0:
        sacar_ficha(jugador)
    elif puedeSacarFicha(valor) and estado_jugadores[jugador]["fuera"]==0:
        sacar_ficha(jugador)
    else:
        mover_ficha(jugador)

def mostrar_turno():
    turno = getTurno()
    turno_label.config(text=f"Turno actual: Jugador {turno+1}")

def avanzar_turno_btn():
    avanzarTurno()
    mostrar_turno()


panel = tk.Frame(main_frame,bg="#e6e6e6")
panel.grid(row=0,column=1,sticky="n",padx=20)

tk.Button(panel,text="Tirar Dado",command=lanzar_dado).pack(pady=5)
resultado_label = tk.Label(panel,text="Dado: ")
resultado_label.pack()

tk.Button(panel,text="Mostrar Turno",command=mostrar_turno).pack(pady=5)
turno_label = tk.Label(panel,text="Turno actual: ")
turno_label.pack()

tk.Button(panel,text="Avanzar Turno",command=avanzar_turno_btn).pack(pady=5)
fichas_label = tk.Label(panel,text="")
fichas_label.pack(pady=5)

root.resizable(False,False)
root.mainloop()
