class Lector():

    def __init__(self, ruta):
        self.ruta = ruta
        self.lineas = ""

    def leer_archivo(self):
        archivo = open(self.ruta, "r")
        for linea in archivo.readlines():
            self.lineas += linea
        archivo.close()
        return self.lineas