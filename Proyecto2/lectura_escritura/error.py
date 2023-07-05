class Error:
    def __init__(self, tipo, token_esperado, descripcion, fila, columna):
        self.tipo = tipo
        self.token_esperado = token_esperado
        self.descripcion = descripcion
        self.fila = fila
        self.columna = columna
        
    def get_tipo(self):
        return self.tipo

    def get_token_esperado(self):
        return self.token_esperado

    def get_descripcion(self):
        return self.descripcion

    def get_fila(self):
        return self.fila

    def get_columna(self):
        return self.columna

