import tkinter as tk
from ctypes import WinDLL, c_int

dll = WinDLL("./LudoLibreria.dll")

tirarDado = dll.tirarDado
tirarDado.restype = c_int

getTurno = dll.getTurno
getTurno.restype = c_int

avanzarTurno = dll.avanzarTurno
avanzarTurno.restype = c_int

puedeSacarFicha = dll.puedeSacarFicha
puedeSacarFicha.argtypes = (c_int,)
puedeSacarFicha.restype = c_int

esComida = dll.esComida
esComida.argtypes = (c_int, c_int, c_int, c_int)
esComida.restype = c_int

esVictoria = dll.esVictoria
esVictoria.argtypes = (c_int, c_int, c_int, c_int)
esVictoria.restype = c_int

esBloqueo = dll.esBloqueo
esBloqueo.argtypes = (c_int, c_int, c_int, c_int)
esBloqueo.restype = c_int

sumarDosNumeros = dll.sumarDosNumeros
sumarDosNumeros.argtypes = (c_int, c_int)
sumarDosNumeros.restype = c_int

restarDosNumeros = dll.restarDosNumeros
restarDosNumeros.argtypes = (c_int, c_int)
restarDosNumeros.restype = c_int


def actualizar_turno_label():
    turno = getTurno()
    turno_label.config(text=f"Turno del Jugador {turno + 1}")


def lanzar_dado():
    resultado = tirarDado()
    resultado_label.config(text=f"Dado: {resultado}")

    # ejemplo de uso MASM
    if puedeSacarFicha(resultado) == 1:
        info_label.config(text="Puede sacar ficha (dado = 6)")
    else:
        info_label.config(text="No puede sacar ficha")

    avanzarTurno()
    actualizar_turno_label()


def probar_masm_extra():
    # valores de ejemplo
    f1, f2, f3, f4 = 10, 10, 3, 5
    bloqueo = esBloqueo(f1, f2, f3, f4)
    victoria = esVictoria(57, 57, 57, 57)
    comida = esComida(12, 0, 12, 1)

    texto = f"""
Bloqueo: {bloqueo}
Victoria: {victoria}
Comida: {comida}
    """
    info_label.config(text=texto)


# interfaz senciulla

root = tk.Tk()
root.title("Ludo + MASM DLL")

turno_label = tk.Label(root, text="Turno del Jugador 1", font=("Arial", 16))
turno_label.pack(pady=10)

btn_dado = tk.Button(root, text="Tirar dado", font=("Arial", 16), command=lanzar_dado)
btn_dado.pack(pady=10)

resultado_label = tk.Label(root, text="Dado: -", font=("Arial", 16))
resultado_label.pack(pady=10)

btn_test = tk.Button(root, text="Probar funciones MASM", font=("Arial", 14), command=probar_masm_extra)
btn_test.pack(pady=10)

info_label = tk.Label(root, text="---", font=("Arial", 14))
info_label.pack(pady=10)

actualizar_turno_label()

root.mainloop()
