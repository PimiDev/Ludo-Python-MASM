from ctypes import WinDLL, c_int

dll = WinDLL("./LudoLibreria.dll")

prueba = dll.sumarDosNumeros
prueba.argtypes = (c_int, c_int)
prueba.restype = c_int

print(prueba(1, 2))

