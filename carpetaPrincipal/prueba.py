import tkinter as tk
from ctypes import WinDLL, c_int


class Ficha:
    def __init__(self, jugador):
        self.jugador = jugador  # referencia al jugador
        self.pos = None  # None = en casa, o índice en camino

class Jugador:
    def __init__(self, color):
        self.color = color
        self.fichas = [Ficha(self) for _ in range(4)]


# Cargar DLL
dll = WinDLL("./LudoLibreria.dll")
tirarDado = dll.tirarDado
tirarDado.restype = c_int


# Funcion para tirar dado
def tirar():
    resultado = tirarDado()
    lbl_dado.config(text=str(resultado), font=("Arial", 40))


# Crear ventana
ventana = tk.Tk()
ventana.title("Ludo 15x15 con colores")
ventana.geometry("800x800")

# Frame para botón y dado
frame_izq = tk.Frame(ventana)
frame_izq.pack(side="left", padx=10, pady=10)

btn_tirar = tk.Button(frame_izq, text="Tirar Dado", command=tirar, font=("Arial", 14))
btn_tirar.pack(pady=10)

lbl_dado = tk.Label(frame_izq, text="", font=("Arial", 40))
lbl_dado.pack(pady=20)

# Canvas para tablero
canvas = tk.Canvas(ventana, width=600, height=600)
canvas.pack(side="right", padx=10, pady=10)

# Tamaño de cada celda
cell_size = 40

# Colores
colors = {
    "rojo": "red",
    "verde": "green",
    "amarillo": "yellow",
    "azul": "blue",
    "camino": "white",
    "centro": "gray"
}

# Dibujar tablero 15x15
for i in range(15):
    for j in range(15):
        x1 = j * cell_size
        y1 = i * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size

        # Bases
        if i < 6 and j < 6:
            color = colors["rojo"]
        elif i < 6 and j > 8:
            color = colors["verde"]
        elif i > 8 and j < 6:
            color = colors["amarillo"]
        elif i > 8 and j > 8:
            color = colors["azul"]
        # Camino vertical y horizontal
        elif j == 7 or i == 7:
            color = colors["camino"]
        # Centro
        elif 6 <= i <= 8 and 6 <= j <= 8:
            color = colors["centro"]
        else:
            color = colors["camino"]

        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

ventana.mainloop()
