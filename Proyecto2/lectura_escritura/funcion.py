class Funcion():

    def __init__(self, tipo, nombre):
        self.tipo = tipo
        self.nombre = nombre
        self.parametros = None
        self.id = None
        self.json = None

    def set_parametros(self, parametros):
        self.parametros = parametros

    def set_id(self):
        if self.parametros[0] != None:
            self.id = self.parametros[0]

    def set_json(self):
        if self.parametros[1] != None:
            self.json = self.parametros[1]