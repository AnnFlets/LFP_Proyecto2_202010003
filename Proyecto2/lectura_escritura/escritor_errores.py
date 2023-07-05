class EscritorErrores():

    def __init__(self, lista_errores):
        self.lista_errores = lista_errores

    def escribir_errores(self):
        archivo = open("resultados\ERRORES_202010003.html", "w+")
        numero_errores = 1
        texto_escribir = "<!DOCTYPE html>\n"
        texto_escribir += "<html lang=\"es\">\n"
        texto_escribir += "<head>\n"
        texto_escribir += "\t<title>Errores</title>\n"
        texto_escribir += "\t<meta charset=\"utf-8\">\n"
        texto_escribir += "</head>\n"
        texto_escribir += "<body>\n"
        texto_escribir += "\t<h1>TABLA DE ERRORES</h1>\n"
        texto_escribir += "\t<br>\n"
        texto_escribir += "\t<table border=\"1\">\n"
        texto_escribir += "\t<tr>\n"
        texto_escribir += "\t\t<td>No.</td>\n"
        texto_escribir += "\t\t<td>Tipo</td>\n"
        texto_escribir += "\t\t<td>Token esperado</td>\n"
        texto_escribir += "\t\t<td>Descripcion</td>\n"
        texto_escribir += "\t\t<td>Fila</td>\n"
        texto_escribir += "\t\t<td>Columna</td>\n"
        texto_escribir += "\t</tr>\n"
        for error in self.lista_errores:
            texto_escribir += "\t<tr>\n"
            texto_escribir += "\t\t<td>" + str(numero_errores) + "</td>\n"
            texto_escribir += "\t\t<td>" + str(error.get_tipo()) + "</td>\n"
            texto_escribir += "\t\t<td>" + str(error.get_token_esperado()) + "</td>\n"
            texto_escribir += "\t\t<td>" + str(error.get_descripcion()) + "</td>\n"
            texto_escribir += "\t\t<td>" + str(error.get_fila()) + "</td>\n"
            texto_escribir += "\t\t<td>" + str(error.get_columna()) + "</td>\n"
            texto_escribir += "\t</tr>\n"
            numero_errores += 1
        texto_escribir += "</table>\n"
        texto_escribir += "</body>\n"
        texto_escribir += "</html>\n"
        archivo.write(texto_escribir)
        archivo.close()