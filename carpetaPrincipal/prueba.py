import tkinter as tk
from ctypes import WinDLL, c_int


dll = WinDLL("./LudoLibreria.dll")

sumarDosNumeros = dll.sumarDosNumeros
sumarDosNumeros.argtypes = [c_int, c_int]
sumarDosNumeros.restype = c_int

restarDosNumeros = dll.restarDosNumeros
restarDosNumeros.argtypes = [c_int, c_int]
restarDosNumeros.restype = c_int

tirarDado = dll.tirarDado
tirarDado.restype = c_int

getTurno = dll.getTurno
getTurno.restype = c_int

avanzarTurno = dll.avanzarTurno
avanzarTurno.restype = c_int

puedeSacarFicha = dll.puedeSacarFicha
puedeSacarFicha.argtypes = [c_int]
puedeSacarFicha.restype = c_int

def lanzar_dado():
    valor = tirarDado()
    resultado_label.config(text=f"Dado: {valor}")

    # Ver si se puede sacar ficha
    if puedeSacarFicha(valor):
        fichas_label.config(text="¡Puedes sacar ficha!")
    else:
        fichas_label.config(text="No puedes sacar ficha.")

def mostrar_turno():
    turno = getTurno()
    turno_label.config(text=f"Turno actual: Jugador {turno + 1}")

def avanzar_turno():
    avanzarTurno()
    mostrar_turno()

def probar_sumar():
    res = sumarDosNumeros(5, 7)
    sumar_label.config(text=f"5 + 7 = {res}")

def probar_restar():
    res = restarDosNumeros(10, 3)
    restar_label.config(text=f"10 - 3 = {res}")

root = tk.Tk()
root.title("Prueba Ludo DLL")

# Botones y etiquetas
tk.Button(root, text="Tirar Dado", command=lanzar_dado).pack(pady=5)
resultado_label = tk.Label(root, text="Dado: ")
resultado_label.pack()

tk.Button(root, text="Mostrar Turno", command=mostrar_turno).pack(pady=5)
turno_label = tk.Label(root, text="Turno actual: ")
turno_label.pack()

tk.Button(root, text="Avanzar Turno", command=avanzar_turno).pack(pady=5)

tk.Button(root, text="Probar Sumar", command=probar_sumar).pack(pady=5)
sumar_label = tk.Label(root, text="")
sumar_label.pack()

tk.Button(root, text="Probar Restar", command=probar_restar).pack(pady=5)
restar_label = tk.Label(root, text="")
restar_label.pack()

fichas_label = tk.Label(root, text="")
fichas_label.pack(pady=5)

# Mostrar ventana
root.mainloop()
